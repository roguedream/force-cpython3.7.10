# m = input("give me input")
# print(m)
# if(m == "input 1"):
#     print(11111)
# if(m == "input 2"):
#     print(222222)

# x = input("123")
# if x == '1':
#     print('TEST 1')
a = 0
while 1:
    a = a + 1
    print(a)
print("OUT OF LOOP")
    # x = input('> ')
    # if x == '1':
    #     a = a + 1
    #     print('TEST 1')
        # break
# test_file = open("aaaaaa.txt","w")
# payload = test_file.readline()
# real_payload = payload.decrypt(a)

# def myfunc():
#     a = 0
#     while a < 20:
#         a = a + 1
#         print(a)
#     print("OUT OF LOOP")

# import dis
# print(dis.dis(myfunc))

# 26           0 LOAD_CONST               1 (0)
#               2 STORE_FAST               0 (a)

#  27           4 SETUP_LOOP              28 (to 34)
#         >>    6 LOAD_FAST                0 (a)
#               8 LOAD_CONST               2 (20)
#              10 COMPARE_OP               0 (<)
#              12 POP_JUMP_IF_FALSE       32

#  28          14 LOAD_FAST                0 (a)
#              16 LOAD_CONST               3 (1)
#              18 BINARY_ADD
#              20 STORE_FAST               0 (a)

#  29          22 LOAD_GLOBAL              0 (print)
#              24 LOAD_FAST                0 (a)
#              26 CALL_FUNCTION            1
#              28 POP_TOP
#              30 JUMP_ABSOLUTE            6
#         >>   32 POP_BLOCK

#  30     >>   34 LOAD_GLOBAL              0 (print)
#              36 LOAD_CONST               4 ('OUT OF LOOP')
#              38 CALL_FUNCTION            1
#              40 POP_TOP
#              42 LOAD_CONST               0 (None)
#              44 RETURN_VALUE
# None