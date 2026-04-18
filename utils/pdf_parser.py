import pdfplumber
import re


# 🔢 Clean numbers like 5,500 → 5500
def clean_number(value):
    value = value.replace(",", "")
    try:
        return float(value)
    except:
        return "N/A"


# 🎯 Extract value from text
def extract_value(text, keywords):

    lines = text.split("\n")

    for i, line in enumerate(lines):

        for key in keywords:
            if key.lower() in line.lower():

                combined = line

                # also check next line (important)
                if i + 1 < len(lines):
                    combined += " " + lines[i + 1]

                # remove things like HbA1C
                combined = re.sub(r"[A-Za-z]+\d+[A-Za-z]*", "", combined)

                # ✅ correct order (decimal first)
                numbers = re.findall(r"\d+\.\d+|\d{1,3}(?:,\d{3})*|\d+", combined)

                if numbers:
                    for num in numbers:
                        clean = num.replace(",", "")

                        try:
                            return float(clean)
                        except:
                            continue

    return "N/A"


# 📋 ALL PARAMETERS
PARAMETERS = {
    # CBC
    "Hemoglobin": ["Hemoglobin", "Hb"],
    "WBC": ["WBC", "Total Leucocytes"],
    "Platelet": ["Platelet count", "Platelet"],
    "RBC": ["RBC"],
    "PCV": ["PCV"],
    "MCV": ["MCV"],
    "MCH": ["MCH"],
    "MCHC": ["MCHC"],
    "RDW": ["RDW"],
    "MPV": ["MPV"],

    # Differential
    "Neutrophils": ["Neutrophils"],
    "Absolute Neutrophils": ["Absolute Neutrophils"],
    "Eosinophils": ["Eosinophils"],
    "Absolute Eosinophils": ["Absolute Eosinophils"],
    "Basophils": ["Basophils"],
    "Absolute Basophils": ["Absolute Basophils"],
    "Lymphocytes": ["Lymphocytes"],
    "Absolute Lymphocytes": ["Absolute Lymphocytes"],
    "Monocytes": ["Monocytes"],
    "Absolute Monocytes": ["Absolute Monocytes"],

    # Liver
    "Bilirubin Total": ["Bilirubin-Total", "Bilirubin Total"],
    "Bilirubin Conjugated": ["Bilirubin-Conjugated"],
    "Bilirubin Unconjugated": ["Bilirubin-Unconjugated"],
    "AST": ["SGOT", "AST"],
    "ALT": ["SGPT", "ALT"],
    "Alkaline Phosphatase": ["Alkaline Phosphatase"],
    "Protein": ["Protein"],
    "Albumin": ["Albumin"],
    "Globulin": ["Globulin"],
    "GGT": ["GGT", "Gamma Glutamyl Transferase"],

    # Diabetes
    "HbA1C": ["HbA1C", "Glycated Hemoglobin"],
    "Estimated Average Glucose": ["Estimated Average Glucose"],
    "Glucose Fasting": ["fasting"],
    "Glucose Post": ["post prandial"],

    # Kidney / Electrolytes
    "Creatinine": ["Creatinine"],
    "Sodium": ["Sodium"],
    "Potassium": ["Potassium"],
    "Chloride": ["Chloride"],

    # Coagulation
    "Prothrombin Time": ["Prothrombin Time"],
    "PT Control": ["Control value"],
    "INR": ["INR"],

    # Lipid
    "Total Cholesterol": ["Total Cholesterol"],
    "Triglycerides": ["Triglycerides"],
    "HDL": ["HDL"],
    "LDL": ["LDL"],
    "VLDL": ["VLDL"],
    "Non HDL": ["Non HDL"],
    "Cholesterol HDL Ratio": ["Cholesterol HDL Ratio"],
    "LDL HDL Ratio": ["LDL HDL Ratio"],

    # Urine
    "Microalbumin": ["Microalbumin"],
    "ACR": ["ACR"],
    "Albumin Creatinine Ratio": ["Albumin Creatinine Ratio"],

    # Others
    "Ammonia": ["Ammonia"]
}


# 📄 MAIN FUNCTION
def extract_parameters_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    data = {}

    # 🔄 Loop through all parameters
    for param, keywords in PARAMETERS.items():
        value = extract_value(text, keywords)
        data[param] = value

    return data