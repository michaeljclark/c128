cmake_minimum_required(VERSION 3.12)

project(c128)

include(CheckCCompilerFlag)
include(CheckCSourceCompiles)

set(CMAKE_C_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include_directories(include)
add_executable(test tests/test.c)
add_executable(bench tests/bench.c)
