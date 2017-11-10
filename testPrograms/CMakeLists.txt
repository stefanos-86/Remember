# Creates one executable for each test case.
# Stick to the style: the support tools need to read it.

cmake_minimum_required(VERSION 2.8)
project(Remember)

add_definitions(-std=c++11 -g -O0)

add_executable(justMain                 justMain.cpp)

# "Legacy" stuff to be removed - don't forget to kill the sample programs!
#add_executable(infiniteMain                 infiniteMain.cpp)
#add_executable(infiniteMain_variables       infiniteMain_variables.cpp)
#add_executable(smallStack                   smallStack.cpp)
#add_executable(bigStack                     bigStack.cpp)
#add_executable(simpleStruct                 simpleStruct.cpp)
#add_executable(nestedStructs                nestedStructs.cpp)
#add_executable(mandrakata                   mandrakata.cpp)
