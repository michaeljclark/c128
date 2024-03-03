#undef NDEBUG
#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "integer.h"

#define X128 "%016llx%016llx"

#define dprintf(...) if (debug) printf(__VA_ARGS__)

#define DEFINE_TEST_OP_NAME(op) t_ ## op
#define DEFINE_TEST_OP_2(op)                                                  \
int DEFINE_TEST_OP_NAME(op)(i128_t a, i128_t e) {                             \
  i128_t r = op(a);                                                           \
  int p = memcmp(&r, &e, sizeof(r)) == 0;                                     \
  dprintf("%s p=%d a=" X128 " e=" X128 " r=" X128 "\n",                       \
    #op, p, a.n[1], a.n[0], e.n[1], e.n[0], r.n[1], r.n[0]);                  \
  return p;                                                                   \
}
#define DEFINE_TEST_OP_2_BIT(op)                                              \
int DEFINE_TEST_OP_NAME(op)(i128_t a, uint e) {                               \
  uint r = op(a);                                                             \
  int p = e == r;                                                             \
  dprintf("%s p=%d a=" X128 " e=%d r=%d\n",                                   \
    #op, p, a.n[1], a.n[0], e, r);                                            \
  return p;                                                                   \
}
#define DEFINE_TEST_OP_3(op)                                                  \
int DEFINE_TEST_OP_NAME(op)(i128_t a, i128_t b, i128_t e) {                   \
  i128_t r = op(a, b);                                                        \
  int p = memcmp(&r, &e, sizeof(r)) == 0;                                     \
  dprintf("%s p=%d a=" X128 " b=" X128 " e=" X128 " r=" X128 "\n",            \
    #op, p, a.n[1], a.n[0], b.n[1], b.n[0], e.n[1], e.n[0], r.n[1], r.n[0]);  \
  return p;                                                                   \
}
#define DEFINE_TEST_OP_3_CMP(op)                                              \
int DEFINE_TEST_OP_NAME(op)(i128_t a, i128_t b, int e) {                      \
  int r = op(a, b);                                                           \
  int p = e == r;                                                             \
  dprintf("%s p=%d a=" X128 " b=" X128 " e=%d r=%d\n",                        \
    #op, p, a.n[1], a.n[0], b.n[1], b.n[0], e, r);                            \
  return p;                                                                   \
}
#define DEFINE_TEST_OP_3_SH(op)                                               \
int DEFINE_TEST_OP_NAME(op)(i128_t a, uint b, i128_t e) {                     \
  i128_t r = op(a, b);                                                        \
  int p = memcmp(&r, &e, sizeof(r)) == 0;                                     \
  dprintf("%s p=%d a=" X128 " b=%-3d e=" X128 " r=" X128 "\n",                \
    #op, p, a.n[1], a.n[0], b, e.n[1], e.n[0], r.n[1], r.n[0]);               \
  return p;                                                                   \
}

static int debug, pass, count;
void accum(int r) { pass += r; count += 1; }

DEFINE_TEST_OP_3(i128_and)
DEFINE_TEST_OP_3(i128_or)
DEFINE_TEST_OP_3(i128_xor)
DEFINE_TEST_OP_3_SH(i128_sll)
DEFINE_TEST_OP_3_SH(i128_srl)
DEFINE_TEST_OP_3_SH(i128_sra)
DEFINE_TEST_OP_2(i128_not)
DEFINE_TEST_OP_2(i128_neg)
DEFINE_TEST_OP_3(i128_add)
DEFINE_TEST_OP_3(i128_sub)
DEFINE_TEST_OP_3(i128_mul)
DEFINE_TEST_OP_3(i128_mulu)
DEFINE_TEST_OP_3(i128_div)
DEFINE_TEST_OP_3(i128_divu)
DEFINE_TEST_OP_3(i128_rem)
DEFINE_TEST_OP_3(i128_remu)
DEFINE_TEST_OP_3_CMP(i128_cmp_eq)
DEFINE_TEST_OP_3_CMP(i128_cmp_lt)
DEFINE_TEST_OP_3_CMP(i128_cmp_gt)
DEFINE_TEST_OP_3_CMP(i128_cmp_ltu)
DEFINE_TEST_OP_3_CMP(i128_cmp_gtu)
DEFINE_TEST_OP_3_CMP(i128_cmp_t)
DEFINE_TEST_OP_3_CMP(i128_cmp_tu)
DEFINE_TEST_OP_2_BIT(i128_clz)
DEFINE_TEST_OP_2_BIT(i128_ctz)
DEFINE_TEST_OP_2_BIT(i128_popcnt)
DEFINE_TEST_OP_2(i128_bswap)
DEFINE_TEST_OP_2(i128_brev)

#include "test.inc"

int main(int argc, const char **argv)
{
    debug = (argc == 2 && strcmp(argv[1], "-d") == 0);
    test_i128_not();
    test_i128_and();
    test_i128_or();
    test_i128_xor();
    test_i128_sll();
    test_i128_srl();
    test_i128_sra();
    test_i128_neg();
    test_i128_add();
    test_i128_sub();
    test_i128_mul();
    test_i128_mulu();
    test_i128_div();
    test_i128_divu();
    test_i128_rem();
    test_i128_remu();
    test_i128_cmp_eq();
    test_i128_cmp_lt();
    test_i128_cmp_gt();
    test_i128_cmp_ltu();
    test_i128_cmp_gtu();
    test_i128_cmp_t();
    test_i128_cmp_tu();
    test_i128_clz();
    test_i128_ctz();
    test_i128_popcnt();
    test_i128_bswap();
    test_i128_brev();
    printf("%d/%d\n", pass, count);
}
