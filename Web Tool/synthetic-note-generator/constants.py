header_titles = ['RAD THERAPY CONSULT VISIT', 'RADIATION THERAPY CONSULT NOTE',
                 'RADIATION ONCOLOGY OUTPT CONSULT NOTE', 'RADIATION CONSULT RESULT', 'RAD/ONC-CONSULT']

states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
    'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
    'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
    'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

RACES = ['white', 'black', 'asian', 'Native American']

ethnicity = ['HISPANIC OR LATINO', 'NOT HISPANIC OR LATINO ']

problem_list = ['Acute osteomyelitis of hand', 'Anxiety', 'Asthma', 'Atrial fibrillation',
                'Benign prostatic hyperplasia', 'Carcinoma of prostate', 'Carpal tunnel syndrome', 'Chronic back pain',
                'Chronic kidney disease stage 2', 'Chronic Low Back Pain', 'Coronary arteriosclerosis',
                'Coronary Artery Disease', 'Cortical senile cataract', 'Depression',
                'Derangement of posterior horn of medial meniscus', 'Dermatophytosis', 'Diabetes',
                'Disorder of refraction', 'Dizziness', 'Elevated PSA', 'Excoriation, neurotic',
                'Generalized Anxiety Disorder', 'GERD', 'Glaucoma suspect', 'Hyperlipidemia', 'Hypertension',
                'Hypertrophy (Benign) of Prostate without Urinary obstruction and other lower Uri',
                'Intermittent claudication', 'Knee Joint replacement Status (Prosthetic or Artificial Device)',
                'Loss of sense of smell', 'Malignant Neoplasm of the Prostate', 'Nuclear sclerosis', 'Obesity',
                'Osteoarthrosis', 'Pelvic pain syndrome', 'Personal History of Exposure to Agent Orange',
                'Prostate cancer', 'Raised prostate specific antigen', 'Reactive airways dysfunction syndrome',
                'Senile nuclear sclerosis', 'Sleep apnea', 'Thyroid nodules', 'Urinary Tract Infections',
                'Vitamin D deficiency']

surgery_list = [
    'Left Inguinal Hernia Repair', 's/p Tonsillectomy', 'LT KNEE ARTHROSCOPY W / DEBRIDEMENT',
    'UMBILICAL HERNIA REPAIR', 'MEDIASTINOSCOPY', 'Cardiac stent', 'LEFT TOTAL KNEE REPLACEMENT',
    'RIGHT TOTAL KNEE ARTHROPLASTY', 'Ablation for AFIB', 'carpal tunnel release'
]

