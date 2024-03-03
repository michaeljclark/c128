# c128

128-bit integer type with logic, shifts, arithmetic and bitmanip.

This header library includes an optimized portable 128-bit integer type:

- int128 implementation for platforms such as Clang and GCC, however,
  the compiler runtime version may be slower than this implementation.
- accelerated 64-bit 128-bit compiler intrinsics for MSVC, Clang and GCC:
  - `i128_umul_i64_i64` - 64-bit multiplication. 128-bit product.
  - `i64_umulh_i64_i64` - 64-bit multiplication, 64-bit high product.
  - `i64_udiv_i128_i64` - 128-bit division, 64-bit divisor, 64-bit quotient,
    64-bit remainder.
  - `i64_udiv_i128_i128` - 128-bit division, 128-bit divisor, 64-bit quotient,
    128-bit remainder. This version uses `clz` to renormalize the divisor.
- fallbacks for platforms that do not provide 128-bit intrinsics.
- libdivide 128-bit divider implementation for comparison purposes.

## Benchmarks

This header library includes a state-of-the-art 128-bit divider which
uses the minimum possible operations on x86-64 targets. 128-bit division
is approximately 4X slower than 64-bit division but potentially 5X faster
than bit-wise dividers in old versions of compiler-rt.

| benchmark (Intel Core i9-7980XE) | time    | cycles |
|:---------------------------------|--------:|-------:|
| `div_128_by_128`                 | 26.78ns |   ~110 |
| `div_128_by_64_large`            | 27.35ns |   ~110 |
| `div_128_by_64_small`            | 22.60ns |    ~90 |
| `div_64_by_64`                   |  7.30ns |    ~30 |

## Building

### Supported Platforms

- Windows, Linux, macOS, FreeBSD

### Building on Linux

```
cmake -B build_linux -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build_linux
```

### Building on Windows

```
cmake -B build_win32 -G "Visual Studio 17 2022" -A x64
cmake --build build_win32 --config RelWithDebInfo
```
