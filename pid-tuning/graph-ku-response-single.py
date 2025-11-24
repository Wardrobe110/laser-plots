import numpy as np
import matplotlib.pyplot as plt

def fun():
    #Reading data
    filename = input("Filename: ")

    try:
        with open(filename, "r") as f:
            f.readline()
            line = f.readline()
    except Exception as e:
        raise RuntimeError("File does not exist")

    #Reading PWM duty
    parts = line.strip().split(",")
    ku = float(parts[0])
    setpoint = float(parts[1])

    #Reading datapoints
    data = np.genfromtxt(filename, delimiter=",", skip_header = 5, skip_footer = 5)
        
    if data.ndim != 2 or data.shape[1] != 2:
        raise RuntimeError("Data points error")

    x = data[:, 0]
    y = data[:, 1]
    
    #Processing data
    x = x - x[0]
    x = x / 1000000;
    y = y / 10.0
    
    #Initial values plot
    plt.figure()
    label = f"Ku {ku:.2f}"
    plt.plot(x, y, color="#ff1f5b", label=label)
    plt.legend()
    
    #Plot config
    plt.xlabel("Czas [s]")
    plt.ylabel("Temperatura [°C]")
    plt.title(f"Setpoint = {setpoint:.0f} [°C]")
    plt.xlim(left = 0, right = x[-1])
    plt.ylim(bottom=0)
    plt.grid()
    plt.tight_layout
    
    #Oscilation time
    
    
    plt.show()

if __name__ == "__main__":
    fun()