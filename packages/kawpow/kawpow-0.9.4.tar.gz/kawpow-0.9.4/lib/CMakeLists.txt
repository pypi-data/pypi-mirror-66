# kawpow: C/C++ implementation of Kawpow, the Ravencoin Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

add_subdirectory(keccak)
add_subdirectory(kawpow)

get_filename_component(KAWPOW_PRIVATE_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR} ABSOLUTE)
set(KAWPOW_PRIVATE_INCLUDE_DIR ${KAWPOW_PRIVATE_INCLUDE_DIR} PARENT_SCOPE)
