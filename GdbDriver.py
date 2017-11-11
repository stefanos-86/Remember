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
import MemoryRepresentation

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

    memory = MemoryRepresentation.Memory()  # The whole goal is to fill this.

    def __init__(self, fobj):
        super().__init__(fobj)
        self.fobj = fobj

    def function(self):
        """This function was re-purposed as the entry point for the memory analisys."""
        self.scan_stack_frame()
        return gdb.FrameDecorator.FrameDecorator.function(self)  # Same text output as without this class.

    def scan_stack_frame(self):
        frame = self.fobj.inferior_frame()
        name = str(frame.name())
        code = frame.block()

        begin_address = str(frame.read_register("sp"))

        end_address = "unknown"
        previous = frame.older()
        if previous is not None:
            end_address = str(previous.read_register("sp"))

        memory_for_frame = ScanMemoryDecorator.memory.add_stack_frame(begin_address, end_address, name)

        for symbol in code:
            if symbol.is_variable:
                variable_type = symbol.type
                if variable_type.code == gdb.TYPE_CODE_PTR:  # Else, check for pointer into the structure!
                    pointed_at_address = frame.read_var(symbol, code)
                    ScanMemoryDecorator.memory.add_pointer(memory_for_frame, pointed_at_address, str(symbol.type),
                                                           symbol.name)
                    self.scan_object(pointed_at_address)

    def scan_object(self, pointer_to_object):
        heap_value = pointer_to_object.dereference()
        type_to_analyze = heap_value.type
        end_address = pointer_to_object + 1  # pointer_to_object is a pointer. Doing + 1 goes one object ahead.
                                             # pointer + type.sizeof is the same error it would be in C!

        if type_to_analyze.code == gdb.TYPE_CODE_STRUCT:
            heap_object = ScanMemoryDecorator.memory.add_heap_object(pointer_to_object, end_address, str(type_to_analyze))
            variables = type_to_analyze.fields()
            for variable in variables:
                if variable.type.code == gdb.TYPE_CODE_PTR:
                    pointer_to_explore = heap_value[variable]

                    pointer_data = ScanMemoryDecorator.memory.add_pointer(heap_object, pointer_to_explore, variable.type, variable.name)
                    if pointer_data.voidness() == "":
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
