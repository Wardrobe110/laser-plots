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
    
    #Reading folder path
    folder = input("Folder: ").strip()
    if not os.path.isdir(folder):
        raise RuntimeError("Folder does not exist")
    
    #File for saving regline results
    results_dir = os.path.join(folder, "results")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "reglines.txt")
    out = open(output_path, "w")
    out.write("filename, duty, a, b, angle_deg\n")
    
    plt.figure()

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        
        if not os.path.isfile(path):
            continue

        with open(path, "r") as f:
            f.readline()
            line = f.readline()

        parts = line.strip().split(",")
        v1 = float(parts[0])
        v2 = float(parts[1])
        pwm_duty = (v1 / v2) * 100.0

        #Reading datapoints
        data = np.genfromtxt(path, delimiter=",", skip_header=5, skip_footer=5)

        if data.ndim != 2 or data.shape[1] != 2:
            raise RuntimeError("Data points error")

        x = data[:, 0]
        y = data[:, 1]

        x = x - x[0]
        x = x / 960000
        y = y / 10.0
        
        if color_index < len(custom_colors):
            plt.plot(x, y, color=custom_colors[color_index],
                     label=f"{filename} ({pwm_duty:.2f}%)")
        else:
            plt.plot(x, y, label=f"{filename} ({pwm_duty:.2f}%)")

        color_index += 1
        
        #Regline locating
        maxIndexY = np.argmax(y)
        window = 100
        baseline = np.mean(y[:window])
        threshold = baseline + 1.0

        found_index = None
        for start in range(0, len(y) - window + 1):
            m = np.mean(y[start : start + window])
            if m > threshold:
                found_index = start
                break

        if found_index is None:
            print(f"No rise section found: {filename}")
            out.write(f"{filename}, [N/A], [N/A], [N/A], [N/A]\n")
            continue

        # --- Regline calculation ---
        x_rise = x[found_index : maxIndexY + 1]
        y_rise = y[found_index : maxIndexY + 1]
        
        try:
            a, b = np.polyfit(x_rise, y_rise, 1)
        except Exception:
            print(f"Regression failed: {filename}")
            continue

        angle_deg = math.degrees(math.atan(a))

        # Save into output file
        out.write(f"{filename}, {pwm_duty:.6f}, {a:.6f}, {b:.6f}, {angle_deg:.6f}\n")
        
    out.close()    
    
    plt.xlabel("Czas [s]")
    plt.ylabel("Temperatura [°C]")
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.grid()
    plt.legend()
    plt.tight_layout()

    img_path = os.path.join(results_dir, "plots.png")
    plt.savefig(img_path)
    
    plt.show()

if __name__ == "__main__":
    fun()