from serial_interface import ThreadedSerial
from ethernet_interface import ThreadedServerExternal, ThreadedServerLocal
from PID import PID
from tools import *
import global_vars
import time



"""
https://www.tutorialspoint.com/python3/python_multithreading.htm
"""

if __name__ == "__main__":

    thread1 = ThreadedServerExternal(1, '', 50000)
    thread2 = ThreadedServerLocal(2, '', 52000)
    thread3 = ThreadedSerial(3, 'COM5', 115200)

    thread1.start()
    thread2.start()
    thread3.start()

    pid_x = PID()
    pid_y = PID()

    angle_x = 1
    angle_y = -1
    while 1:
    # for i in range(10):
    #     time.sleep(0.1)
    #     print(pid_x.calculate(angle_x), pid_y.calculate(angle_y))
    #     angle_x -= 1
    #     angle_y -= 1

        global_vars.port_info += 5
        # print(global_vars.port_info)
        if global_vars.local_message is not None:
            frame_number, left, top, width, height, confidence = handle_local_bytes(global_vars.local_message)
            diff_x, diff_y = calculate_instantaneous_angle(left, top, width, height)

            diff_x_pid, diff_y_pid = pid_x.calculate(diff_x), pid_y.calculate(diff_y)
            print("{}x{}, {:.2f}x{:.2f}, pid:{:.2f}x{:.2f}".format(left,top,diff_x, diff_y, diff_x_pid, diff_y_pid))
            thread3.run(angle_x=diff_x, angle_y=diff_y)
            global_vars.local_message = None



    thread1.join()
    thread2.join()
    thread3.join()

    print("Exiting Main Thread")
