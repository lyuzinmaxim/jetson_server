import socket
import threading
import global_vars


class ThreadedServerLocal(threading.Thread):
    def __init__(self, threadID, host, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host = host
        self.port = port
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def run(self, verbose=False):
        if verbose: print("Starting " + self.name)

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

    def run(self):
        print("Starting " + self.name)

        while True:
            try:
                data = self.socket.recvfrom(512)[0]
                if data:
                    print(data, "from", self.port)
                else:
                    raise TypeError('Client disconnected')
            except KeyboardInterrupt:
                self.socket.close()

        print("Exiting " + self.name)