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
        # print("{} {:.2f} {:.2f} {:.2f} {:.2f} {} {}".format(global_vars.enable_serial,global_vars.dt, global_vars.kp, global_vars.ki, global_vars.kd,
        #                                                  global_vars.min_angle, \
        #                                                  global_vars.max_angle))
        pid_x.min_angle, pid_x.max_angle, pid_x.dt, pid_x.kp, pid_x.ki, pid_x.kd = \
            global_vars.min_angle, global_vars.max_angle, global_vars.dt, global_vars.kp, global_vars.ki, global_vars.kd
        pid_y.min_angle, pid_y.max_angle, pid_y.dt, pid_y.kp, pid_y.ki, pid_y.kd = \
            global_vars.min_angle, global_vars.max_angle, global_vars.dt, global_vars.kp, global_vars.ki, global_vars.kd

        if global_vars.local_message is not None:
            frame_number, left, top, width, height, confidence = handle_local_bytes(global_vars.local_message)
            diff_x, diff_y = calculate_instantaneous_angle(left, top, width, height)

            diff_x_pid, diff_y_pid = pid_x.calculate(diff_x), pid_y.calculate(diff_y)
            print("{}x{}, {:.2f}x{:.2f}, pid:{:.2f}x{:.2f}".format(left, top, diff_x, diff_y, diff_x_pid, diff_y_pid))

            if global_vars.enable_serial:
                thread3.run(angle_x=diff_x, angle_y=diff_y)
                print("aaa")
            global_vars.local_message = None

    thread1.join()
    thread2.join()
    thread3.join()

    print("Exiting Main Thread")
