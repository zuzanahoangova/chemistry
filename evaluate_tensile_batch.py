import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from scipy.stats import linregress
import csv

# Load data from a CSV file
def load_data(filename):
    data = pd.read_csv(filename)
    return data['Strain'], data['Stress']


# Function to perform linear regression
def linear_regression(x, y):
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return slope, intercept


# Function to plot stress-strain curve and axis settings
def plot_stress_strain_curve(ax, strain, stress):
    # Plot the stress-strain curve
    ax.plot(strain, stress, label='Stress-Strain Curve', color='black')

    # Set axis limits and labels
    plt.axis([-0.1, 4, -20, 800])
    ax.set_xlabel('Strain (%)', fontsize=20)
    ax.set_ylabel('Stress (MPa)', fontsize=20)
    ax.tick_params(axis='both', labelsize=16)

def save_to_csv(filepath, base_name, slope, rm_y, r02_y, elon_A_x):
    file_exists = os.path.isfile(filepath)  # Check if the file already exists
    headers = ['Sample', 'E (GPa)', 'Rm (MPa)', 'Rp0.2 (MPa)', 'A (%)']
    row = [base_name, round(slope/10), round(rm_y), round(r02_y), round(elon_A_x, 4)]

    # Open the file in append mode or create it if it doesn't exist
    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:  # If file doesn't exist, write headers first
            writer.writerow(headers)
        writer.writerow(row)
    print(f"Data saved for {base_name} to {filepath}.")


# Interactive plotting and data selection
def interactive_plot(strain, stress, folder_path, base_name):
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

    # Call the function to plot the stress-strain curve and set axis settings
    plot_stress_strain_curve(ax, strain, stress)

    selected_points = {'x': [], 'y': []}
    results = {}

    def onselect(xmin, xmax):
        # Clear previous lines and points except the stress-strain curve
        ax.cla()  # Clears the axes

        # Call the function again to re-plot the stress-strain curve
        plot_stress_strain_curve(ax, strain, stress)

        # Get the selected range of data
        mask = (strain >= xmin) & (strain <= xmax)
        selected_x = strain[mask]
        selected_y = stress[mask]
        selected_points['x'] = selected_x
        selected_points['y'] = selected_y

        # Perform linear regression
        slope, intercept = linear_regression(selected_x, selected_y)
        reg_line = slope * strain + intercept
        ax.plot(strain, reg_line, '--', color='tab:red', label=f'Hooke\'s Law (E)')

        # 1. Find Rm
        rm_y = max(stress)
        rm_id = stress.idxmax()
        rm_x = strain[rm_id]

        # 2. Find A
        elon_A_x = rm_x - rm_y / slope  # Intersection with x-axis (where stress = 0)
        ax.plot([rm_x, elon_A_x], [rm_y, 0], '--', color='tab:gray')

        # 3. Find R02
        b = -slope * 0.2
        difference = np.abs(stress - (slope * strain + b))
        intersection_idx = np.argmin(difference)
        r02_x = strain[intersection_idx]
        r02_y = stress[intersection_idx]
        ax.plot([r02_x, 0.2], [r02_y, 0], '--', color='tab:gray')

        # Plot the points (maximum stress, intersection A, intersection I)
        ax.plot(rm_x, rm_y, 'ro')
        ax.text(rm_x - 0.05, rm_y + 20, f'R$_m$', fontsize=16, color='k')
        ax.plot(elon_A_x, 0, 'ro')
        ax.text(elon_A_x + 0.08, 5, f'A', fontsize=16, color='k')
        ax.plot(r02_x, r02_y, 'ro')
        ax.text(r02_x + 0.08, r02_y - 50, f'R$_{{0.2}}$', fontsize=16, color='k')

        ax.legend(fontsize=12)
        plt.draw()

        results.update({'slope': slope, 'rm_y': rm_y, 'r02_y': r02_y, 'elon_A_x': elon_A_x})

    # SpanSelector widget for selecting range
    span = SpanSelector(ax, onselect, 'horizontal', useblit=True, props=dict(alpha=0.5, facecolor='red'))

    # Save the figure when the plot window is closed
    def save_plot(event):
        output_file = os.path.join(folder_path, f'{base_name}.png')
        fig.savefig(output_file, dpi=300)  # Save the figure to a file
        print(f"Plot {base_name} saved successfully.")

        if results:
            output_csv = os.path.join(folder_path, 'tensile_data.csv')
            save_to_csv(output_csv, base_name, results['slope'], results['rm_y'], results['r02_y'], results['elon_A_x'])
        else:
            print("Tensile data not saved.")

    fig.canvas.mpl_connect('close_event', save_plot)

    plt.legend()
    plt.show()


# Runs the whole plotting process
def plot_linreg(filename, folder_path):
    dat_file_path = os.path.join(folder_path, filename)
    strain, stress = load_data(dat_file_path)
    base_name = os.path.splitext(filename)[0]
    interactive_plot(strain, stress, folder_path, base_name)

def main():
    folder_path = input("Enter folder path: ")
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            try:
                plot_linreg(file_name, folder_path)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
        else:
            print(f"{file_name} skip")

    print("Plotting complete!")


if __name__ == "__main__":
    main()