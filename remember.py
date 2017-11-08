import argparse
import logging as log
import os
import pickle
import subprocess


# Entry point for the tool.
# Check usage with --help.


def parse_command_line():
    parser = argparse.ArgumentParser(description='Scans a core dump for pointers and draws the object it finds.',
                                     epilog="(C) 2017 - Stefano",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("core_file",
                        help="Core file to analize.")

    parser.add_argument("binary",
                        help="Program corresponding to the core. Did you compile with -g?.")

    log_file = "/dev/null"
    parser.add_argument("-l", "--logfile",
                        help="Where to store the tool log messages. Useful for debugging.",
                        default=log_file,
                        required=False)

    parser.add_argument("-o", "--output",
                        help="Name of the drawing to be produced. Verbatim (won't add extension). \
                              The file is in SVG format.  (default: <core file name>.svg).",
                        # Argparse does not support inter-dependant parameters.
                        required=False)

    return parser.parse_args()


def create_parameters_file(parameters):
    """As far as I know there is no way to pass parameters to the script that will be executed insider GDB.
       Some people on the internet even recommends to patch said script on the fly.
       To "balance", I create a python module that contains the parameters and can be included
       by the script from inside GDB."""
    parameter_file_name = os.path.abspath("RememberParameters.py")
    if os.path.exists(parameter_file_name):
        log.info("Overwriting " + parameter_file_name)

    parameter_file = open(parameter_file_name, "w")
    parameter_file.write(pickle.dumps(parameters))


def check_dot_file(dot_file):
    """Logs a message if the file that will be filled with the dot-format output already exists."""
    if os.path.exists(dot_file):
        log.info("Overwriting " + dot_file)


def invoke_gdb(core_file, binary):
    """Actually starts the debugger (passing it our special script to capture the memory)."""
    log.info("Calling GDB.")
    subprocess.call(["gdb", "-c", core_file, "-x", "gdb_driver.py", binary])


def draw_graph(dot_input, graph_output):
    """Call Graphviz to transform the output into an image."""
    subprocess.call(["dot", "-Tsvg", dot_input, "-o" + graph_output])
    log.info("Created image at " + graph_output)


if __name__ == "__main__":
    args = parse_command_line()

    core_file = os.path.abspath(args.core_file)
    log_file = os.path.abspath(args.logfile)
    binary = os.path.abspath(args.binary)

    output_file = core_file + ".svg"
    if args.output is not None:
        output_file = os.path.abspath(args.output)

    log.basicConfig(filename=log_file,
                    filemode="w",
                    level=log.DEBUG)

    log.info(args)

    dot_file = os.path.abspath("RememberOutput.dot")
    check_dot_file(dot_file)
    invoke_gdb(core_file, binary)
    draw_graph(dot_file, output_file)

    log.info("End.")