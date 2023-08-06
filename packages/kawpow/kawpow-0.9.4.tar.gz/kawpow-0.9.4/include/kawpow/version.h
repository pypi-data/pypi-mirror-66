/* kawpow: C/C++ implementation of Kawpow, the Ravencoin Proof of Work algorithm.
 * Copyright 2019 Pawel Bylica.
 * Licensed under the Apache License, Version 2.0.
 */

#pragma once

/** The kawpow library version. */
#define KAWPOW_VERSION "0.9.4"

#ifdef __cplusplus
namespace kawpow
{
/// The kawpow library version.
constexpr auto version = KAWPOW_VERSION;

}  // namespace kawpow
#endif
