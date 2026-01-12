TEMPERATURE AND HUMIDITY MONITORING SYSTEM
README.txt

OVERVIEW

This project implements a simple system for measuring, logging, and visualizing temperature and relative humidity using an Arduino board and Python scripts.

The workflow is:

Arduino reads temperature and humidity via I2C and sends values over Serial

A Python script reads the Serial data, averages the measurements, and saves them to daily text files

Another Python script reads the saved files and displays temperature and humidity evolution in a GUI

The system is suitable for laboratory monitoring and long term measurements.

FILE STRUCTURE

read_i2c_sensor_values_on_serial_2024feb04_v02.ino
Read_com_port_for_temp_hum_2026_01_12_v01.py
Plot_temp_rh_from_file_2026_01_12_v09.py

ARDUINO CODE

File:
read_i2c_sensor_values_on_serial_2024feb04_v02.ino

Purpose:

Reads temperature and relative humidity from an I2C sensor

Sends formatted data over the Serial port

Serial output format (must be preserved):

Relative Humidity [%]: 45.2; Temperature [C]: 23.1

Requirements:

Arduino board

I2C temperature and humidity sensor (for example BME280)

Baud rate set to 115200

PYTHON SERIAL ACQUISITION AND LOGGING

File:
Read_com_port_for_temp_hum_2026_01_12_v01.py

Purpose:

Reads Serial data from Arduino

Extracts temperature and humidity

Buffers values and computes averages

Saves averaged values to daily text files

Output file format:

HH:MM:SS, temp: 23.15, rh: 45.80

Each file is named:
YYYY-MM-DD.txt

Main configuration parameters:

COM_PORT = "COM3"
BAUD_RATE = 115200
DATA_DIR = "D:/data/sensors"

Averaging interval:
Currently set to 20 seconds for testing.
Change to 1800 seconds for 30 minute averages.

Python requirements:

Python 3

pyserial

Install dependency:
pip install pyserial

PYTHON PLOTTING AND GUI

File:
Plot_temp_rh_from_file_2026_01_12_v09.py

Purpose:

Reads daily data files

Displays temperature and humidity for the last 24 hours

Shows the most recent values

Allows saving plots as PNG files

Directories used:

DATA_DIR = D:/data/sensors/
SAVE_DIR = D:/data/sensors/saved_plots/

Plot features:

X axis: time (last 24 hours)

Temperature shown in red

Humidity shown in blue

Automatic refresh every 30 seconds

Python requirements:

Python 3

matplotlib

tkinter (included by default on Windows)

Install matplotlib:
pip install matplotlib

TYPICAL USAGE

Upload the Arduino sketch to the board

Connect Arduino via USB

Run the acquisition script:
python Read_com_port_for_temp_hum_2026_01_12_v01.py

Let it run to generate daily files

Run the plotting script:
python Plot_temp_rh_from_file_2026_01_12_v09.py

NOTES

Local system time is used

Data is appended continuously

Missing or partial files are handled gracefully

Serial message format must not be changed

POSSIBLE EXTENSIONS

CSV output

Multiple sensor support

Configurable averaging interval

Network or database storage

Sensor ID tagging
