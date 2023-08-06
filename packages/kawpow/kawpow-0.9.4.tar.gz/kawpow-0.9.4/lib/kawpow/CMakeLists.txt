# kawpow: C/C++ implementation of Kawpow, the Ravencoin Proof of Work algorithm.
# Copyright 2018-2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

include(GNUInstallDirs)

add_library(
    kawpow
    bit_manipulation.h
    builtins.h
    endianness.hpp
    ${include_dir}/kawpow/kawpow.h
    ${include_dir}/kawpow/kawpow.hpp
    kawpow-internal.hpp
    kawpow.cpp
    ${include_dir}/kawpow/hash_types.h
    managed.cpp
    kiss99.hpp
    primes.h
    primes.c
    ${include_dir}/kawpow/progpow.hpp
    progpow.cpp
)

target_link_libraries(kawpow PRIVATE keccak)
target_include_directories(kawpow PUBLIC $<BUILD_INTERFACE:${include_dir}>$<INSTALL_INTERFACE:include>)
if(CABLE_COMPILER_GNULIKE AND NOT SANITIZE MATCHES undefined)
    target_compile_options(kawpow PRIVATE $<$<COMPILE_LANGUAGE:CXX>:-fno-rtti>)
endif()

install(
    TARGETS kawpow
    EXPORT kawpowTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
