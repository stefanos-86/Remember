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

    for block in memory_image.objects:
        draw_stack_frame(block, graph)

    return graph.source


def draw_stack_frame(block, graph):
    label =  block.name_or_type + '|' \
            + str(block.start_address) + ' - ' + str(block.end_address)
    graph.node(str(block.start_address), label)  # The node id is the "beginning" of the object in memory.
