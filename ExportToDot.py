# This file is a "friend" of the memory representation that can read it and create a dot file.

# This script runs "inside" gdb and can't access the system-installed libraries.
# I can not think of a satisfactory way to detect the path and pass it here.
# But I suspect that is the standard place where packages are, so this should be
# generic enough.
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from graphviz import Digraph


def export(memory_image):
    graph = Digraph('Memory Dump', node_attr={'shape': 'record'})
    graph.attr(rankdir='LR')

    memory_image.resolve_pointed_objects()
    for block in memory_image.objects:
        draw_memory_object(block, graph)

    return graph.source


def draw_memory_object(block, graph):
    label = block.name_or_type + '|' + \
            block.start_address + ' - ' + block.end_address

    # Append all the ports.
    exit_port_count = 0
    for pointer in block.outgoing_pointers:
        if pointer.is_valid():
            port_name = "<p" + str(exit_port_count) + "> "
            label += "|" + port_name + pointer.name
            draw_pointer(str(exit_port_count), pointer, block, graph)
            exit_port_count += 1
        else:
            label += "|" + pointer.name + " " + pointer.special_case

    graph.node(block.start_address, label)  # The node id is the "beginning" of the object in memory.


def draw_pointer(port_number, pointer, block, graph):
    origin_node_port = block.start_address + ":p" + port_number
    if pointer.pointed_object is None:
        destination_node = "UNKNOWN"
    else:
        destination_node = pointer.pointed_object.start_address
    graph.edge(origin_node_port, destination_node)


