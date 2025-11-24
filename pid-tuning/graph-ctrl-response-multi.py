import numpy as np
import math
import matplotlib.pyplot as plt
import os

def fun():
    color_index = 0
    custom_colors = [
        "#ff1f5b",
        "#00CD6C",
        "#009ADE",
        "#AF58BA",
        "#FFC61E",
        "#F28522"
    ]
    
    folder = input("Folder: ").strip()
    if not os.path.isdir(folder):
        raise RuntimeError("Folder does not exist")
    
    results_dir = os.path.join(folder, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Plot batching
    curves_per_plot = 6
    figure_index = 1
    curve_counter = 0
    plt.figure()

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if not os.path.isfile(path):
            continue

        # Header parsing
        with open(path, "r") as f:
            f.readline()
            line = f.readline()

        isPid = 1
        parts = line.strip().split(",")
        kp = float(parts[0])
        ki = float(parts[1])
        try:
            kd = float(parts[2])
        except Exception as e:
            isPid = 0
            
        setpoint = float(parts[3])

        # Data loading
        data = np.genfromtxt(path, delimiter=",", skip_header=5, skip_footer=5)
        if data.ndim != 2 or data.shape[1] != 2:
            raise RuntimeError("Data points error")

        x = data[:, 0]
        y = data[:, 1]

        x = (x - x[0]) / 1_000_000
        y = y / 10.0
        
        # Start a new figure after 6 curves
        if curve_counter == curves_per_plot:
            plt.xlabel("Czas [s]")
            plt.ylabel("Temperatura [°C]")
            plt.title(f"Setpoint = {setpoint:.0f} [°C]")
            plt.xlim(left=0)
            plt.ylim(bottom=0)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            
            fig_path = os.path.join(results_dir, f"plots_{figure_index}.png")
            plt.savefig(fig_path)
            
            figure_index += 1
            curve_counter = 0p
            plt.figure()
            
        # Plotting
        if color_index >= len(custom_colors):
            color_index = 0;
        color = custom_colors[color_index]
        if isPid:
            plt.plot(x, y, color=color, label=f"Kp {kp:.2f}, Ki {ki:.7f}, Kd {kd:.7f}")
        else:
            plt.plot(x, y, color=color, label=f"Kp {kp:.2f}, Ki {ki:.7f}, Kd [N/A]")

        color_index += 1
        curve_counter += 1
        
        
    # Save last figure if it contains any curves
    if curve_counter > 0:
        plt.xlabel("Czas [s]")
        plt.ylabel("Temperatura [°C]")
        plt.title(f"Setpoint = {setpoint:.0f} [°C]")
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.grid()
        plt.legend()
        plt.tight_layout()
        fig_path = os.path.join(results_dir, f"plots_{figure_index}.png")
        plt.savefig(fig_path)

    plt.show()

if __name__ == "__main__":
    fun()