medication_list = [
    'AMLODIPINE BESYLATE 5MG TAB TAKE ONE TABLET BY MOUTH EVERY DAY',
    'CARBOXYMETHYLCELLULOSE NA 0.5% OPH SOLN INSTILL 1 DROP IN EACH EYE THREE TIMES A DAY',
    'CHOLECALCIFEROL (VIT D3) 400UNIT TAB TAKE TWO TABLETS BY MOUTH EVERY DAY',
    'FERROUS SULFATE 325MG TAB TAKE ONE TABLET BY MOUTH THREE TIMES A DAY (AN HOUR BEFORE OR TWO HOURS AFTER A MEAL; TAKE WITH FOOD IF THIS UPSETS YOUR STOMACH)',
    'FLECAINIDE ACETATE 150MG TAB TAKE ONE TABLET BY MOUTH TWICE A DAY',
    'METOPROLOL SUCCINATE 50MG SA TAB TAKE ONE-HALF TABLET BY MOUTH EVERY DAY',
    'RIVAROXABAN 20MG TAB TAKE ONE TABLET BY MOUTH EVERY EVENING WITH FOOD (CONSULT PROVIDER BEFORE STOPPING)',
    'SILDENAFIL CITRATE 100MG TAB TAKE ONE-HALF TABLET BY MOUTH AN HOUR_BEFORE SEX. (NO MORE THAN 1 DOSE PER 24 HOURS) NO NITRATES',
    'TAMSULOSIN 0.4MG CAP TAKE ONE CAPSULE BY MOUTH AT BEDTIME (DO NOT TAKE WITHIN 4 HOURS OF SILDENAFIL)',
    'UREA 20% CREAM APPLY A SUFFICIENT AMOUNT EXTERNALLY EVERY DAY',
    'HYDROCHLOROTHIAZIDE 12.5MG CAP TAKE ONE CAPSULE BY MOUTH EVERY DAY FOR BLOOD PRESSURE',
    'IBUPROFEN 800MG TAB TAKE ONE TABLET BY MOUTH EVERY DAY IF NEEDED FOR PAIN',
    'LISINOPRIL 40MG TAB TAKE ONE TABLET BY MOUTH EVERY DAY FOR BLOOD PRESSURE',
    'OMEPRAZOLE 20MG EC CAP TAKE ONE CAPSULE BY MOUTH BEFORE BREAKFAST (AT LEAST 15-30 MINUTES BEFORE EATING) FOR STOMACH - DO NOT CRUSH TAB/CAP',
    'ALBUTEROL 100/IPRATRO 20MCG 120D PO INHL',
    'DEXAMETHASONE NA PHOSPHATE 0.1% OPH SOLN',
    'DOCUSATE NA 50MG/SENNOSIDES 8.6MG TAB',
    'HYDROCODONE 5MG/ACETAMINOPHEN 325MG TAB',
    'MELOXICAM 15MG TAB',
    'NUTRITION SUPL BOOST PLUS/VANILLA LIQUID',
    'POLYETHYLENE GLYCOL 3350 ORAL PWDR',
    'TRAMADOL HCL 50MG TAB',
    'LEVOFLOXACIN TAB 500MG TAKE ONE TABLET BY MOUTH EVERY',
    'LEVOTHYROXINE NA 0.1MG TAB TAKE ONE TABLET BY MOUTH',
    'MEGESTROL ACETATE 40MG TAB TAKE ONE TABLET BY MOUTH',
    'NITROGLYCERIN TAB SL 0.4 MG DISSOLVE ONE TABLET',
    'SIMVASTATIN TAB 20 MG TAKE ONE-HALF TABLET BY MOUTH',
    'ASPIRIN 81MG EC TAB TAKE ONE TABLET BY MOUTH ONCE DAILY',
    'BACLOFEN 10MG TAB TAKE ONE TABLET BY MOUTH THREE TIMES A DAY',
    'BUDESONIDE 80/FORMOTER 4.5MCG 120D INH INHALE 2 PUFFS BY MOUTH TWICE A DAY',
    'CHOLECALCIFEROL (VIT D3) 1,000UNIT TAB TAKE FOUR TABLETS BY MOUTH ONCE DAILY',
    'SENNOSIDES 8.6MG TAB TAKE TWO TABLETS BY MOUTH ONCE DAILY',
    'TIOTROPIUM 18MCG INHL CAP 30 INHALE 18 MCG',
    'AMITRIPTYLINE HCL 25MG',
    'ROSUVASTATIN CA 40MG TAB',
    'HCTZ 12.5/LISINOPRIL 10MG TAB',
    'BUDESONIDE 160/FORMOTER 4.5MCG 120D INH',
    'GABAPENTIN 600MG',
    'BUPROPION HCL 75MG TAB',
    'AMIODARONE HCL (PACERONE) 200MG',
    'SUNSCREEN-30 PABA-FREE COMBINATION'
]

allergy_list = ['peanuts', 'tree nuts', 'wheat', 'soy', 'fish', 'shellfish', 'latex', 'amoxicillin',
                'ampicillin', 'penicillin', 'tetracycline', 'ibuprofen', 'aspirin', 'aleve']


# Preset ranges for bulk generation
PRESET_RANGES = {
    "age": [
        {"label": "Young Adult", "range": [18, 30]},
        {"label": "Adult", "range": [31, 45]},
        {"label": "Middle Age", "range": [46, 60]},
        {"label": "Senior", "range": [61, 75]},
        {"label": "Elderly", "range": [76, 90]},
        {"label": "Advanced Age", "range": [91, 100]}
    ],
    "aua": [
        {"label": "Mild symptoms", "range": [0, 7]},
        {"label": "Moderate symptoms", "range": [8, 19]},
        {"label": "Severe symptoms", "range": [20, 35]}
    ],
    "ipss": [
        {"label": "Mild symptoms", "range": [0, 7]},
        {"label": "Moderate symptoms", "range": [8, 19]},
        {"label": "Severe symptoms", "range": [20, 35]}
    ],
    "shim": [
        {"label": "Severe ED", "range": [1, 7]},
        {"label": "Moderate ED", "range": [8, 11]},
        {"label": "Mild to Moderate ED", "range": [12, 16]},
        {"label": "Mild ED", "range": [17, 21]},
        {"label": "No ED", "range": [22, 25]}
    ],
    "ecog": [
        {"label": "Fully active to restricted", "range": [0, 1]},
        {"label": "Limited self-care", "range": [2, 3]},
        {"label": "Disabled to completely disabled", "range": [3, 4]}
    ],
    "psa": [
        {"label": "Normal range", "range": [0, 4]},
        {"label": "Slightly elevated", "range": [4.1, 10]},
        {"label": "Moderately elevated", "range": [10.1, 20]},
        {"label": "Significantly elevated", "range": [20.1, 50]}
    ],
    "performance_score": [
        {"label": "Limited self-care", "range": [50, 70]},
        {"label": "Unable to work", "range": [71, 80]},
        {"label": "Normal activity with effort", "range": [81, 90]},
        {"label": "Normal, no complaints", "range": [91, 100]}
    ],
    "temperature": [
        {"label": "Below normal", "range": [96.0, 97.5]},
        {"label": "Normal range", "range": [97.6, 99.0]},
        {"label": "Elevated", "range": [99.1, 101.0]}
    ],
    "systolic": [
        {"label": "Normal", "range": [90, 120]},
        {"label": "Elevated", "range": [121, 140]},
        {"label": "High Stage 1", "range": [141, 160]},
        {"label": "High Stage 2", "range": [161, 180]}
    ],
    "diastolic": [
        {"label": "Normal", "range": [60, 80]},
        {"label": "Elevated", "range": [81, 90]},
        {"label": "High Stage 1", "range": [91, 100]},
        {"label": "High Stage 2", "range": [101, 120]}
    ],
    "pulse": [
        {"label": "Lower normal", "range": [60, 75]},
        {"label": "Normal", "range": [76, 90]},
        {"label": "Elevated", "range": [91, 120]}
    ],
    "respiration": [
        {"label": "Normal", "range": [12, 16]},
        {"label": "Mild elevation", "range": [17, 20]},
        {"label": "Moderate elevation", "range": [21, 25]}
    ],
    "weight": [
        {"label": "Lower weight range", "range": [100, 150]},
        {"label": "Middle weight range", "range": [151, 200]},
        {"label": "Higher weight range", "range": [201, 250]},
        {"label": "Highest weight range", "range": [251, 300]}
    ],
    "pain": [
        {"label": "Mild pain", "range": [0, 3]},
        {"label": "Moderate pain", "range": [4, 6]},
        {"label": "Severe pain", "range": [7, 10]}
    ]
}

