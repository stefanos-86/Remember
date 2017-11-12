import os
import shutil
import subprocess
import time

import TestSuite as ts

# This scripts automates the creation of the test core dumps.
#
# It relies on the "conventional" position and content of the CMakeLists.txt to find the programs.
# The test programs must take no arguments.
#
# May require the sudo password because only the superuser can command to core a process.
#
# It also assumes that the programs will block at exactly the right spot during the execution
# before it cores them. But there is no specific syncronization to achieve this. Just infinite loops
# to block and a small wait in the script.
# It is bad parallel programming, but it works well enough in practice.


def clean_up_core_folder():
    """Erases and re-create any pre-existing folder for the core files."""
    if os.path.exists(ts.CORES_FOLDER):
        shutil.rmtree(ts.CORES_FOLDER)
    os.makedirs(ts.CORES_FOLDER)
    print "Re-created " + ts.CORES_FOLDER


def compile_test_programs():
    """Invokes CMake and make to create the test binaries.
       Calls a debug build as I don't want optimizations to get in the way."""
    subprocess.call(["cmake", "-DCMAKE_BUILD_TYPE=Debug", ts.TEST_PROGRAMS_FOLDER], cwd=ts.TEST_PROGRAMS_FOLDER)
    subprocess.call(["make"], cwd=ts.TEST_PROGRAMS_FOLDER)
    print "All test programs compiled."


def run_and_core(executable):
    """Start the test program, then takes a core dump and kills it."""
    test_program = subprocess.Popen([os.path.join(ts.TEST_PROGRAMS_FOLDER, executable)])
    pid = str(test_program.pid)
    time.sleep(1)  # Theoretically incorrect, but sufficient for our purposes.
    subprocess.call(["sudo", "gcore", "-o", os.path.join(ts.CORES_FOLDER, executable), pid])
    subprocess.call(["kill", pid])
    print "Created core file for " + executable


if __name__ == "__main__":
    clean_up_core_folder()
    compile_test_programs()
    executables = ts.find_test_cases()
    for program in executables:
        print "Working on " + program
        run_and_core(program)
