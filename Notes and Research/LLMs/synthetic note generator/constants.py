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

race = ['white', 'black', 'asian', 'Native American']

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
