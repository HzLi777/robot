from gpiozero import DistanceSensor
import time
import threading

# Define the GPIO pins for each ultrasonic sensor
SENSORS = {
    "sensor_1": DistanceSensor(echo=5, trigger=6),  # Physical Pins 29, 31
}

# Function to measure distance continuously for each sensor
def measure_sensor(name, sensor):
    while True:
        distance_cm = sensor.distance * 100  # Convert meters to cm
        print(f"{name}: {distance_cm:2f} cm")
        time.sleep(0.5)  # Measure every 0.5 seconds

# Start multi-threaded measurement
threads = []
for name, sensor in SENSORS.items():
    thread = threading.Thread(target=measure_sensor, args=(name, sensor))
    threads.append(thread)
    thread.start()

# Handle script exit safely
try:
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    print("\nProgram terminated!")