import os
import shutil
import subprocess
import time

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


CORES_FOLDER = os.path.abspath("testCores")
TEST_PROGRAMS_FOLDER = os.path.abspath("testPrograms")


def clean_up_core_folder():
    """Erases and re-create any pre-existing folder for the core files."""
    if os.path.exists(CORES_FOLDER):
        shutil.rmtree(CORES_FOLDER)
    os.makedirs(CORES_FOLDER)
    print "Re-created " + CORES_FOLDER


def compile_test_programs():
    """Invokes CMake and make to create the test binaries.
       Calls a debug build as I don't want optimizations to get in the way."""
    subprocess.call(["cmake", "-DCMAKE_BUILD_TYPE=Debug", TEST_PROGRAMS_FOLDER], cwd=TEST_PROGRAMS_FOLDER)
    subprocess.call(["make"], cwd=TEST_PROGRAMS_FOLDER)
    print "All test programs compiled."


def find_executables():
    """Explores the conventional test programs folder to find all the executables in the cmake file. """
    programs = []
    expected_line_beginning = "add_executable("
    expected_line_beginning_size = len(expected_line_beginning)
    cmake_file = open(os.path.join(TEST_PROGRAMS_FOLDER, "CMakeLists.txt"))

    for line in cmake_file:
        if line.startswith(expected_line_beginning):
            end_of_name = line.find(" ")
            program_name = line[expected_line_beginning_size:end_of_name]
            programs.append(program_name)
            print "Detected test program " + program_name

    return programs


def run_and_core(executable):
    """Start the test program, then takes a core dump and kills it."""
    test_program = subprocess.Popen([os.path.join(TEST_PROGRAMS_FOLDER, executable)])
    pid = str(test_program.pid)
    time.sleep(1)  # Theoretically incorrect, but sufficient for our purposes.
    subprocess.call(["sudo", "gcore", "-o", os.path.join(CORES_FOLDER, executable), pid])
    subprocess.call(["kill", pid])
    print "Created core file for " + executable


if __name__ == "__main__":
    clean_up_core_folder()
    compile_test_programs()
    executables = find_executables()
    for program in executables:
        run_and_core(program)
