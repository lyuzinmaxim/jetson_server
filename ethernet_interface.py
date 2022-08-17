import socket
import threading
import global_vars
import struct


class ThreadedServerLocal(threading.Thread):
    def __init__(self, threadID, host, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host = host
        self.port = port
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def run(self, verbose=False):
        if verbose:
            print("Starting " + self.name)

        while True:
            try:
                global_vars.local_message = self.socket.recvfrom(512)[0]
                if global_vars.local_message:
                    if verbose: print(global_vars.local_message, "from", self.port)
                    global_vars.port_info = 0
                    # return data
                else:
                    raise TypeError('Client disconnected')
            except KeyboardInterrupt:
                self.socket.close()

        print("Exiting " + self.name)


class ThreadedServerExternal(threading.Thread):
    def __init__(self, threadID, host, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host = host
        self.port = port
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.client = None

    def run(self):
        # print("Starting " + self.name)

        while True:
            try:
                data, self.client = self.socket.recvfrom(512)
                # print(self.client, data[0:2])
                if data[0:2] == b'\xaa\xaa':
                    decoded_enable = data[2:4]
                    decoded_dt = data[4:8]
                    decoded_kp, decoded_ki, decoded_kd = data[8:12], data[12:16], data[16:20]
                    decoded_min_angle, decoded_max_angle = data[20:22], data[22:24]

                    global_vars.enable_serial = int.from_bytes(decoded_enable, "big")
                    global_vars.dt = float(struct.unpack('>f', decoded_dt)[0])
                    global_vars.kp = float(struct.unpack('>f', decoded_kp)[0])
                    global_vars.ki = float(struct.unpack('>f', decoded_ki)[0])
                    global_vars.kd = float(struct.unpack('>f', decoded_kd)[0])
                    global_vars.min_angle = int.from_bytes(decoded_min_angle, "big", signed=True)
                    global_vars.max_angle = int.from_bytes(decoded_max_angle, "big", signed=True)

                    # print(data, "from", self.port)

                elif data[0:2] == b'\xaa\xbb':
                    self.socket.sendto(bytes.fromhex('BBBB') + \
                                       int(global_vars.enable_serial).to_bytes(2, byteorder='big', signed=True) + \
                                       struct.pack(">f", global_vars.dt) + \
                                       struct.pack(">f", global_vars.kp) + \
                                       struct.pack(">f", global_vars.ki) + \
                                       struct.pack(">f", global_vars.kd) + \
                                       int(global_vars.min_angle).to_bytes(2, byteorder='big', signed=True) + \
                                       int(global_vars.max_angle).to_bytes(2, byteorder='big', signed=True),
                                       self.client)


                # else:
                #     raise TypeError('Client disconnected')
            except socket.error:
                pass
            except KeyboardInterrupt:
                self.socket.close()

        print("Exiting " + self.name)
