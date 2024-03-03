#!/usr/bin/env python3

import random

# integer utilities

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def int_to_uint128(n):
	if n < 0:
		n = ((-n ^ (2 ** 128 - 1)) + 1) % (2 ** 128)
	return n

def uint128_to_int(n):
	if n & ((2 ** 127)-1):
		n = -(((n ^ (2 ** 128 - 1)) + 1) % (2 ** 128))
	return n

def int_to_i128_t(n,len,size,s):
	n = int_to_uint128(n)
	a = n.to_bytes(length=len, byteorder='little', signed=s)
	b = map(lambda x: int.from_bytes(x, byteorder='little'), chunks(a, size))
	c = map(lambda x: hex(x), b)
	d = map(lambda x: "%sLL" % x, c)
	return "(i128_t){%s}" % ",".join(d)

def gen_int128_random(i,j):
	x = random.randint(i,j)
	a = random.randint(0, 2 ** x - 1)
	s = random.randint(0,1)
	if s:
		a = -(a & ((2 ** 127)-1))
	return a

# generator functions

def gen_int128_test_oper2(op,l,a):
	e = l(a) % (2 ** 128)
	a_s = int_to_i128_t(a, 16, 8, False)
	e_s = int_to_i128_t(e, 16, 8, False)
	print("%4saccum(t_%s(%s,\n%22s%s));" % \
		("", op, a_s, "", e_s))

def gen_int128_test_bits2(op,l,a):
	e = l(a)
	a_s = int_to_i128_t(a, 16, 8, False)
	print("%4saccum(t_%s(%s,\n%22s%d));" % \
		("", op, a_s, "", e))

def gen_int128_test_oper3(op,l,a,b):
	e = l(a,b) % (2 ** 128)
	a_s = int_to_i128_t(a, 16, 8, False)
	b_s = int_to_i128_t(b, 16, 8, False)
	e_s = int_to_i128_t(e, 16, 8, False)
	print("%4saccum(t_%s(%s,\n%22s%s,\n%22s%s));" % \
		("", op, a_s, "", b_s, "", e_s))

def gen_int128_test_cmp3(op,l,a,b):
	e = l(a,b)
	a_s = int_to_i128_t(a, 16, 8, False)
	b_s = int_to_i128_t(b, 16, 8, False)
	print("%4saccum(t_%s(%s,\n%22s%s,\n%22s%d));" % \
		("", op, a_s, "", b_s, "", e))

def gen_int128_test_shamt3(op,l,a,shamt):
	e = l(a,shamt) % (2 ** 128)
	a_s = int_to_i128_t(a, 16, 8, False)
	e_s = int_to_i128_t(e, 16, 8, False)
	print("%4saccum(t_%s(%s,%d,\n%22s%s));" % \
		("", op, a_s, shamt, "", e_s))

def gen_int128_test_oper2_r(op,l,i,j):
	a = gen_int128_random(i,j)
	gen_int128_test_oper2(op,l,a)

def gen_int128_test_bits2_r(op,l,i,j):
	a = gen_int128_random(i,j)
	gen_int128_test_bits2(op,l,a)

def gen_int128_test_oper3_r(op,l,i,j):
	a = gen_int128_random(i,j)
	b = gen_int128_random(i,j)
	gen_int128_test_oper3(op,l,a,b)

def gen_int128_test_cmp3_r(op,l,i,j):
	a = gen_int128_random(i,j)
	b = gen_int128_random(i,j)
	gen_int128_test_cmp3(op,l,a,b)

def gen_int128_test_shamt3_r(op,l,i,j,shamt):
	a = gen_int128_random(i,j)
	gen_int128_test_shamt3(op,l,a,shamt)

def gen_int128_tests_oper2(op,l,n,i,j):
	print("void test_%s()\n{" % op);
	for h in range(0,n):
		gen_int128_test_oper2_r(op,l,i,j)
	print("}")

def gen_int128_tests_bits2(op,l,n,i,j):
	print("void test_%s()\n{" % op);
	for h in range(0,n):
		gen_int128_test_bits2_r(op,l,i,j)
	print("}")

def gen_int128_tests_oper3(op,l,n,i,j):
	print("void test_%s()\n{" % op);
	for h in range(0,n):
		gen_int128_test_oper3_r(op,l,i,j)
	print("}")

def gen_int128_tests_cmp3(op,l,n,i,j):
	print("void test_%s()\n{" % op);
	for h in range(0,n):
		gen_int128_test_cmp3_r(op,l,i,j)
	print("}")

def gen_int128_tests_shamt3(op,l,n,i,j,k):
	print("void test_%s()\n{" % op);
	for h in range(0,n):
		gen_int128_test_shamt3_r(op,l,i,j,random.randint(0,k))
	gen_int128_test_shamt3_r(op,l,i,j,0)
	gen_int128_test_shamt3_r(op,l,i,j,127)
	print("}")

# bitmanip functions

def clz(v):
	count = 0
	for i in reversed(range(128)):
		if (v & (1 << i)) == 0:
			count += 1
		else:
			break
	return count

def ctz(v):
	count = 0
	for i in range(v.bit_length()):
		if (v & (1 << i)) == 0:
			count += 1
		else:
			break
	return count

def popcnt(v):
	count = 0
	for i in range(v.bit_length()):
		if (v & (1 << i)) != 0:
			count += 1
	return count

# test functions

def fun_not(a):
	return ~a

def fun_and(a, b):
	return a & b

def fun_or(a, b):
	return a | b

def fun_xor(a, b):
	return a ^ b

