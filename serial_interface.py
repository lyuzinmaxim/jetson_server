import threading
import serial
import struct
from tools import CalculateCRC


class ThreadedSerial(threading.Thread):
    def __init__(self, threadID, device, speed=57600):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.device = device
        self.speed = speed
        self.serial = serial.Serial(port=device, baudrate=speed,write_timeout=0.05)

    def run(self, angle_x=0.1, angle_y=-0.1, distance=100, verbose=False):

        if verbose: print("Starting " + self.name)

        if verbose: print("Using port: {}".format(self.serial.name))
        data = bytes.fromhex('FACE') + \
                   int(60000).to_bytes(2, byteorder='little') + \
                   int(19).to_bytes(1, byteorder='little') + \
                   bytes.fromhex('11') + \
                   int(3500).to_bytes(2, byteorder='little') + \
                   int(7).to_bytes(2, byteorder='little') + \
                   int(3).to_bytes(2, byteorder='little') + \
                   bytearray(struct.pack("f", angle_x)) + \
                   bytearray(struct.pack("f", angle_y)) + \
                   bytearray(struct.pack("f", distance))

        data += (CalculateCRC(data)).to_bytes(2, byteorder='little')
        try:
            self.serial.write(data)
            # print("Sent {} bytes:".format(len(data)), ["%02x" % b for b in data])
            response = self.serial.read(25)
            # print("Output:{}".format(response.hex()))
        finally:

            if verbose: print("UP and DOWN done")
            pass
            # self.serial.close()
            # self.serial.__del__()

        # with self.serial as s:
        #     print("Using port: {}".format(s.name))
        #     data = bytes.fromhex('FACE') + \
        #            int(60000).to_bytes(2, byteorder='little') + \
        #            int(19).to_bytes(1, byteorder='little') + \
        #            bytes.fromhex('11') + \
        #            int(3500).to_bytes(2, byteorder='little') + \
        #            int(7).to_bytes(2, byteorder='little') + \
        #            int(3).to_bytes(2, byteorder='little') + \
        #            bytearray(struct.pack("f", 10)) + \
        #            bytearray(struct.pack("f", -0.2)) + \
        #            bytearray(struct.pack("f", 1001))
        #
        #     data += (CalculateCRC(data)).to_bytes(2, byteorder='little')
        #
        #     s.write(data)
        #     print("Sent {} bytes:".format(len(data)),["%02x" % b for b in data])
        #     response = s.read(25)
        #     print("Output:{}".format(response.hex()))
        #
        # s.close()