import RPi.GPIO as GPIO
from time import sleep
import evdev
import subprocess
from evdev import InputDevice, categorize, ecodes
from motors.dc_motors_control import forward, backward, left, right, stop
from motors.suction_motors_control import suction_init, suction_on, suction_off, suction_cleanup


def run_camera():
    print("\n Running real_time_recognize.py...")
    subprocess.run(["python3", "/home/Haozhe/robot/camera/real_time_recognize.py"])

def listen_to_controller():
    devices = [InputDevice(path) for path in evdev.list_devices()]
    controller = None
    for device in devices:
        if "Pro Controller" in device.name:
            controller = InputDevice(device.path)
            print(f"Pro Controller connected: {device.name}")
            break

    if controller is None:
        print(" Pro Controller not found. Make sure it's paired via Bluetooth.")
        GPIO.cleanup()
        return

    BUTTON_Y = 308
    BUTTON_A = 305
    BUTTON_X = 307
    BUTTON_ZR = 313
    BUTTON_R = 311
      

    print("Use controller to control the motors. Press Y to start camera. START to exit.")
    try:
        #init suction motor
        current_throttle_us = 1100  # Start at 10%
        suction_init()
        
        #control dc motors
        for event in controller.read_loop():
            if event.type == ecodes.EV_ABS:
                if event.code == ecodes.ABS_HAT0Y:
                    if event.value == -1:
                        print("Forward")
                        forward()
                    elif event.value == 1:
                        print("Backward")
                        backward()
                    elif event.value == 0:
                        print("Stop")
                        stop()
                elif event.code == ecodes.ABS_HAT0X:
                    if event.value == -1:
                        print("Left")
                        left()
                    elif event.value == 1:
                        print("Right")
                        right()
                    elif event.value == 0:
                        print("Stop")
                        stop()
            

            elif event.type == ecodes.EV_KEY:
                # run camera
                if event.code == BUTTON_Y and event.value == 1:
                    run_camera()

                # suction on A
                elif event.code == BUTTON_A and event.value == 1:
                    suction_on(current_throttle_us)
                    print(f"Suction started at {int((current_throttle_us - 1000)/10)}% power")

                # increase suction R
                elif event.code == BUTTON_R and event.value == 1:
                    if current_throttle_us <= 1900:
                        current_throttle_us += 100
                        suction_on(current_throttle_us)
                        print(f"Suction increased to {int((current_throttle_us - 1000)/10)}%")

                # decrease suction ZR
                elif event.code == BUTTON_ZR and event.value == 1:
                    if current_throttle_us >= 1100:
                        current_throttle_us -= 100
                        suction_on(current_throttle_us)
                        print(f"Suction decreased to {int((current_throttle_us - 1000)/10)}%")

                # suction off X
                elif event.code == BUTTON_X and event.value == 1:
                    suction_off()
                    print("Suction stopped")

                # exit
                elif event.code == ecodes.BTN_START and event.value == 1:
                    print("Exiting and cleaning up...")
                    suction_off()
                    suction_cleanup()
                    GPIO.cleanup()
                    break

    except KeyboardInterrupt:
        print("Interrupted by user.")
        stop()
        suction_cleanup()
        GPIO.cleanup()


if __name__ == '__main__':
    listen_to_controller()