def fun_sll(a, shamt):
	r = a << shamt
	return r

def fun_srl(a, shamt):
	r = uint128_to_int(int_to_uint128(a) >> shamt)
	return r

def fun_sra(a, shamt):
	r = a >> shamt
	return r

def fun_neg(a):
	return -a

def fun_add(a, b):
	return a + b

def fun_sub(a, b):
	return a - b

def fun_mul(a, b):
	r = a * b
	x = int_to_uint128(r)
	if r < 0:
		x = x | (1 << 127)
	else:
		x = x & ((1 << 127) - 1)
	return x

def fun_mulu(a, b):
	a = int_to_uint128(a)
	b = int_to_uint128(b)
	r = a * b
	x = int_to_uint128(r)
	return r

def fun_div(a, b):
	s_a = a >> 127
	s_b = b >> 127
	s_q = s_a ^ s_b
	a = (a ^ s_a) - s_a
	b = (b ^ s_b) - s_b
	if b:
		q = a // b
	else:
		q = -1
	x = int_to_uint128((q ^ s_q) - s_q)
	if x and s_q:
		return x | (1 << 127)
	else:
		return x & ((1 << 127) - 1)

def fun_divu(a, b):
	a = int_to_uint128(a)
	b = int_to_uint128(b)
	if b:
		q = a // b
	else:
		q = -1
	return int_to_uint128(q)

def fun_rem(a, b):
	s_a = a >> 127
	s_b = b >> 127
	a = (a ^ s_a) - s_a
	b = (b ^ s_b) - s_b
	if b:
		q = a % b
	else:
		q = a
	x = int_to_uint128((q ^ s_a) - s_a)
	if x and s_a:
		return x | (1 << 127)
	else:
		return x & ((1 << 127) - 1)

def fun_remu(a, b):
	a = int_to_uint128(a)
	b = int_to_uint128(b)
	if b:
		q = a % b
	else:
		q = a
	return int_to_uint128(q)

def fun_cmp_eq(a, b):
	return a == b

def fun_cmp_lt(a, b):
	return a < b

def fun_cmp_gt(a, b):
	return a > b

def fun_cmp_ltu(a, b):
	a = int_to_uint128(a)
	b = int_to_uint128(b)
	return a < b

def fun_cmp_gtu(a, b):
	a = int_to_uint128(a)
	b = int_to_uint128(b)
	return a > b

def fun_cmp_t(a, b):
	if a == b:
		return 0
	elif a < b:
		return -1
	else:
		return 1

def fun_cmp_tu(a, b):
	a = int_to_uint128(a)
	b = int_to_uint128(b)
	if a == b:
		return 0
	elif a < b:
		return -1
	else:
		return 1

def fun_clz(a):
	a = int_to_uint128(a)
	return clz(a)

def fun_ctz(a):
	a = int_to_uint128(a)
	return ctz(a)

def fun_popcnt(a):
	a = int_to_uint128(a)
	return popcnt(a)

def fun_bswap(a):
	n = int_to_uint128(a)
	a = n.to_bytes(length=16, byteorder='little')
	b = int.from_bytes(a, byteorder='big')
	return b

def fun_brev(a):
	n = int_to_uint128(a)
	r = 0
	for i in range(0,128):
		r |= ((n >> i) & 1) << (127-i)
	return r

def gen_int128_tests_all(n):
	gen_int128_tests_oper2('i128_not', fun_not, n, 8, 127)
	gen_int128_tests_oper3('i128_and', fun_and, n, 8, 127)
	gen_int128_tests_oper3('i128_or', fun_or, n, 8, 127)
	gen_int128_tests_oper3('i128_xor', fun_xor, n, 8, 127)
	gen_int128_tests_shamt3('i128_sll', fun_sll, n, 48, 127, 127)
	gen_int128_tests_shamt3('i128_srl', fun_srl, n, 96, 127, 127)
	gen_int128_tests_shamt3('i128_sra', fun_sra, n, 96, 127, 127)
	gen_int128_tests_oper2('i128_neg', fun_neg, n, 8, 127)
	gen_int128_tests_oper3('i128_add', fun_add, n, 8, 127)
	gen_int128_tests_oper3('i128_sub', fun_sub, n, 8, 127)
	gen_int128_tests_oper3('i128_mul', fun_mul, n, 8, 127)
	gen_int128_tests_oper3('i128_mulu', fun_mulu, n, 8, 127)
	gen_int128_tests_oper3('i128_div', fun_div, n, 8, 127)
	gen_int128_tests_oper3('i128_divu', fun_divu, n, 8, 127)
	gen_int128_tests_oper3('i128_rem', fun_rem, n, 8, 127)
	gen_int128_tests_oper3('i128_remu', fun_remu, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_eq', fun_cmp_eq, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_lt', fun_cmp_lt, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_gt', fun_cmp_gt, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_ltu', fun_cmp_ltu, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_gtu', fun_cmp_gtu, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_t', fun_cmp_t, n, 8, 127)
	gen_int128_tests_cmp3('i128_cmp_tu', fun_cmp_tu, n, 8, 127)
	gen_int128_tests_bits2("i128_clz", fun_clz, n, 8, 127)
	gen_int128_tests_bits2("i128_ctz", fun_ctz, n, 8, 127)
	gen_int128_tests_bits2("i128_popcnt", fun_popcnt, n, 8, 127)
	gen_int128_tests_oper2("i128_bswap", fun_bswap, n, 8, 127)
	gen_int128_tests_oper2("i128_brev", fun_brev, n, 8, 127)

gen_int128_tests_all(550)
