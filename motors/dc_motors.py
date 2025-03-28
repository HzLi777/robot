import RPi.GPIO as GPIO
from time import sleep

# Motor A pins
in1 = 23
in2 = 24
ena = 25

# Motor B pins
in3 = 27
in4 = 22
enb = 17

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

# Start PWM
pwmA = GPIO.PWM(ena, 1000)
pwmB = GPIO.PWM(enb, 1000)
pwmA.start(50)  # default medium speed
pwmB.start(50)

direction = 'f'  # default direction forward

print("\nDual Motor Test - L298N with Raspberry Pi")
print("Controls:")
print("r - run")
print("s - stop")
print("f - forward")
print("b - backward")
print("l - turn left")
print("r - turn right")
print("1 - low speed")
print("2 - medium speed")
print("3 - high speed")
print("e - exit")
print("------------------------------------------")

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

while True:
    x = input("Enter command: ").lower()

    if x == 'r':
        print("Run")
        if direction == 'f':
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
        elif direction == 'b':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)

    elif x == 's':
        print("Stop")
        stop()

    elif x == 'f':
        print("Set direction: Forward")
        direction = 'f'
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    elif x == 'b':
        print("Set direction: Backward")
        direction = 'b'
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)

    elif x == 'l':
        print("Turn left")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    elif x == 'r':
        print("Turn right")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)

    elif x == '1':
        print("Low speed")
        pwmA.ChangeDutyCycle(30)
        pwmB.ChangeDutyCycle(30)

    elif x == '2':
        print("Medium speed")
        pwmA.ChangeDutyCycle(50)
        pwmB.ChangeDutyCycle(50)

    elif x == '3':
        print("High speed")
        pwmA.ChangeDutyCycle(75)
        pwmB.ChangeDutyCycle(75)

    elif x == 'e':
        print("Exiting and cleaning up...")
        stop()
        GPIO.cleanup()
        break

    else:
        print("Invalid command. Try again.")
