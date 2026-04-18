NORMAL_RANGES = {
    "Hemoglobin": (13.2, 16.6),
    "WBC": (4000, 10000),
    "Platelet": (150000, 410000),
    "RBC": (4.0, 6.0),
    "Bilirubin": (0.10, 1.20),
    "Glucose": (70, 140),
    "HbA1C": (4, 6)
}


def get_status(value, normal_range):
    if not isinstance(value, (int, float)):
        return "Unknown"

    low, high = normal_range

    if value < low:
        return "Low"
    elif value > high:
        return "High"
    else:
        return "Normal"


def compare_reports(r1, r2):

    result = []

    keys = set(r1.keys()).union(set(r2.keys()))

    for k in keys:

        v1 = r1.get(k, "N/A")
        v2 = r2.get(k, "N/A")

        change = ""

        # Only compare numbers
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):

            if v1 == v2:
                change = ""   # no change

            elif v2 > v1:
                change = "⬆ Increased"

            elif v2 < v1:
                change = "⬇ Decreased"

        else:
            change = "⚠ Missing"

        result.append([k, v1, v2, change])

    return result