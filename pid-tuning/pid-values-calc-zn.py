def zn_from_ku_tu(Ku, Tu):
    if Ku <= 0 or Tu <= 0:
        raise ValueError("Ku and Tu must be positive")

    results = {}

    # P
    results["P"] = {
        "Kp": 0.5 * Ku,
        "Ti": None,
        "Td": None,
        "Ki": None,
        "Kd": None
    }

    # PI
    results["PI"] = {
        "Kp": 0.45 * Ku,
        "Ki": 0.54 * Ku / Tu,
        "Kd": None
    }

    # PD
    results["PD"] = {
        "Kp": 0.8 * Ku,
        "Ki": None,
        "Kd": 0.10 * Ku * Tu
    }

    # Classic PID
    results["Classic PID"] = {
        "Kp": 0.6 * Ku,
        "Ki": 1.2 * Ku / Tu,
        "Kd": 0.075 * Ku * Tu
    }

    # Pessen Integral Rule
    results["Pessen"] = {
        "Kp": 0.7 * Ku,
        "Ki": 1.75 * Ku / Tu,
        "Kd": 0.105 * Ku * Tu
    }

    # Some overshoot
    results["Some overshoot"] = {
        "Kp": 0.33 * Ku,
        "Ki": 0.66 * Ku / Tu,
        "Kd": 0.11 * Ku * Tu
    }

    # No overshoot
    results["No overshoot"] = {
        "Kp": 0.20 * Ku,
        "Ki": 0.40 * Ku / Tu,
        "Kd": 0.066 * Ku * Tu
    }

    return results


if __name__ == "__main__":
    Ku = float(input("Ku: "))
    Tu = float(input("Tu: "))

    params = zn_from_ku_tu(Ku, Tu)

    for mode, vals in params.items():
        print(f"\n=== {mode} ===")
        for k, v in vals.items():
            print(f"{k}: {v}")
