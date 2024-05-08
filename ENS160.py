import time
import smbus

# Define I2C address of the sensor
SENSOR_ADDR = 0x53

# Define register addresses for sensor data
AQI_REGISTER = 0x35
#TVOC_REGISTER = 0x38
ECO2_REGISTER = 0x37
#0x01, 0x20, 0x36, 0x81 = 256
#0x35 = 1
#0x37 = petites valeurs qui varient
#0x38 = grosses valeurs qui varient
#0x80 = 24577
#0x7F = 96

# Initialize I2C bus
bus = smbus.SMBus(1) # Assuming Raspberry Pi 3 uses I2C bus 1

# Function to read sensor data
def read_sensor_data(register):
    # Read 2 bytes of data from the specified register
    data = bus.read_i2c_block_data(SENSOR_ADDR, register, 2)
    # Combine the bytes into a single 16-bit value
    value = (data[0] << 8) + data[1]
    return value

while True:
    # Read sensor data
    aqi = read_sensor_data(AQI_REGISTER)
    #tvoc = read_sensor_data(TVOC_REGISTER)
    eco2 = read_sensor_data(ECO2_REGISTER)
    
    # Print sensor data
    print("AQI (1-5):", aqi)
    #print("TVOC (ppb):", tvoc)
    print("eCO2 (ppm):", eco2)
    print()
    
    # Wait before reading again
    time.sleep(1)
