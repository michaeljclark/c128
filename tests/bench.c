#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <time.h>

#include "integer.h"

#define MEASURE(n, b, x, u, v) {                                      \
    double s; int i; clock_t start, end;                              \
    start = clock();                                                  \
    for (i = 0; i < n; ++i) { x(u,v); }                               \
    end = clock();                                                    \
    s = ((double)(end - start) * 1e9) / (CLOCKS_PER_SEC * (double)n); \
    printf("%-26s%8.2fns\n", b, s);                                   \
}

const i128_t u1 = {0x500fcaea783e2246LL,0xfffe2f93e4ac9f2cLL};
const i128_t v1 = {0x1d46e94065c04c77LL,0xab5LL};

const i128_t u2 = {0x7456198f33449ae5LL,0x78d3f95b6c5d61LL};
const i128_t v2 = {0x8eebLL,0x0LL};

const i128_t u3 = {0x1ba1a4dfe28428c3LL,0x9a232LL};
const i128_t v3 = {0xa71fea28be21bLL,0x0LL};

const i128_t u4 = {0x500fcaea783e2246LL,0x0LL};
const i128_t v4 = {0x1d46e94065c04c77LL,0x0LL};

int main(int argc, const char **argv)
{
    MEASURE(10000000, "div_128_by_128", i128_divu, u1, v1);
    MEASURE(10000000, "div_128_by_64_large", i128_divu, u2, v2);
    MEASURE(10000000, "div_128_by_64_small", i128_divu, u3, v3);
    MEASURE(10000000, "div_64_by_64", i128_divu, u4, v4);
}
