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

## Implementation

The 128-bit divider uses accelerated 128-bit by 64-bit primitive to perform
step-wise base 2^64 long division using the divide instruction at most twice.
This is the dispatch function that chooses the division method:

```
/* 128-bit unsigned divmod using optimized intrinsics */

static inline i128_t i128_divmodu(i128_t u, i128_t v, i128_t *r)
{
    i128_t q;

    if (v.hi == 0 && v.lo == 0) {                   /* division by zero */
        q = i128_from_i64(-1);
        *r = u;
    }
    else if (u.hi == 0) {                           /* 64-bit dividend */
        if (v.hi == 0) {                            /* 64-bit divisor */
            q.hi = 0;
            q.lo = u.lo / v.lo;
            r->hi = 0;
            r->lo = u.lo % v.lo;
        } else {                                    /* 128-bit divisor */
            q = i128_from_u64(0);
            *r = u;
        }
    }
    else if (v.hi == 0) {                           /* 128-bit by 64-bit */
        i128_t q;
        r->hi = 0;
        if ((u64)u.hi < v.lo) {                     /* 64-bit quotient */
            q.hi = 0;
            q.lo = i64_udiv_i128_i64(u, v.lo, &r->lo);
        } else {                                    /* 128-bit quotient */
            i128_t u2, u3;
            u2 = i128_from_u64(u.hi);
            q.hi = i64_udiv_i128_i64(u2, v.lo, (u64*)&u3.hi);
            u3.lo = u.lo;
            q.lo = i64_udiv_i128_i64(u3, v.lo, &r->lo);
        }
        return q;
    }
    else {                                           /* 128-bit by 128-bit */
        q.hi = 0;
        q.lo = i64_udiv_i128_i128(u, v, r);
    }

    return q;
}
```

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
