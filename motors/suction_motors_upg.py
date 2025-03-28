import pigpio
import time

# Two ESC signal pins (Pin 7 and Pin 40)
ESC1_GPIO = 4    # GPIO4 -> Suction Motor 1
ESC2_GPIO = 21   # GPIO21 -> Suction Motor 2

# Initialize pigpio library and connect to daemon at localhost:8888
pi = pigpio.pi()
if not pi.connected:
    print(" Failed to connect to pigpio daemon at localhost:8888. Please start with: sudo pigpiod")
    exit(1)

def suction_init():
    print("Initializing suction ESC with 1000μs pulses")
    for _ in range(20):  # Send 1000μs pulses for 1 second to stabilize ESC
        pi.set_servo_pulsewidth(ESC1_GPIO, 1000)
        pi.set_servo_pulsewidth(ESC2_GPIO, 1000)
        time.sleep(0.05)

def suction_on(strength_us=1300):
    print(f"Suction motor on ({strength_us}μs)")
    pi.set_servo_pulsewidth(ESC1_GPIO, strength_us)
    pi.set_servo_pulsewidth(ESC2_GPIO, strength_us)

def suction_off():
    print("Suction motor off (1000μs)")
    pi.set_servo_pulsewidth(ESC1_GPIO, 1000)
    pi.set_servo_pulsewidth(ESC2_GPIO, 1000)

def suction_cleanup():
    print("Stopping PWM and cleaning up pigpio")
    pi.set_servo_pulsewidth(ESC1_GPIO, 0)
    pi.set_servo_pulsewidth(ESC2_GPIO, 0)
    pi.stop()
    print("Suction motor PWM stopped and pigpio released")
