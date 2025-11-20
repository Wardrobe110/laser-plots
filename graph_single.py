import numpy as np
import matplotlib.pyplot as plt

def fun():
    #Reading data
    filename = input("Filename: ")
        
    #Reading PWM duty
    try:
        with open(filename, "r") as f:
            f.readline()
            line = f.readline()
    except Exception as e:
        raise RuntimeError("File doesn't exist")

    parts = line.strip().split(",")
    v1 = float(parts[0])
    v2 = float(parts[1])
    pwm_duty = (v1 / v2) * 100.0

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
    plt.plot(x, y, color="#ff1f5b")
    
    #Plot config
    plt.xlabel("Czas [s]")
    plt.ylabel("Temperatura [°C]")
    plt.title(f"PWM duty = {pwm_duty:.0f}%")
    plt.xlim(left = 0, right = x[-1])
    plt.ylim(bottom=0)
    plt.grid()
    plt.tight_layout()
    
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
    
    #Regline calculating
    x_rise = x[found_index : maxIndexY + 1]
    y_rise = y[found_index : maxIndexY + 1]
    
    try:
        a, b = np.polyfit(x_rise, y_rise, 1)
        y_reg = a * x_rise + b
        print("Regline a: ", a)
        print("Regline angle: ", np.arctan(a))
        print("Regline b: ", b)
        plt.plot(x_rise, y_reg, color="#00CD6C")
    except Exception as e:
        print("Could not find the slope")
    
    plt.show()

if __name__ == "__main__":
    fun()