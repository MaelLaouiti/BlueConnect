import smbus
import time

# Define I2C address for BH1750 sensor
BH1750_ADDR = 0x23

# Define command to measure continuously in high resolution mode
CONTINUOUS_HIGH_RES_MODE = 0x10

# Create an instance of the smbus module to communicate with I2C
bus = smbus.SMBus(1)

# Function to read light intensity from the sensor
def read_light_intensity():
    # Send command to measure light intensity
    bus.write_byte(BH1750_ADDR, CONTINUOUS_HIGH_RES_MODE)
    
    # Wait for measurement to be ready (depends on the integration time)
    time.sleep(0.2)  # Adjust this value according to your sensor's integration time
    
    # Read 2 bytes of data from the sensor
    data = bus.read_i2c_block_data(BH1750_ADDR, 0x00, 2)
    
    # Convert the data to lux
    light_intensity = (data[1] + (256 * data[0])) / 1.2
    
    return light_intensity

try:
    while True:
        # Read light intensity
        intensity = read_light_intensity()
        
        # Print the light intensity
        print("Light Intensity: {} lux".format(intensity))
        
        # Wait for some time before taking the next measurement
        time.sleep(1)  # Adjust this value as per your requirement

except KeyboardInterrupt:
    print("Measurement stopped by the user")
