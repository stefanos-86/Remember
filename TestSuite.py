# Here we have some common code to handle the full-stack test cases.

import os


CORES_FOLDER = os.path.abspath("testCores")
TEST_PROGRAMS_FOLDER = os.path.abspath("testPrograms")


def find_test_cases():
    """Explores the conventional test programs folder to find all the executables to build in the cmake file. """
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
