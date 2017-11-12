# Credits
# https://vjordan.info/log/fpga/tag/gdb.html
# https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html#Python-API

import gdb
import logging as log
import os
import pickle
import sys

# Bring the support modules into view.
sys.path.append(".")
import ExportToDot
import MemoryRepresentation as mem

def load_parameters():
    """Read the "bridge file to get back the arguments."""
    parameter_file_name = os.path.abspath("gdb_driver.params")
    parameter_file = open(parameter_file_name, "rb")
    return pickle.loads(parameter_file.read())


def prepare_logging(args):
    """There is no way to synch log from two processes, must use a different file.
       I could try to flush the logs, maybe (as I know that the main script stops working while
       GDB runs), but it is easier this way."""
    local_log_file = os.path.abspath(args.logfile) + ".gdb"
    log.basicConfig(filename=local_log_file,
                    filemode="a",  # Must append to the file already created by the main script.
                    level=log.DEBUG)


def gdb_command(command):
    """Sends a command to GDB, as if using its normal interface."""
    #                            + not a TTY
    #                            |      + output as string
    return gdb.execute(command, False, True)


def save_results():
    dot_file = os.path.abspath("RememberOutput.dot")
    result_file = open(dot_file, "w")
    result_graph = ExportToDot.export(ScanMemoryDecorator.memory)
    result_file.write(result_graph)
    result_file.flush()


class ScanMemoryDecorator(gdb.FrameDecorator.FrameDecorator):
    """This GDB decorator simply produces the default result for each stack frame.
       But it also explores all the pointers into the stack frame and visits the memory as far as it can get
       to collect a representation of the objects it finds.

        The representation must be saved in a class-level variable because construction and interface of the instances
        are "locked down" by GDB and there is no place to pass extra parameters (that I know of). """

    memory = mem.Memory()  # The whole goal is to fill this.

    def __init__(self, fobj):
        super().__init__(fobj)
        self.fobj = fobj

    def function(self):
        """This function was re-purposed as the entry point for the memory analysis."""
        self.scan_stack_frame()
        return gdb.FrameDecorator.FrameDecorator.function(self)  # Same text output as without this class.


    def scan_stack_frame(self):
        frame = self.fobj.inferior_frame()

        function_name = str(frame.name())
        begin_address = str(frame.read_register("sp"))  # The stack grows "going down", begin is higher then end.


        called_from_frame = frame.older()
        if called_from_frame is None:
            end_address = mem.UNKNOWN_ADDRESS
        else:  # This frame ends where the other one started.
            end_address = str(called_from_frame.read_register("sp"))

        frame_image = mem.MemoryObject(function_name, begin_address, end_address)
        ScanMemoryDecorator.memory.add_object(frame_image)

        self.scan_local_variables(frame, frame_image)


    def scan_local_variables(self, frame, frame_image):
        """Check what is in a stack frame for more pointers or struct to explore."""
        function_code = frame.block()

        for symbol in function_code:
            if symbol.is_variable or symbol.is_argument:
                variable_type = symbol.type
                if variable_type.code == gdb.TYPE_CODE_PTR:
                    pointed_at_address = frame.read_var(symbol, function_code)
                    new_pointer = mem.Pointer(symbol.name,
                                              str(pointed_at_address),
                                              pointed_at_address.is_optimized_out)
                    frame_image.add_outgoing_pointer(new_pointer)
                    # Navigate into the object to see if there are more pointers in it.
                    self.scan_object(pointed_at_address)


    def scan_object(self, object_address):
        pointed_struct = object_address.dereference()
        type_to_analyze = pointed_struct.type

        if type_to_analyze.code == gdb.TYPE_CODE_STRUCT:
            end_address = object_address + 1  # pointer_to_object is a pointer. Doing + 1 goes one object ahead.
                                              # pointer + type.sizeof is the same error it would be in C!
            heap_object = mem.MemoryObject(str(type_to_analyze),
                                           str(object_address),
                                           str(end_address))
            self.memory.add_object(heap_object)
            self.scan_members(pointed_struct, heap_object)


    def scan_members(self, pointed_struct, heap_object):
            type_to_analyze = pointed_struct.type
            class_variables = type_to_analyze.fields()
            for variable in class_variables:
                log.debug("There is a variable " + str(variable.name))
                if variable.type.code == gdb.TYPE_CODE_PTR:
                    pointer_to_explore = pointed_struct[variable]
                    new_pointer = mem.Pointer(str(variable.name),
                                              str(pointer_to_explore),
                                              pointer_to_explore.is_optimized_out)
                    heap_object.add_outgoing_pointer(new_pointer)
                    if new_pointer.is_valid():  # Keep going.
                        self.scan_object(pointer_to_explore)



class ScanMemoryFilter():
    """ "Glue code" to attach the memory scanner to GDB. """
    def __init__(self):
        self.name = "ScanMemoryFilter"
        self.priority = 100
        self.enabled = True
        gdb.frame_filters[self.name] = self

    def filter(self, frame_iter):
        frame_iter = map(ScanMemoryDecorator,
                                    frame_iter)
        return frame_iter


#  Main processing is down here.

args = load_parameters()
prepare_logging(args)
log.info("Reloaded " + str(args))


ScanMemoryFilter();
gdb_output = gdb_command("info stack") # Triggers the memory visit and so makes GDB call our filter.
log.info(gdb_output)

save_results()

gdb.execute('quit')
