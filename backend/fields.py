YN = [("1", "Yes"), ("2", "No")]
GROUPS = [
    ("Profile", [
        ("RIAGENDR", "Sex", "select", [("1", "Male"), ("2", "Female")]),
        ("RIDRETH1", "Ethnicity", "select", [("1", "Mexican American"), ("2", "Other Hispanic"),
                                              ("3", "White"), ("4", "Black"), ("5", "Other / Multi")]),
    ]),
    ("Body measurements", [
        ("BMXHT", "Height (cm)", "number", "e.g. 166"), ("BMXWT", "Weight (kg)", "number", "e.g. 70"),
        ("BMXWAIST", "Waist (cm)", "number", "e.g. 90"),
    ]),
    ("Blood pressure", [
        ("BPXSY1", "Systolic BP (mmHg)", "number", "e.g. 120"), ("BPXDI1", "Diastolic BP (mmHg)", "number", "e.g. 80"),
        ("BPXPLS", "Pulse (beats/min)", "number", "e.g. 72"),
    ]),
    ("Blood tests (if you have a report)", [
        ("LBXGH", "HbA1c (%)", "number", "e.g. 5.4"), ("LBXSGL", "Glucose (mg/dL)", "number", "e.g. 92"),
        ("LBXSCR", "Creatinine (mg/dL)", "number", "e.g. 0.9"), ("LBXTC", "Total cholesterol (mg/dL)", "number", "e.g. 185"),
        ("LBDHDD", "HDL cholesterol (mg/dL)", "number", "e.g. 50"), ("LBXSAL", "Albumin (g/dL)", "number", "e.g. 4.2"),
        ("LBXHGB", "Hemoglobin (g/dL)", "number", "e.g. 14"), ("LBXWBCSI", "WBC (1000 cells/uL)", "number", "e.g. 6.8"),
        ("LBXPLTSI", "Platelets (1000 cells/uL)", "number", "e.g. 240"), ("LBXSATSI", "ALT (U/L)", "number", "e.g. 20"),
        ("LBXSASSI", "AST (U/L)", "number", "e.g. 20"), ("LBXSUA", "Uric acid (mg/dL)", "number", "e.g. 5.3"),
        ("LBXSBU", "Blood urea nitrogen (mg/dL)", "number", "e.g. 14"),
    ]),
    ("Health history", [
        ("BPQ020", "Told you have high blood pressure?", "select", YN),
        ("BPQ080", "Told you have high cholesterol?", "select", YN),
        ("DIQ010", "Told you have diabetes?", "select", [("1", "Yes"), ("2", "No"), ("3", "Borderline")]),
        ("SMQ020", "Smoked 100+ cigarettes in life?", "select", YN),
        ("RHQ031", "Regular periods in past 12 months? (women)", "select", YN),
    ]),
]
CODES = [c for _, fs in GROUPS for c, *_ in fs]

