# use pyserial
import serial
import time
from datetime import datetime
from pathlib import Path

# COM port settings
COM_PORT = "COM3"
BAUD_RATE = 115200

# File directory for saving data
DATA_DIR = Path("D:/data/sensors")  # change if needed

def read_serial_data(port: str, baudrate: int, timeout: int = 3) -> str:
    """
    Read one line from serial port and return it as text.
    """
    with serial.Serial(port, baudrate, timeout=timeout) as ser:
        raw = ser.readline()
        # be robust to weird bytes
        return raw.decode(errors="replace").strip()

def save_data_to_file(line: str, filepath: Path) -> None:
    """
    Append one line to a text file.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)  # make sure folder exists
    print(f"Writing data to file: {filepath}")
    with filepath.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def average_data(values):
    """
    Calculate the average of a list of numeric values.
    """
    return (sum(values) / len(values)) if values else None

if __name__ == "__main__":
    # Initialize variables
    data_buffer = {"temperature": [], "humidity": []}
    start_time = time.time()

    # Make sure base folder exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            # Read data from serial port
            data = read_serial_data(COM_PORT, BAUD_RATE)
            if not data:
                continue

            print("Received data:", data)

            # Check if the received data matches the expected format
            if "Relative Humidity [%]:" in data and "Temperature [C]:" in data:
                # Expected example:
                # "Relative Humidity [%]: 45.2; Temperature [C]: 23.1"
                parts = data.split(";")
                if len(parts) < 2:
                    print("Unexpected split format:", data)
                    continue

                humidity_str = parts[0].split(":", 1)[1].strip()
                temperature_str = parts[1].split(":", 1)[1].strip()

                # Convert temperature and humidity to float
                temperature = float(temperature_str)
                humidity = float(humidity_str)

                # Append data to buffer
                data_buffer["temperature"].append(temperature)
                data_buffer["humidity"].append(humidity)

                # Check if 30 minutes have elapsed
                elapsed_time = time.time() - start_time
                if elapsed_time >= 20 :  # 30 seconds in seconds
                    # Calculate averages
                    avg_temperature = average_data(data_buffer["temperature"])
                    avg_humidity = average_data(data_buffer["humidity"])

                    # Build daily filename inside DATA_DIR
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    filename = DATA_DIR / f"{current_date}.txt"

                    # Prepare line to save
                    line = (
                        f"{datetime.now().strftime('%H:%M:%S')}, "
                        f"temp: {avg_temperature:.2f}, "
                        f"rh: {avg_humidity:.2f}"
                    )

                    # Save data to file
                    save_data_to_file(line, filename)

                    # Reset buffer and timer
                    data_buffer = {"temperature": [], "humidity": []}
                    start_time = time.time()

            else:
                print("Received data does not match expected format:", data)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
