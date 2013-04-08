# Hopper gdb script.  Effectively the same as the "HopperGDBServer" program that ships with Hopper, but works cross-platform
# Note that if you use this to debug a Linux process on another system, and you "override executable path", you may get an annoying error asking you select the file.
#      If you just hit cancel, it will continue to work anyway.
# bradenthomas@me.com

from twisted.internet import reactor,protocol,defer
import pybonjour,struct,socket,os,sys

HOPPER_GDB_PROTOCOL_VERSION = 1
VERBOSE = (os.getenv("VERBOSE") != None)

class HopperBonjour(object):
   def __init__(self, name, port):
      self.rsock = pybonjour.DNSServiceRegister(name=name, 
               regtype="_hopper._tcp",
               port=port,
               callBack=self.register_callback,
               domain="local.")
      reactor.addReader(self)
   def register_callback(self,sdRef,flags,err,name,regtype,domain):
      if err==pybonjour.kDNSServiceErr_NoError:
         print "Registered %s/%s/%s" % (name,regtype,domain)
   def logPrefix(self): return "HopperBonjour"
   def fileno(self): return self.rsock.fileno()
   def doRead(self): pybonjour.DNSServiceProcessResult(self.rsock)
   def connectionLost(self, reason): pass

class GDBProtocol(protocol.ProcessProtocol):
   def __init__(self, hopper):
      self.hopper = hopper
   def connectionMade(self):
      if VERBOSE: print "gdb connection made"
      self.hopper.gdbConnectionMade()
   def outReceived(self, data):
      if VERBOSE: print "GDB OUT RECEIVED",repr(data)
      self.hopper.transport.write(data)
   def errReceived(self, data):
      if VERBOSE: print "GDB ERR RECEIVED",repr(data)
      sys.stderr.write(data)
      sys.stderr.flush()
   def processExited(self, status):
      if VERBOSE: print "GDB EXIT",status
      self.hopper.transport.loseConnection()

class HopperProtocol(protocol.Protocol):
   def __init__(self, override_file, override_args):
      self.state = 0
      self.gdb = None
      self.override_file = override_file
      self.override_args = override_args
   def connectionMade(self):
      if VERBOSE: print "Connection made"
      self.transport.write("HopperGDBServer")
   def gdbConnectionMade(self):
      self.state = 4
      self.transport.write(chr(1))
   def modifyCommand(self, data):
      out = data
      try:
         (command_no, command_data) = data.split("-",1)
         if command_data.startswith("file-exec-file") and self.override_file:
            out = "%s-file-exec-file \"%s\"\n"%(command_no,self.override_file)
      except:
         pass
      if VERBOSE and out != data: print "MODIFIED",repr(out)
      return out
   def dataReceived(self, data):
      #if VERBOSE: print "Received",repr(data)
      if self.state == 0 and data == "Hopper":
         self.state = 1
         data = data[6:]
         self.transport.write(struct.pack("<H", HOPPER_GDB_PROTOCOL_VERSION))
      if self.state == 1 and len(data) >= 2:
         self.state = 2
         remote_version, = struct.unpack("<H", data[:2])
         data = data[2:]
         if remote_version != HOPPER_GDB_PROTOCOL_VERSION:
            if VERBOSE: print "Unsupported version",remote_version
            self.transport.loseConnection()
            return
      if self.state == 2 and len(data) > 0:
         self.gdb_arch = data.strip("\x00")
         self.state = 3
         data = ""
      if self.state == 3:
         if sys.platform == "darwin":
            launch_args = ["gdb", "--arch=%s"%self.gdb_arch, "--quiet", "--nx", "--interpreter=mi1"]
         else:
            launch_args = ["gdb", "--quiet", "--nx", "--interpreter=mi1"]
         if self.override_args and len(self.override_args):
            launch_args.extend(["--args", self.override_file]+self.override_args)
         elif self.override_file:
            launch_args.append(self.override_file)         
         if VERBOSE: print "Launch:",str(launch_args)
         self.gdb = GDBProtocol(self)
         reactor.spawnProcess(self.gdb, "/usr/bin/gdb", args=launch_args)
      if self.state == 4 and self.gdb != None:
         if VERBOSE: print "WRITE TO GDB",repr(data)
         data = self.modifyCommand(data)
         self.gdb.transport.write(data)


class HopperFactory(protocol.ServerFactory):
   protocol = HopperProtocol
   def __init__(self, override_file, override_args):
      self.override_file = override_file
      self.override_args = override_args
   def buildProtocol(self, addr):
      return self.protocol(self.override_file, self.override_args)

argc = len(sys.argv)-1
if argc == 1 and sys.argv[1] == "-h":
   print "Usage: hoppergdb_to_gdb.py [override executable path]"
   sys.exit(0)
override_file = None
override_args = []
if argc > 1 and os.path.exists(sys.argv[1]):
   override_file = sys.argv[1]
   override_args = sys.argv[1:]

p = reactor.listenTCP(0, HopperFactory(override_file, override_args))
HopperBonjour(socket.gethostname(), p.getHost().port)
reactor.run()