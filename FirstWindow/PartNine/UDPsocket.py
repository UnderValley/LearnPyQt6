import socket
import zss_debug_pb2

UDP_IP = "127.0.0.1"
UDP_PORT = 22001

a = zss_debug_pb2.Debug_Msgs()

sock = socket.socket(socket.AF_INET,
                    socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(zss_debug_pb2.Debug_Msg.Debug_Type.LINE)
# print(len(a.msgs))
# print(a.msgs[0])
while True:
    data, addr = sock.recvfrom(65535)
    a.ParseFromString(data)
    # print("received message: %s \n***************************************" % a)
    print(len(a.msgs))
    i = 0
    while i < len(a.msgs):
        assd = a.msgs[i]
        i += 1
    print("********\n")
    # print(a)
    print("********\n")