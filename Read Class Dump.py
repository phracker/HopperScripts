# coding=utf-8
"""Reads output of class-dump to label procedures in Hopper"""

import ctypes
import ctypes.util
import os
import re
from subprocess import Popen, PIPE


def get_original_file_name(doc_obj_addr):
    """Read original path of the binary from private Hopper document.

    May cause crashes"""
    objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))
    objc.objc_getClass.restype = ctypes.c_void_p
    objc.sel_registerName.restype = ctypes.c_void_p
    objc.objc_msgSend.restype = ctypes.c_void_p
    objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    NSAutoreleasePool = objc.objc_getClass('NSAutoreleasePool')
    pool = objc.objc_msgSend(NSAutoreleasePool, objc.sel_registerName('alloc'))
    pool = objc.objc_msgSend(pool, objc.sel_registerName('init'))

    originalFilePath = ctypes.cast(
        objc.objc_msgSend(
            objc.objc_msgSend(
                objc.objc_msgSend(doc_obj_addr, objc.sel_registerName("disassembledFile")),
                objc.sel_registerName("originalFilePath")),
            objc.sel_registerName("UTF8String")),
        ctypes.c_char_p).value

    objc.objc_msgSend(pool, objc.sel_registerName('release'))
    return originalFilePath


def read_command(cmd, cwd=None, encoding='utf-8'):
    """Run shell command and read output.

    @param cmd: Command to be executed.
    @type cmd: string

    @param cwd: Working directory.
    @type cwd: string

    @param encoding: Encoding used to decode bytes returned by Popen into string.
    @type encoding: string

    @return: Output of the command: (<returncode>, <output>)
    @rtype: tuple"""
    p = Popen(cmd, shell=True, stdout=PIPE, cwd=cwd)
    output = p.communicate()[0]
    output = output.decode(encoding)
    return p.returncode, output


def read_class_dump(binary_path):
    """Read class dump (both class-dump and class-dump-z) and return list of lines.

    @param binary_path: Path to the binary for class-dump.
    @type binary_path: unicode

    @return: List of lines
    @rtype: list"""
    class_dump_path = None
    class_dump_z_path = None
    for prefix in os.getenv("PATH",os.defpath).split(os.pathsep) + ["/usr/local/bin", "/opt/bin"]:
        if os.path.exists(os.path.join(prefix, "class-dump")):
            class_dump_path = os.path.join(prefix, "class-dump")

        if os.path.exists(os.path.join(prefix, "class-dump-z")):
            class_dump_z_path = os.path.join(prefix, "class-dump-z")

    if not class_dump_path and not class_dump_z_path:
        doc.log("ERROR: Cannot find class-dump or class-dump-z")
        raise Exception("Missing class-dump")

    class_dump = []
    cwd = os.path.dirname(binary_path)

    if class_dump_path:
        returncode, output = read_command("{0} -a -A \"{1}\"".format(class_dump_path, binary_path), cwd)
        class_dump += output.splitlines()

    if class_dump_z_path:
        returncode, output = read_command("{0} -A \"{1}\"".format(class_dump_z_path, binary_path), cwd)
        class_dump += output.splitlines()

    return class_dump


def process(lines, doc):
    def on_method(address, name):
        doc.setNameAtAddress(address, name)
        if doc.getSegmentAtAddress(address) is not None:
            doc.getSegmentAtAddress(address).markAsProcedure(address)
            #doc.log("Method: {0} at 0x{1:x}".format(name, address))

    def on_ivar(address, name):
        segment = doc.getSegmentAtAddress(address)
        if segment is not None and segment.getName() == "__objc_ivar":
            doc.setNameAtAddress(address, name)
            #doc.log("Ivar: {0} at 0x{1:x} (2}".format(name), address, segment.getName())

    in_methods = False
    in_ivars = False
    interface_name = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("@interface"):
            m = re.match("^@interface +(?P<name>.*):(?P<rest>.*)", line)
            if m is not None:
                interface_name = m.group('name').strip()
                in_ivars = True
                in_methods = False
                #doc.log(line)
        if line.startswith("@end"):
            in_methods = False
            in_ivars = False
        elif in_ivars and line.startswith("}"):
            in_ivars = False
            in_methods = True
        elif in_ivars:
            m = re.match("^(?P<type>.*(\*| ))(?P<name>[a-zA-Z].*);.*(?P<address>0[xX][0-9a-fA-F]+).*", line)
            if m is not None:
                ivar_type = m.group('type').strip()
                ivar_name = m.group('name').strip()
                ivar_address = int(m.group('address'), 16)
                ivar_info_name = "({0}) {1}.{2}".format(ivar_type, interface_name, ivar_name)
                on_ivar(ivar_address, ivar_info_name)
        elif in_methods:
            m = re.match("(?P<scope>^(\+|\-)) *\((?P<type>.*?)\) *(?P<signature>.*);.*(?P<address>0[xX][0-9a-fA-F]+).*", line)
            if m is not None:
                method_scope = m.group('scope')
                method_type = m.group('type').strip()
                method_signature = m.group('signature').strip()
                method_address = int(m.group('address'), 16)
                method_info_name = "{0} ({1}) [{2} {3}]".format(method_scope, method_type, interface_name, method_signature)
                on_method(method_address, method_info_name)
            else:
                m = re.match("^@property(?P<attributes>\(.+?\))?.+?(?P<type>[a-zA-Z].*(\*| ))(?P<name>[a-zA-Z].*);(?P<rest>.*)", line)
                if m is not None:
                    property_attributes = m.group('attributes')
                    property_type = m.group('type').strip()
                    property_name = m.group('name').strip()
                    rest = m.group('rest')

                    m = re.match(".*G=(?P<getter>0[xX][0-9a-fA-F]+).*", rest)
                    if m is not None:
                        property_getter_address = m.group('getter')

                        m = re.match(".*getter=(?P<name>[a-zA-Z][a-zA-Z0-9]*).*", property_attributes)
                        if m is not None:
                            property_getter_name = m.group('name')
                        else:
                            property_getter_name = property_name

                        property_getter_info_name = "- ({0}) [{1} {2}]".format(property_type, interface_name, property_getter_name)
                        on_method(property_getter_address, property_getter_info_name)

                    m = re.match(".*S=(?P<setter>0[xX][0-9a-fA-F]+).*", rest)
                    if m is not None:
                        property_setter_address = m.group('setter')

                        m = re.match(".*setter=(?P<name>[a-zA-Z][a-zA-Z0-9]*).*", property_attributes)
                        if m is not None:
                            property_setter_name = m.group('name')
                        else:
                            property_setter_name = "set{0}".format(property_name[0].upper() + property_name[1:])

                        property_setter_info_name = "- (void) [{0} {1}]".format(interface_name, property_setter_name)
                        on_method(property_setter_address, property_setter_info_name)
                else:
                    doc.log("INFO: Unknown \"{0}\"".format(line))


doc = Document.getCurrentDocument()
binary_path = get_original_file_name(doc.__internal_document_addr__)
process(read_class_dump(binary_path), doc)
doc.refreshView()
