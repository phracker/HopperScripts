# Reads output of class-dump to label procedures in Hopper
# bradenthomas@me.com

import os,subprocess

def get_original_file_name(doc_obj_addr):
   # just to be crazy, find the original path with ctypes
   # may cause crashes :-)
   import ctypes, ctypes.util
   objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))
   objc.objc_getClass.restype = ctypes.c_void_p
   objc.sel_registerName.restype = ctypes.c_void_p
   objc.objc_msgSend.restype = ctypes.c_void_p
   objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

   NSAutoreleasePool = objc.objc_getClass('NSAutoreleasePool')
   pool = objc.objc_msgSend(NSAutoreleasePool, objc.sel_registerName('alloc'))
   pool = objc.objc_msgSend(pool, objc.sel_registerName('init'))

   originalFilePath = str(
                  ctypes.cast(
                     objc.objc_msgSend(
                        objc.objc_msgSend(
                           objc.objc_msgSend(doc_obj_addr, objc.sel_registerName("disassembledFile")),
                           objc.sel_registerName("originalFilePath")),
                        objc.sel_registerName("UTF8String")),
                     ctypes.c_char_p).value
                  )

   objc.objc_msgSend(pool, objc.sel_registerName('release'))
   return originalFilePath

doc = Document.getCurrentDocument()

executable_path = get_original_file_name(doc.__internal_document_addr__)

class_dump_path = None
class_dump_z_path = None
for prefix in os.getenv("PATH",os.defpath).split(os.pathsep)+["/usr/local/bin","/opt/bin"]:
   if os.path.exists(os.path.join(prefix, "class-dump")):
      class_dump_path = os.path.join(prefix, "class-dump")
   if os.path.exists(os.path.join(prefix, "class-dump-z")):
      class_dump_z_path = os.path.join(prefix, "class-dump-z")

if not class_dump_path and not class_dump_z_path:
   doc.log("Error: Cannot find class-dump or class-dump-z")
   raise Exception("Missing class-dump")

doc.log("Found utilities: %s and %s"%(str(class_dump_path), str(class_dump_z_path)))

# Run both utilities, because don't know what Obj-C ABI is at this point
if class_dump_path:
   p = subprocess.Popen([class_dump_path, "-A", "-a", executable_path], stdout=subprocess.PIPE)
   class_dump_data = p.communicate()[0]
else:
   class_dump_data = ""

if class_dump_z_path:
   p = subprocess.Popen([class_dump_z_path, "-A", executable_path], stdout=subprocess.PIPE)
   class_dump_z_data = p.communicate()[0]
else:
   class_dump_z_data = ""

def found_method(addr, name):
   doc.log(hex(addr)+": "+name)
   doc.setNameAtAddress(addr, name)
   if doc.getSegmentAtAddress(addr) != None:
      doc.getSegmentAtAddress(addr).markAsProcedure(addr)

for parse_data in [class_dump_data, class_dump_z_data]:
   in_interface = False
   in_ivars = False
   interface_name = None
   for cl_line in parse_data.splitlines():
      cl_line = cl_line.strip()
      if not len(cl_line): continue
      if cl_line.startswith("@interface"):
         try:
            interf_comps = cl_line.split()
            if interf_comps[2] == ":":
               interface_name = cl_line.split()[1]
               doc.log("INTERFACE: %s | %s"%(interface_name, cl_line.strip()))
               in_ivars = True
         except:
            continue
      if cl_line.startswith("@end"):
         in_interface = False
         in_ivars = False
      elif in_ivars and cl_line.startswith("}"):
         in_ivars = False
         in_interface = True
      elif in_ivars:
         ivar_cmps = cl_line.strip().split(";")
         if len(ivar_cmps) == 2:
            ivar_name_cmps = ivar_cmps[0].rsplit(None, 1)
            if len(ivar_name_cmps) == 2:
               ivar_type, ivar_name = ivar_name_cmps
               if ivar_name.startswith("*"):
                  ivar_name = ivar_name[1:]
                  ivar_type += "*"
               ivar_info_name = "(%s) %s.%s"%(ivar_type, interface_name, ivar_name)

               ivar_addr_str = ivar_cmps[1].split()[-1]
               if ivar_addr_str.startswith("0x"):
                  ivar_addr = int(ivar_addr_str[2:], 16)
                  ivar_seg = doc.getSegmentAtAddress(ivar_addr)
                  if ivar_seg and ivar_seg.getName() == "__objc_ivar":
                     doc.log("Ivar: %s at 0x%x (%s)"%(str(ivar_info_name), ivar_addr, ivar_seg.getName()))
                     doc.setNameAtAddress(ivar_addr, ivar_info_name)
      elif in_interface:
         if cl_line[0] in ["+","-"]:
            sel_cmps = cl_line.strip().split(";")
            if len(sel_cmps) == 2:
               ret_arg_idx = sel_cmps[0].find(")")+1
               ret_arg = sel_cmps[0][1:ret_arg_idx]
               method_name = "%s %s [%s %s]"%(cl_line[0], ret_arg, interface_name, sel_cmps[0][ret_arg_idx:])
               method_imp = sel_cmps[1][4:]
               # class-dump-z format
               if method_imp.startswith("0x"):
                  method_addr = int(method_imp[2:],16)-1 # I don't remember why I put this in.  Should probably drop last bit for thumb vs ARM
                  found_method(method_addr, method_name)
               # class-dump format
               elif method_imp.startswith("IMP=0x"):
                  method_addr = int(method_imp[6:],16)
                  found_method(method_addr, method_name)                  
               else:
                  doc.log("Warning: Unknown method format: %s"%method_imp)
         elif cl_line.startswith("@property"):
            sel_cmps = cl_line.strip().split(";")
            if len(sel_cmps) >= 2:
               prop_flags_idx = sel_cmps[0].find(")")+1
               prop_name_and_type = sel_cmps[0][prop_flags_idx:].strip().split(" ")
               getter = None
               setter = None
               for x in sel_cmps[1:]:
                  g_idx = x.find("G=")
                  s_idx = x.find("S=")
                  if g_idx > 0: getter = x[g_idx+2:]
                  if s_idx > 0: setter = x[s_idx+2:]
               if getter and getter.startswith("0x"):
                  method_addr = int(getter, 16)-1
                  method_name = "- (%s) [%s %s]"%(prop_name_and_type[0], interface_name, prop_name_and_type[1])
                  found_method(method_addr, method_name)
               if setter and setter.startswith("0x"):
                  method_addr = int(setter, 16)-1
                  method_name = "- (%s) [%s set_%s]"%(prop_name_and_type[0], interface_name, prop_name_and_type[1])
                  found_method(method_addr, method_name)
                  
         else:
            doc.log("Info: Unknown: %s: %s"%(interface_name, cl_line.strip()))

doc.refreshView()