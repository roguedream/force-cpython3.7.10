def f():
    b = 1
    def g():
        return b
print(f())


#   1           0 LOAD_CONST               0 (<code object f at 0x0000024B6831F390, file "test-merge.py", line 1>)
#               2 LOAD_CONST               1 ('f')
#               4 MAKE_FUNCTION            0
#               6 STORE_NAME               0 (f)

#   5           8 LOAD_NAME                1 (print)
#              10 LOAD_NAME                0 (f)
#              12 CALL_FUNCTION            0
#              14 CALL_FUNCTION            1
#              16 POP_TOP
#              18 LOAD_CONST               2 (None)
#              20 RETURN_VALUE

# Disassembly of <code object f at 0x0000024B6831F390, file "test-merge.py", line 1>:
#   2           0 LOAD_CONST               1 (1)
#               2 STORE_DEREF              0 (b)

#   3           4 LOAD_CLOSURE             0 (b)
#               6 BUILD_TUPLE              1
#               8 LOAD_CONST               2 (<code object g at 0x0000024B6831BED0, file "test-merge.py", line 3>)
#              10 LOAD_CONST               3 ('f.<locals>.g')
#              12 MAKE_FUNCTION            8
#              14 STORE_FAST               0 (g)
#              16 LOAD_CONST               0 (None)
#              18 RETURN_VALUE

# Disassembly of <code object g at 0x0000024B6831BED0, file "test-merge.py", line 3>:
#   4           0 LOAD_DEREF               0 (b)
#               2 RETURN_VALUE

# a = 5
# def foo():
#     global a
#     if a > 1:
#         a = 30
#         print(a)
#     else:
#         a = 20
#         print(a)

# foo()
# _uname_cache = ""
# import os

# def lol():
#     global _uname_cache
#     no_os_uname = 0
#     if _uname_cache is not None:
#         return _uname_cache
#     else:
#         processor = ''
#         try:
#             system, node, release, version, machine = os.uname()
#         except AttributeError:
#             no_os_uname = 1
#         print("aaaaaaaaaaaaaaaa")
#         print("cccccccccccccccccccc")
#         if no_os_uname or system:
#             print("here")

# print(lol())
# print("only once")
# a = 0
# if a: print(a)
# else: print(a)

# a = [x for x in range(10) if x > 2]
# print(a)
# if a:
#     print(a)
# else:
#     print(a)

# if a:
#     print(a)
# print(a)

# a = 1
# if(a == 0):
#     print("1 branch 1")
#     print("1 branch 1 - 2")
#     if(a ==1):
#         print("1 branch 2")
#         print("1 branch 2 - 2")
#         if(a == 2):
#             print("1 branch 3")
#             print("1 branch 3 - 2")
#         else:
#             print("1 branch 3 else")
#             print("1 branch 3 else - 2")
#     else:
#         print("1 branch 2 else")
#         print("1 branch 2 else - 2")
# else:
#     print("1 branch 1 else")
#     if(a == 4):
#         print("1 branch 4")
#     else:
#         print("1 branch 4 else")
#         print("1 branch 4 else - 2")

# print("cut here")
# # print("aaaaaaaaaaaaaa")
# print("this should only be once")

# 1           0 LOAD_CONST               0 (1)
#               2 STORE_NAME               0 (a)

#   2           4 LOAD_NAME                0 (a)
#               6 LOAD_CONST               1 (0)
#               8 COMPARE_OP               2 (==)
#              10 POP_JUMP_IF_FALSE      114

#   3          12 LOAD_NAME                1 (print)
#              14 LOAD_CONST               2 ('1 branch 1')
#              16 CALL_FUNCTION            1
#              18 POP_TOP

#   4          20 LOAD_NAME                1 (print)
#              22 LOAD_CONST               3 ('1 branch 1 - 2')
#              24 CALL_FUNCTION            1
#              26 POP_TOP

#   5          28 LOAD_NAME                0 (a)
#              30 LOAD_CONST               0 (1)
#              32 COMPARE_OP               2 (==)
#              34 POP_JUMP_IF_FALSE       96

#   6          36 LOAD_NAME                1 (print)
#              38 LOAD_CONST               4 ('1 branch 2')
#              40 CALL_FUNCTION            1
#              42 POP_TOP

#   7          44 LOAD_NAME                1 (print)
#              46 LOAD_CONST               5 ('1 branch 2 - 2')
#              48 CALL_FUNCTION            1
#              50 POP_TOP

#   8          52 LOAD_NAME                0 (a)
#              54 LOAD_CONST               6 (2)
#              56 COMPARE_OP               2 (==)
#              58 POP_JUMP_IF_FALSE       78

#   9          60 LOAD_NAME                1 (print)
#              62 LOAD_CONST               7 ('1 branch 3')
#              64 CALL_FUNCTION            1
#              66 POP_TOP

#  10          68 LOAD_NAME                1 (print)
#              70 LOAD_CONST               8 ('1 branch 3 - 2')
#              72 CALL_FUNCTION            1
#              74 POP_TOP
#              76 JUMP_ABSOLUTE          112

#  12     >>   78 LOAD_NAME                1 (print)
#              80 LOAD_CONST               9 ('1 branch 3 else')
#              82 CALL_FUNCTION            1
#              84 POP_TOP

#  13          86 LOAD_NAME                1 (print)
#              88 LOAD_CONST              10 ('1 branch 3 else - 2')
#              90 CALL_FUNCTION            1
#              92 POP_TOP
#              94 JUMP_ABSOLUTE          156

#  15     >>   96 LOAD_NAME                1 (print)
#              98 LOAD_CONST              11 ('1 branch 2 else')
#             100 CALL_FUNCTION            1
#             102 POP_TOP

#  16         104 LOAD_NAME                1 (print)
#             106 LOAD_CONST              12 ('1 branch 2 else - 2')
#             108 CALL_FUNCTION            1
#             110 POP_TOP
#         >>  112 JUMP_FORWARD            42 (to 156)

#  18     >>  114 LOAD_NAME                1 (print)
#             116 LOAD_CONST              13 ('1 branch 1 else')
#             118 CALL_FUNCTION            1
#             120 POP_TOP

#  19         122 LOAD_NAME                0 (a)
#             124 LOAD_CONST              14 (4)
#             126 COMPARE_OP               2 (==)
#             128 POP_JUMP_IF_FALSE      140

#  20         130 LOAD_NAME                1 (print)
#             132 LOAD_CONST              15 ('1 branch 4')
#             134 CALL_FUNCTION            1
#             136 POP_TOP
#             138 JUMP_FORWARD            16 (to 156)

#  22     >>  140 LOAD_NAME                1 (print)
#             142 LOAD_CONST              16 ('1 branch 4 else')
#             144 CALL_FUNCTION            1
#             146 POP_TOP

#  23         148 LOAD_NAME                1 (print)
#             150 LOAD_CONST              17 ('1 branch 4 else - 2')
#             152 CALL_FUNCTION            1
#             154 POP_TOP

#  25     >>  156 LOAD_NAME                1 (print)
#             158 LOAD_CONST              18 ('cut here')
#             160 CALL_FUNCTION            1
#             162 POP_TOP

#  27         164 LOAD_NAME                1 (print)
#             166 LOAD_CONST              19 ('this should only be once')
#             168 CALL_FUNCTION            1
#             170 POP_TOP
#             172 LOAD_CONST              20 (None)
#             174 RETURN_VALUE
