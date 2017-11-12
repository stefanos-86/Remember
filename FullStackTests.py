# Test rig to do tests on the completed machinery.
# Runs GDB on one (or all) test core files and compare the test result with what
# is stored in the <test case name>_result.txt file(s).
# This too relies on a convention on the file names linking test cases, expected results, executables and core files.

import argparse
import difflib
import os
import re
import subprocess

import TestSuite as ts

LOGS_FOR_TESTS = "FullStackTest.log"

def parse_command_line():
    parser = argparse.ArgumentParser(description='Utility to quickly run the full stack test cases. '
                                                 'Run CreateTestCores.py first.'
                                                 'Stick to the file naming conventions.'
                                                 'Test cases are listed in the CMakeList.txt in'
                                                 ' ' + ts.TEST_PROGRAMS_FOLDER,
                                     epilog="(C) 2017 - Stefano",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-t", "--test_case",
                        help="Runs only the specified test case. Runs everything if not provided (None).",
                        required=False)

    return parser.parse_args()


def find_core_file(test_name):
    """Walks the test directory to detect a core file with the same name as the test case."""
    for subdir, dirs, files in os.walk(ts.CORES_FOLDER):
        for file in files:
            if file.startswith(test_name):
                    return os.path.join(subdir, file)
    return None


def assert_result(test_name):
    """Compares the expected and actual results. Prints the diff in case of error, nothing otherwise."""
    expected_result_file = os.path.join(ts.TEST_PROGRAMS_FOLDER, test_name + "_result.dot")

    with open(expected_result_file) as f:
        expected = f.readlines()

    with open(os.path.abspath("RememberOutput.dot")) as f:
        actual = f.readlines()

    expected = generic_addresses(expected)
    actual = generic_addresses(actual)

    changes = difflib.unified_diff(expected, actual,
                                   fromfile='expected_result_file',
                                   tofile='RESULT_FROM_TEST', lineterm='')
    result_lines = []
    for line in changes:
        result_lines.append(line)

    if len(result_lines) > 0:
        print " #################### FAIL ####################"
        for line in result_lines:
            print line,
        print " ##############################################"


def generic_addresses(dot_content):
    """The stack changes every time the core files are recreated.
       Should I commit the core files and the binaries in the repo?
       Or should I "wildcard" the addresses? Or abandon this way of testing?
       ...I wish I knew. For now, I replace the addresses with "generics"."""
    address_translation = {}
    address = re.compile("(0x[0-9a-f]+)")
    address_counter = 0
    filtered_result = []

    for line in dot_content:
        parts = address.split(line)
        filtered_line = ""
        for part in parts:
            if re.match(address, part):
                replacement = address_translation.get(part)
                if replacement is None:
                    replacement = "0xAddress_" + str(address_counter)
                    address_translation[part] = replacement
                    filtered_line += replacement
                    address_counter += 1
            else:
                filtered_line += part
        filtered_result.append(filtered_line)
    return filtered_result



def run_test(test_name):
    """Calls gdb with our driver and compares the result with the expected output."""
    core_file = find_core_file(test_name)
    if core_file is None:
        raise Exception("No core file for " + test_name)

    exeutable_file = os.path.join(ts.TEST_PROGRAMS_FOLDER, test_name)
    subprocess.call(["python", "remember.py", core_file,  exeutable_file,
                     "-l", LOGS_FOR_TESTS, "-o", "GraphFromLastTest.svg"])

    assert_result(test_name)

if __name__ == "__main__":
    args = parse_command_line()

    if args.test_case is None:
        test_list = ts.find_test_cases()
    else:
        test_list = [args.test_case]

    print "Tests to run " + str(test_list)

    for test_case in test_list:
        run_test(test_case)

