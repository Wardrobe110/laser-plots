import numpy as np
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
    
    #Reading folder path
    folder = input("Folder: ").strip()
    if not os.path.isdir(folder):
        raise RuntimeError("Folder does not exist")
    
    plt.figure()

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        
        if not os.path.isfile(path):
            continue

        try:
            with open(path, "r") as f:
                f.readline()
                line = f.readline()
        except Exception:
            print(f"Skipping file: cannot read header -> {filename}")
            continue

        try:
            parts = line.strip().split(",")
            v1 = float(parts[0])
            v2 = float(parts[1])
            pwm_duty = (v1 / v2) * 100.0
        except Exception:
            print(f"Skipping file: malformed PWM line -> {filename}")
            continue

        try:
            data = np.genfromtxt(path, delimiter=",", skip_header=5, skip_footer=5)
        except Exception:
            print(f"Skipping file: cannot parse numeric data -> {filename}")
            continue

        if data.ndim != 2 or data.shape[1] != 2:
            print(f"Skipping file: data points error -> {filename}")
            continue

        x = data[:, 0]
        y = data[:, 1]

        x = x - x[0]
        x = x / 1_000_000
        y = y / 10.0
        
        if color_index < len(custom_colors):
            plt.plot(x, y, color=custom_colors[color_index],
                     label=f"{filename} ({pwm_duty:.2f}%)")
        else:
            plt.plot(x, y, label=f"{filename} ({pwm_duty:.2f}%)")

        color_index += 1

    plt.xlabel("Czas [s]")
    plt.ylabel("Temperatura [°C]")
    plt.title("All files in folder")
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fun()