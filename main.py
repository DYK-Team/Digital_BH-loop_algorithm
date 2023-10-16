#
# Digital BH-loop algorithm
# Project repository on GitHub: https://github.com/DYK-Team/Digital_BH-loop_algorithm
# 15/10/2023
#
# Authors:
# Ekaterina Nefedova, Dr. Mark Nemirovich, Dr. Nikolay Udanov, and Prof. Larissa Panina
# MISiS, Moscow, Russia, https://en.misis.ru/
#
# Dr. Dmitriy Makhnovskiy
# DYK+ team, United Kingdom, www.dykteam.com
#

import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import tkinter as tk

# Default input parameter values
pi = np.pi  # pi-constant 3.1415....
default_B_scale = 1.0  # This scale depends on the measurement units (V or mV) and the wire length and diameter
default_H_scale = 1.0  # This scale depends on the measurement units (V or mV) and the wire length and diameter
default_window_size = 5  # Moving Average Window. You can change from the GUI window.

# Function to run the code with the entered parameters
def run_code():
    directory_path = directory_path_entry.get()  # Copy and paste the directory path to the GUI window
    name = name_entry.get()  # Enter the file name without the CSV extension to the GUI window (e.g. 50kHz)
    time_increment = float(time_increment_entry.get())  # Enter the time increment (s) to the GUI window
    B_scale = float(B_scale_entry.get())
    H_scale = float(H_scale_entry.get())
    window_size = int(window_size_entry.get())

    # Full file name, including the directory path and the csv extension
    file_name = directory_path + '\\' +name + '.csv'

    # Data from the CSV file (two columns without header)
    data = np.genfromtxt(file_name, delimiter=',')
    response_values = data[:, 0]  # First column: response values which are proportional to the induction B
    sin_values = data[:, 1]  # Second column: sinusoid values which are proportional to the scanning magnetic field H
    N = len(sin_values)  # Number of points in each column

    # Time values based on the time increment
    time = np.arange(0, N * time_increment, time_increment)

    # Estimation for the sinusoid amplitude
    A0 = np.max(sin_values)

    # Scenarios for selecting sine wave vertices
    scenario = 1 if sin_values[0] >= 0 else 2

    # Skipping initial values until the sinusoid changes sign. After this, the search for vertices begins.
    i = 0
    while i <= N - 1 and ((scenario == 1 and sin_values[i] >= 0) or (scenario == 2 and sin_values[i] <= 0)):
        i += 1
    start = i  # Start index

    # Searching for the indices of the first positive and negative sinusoid vertices

    # Set of indices near the positive vertex of the sinusoid
    def pset(start, y_values):
        positive_set = []
        i = start
        while i <= N - 1 and y_values[i] >= 0:
            if A0 * 0.9 <= y_values[i] <= A0:
                positive_set.append(i)
            i += 1
        stop = i
        return np.array(positive_set), stop

    # Set of indices near the negative vertex of the sinusoid
    def nset(start, y_values):
        negative_set = []
        i = start
        while i <= N - 1 and y_values[i] <= 0:
            if -A0 <= y_values[i] <= -A0 * 0.9:
                negative_set.append(i)
            i += 1
        stop = i
        return np.array(negative_set), stop

    if scenario == 1:
        negative_set, stop = nset(start, sin_values)
        positive_set = pset(stop, sin_values)[0]
    elif scenario == 2:
        positive_set, stop = pset(start, sin_values)
        negative_set = nset(stop, sin_values)[0]

    # Average indices for the found sets of the negative and positive sinusoid vertices
    positive_set_aver = float(sum(positive_set) / len(positive_set))
    negative_set_aver = float(sum(negative_set) / len(negative_set))

    # Integer indices for the found negative and positive sinusoid vertices
    pvertex = int(positive_set_aver)
    nvertex = int(negative_set_aver)

    # Estimations of the period (T0) and frequency (f0) of the sinusoid
    T0 = abs(positive_set_aver - negative_set_aver) * time_increment * 2
    f0 = 1 / T0

    # Improving A0: average amplitude of the sinusoid calculated from two vertices
    A0 = (sin_values[pvertex] - sin_values[nvertex]) / 2.0

    # Estimation of the sinusoid phase (ph0) in radians
    # Only positive phase will be used (anticlockwise rotation)
    qT = int(abs(pvertex - nvertex) / 2)  # Index difference for the quarter period
    value = max(-1.0, min(sin_values[0] / A0, 1.0))  # Normalising the zero-index value and clamping it to [-1, 1]
    phase = np.arcsin(value)  # Phase calculated from the arcsin function in the range [-pi/2, pi/2]
    if scenario == 1:  # First scenario sin_values[0] >= 0
        if sin_values[qT] >= 0:
            ph0 = phase  # First quarter
        else:
            ph0 = pi - phase  # Second quarter
    else:  # Second scenario sin_values[0] <= 0
        if sin_values[qT] <= 0:
            ph0 = pi - phase  # Third quarter
        else:
            ph0 = 2.0 * pi + phase  # Fourth quarter

    print('Estimated amplitude = ', A0)
    print('Estimated frequency = ', f0, ' Hz')
    print('Estimated phase = ', ph0, ' rads')
    print('Estimated phase = ', np.degrees(ph0), ' degrees')

    # Sinusoidal function used in the fitting
    def sinusoid(t, A, f, phase):
        return A * np.sin(2 * pi * f * t + phase)

    # Fitting the data (second column) to the sinusoid
    params, covariance = curve_fit(sinusoid, time, sin_values, p0=[A0, f0, ph0])  # [A0, f0, ph0] - initial values

    # Extracted fitting parameters
    A_fit, f_fit, ph_fit = params

    # Fitted sinusoid curve
    sinusoid_fit = sinusoid(time, A_fit, f_fit, ph_fit)
    ph_degrees = np.degrees(ph_fit)

    print('')
    print('Fitted amplitude = ', A_fit)
    print('Fitted frequency = ', f_fit, ' Hz')
    print('Fitted phase = ', ph_fit, ' rads')
    print('Fitted phase = ', ph_degrees, ' degrees')

    # Calculation of the reference time points t123 used in the numerical integration
    if scenario == 1:  # First scenario sin_values[0] >= 0
        t1 = (3.0 * pi / 2.0 - ph_fit) / (2.0 * pi * f_fit)
        t2 = (5.0 * pi / 2.0 - ph_fit) / (2.0 * pi * f_fit)
    else:  # Second scenario sin_values[0] <= 0
        t1 = (5.0 * pi / 2.0 - ph_fit) / (2.0 * pi * f_fit)
        t2 = (7.0 * pi / 2.0 - ph_fit) / (2.0 * pi * f_fit)
    t3 = t2 + 0.5 / f_fit

    print('')
    print('Reference time t1 = ', t1, ' s')
    print('Reference time t2 = ', t2, ' s')
    print('Reference time t3 = ', t3, ' s')

    # Indexes corresponding to the reference time moments
    refindex1 = int(t1 / time_increment)
    refindex2 = int(t2 / time_increment)
    refindex3 = int(t3 / time_increment)

    print('')
    print('Reference index 1 = ', refindex1)
    print('Reference index 2 = ', refindex2)
    print('Reference index 3 = ', refindex3)

    # Writing the parameters to the txt file
    with open(directory_path + '\\' + 'signal_parameters.txt', 'w') as file:
        file.write('\n')
        file.write('File name and directory {}\n'.format(file_name))
        file.write('\n')
        file.write('Time increment = {} s\n'.format(time_increment))
        file.write('Fitted sinusoid amplitude = {} (your units)\n'.format(A_fit))
        file.write('Fitted sinusoid frequency = {} Hz\n'.format(f_fit))
        file.write('Fitted sinusoid phase = {} rads\n'.format(ph_fit))
        file.write('Fitted sinusoid phase = {} degrees\n'.format(ph_degrees))
        file.write('\n')
        file.write('B-scale = {} \n'.format(B_scale))
        file.write('H-scale = {} \n'.format(H_scale))
        file.write('\n')
        file.write('Reference time t1 = {} s \n'.format(t1))
        file.write('Reference time t2 = {} s \n'.format(t2))
        file.write('Reference time t3 = {} s \n'.format(t3))
        file.write('\n')
        file.write('Reference index 1 = {} \n'.format(refindex1))
        file.write('Reference index 2 = {} \n'.format(refindex2))
        file.write('Reference index 3 = {} \n'.format(refindex3))

    # Plot the original data and the fitted curve
    plt.figure(figsize=(10, 6))
    plt.scatter(time, sin_values, label='Original Data', color='blue', marker='o')
    plt.plot(time, sinusoid_fit, label='Fitted Sinusoid', color='red')

    # Add vertical lines at t1, t2, and t3
    plt.axvline(x=t1, color='green', linestyle='--', label='t1')
    plt.axvline(x=t2, color='purple', linestyle='--', label='t2')
    plt.axvline(x=t3, color='orange', linestyle='--', label='t3')

    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Sinusoidal Fit with Reference Points t1, t2, and t3')
    plt.legend()
    plt.grid(True)

    # Saving the plot as an image
    plt.savefig(directory_path + '\\' + 'sinusoid_fitting_reference_points.png')

    plt.show()

    # Forward integration of the voltage response between the reference indexes 1 and 2
    B_forward = []
    H_forward = []
    integral_value = 0.0
    for i in range(refindex1, refindex2):
        H_forward.append(sin_values[i])
        for i in range(refindex1, i):
            integral_value += 0.5 * (response_values[i] + response_values[i + 1]) * time_increment  # Trapezoid method
        B_forward.append(integral_value)

    # Reverse integration of the voltage response between the reference indexes 2 and 3
    B_reverse = []
    H_reverse = []
    integral_value = 0.0
    for i in range(refindex2, refindex3):
        H_reverse.append(sin_values[i])
        for i in range(refindex2, i):
            integral_value += 0.5 * (response_values[i] + response_values[i + 1]) * time_increment  # Trapezoid method
        B_reverse.append(integral_value)

    # Rescaling the magnetic induction B and the field H from the data values
    B_forward = np.array(B_forward) * B_scale
    H_forward = -np.array(H_forward) * H_scale
    lf = len(B_forward)  # Number of points in the forward BH curve
    B_reverse = np.array(B_reverse) * B_scale
    H_reverse = -np.array(H_reverse) * H_scale
    lr = len(B_reverse)  # Number of points in the reverse BH curve

    # Defining the concavity con_forward of the forward BH curve
    # B = af + bf * H is the straight line between the forward BH curve ends
    bf = (B_forward[lf - 1] - B_forward[0]) / (H_forward[lf - 1] - H_forward[0])
    af = (B_forward[0] * H_forward[lf - 1] - B_forward[lf - 1] * H_forward[0]) / (H_forward[lf - 1] - H_forward[0])
    # Direction of the concavity
    if (af + bf * (H_forward[lf - 1] - H_forward[0]) / 2) >= B_forward[int(lf / 2)]:
        con_forward = 'down'
    else:
        con_forward = 'up'

    # Defining the concavity con_reverse of the reverse BH curve
    # B = ar + br * H is the straight line between the reverse BH curve ends
    br = (B_reverse[lr - 1] - B_reverse[0]) / (H_reverse[lr - 1] - H_reverse[0])
    ar = (B_reverse[0] * H_reverse[lr - 1] - B_reverse[lr - 1] * H_reverse[0]) / (H_reverse[lr - 1] - H_reverse[0])
    # Direction of the concavity
    if (ar + br * (H_reverse[lr - 1] - H_reverse[0]) / 2) >= B_reverse[int(lr / 2)]:
        con_reverse = 'down'
    else:
        con_reverse = 'up'

     # Vertical shifts of the BH curves
    if con_forward == 'up':
        B_forward = B_forward + abs(B_forward[0] - B_forward[lf - 1]) / 2
    else:
        B_forward = B_forward - abs(B_forward[0] - B_forward[lf - 1]) / 2

    if con_reverse == 'up':
        B_reverse = B_reverse + abs(B_reverse[0] - B_reverse[lr - 1]) / 2
    else:
        B_reverse = B_reverse - abs(B_reverse[0] - B_reverse[lr - 1]) / 2

    # Function for computing the moving average
    def moving_average(data, window_size):
        cumsum = np.cumsum(data)
        cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
        return cumsum[window_size - 1:] / window_size

    # Smoothing the data using moving averages
    B_forward_smoothed = moving_average(B_forward, window_size)
    H_forward_smoothed = moving_average(H_forward, window_size)
    B_reverse_smoothed = moving_average(B_reverse, window_size)
    H_reverse_smoothed = moving_average(H_reverse, window_size)

    # Creating the graph of smoothed curves
    plt.figure(figsize=(10, 6))
    plt.plot(H_forward_smoothed, B_forward_smoothed, label='Smoothed B_forward vs. H_forward', color='blue')
    plt.plot(H_reverse_smoothed, B_reverse_smoothed, label='Smoothed B_reverse vs. H_reverse', color='red')
    plt.xlabel('H (A/m)')
    plt.ylabel('B (T)')
    plt.title('Smoothed Magnetic Hysteresis Loop')
    plt.legend()
    plt.grid(True)

    # Saving the data and smoothed curves to a CSV file
    data = np.column_stack((H_forward_smoothed, B_forward_smoothed, H_reverse_smoothed, B_reverse_smoothed))
    header = ['H_forward (A/m)', 'B_forward_smoothed (T)', 'H_reverse (A/m)', 'B_reverse_smoothed (T)']

    with open(directory_path + '\\' + 'smoothed_hysteresis_data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

    # Saving the plot as an image
    plt.savefig(directory_path + '\\' + 'smoothed_hysteresis_plot.png')

    plt.show()

# Create a function to stop the code execution
def stop_code():
    quit()

# Main GUI window
root = tk.Tk()
root.title("Input Parameters")

# Labels and entry fields for input parameters
directory_path_label = tk.Label(root, text="Directory Path:")
directory_path_label.pack()
directory_path_entry = tk.Entry(root)
directory_path_entry.pack()

name_label = tk.Label(root, text="File Name (without extension):")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

time_increment_label = tk.Label(root, text="Time Increment (s):")
time_increment_label.pack()
time_increment_entry = tk.Entry(root)
time_increment_entry.pack()

B_scale_label = tk.Label(root, text="B-scale:")
B_scale_label.pack()
B_scale_entry = tk.Entry(root)
B_scale_entry.insert(0, default_B_scale)  # Default value
B_scale_entry.pack()

H_scale_label = tk.Label(root, text="H-scale:")
H_scale_label.pack()
H_scale_entry = tk.Entry(root)
H_scale_entry.insert(0, default_H_scale)  # Default value
H_scale_entry.pack()

window_size_label = tk.Label(root, text="Moving Average Window:")
window_size_label.pack()
window_size_entry = tk.Entry(root)
window_size_entry.insert(0, default_window_size)  # Default value
window_size_entry.pack()

# Frame to hold the buttons in one row
button_frame = tk.Frame(root)
button_frame.pack()

# "Run Code" button with some padding to the right
run_button = tk.Button(button_frame, text="Run Code", command=run_code)
run_button.pack(side=tk.LEFT, padx=5)  # Adjust the padx value as needed

# "Stop Code" button with some padding to the left
stop_button = tk.Button(button_frame, text="Stop Code", command=stop_code)
stop_button.pack(side=tk.LEFT, padx=5)  # Adjust the padx value as needed

# Main event loop
root.mainloop()