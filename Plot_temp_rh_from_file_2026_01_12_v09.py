import os
import matplotlib
matplotlib.use('TkAgg')  # Set backend to TkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter as tk

# File directory for saved data
DATA_DIR = 'D:/data/sensors/'
SAVE_DIR = 'D:/data/sensors/saved_plots/'

def read_data_from_file(filename):
    """
    Read data from a text file with the specified format.
    """
    temperature = []
    humidity = []
    timestamps = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 3:  # Check if the line has at least three parts
                try:
                    # Extract timestamp and date from the line
                    timestamp_str = parts[0].strip()
                    date_str = os.path.basename(filename).split('.')[0]  # Extract date from the file name
                    full_timestamp_str = f"{date_str} {timestamp_str}"
                    
                    timestamp = datetime.strptime(full_timestamp_str, '%Y-%m-%d %H:%M:%S')
                    temperature.append(float(parts[1].split(':')[1].strip()))
                    humidity.append(float(parts[2].split(':')[1].strip()))
                    timestamps.append(timestamp)
                except (IndexError, ValueError) as e:
                    print(f"Error: {e} - Line: {line}")
    return temperature, humidity, timestamps

def plot_data(temperature, humidity, timestamps, ax):
    """
    Plot temperature and humidity data.
    """
    ax.clear()
    ax.scatter(timestamps, temperature, label='Temperature (°C)', color='r', marker='o')
    ax.scatter(timestamps, humidity, label='Humidity (%)', color='b', marker='o')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')

    # Set x-axis limits to show only the last 24 hours
    last_24_hours = datetime.now() - timedelta(hours=24)
    ax.set_xlim([last_24_hours, datetime.now()])

    ax.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))

    ax.set_title(f'Temperature and Humidity Variation in Last 24 Hours: {timestamps[0].strftime("%Y-%m-%d")} - {timestamps[-1].strftime("%Y-%m-%d")}')
    ax.legend()
    ax.grid(True)
    ax.set_ylim([-15, 100])  # Set y-axis limit for humidity

def update_plot():
    """
    Update the plot with new data.
    """
    global ax, fig

    # Get file paths for the last 24 hours
    current_time = datetime.now()
    start_time = current_time - timedelta(hours=24)
    filepaths = []
    while current_time > start_time:
        filepath = os.path.join(DATA_DIR, current_time.strftime('%Y-%m-%d.txt'))
        if os.path.exists(filepath):
            filepaths.append(filepath)
        current_time -= timedelta(hours=1)

    # Read data from files
    temperature_data = []
    humidity_data = []
    all_timestamps = []
    for filepath in reversed(filepaths):  # Reversed to start from the earliest file
        temp, hum, timestamps = read_data_from_file(filepath)
        temperature_data.extend(temp)
        humidity_data.extend(hum)
        all_timestamps.extend(timestamps)

    # Plot data
    plot_data(temperature_data, humidity_data, all_timestamps, ax)

    # Update last values
    if timestamps:
        temp_value.set(f'{temperature_data[-1]:.2f} °C')
        hum_value.set(f'{humidity_data[-1]:.2f} %')

    plt.draw()

def save_plot():
    """
    Save the current plot as a PNG file.
    """
    current_time = datetime.now()
    save_path = os.path.join(SAVE_DIR, f'plot_{current_time.strftime("%Y%m%d%H%M%S")}.png')
    fig.savefig(save_path)
    print(f'Plot saved at: {save_path}')

def auto_update_plot():
    """
    Periodically update the plot with new data.
    """
    update_plot()
    root.after(30000, auto_update_plot)  # Update every 30 seconds (30000 milliseconds)

def main():
    """
    Main function to set up the plot window and update button.
    """
    global ax, fig, root, temp_value, hum_value

    root = tk.Tk()
    root.title("Temperature and Humidity Plot")

    fig, ax = plt.subplots(figsize=(10, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    values_frame = tk.Frame(root)
    values_frame.pack(side=tk.BOTTOM, fill=tk.X)

    temp_label = tk.Label(values_frame, text="Temperature", font=('Arial', 16))
    temp_label.grid(row=0, column=0, padx=(10, 5))
    temp_value = tk.StringVar()
    temp_value.set("-")
    temp_display = tk.Label(values_frame, textvariable=temp_value, font=('Arial', 24))
    temp_display.grid(row=0, column=1, padx=5)

    hum_label = tk.Label(values_frame, text="Humidity", font=('Arial', 16))
    hum_label.grid(row=0, column=2, padx=(10, 5))
    hum_value = tk.StringVar()
    hum_value.set("-")
    hum_display = tk.Label(values_frame, textvariable=hum_value, font=('Arial', 24))
    hum_display.grid(row=0, column=3, padx=(5, 10))

    update_button = tk.Button(root, text="Update", command=update_plot)
    update_button.pack(side=tk.BOTTOM, pady=10)

    update_plot()  # Initially plot the data

    root.protocol("WM_DELETE_WINDOW", root.quit)  # Close the program when the window is closed
    
    # Schedule the auto-update function
    root.after(0, auto_update_plot)

    root.mainloop()

if __name__ == "__main__":
    # Create the SAVE_DIR directory if it doesn't exist
    os.makedirs(SAVE_DIR, exist_ok=True)
    main()
