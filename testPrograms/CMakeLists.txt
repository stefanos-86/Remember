# Creates one executable for each test case.
# Stick to the style: the support tools need to read it.

cmake_minimum_required(VERSION 2.8)
project(Remember)

add_definitions(-std=c++11 -g -O0)

add_executable(justMain                 justMain.cpp)
add_executable(mainLocalVariables       mainLocalVariables.cpp)
add_executable(recursiveStack           recursiveStack.cpp)
add_executable(stackWithPointers        stackWithPointers.cpp)
add_executable(stackLoop                stackLoop.cpp)
add_executable(chainOfPointers          chainOfPointers.cpp)
add_executable(heapLoop                 heapLoop.cpp)
add_executable(references               references.cpp)
add_executable(pointersInside           pointersInside.cpp)

# Not really intended for testing, but more to create nice graphs for demo purposes.
add_executable(demo demo.cpp)