# Add ranges for list quantities
LIST_QUANTITY_RANGES = {
    "medications": [
        {"label": "Few medications", "range": [0, 3]},
        {"label": "Moderate number", "range": [4, 7]},
        {"label": "Many medications", "range": [8, 12]},
        {"label": "Extensive medications", "range": [13, 15]}
    ],
    "allergies": [
        {"label": "Few allergies", "range": [0, 2]},
        {"label": "Moderate number", "range": [3, 5]},
        {"label": "Many allergies", "range": [6, 8]}
    ],
    "problems": [
        {"label": "Few problems", "range": [0, 3]},
        {"label": "Moderate number", "range": [4, 7]},
        {"label": "Many problems", "range": [8, 12]}
    ],
    "surgeries": [
        {"label": "Minimal surgical history", "range": [0, 1]},
        {"label": "Moderate surgical history", "range": [2, 3]},
        {"label": "Extensive surgical history", "range": [4, 5]}
    ]
}

hpi_command_phrases = [
    'Regenerate this note in a concise, clinical manner. Keep existing placeholder numbers in their curly braces. Do not add any numbers or unnecessary information. Do not use helper phrases such as "Here is the rewritten note". If the variable {10} is present, treat it like a whole sentence. Otherwise, do not add it.\n',
    'Rewrite this note formally and clinically, preserving placeholder numbers in curly braces. Avoid adding any numbers or extra details. Do not use introductory phrases like "Here is the rewritten note". If the variable {10} is present, treat it like a whole sentence. Otherwise, do not add it.\n',
    'Reconstruct this note in a clinical and concise, maintaining the placeholder numbers within curly braces. Do not introduce new numbers or superfluous content. Exclude lead-in phrases such as "Here is the rewritten note". If the variable {10} is present, treat it like a whole sentence. Otherwise, do not add it.\n',
    'Transform this note into a clinical, concise version. Retain placeholder numbers in curly braces without adding new numbers or unnecessary details. Omit preambles like "Here is the rewritten note". If the variable {10} is present, treat it like a whole sentence. Otherwise, do not add it.\n',
    'Rephrase this note with a clinical and formal tone, ensuring placeholder numbers in curly braces are preserved. Do not include additional numbers or extraneous information. Avoid introductory statements like "Here is the rewritten note". If the variable {10} is present, treat it like a whole sentence. Otherwise, do not add it.\n'
]

asmplan_command_phrases = [
    'Regenerate this note in a concise clinical manner. Keep existing placeholder numbers in their curly braces. Do not add any numbers or unnecessary information. Do not use helper phrases such as "Here is the rewritten note".\n',
    'Rewrite this note formally and clinically, preserving placeholder numbers in curly braces. Avoid adding any numbers or extra details. Do not use introductory phrases like "Here is the rewritten note".\n',
    'Reconstruct this note in a clinical and concise, maintaining the placeholder numbers within curly braces. Do not introduce new numbers or superfluous content. Exclude lead-in phrases such as "Here is the rewritten note".\n',
    'Transform this note into a clinical, concise version. Retain placeholder numbers in curly braces without adding new numbers or unnecessary details. Omit preambles like "Here is the rewritten note".\n',
    'Rephrase this note with a clinical and formal tone, ensuring placeholder numbers in curly braces are preserved. Do not include additional numbers or extraneous information.\n'
]
