import RPi.GPIO as GPIO
import time

# Two ESC signal pins (Pin 7 and Pin 40)
ESC1_GPIO = 4    # Pin 7  -> Suction Motor 1
ESC2_GPIO = 21   # Pin 40 -> Suction Motor 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC1_GPIO, GPIO.OUT)
GPIO.setup(ESC2_GPIO, GPIO.OUT)

# Set PWM frequency to 50Hz
pwm1 = GPIO.PWM(ESC1_GPIO, 50)
pwm2 = GPIO.PWM(ESC2_GPIO, 50)
pwm1.start(5)  # Start with 1000μs signal to keep ESC idle
pwm2.start(5)

def set_throttle(pwm, us):
    """Convert microseconds to duty cycle and send to PWM channel"""
    dc = (us / 20000.0) * 100
    pwm.ChangeDutyCycle(dc)

def suction_init():
    print("Initializing suction ESC (1000μs with repeated pulses)")
    for _ in range(20):  # Send 1000μs multiple times to ensure ESC locks in
        set_throttle(pwm1, 1000)
        set_throttle(pwm2, 1000)
        time.sleep(0.05)

def suction_on(strength_us=1300):
    print(f"Suction motor on ({strength_us}μs)")
    set_throttle(pwm1, strength_us)
    set_throttle(pwm2, strength_us)

def suction_off():
    print("Suction motor off (1000μs)")
    set_throttle(pwm1, 1000)
    set_throttle(pwm2, 1000)

def suction_cleanup():
    print("Stopping PWM and cleaning up GPIO")
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    print("Suction motor PWM stopped and GPIO cleaned up")
