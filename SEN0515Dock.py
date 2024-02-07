import smbus
import time

# Define the I2C address of the ENS160 sensor
ENS160_I2C_ADDRESS = 0x70

# Create an instance of the SMBus
bus = smbus.SMBus(1)  # 1 indicates the I2C bus number on Raspberry Pi 3

# Function to read data from the ENS160 sensor
def read_ens160_data():
    try:
        # Read 9 bytes of data from the ENS160 sensor
        data = bus.read_i2c_block_data(ENS160_I2C_ADDRESS, 0, 9)

        # Parse the data
        co2 = (data[0] << 8) | data[1]
        tvoc = (data[2] << 8) | data[3]
        humidity = (data[4] << 8) | data[5]
        temperature = ((data[6] << 8) | data[7]) / 100.0
        status = data[8]

        return co2, tvoc, humidity, temperature, status

    except Exception as e:
        print(f"Error reading data from ENS160: {e}")
        return None

# Main loop to continuously read and print sensor data
try:
    while True:
        # Read data from the ENS160 sensor
        sensor_data = read_ens160_data()

        if sensor_data:
            co2, tvoc, humidity, temperature, status = sensor_data

            # Print the sensor data
            print(f"CO2: {co2} ppm, TVOC: {tvoc} ppb, Humidity: {humidity}%, Temperature: {temperature}°C, Status: {status}")

        # Wait for 1 second before reading again
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting the program.")
finally:
    # Cleanup when the program is interrupted
    bus.close()
