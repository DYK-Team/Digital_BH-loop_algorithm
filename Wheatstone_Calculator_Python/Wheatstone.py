#
# Wheatstone calculator
# Project repository on GitHub: https://github.com/DYK-Team/Digital_BH-loop_algorithm
# 16/10/2023
#
# Authors:
# Ekaterina Nefedova, Dr. Mark Nemirovich, Dr. Nikolay Udanov, and Prof. Larissa Panina
# MISiS, Moscow, Russia, https://en.misis.ru/
#
# Dr. Dmitriy Makhnovskiy
# DYK+ team, United Kingdom, www.dykteam.com
#

import tkinter as tk
from PIL import Image, ImageTk

def calculate():
    R0 = float(R0_entry.get())
    R1 = float(R1_entry.get())
    R3 = float(R3_entry.get())
    Rw = float(Rw_entry.get())

    # Calculate R2 that provides the balance of the bridge circuit
    R2 = R1 * Rw / R3

    # Calculate VM / Vout
    VM_Vout = (R3 + Rw) / R3

    # Calculate Vw / V0
    Vw_V0 = ((R1 + R2) * Rw) / (R0 * (R1 + R2 + R3 + Rw) + (R1 + R2) * (R3 + Rw))

    # Update the equation label with the calculated R2 value and the value for VM / Vout and Vw / V0
    equation_label.config(text=f"R2 = Rw x R1 / R3 = {R2:.3f} Ohms\n\nVM / Vout = (R3 + Rw) / R3 = {VM_Vout:.3f}"
                               f"\n\nVw / V0 = {Vw_V0:.3f}")

# Function to stop the calculation and close the program
def stop_calculation():
    window.quit()

# Create the main window
window = tk.Tk()
window.title("Resistor Calculator")

# Create a frame for the left side
left_frame = tk.Frame(window)
left_frame.grid(row=0, column=0, padx=10, pady=10)  # Increased space using pady

# Create a frame for the right side (picture)
right_frame = tk.Frame(window)
right_frame.grid(row=0, column=1, padx=10, pady=10)  # Increased space using pady

# Add a message for entering resistor values
message_label = tk.Label(left_frame, text="Enter the resistor values in Ohms:")
message_label.grid(row=0, columnspan=2, pady=10)  # Increased space using pady

# Create labels and entry fields for resistor values with increased space
R0_label = tk.Label(left_frame, text="R0:")
R0_label.grid(row=1, column=0, pady=10)  # Increased space using pady
R0_entry = tk.Entry(left_frame)
R0_entry.grid(row=1, column=1, pady=10)  # Increased space using pady

R1_label = tk.Label(left_frame, text="R1:")
R1_label.grid(row=2, column=0, pady=10)  # Increased space using pady
R1_entry = tk.Entry(left_frame)
R1_entry.grid(row=2, column=1, pady=10)  # Increased space using pady

R3_label = tk.Label(left_frame, text="R3:")
R3_label.grid(row=3, column=0, pady=10)  # Increased space using pady
R3_entry = tk.Entry(left_frame)
R3_entry.grid(row=3, column=1, pady=10)  # Increased space using pady

Rw_label = tk.Label(left_frame, text="Rw:")
Rw_label.grid(row=4, column=0, pady=10)  # Increased space using pady
Rw_entry = tk.Entry(left_frame)
Rw_entry.grid(row=4, column=1, pady=10)  # Increased space using pady

# Create a label to display the R2 and Vw / Vout equations with increased space
equation_label = tk.Label(left_frame, text="R2 = Rw x R1 / R3\n\nVM / Vout = (R3 + Rw) / R3\n\nVw / V0 = ...")
equation_label.grid(row=5, columnspan=2, pady=20)  # Increased space using pady

# Create buttons to trigger the calculation and stop the calculation with increased space
calculate_button = tk.Button(left_frame, text="Calculate", command=calculate)
calculate_button.grid(row=6, column=0, pady=10)  # Increased space using pady

stop_button = tk.Button(left_frame, text="STOP", command=stop_calculation)
stop_button.grid(row=6, column=1, pady=10)  # Increased space using pady

# Create a label to display the result
result_label = tk.Label(left_frame, text="")
result_label.grid(row=7, columnspan=2, pady=10)  # Increased space using pady

# Open and resize the PNG image using Pillow without any filters
image = Image.open("Circuit.png")
new_width = 600  # Adjust the desired width for a larger picture
aspect_ratio = float(new_width) / float(image.width)
new_height = int(image.height * aspect_ratio)
image = image.resize((new_width, new_height))

photo = ImageTk.PhotoImage(image)
image_label = tk.Label(right_frame, image=photo)
image_label.photo = photo  # To prevent the image from being garbage collected
image_label.grid(row=0, column=0)

# Start the GUI event loop
window.mainloop()

