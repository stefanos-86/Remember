import logging as log

UNKNOWN_ADDRESS = "Unknown"


class MemoryObject:
    """Represents data that takes space in memory. For example, a C++ object.
       Stack frames fits here too: they take some space and have local variables acting as the fields."""

    def __init__(self, name_or_type, start_address, end_address):
        self.name_or_type = name_or_type        # Function name for the stack, type of the object otherwise.
        self.start_address = start_address
        self.end_address = end_address

        self.outgoing_pointers = []


    def add_outgoing_pointer(self, pointer):
        self.outgoing_pointers.append(pointer)

    def contains(self, pointer):
        """True if and only if the pointer points to something into this block."""
        if self.start_address == UNKNOWN_ADDRESS or self.end_address == UNKNOWN_ADDRESS:
            return False

        return self.address_to_int(self.start_address) <= \
               self.address_to_int(pointer.pointed_address) < \
               self.address_to_int(self.end_address)

    def address_to_int(self, address):
        """Pointers start with 0x, references with @0x, but both must be convertible to something we can
           compare and order, to guess where things are in memory."""
        clean_address = address
        if address.startswith("@"):
            clean_address = address[1:]
        return int(clean_address, 0)  # Base 0 is hex with 0x in front.


class Pointer:
    """Pointer in the C sense. Connects two memory objects."""

    SPECIAL_CASE_OPTIMIZED = "(optimized out)"
    SPECIAL_CASE_NULL = "(nullptr)"
    NORMAL_CASE = ""

    def __init__(self, name, pointed_address, optimized):
        self.name = name
        self.pointed_address = pointed_address
        self.pointed_object = None  # To be resolved once all the objects are known.

        self.special_case = Pointer.NORMAL_CASE
        if self.pointed_address == "0x0":
            self.special_case = Pointer.SPECIAL_CASE_NULL
        if optimized:
            self.special_case = Pointer.SPECIAL_CASE_OPTIMIZED

    def is_valid(self):
        return self.special_case == Pointer.NORMAL_CASE


class Memory:
    """Representation of all the objects in memory that we could find."""
    def __init__(self):
        self.objects = []

    def add_object(self, memory_object):
        self.objects.append(memory_object)

    def resolve_pointed_objects(self):
        """A pointer is only a memory address. Into which object does it fall?
           This can be determined only after all objects have been explored and their
           addresses are known."""
        for memory_object in self.objects:
            for pointer in memory_object.outgoing_pointers:
                if pointer.is_valid():
                    self.resolve_pointer(pointer)

    def resolve_pointer(self, pointer):
        for memory_object in self.objects:
            log.debug("Resolve " + pointer.name + " against " + memory_object.start_address)
            if memory_object.contains(pointer):
                pointer.pointed_object = memory_object
                return  # No point into going further, we found the target.

    def unknown_object(self, object_address):
        for memory_object in self.objects:
            fake_pointer = Pointer("Fake", object_address, False)  # Contains expects a pointer, not just an address.
            if memory_object.contains(fake_pointer):
                return False
        return True
