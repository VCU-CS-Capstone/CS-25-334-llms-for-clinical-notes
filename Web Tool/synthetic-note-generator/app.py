from flask import Flask, render_template, request, jsonify
from note import ConsultNote
import traceback
from datetime import datetime
import numpy as np
import json
import random
from constants import medication_list, allergy_list, problem_list, surgery_list
from constants import PRESET_RANGES, LIST_QUANTITY_RANGES

app = Flask(__name__)

# ---------- Custom JSON Encoder for numpy + datetime ----------
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder  # Deprecated in Flask 2.3+, consider migration if needed

def convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# ---------- Safe Parsing Helpers ----------
def safe_int(value, default=None, min_val=None, max_val=None):
    if not value:
        return default
    try:
        result = int(value)
        if (min_val is not None and result < min_val) or (max_val is not None and result > max_val):
            return default
        return result
    except ValueError:
        return default

def safe_float(value, default=None, min_val=None, max_val=None):
    if not value:
        return default
    try:
        result = float(value)
        if (min_val is not None and result < min_val) or (max_val is not None and result > max_val):
            return default
        return result
    except ValueError:
        return default

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/single')
def single_note():
    return render_template('index.html')

@app.route('/bulk')
def bulk_notes():
    return render_template('bulk.html')

@app.route('/get_options')
def get_options():
    return jsonify({
        'medications': medication_list,
        'allergies': allergy_list,
        'problem_list': problem_list,
        'surgery_list': surgery_list
    })

@app.route('/get_ranges')
def get_ranges():
    return jsonify({**PRESET_RANGES, **LIST_QUANTITY_RANGES})

# ---------- Single Note Generation ----------
@app.route('/generate_note', methods=['POST'])
def generate_note():
    try:
        data = request.get_json()

        patient = data.get('patient', {})
        note_type = data.get('noteType', {})
        include_sections = data.get('includeSections', {})
        vitals = data.get('vitals', {})
        staging = data.get('staging', {})
        social_history = data.get('social_history', {})
        prior_treatment = data.get('prior_treatment', {})

        processed_data = {
            'note_generation_type': note_type.get('generation'),
            'clinical_note_type': note_type.get('clinical', 'consult').lower(),

            'patient_age': safe_int(patient.get('age'), None, 18, 100),
            'patient_sex': patient.get('sex'),
            'patient_race': patient.get('race'),
            'patient_ethnicity': patient.get('ethnicity'),
            'patient_first_name': patient.get('first_name'),
            'patient_last_name': patient.get('last_name'),

            'note_author': data.get('note_author'),
            'note_cosigner': data.get('note_cosigner'),

            'aua': safe_int(data.get('aua')),
            'ipss': safe_int(data.get('ipss')),
            'shim': safe_int(data.get('shim')),
            'ecog': safe_int(data.get('ecog')),
            'psa_score': safe_float(data.get('psa', {}).get('score')),
            'performance_score': safe_int(data.get('performance_score')),

            'medications': data.get('medications', []),
            'allergies': data.get('allergies', []),
            'problem_list': data.get('problem_list', {}).get('active_problems', []),
            'surgical_history': data.get('problem_list', {}).get('surgical_history', []),

            'base_date': parse_date(data.get('base_date')),
            'mri_date': parse_date(data.get('mri_date')),
            'pelvic_ct_date': parse_date(data.get('pelvic_ct')),
            'pelvic_mri_date': parse_date(data.get('pelvic_mri')),
            'bone_scan_date': parse_date(data.get('bone_scan')),

            'temperature': safe_float(vitals.get('temperature')),
            'blood_pressure_systolic': safe_int(vitals.get('blood_pressure', {}).get('systolic')),
            'blood_pressure_diastolic': safe_int(vitals.get('blood_pressure', {}).get('diastolic')),
            'pulse': safe_int(vitals.get('pulse')),
            'respiration': safe_int(vitals.get('respiration')),
            'weight': safe_int(vitals.get('weight')),
            'pain': safe_int(vitals.get('pain')),

            'risk_level': staging.get('risk'),
            'tnm': staging.get('tnm'),
            'group_stage': staging.get('group_stage'),
            'histology': staging.get('histology'),

            'prostatectomy': data.get('prostatectomy'),
            'colonoscopy': data.get('colonoscopy'),

            'prior_rt': prior_treatment.get('prior_rt'),
            'prior_rt_date': parse_date(prior_treatment.get('prior_rt_date')),
            'chemotherapy_prescribed': prior_treatment.get('chemotherapy_prescribed'),
            'hormone_therapy_prescribed': prior_treatment.get('hormone_therapy_prescribed'),

            'alcohol_history': social_history.get('alcohol_history'),
            'smoking_history': social_history.get('smoking_history'),

            'include_hpi': include_sections.get('hpi', True),
            'include_vitals': include_sections.get('vitals', True),
            'include_social': include_sections.get('social', True),
            'include_medical': include_sections.get('medical', True),
            'include_exam': include_sections.get('exam', True),
            'include_imaging': include_sections.get('imaging', True),
            'include_plan': include_sections.get('plan', True),

            'regen_hpi': data.get('regenSections', {}).get('regenerate_hpi', False),
            'regen_assmplan': data.get('regenSections', {}).get('regenerate_assmplan', False),
        }

        note = ConsultNote(**processed_data)
        note_data = convert_numpy_types(note.get_data_fields())
        note_text = note.get_text()

        return jsonify({
            'text': note_text,
            'data': note_data
        })

    except Exception as e:
        print("Error generating note:", e)
        print(traceback.format_exc())
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

# ---------- Bulk Note Generation ----------
def get_random_value_in_range(range_values):
    min_val, max_val = range_values
    if isinstance(min_val, float) or isinstance(max_val, float):
        return round(random.uniform(min_val, max_val), 2)
    return random.randint(min_val, max_val)

@app.route('/generate_bulk_notes', methods=['POST'])
def generate_bulk_notes():
    try:
        data = request.get_json()
        num_notes = int(data.get('num_notes', 1))
        ranges = data.get('ranges', {})

        if not (1 <= num_notes <= 1000):
            return jsonify({'error': 'Number of notes must be between 1 and 1000'}), 400

        generated_notes = []

        for _ in range(num_notes):
            note_params = {}

            # Handle note type selection
            note_type = ranges.get('noteType', 'random')
            if note_type == 'random':
                # Randomly select one of the four note types
                clinical_note_type = random.choice(['initial', 'followup', 'treatment', 'summary'])
            else:
                clinical_note_type = note_type
            
            note_params['clinical_note_type'] = clinical_note_type

            # Process regeneration options
            note_params['regen_hpi'] = ranges.get('regenerateHPI', False)
            note_params['regen_assmplan'] = ranges.get('regenerateAssmPlan', False)

            for field, range_values in ranges.items():
                if field in ['noteType', 'regenerateHPI', 'regenerateAssmPlan']:
                    # Skip these as they're handled separately
                    continue
                
                if field == 'age':
                    note_params['patient_age'] = get_random_value_in_range(range_values)
                elif field in ['aua', 'ipss', 'shim', 'ecog', 'performance_score']:
                    note_params[field] = get_random_value_in_range(range_values)
                elif field == 'psa':
                    note_params['psa_score'] = get_random_value_in_range(range_values)
                elif field == 'temperature':
                    note_params['temperature'] = get_random_value_in_range(range_values)
                elif field == 'systolic':
                    note_params['blood_pressure_systolic'] = get_random_value_in_range(range_values)
                elif field == 'diastolic':
                    note_params['blood_pressure_diastolic'] = get_random_value_in_range(range_values)
                elif field in ['pulse', 'respiration', 'weight', 'pain']:
                    note_params[field] = get_random_value_in_range(range_values)

            if 'medications' in ranges:
                quantity = get_random_value_in_range(ranges['medications'])
                note_params['medications'] = random.sample(medication_list, min(max(0, quantity), len(medication_list)))

            if 'allergies' in ranges:
                quantity = get_random_value_in_range(ranges['allergies'])
                note_params['allergies'] = random.sample(allergy_list, min(max(0, quantity), len(allergy_list)))

            if 'problems' in ranges:
                quantity = get_random_value_in_range(ranges['problems'])
                note_params['problem_list'] = random.sample(problem_list, min(max(0, quantity), len(problem_list)))

            if 'surgeries' in ranges:
                quantity = get_random_value_in_range(ranges['surgeries'])
                note_params['surgical_history'] = random.sample(surgery_list, min(max(0, quantity), len(surgery_list)))

            # Handle categorical selections if present in ranges
            categorical_fields = {
                'sex': 'patient_sex',
                'race': 'patient_race',
                'ethnicity': 'patient_ethnicity',
                'tnm': 'tnm',
                'riskLevel': 'risk_level',
                'groupStage': 'group_stage',
                'alcoholHistory': 'alcohol_history',
                'smokingStatus': 'smoking_status',
                'prostatectomy': 'prostatectomy',
                'colonoscopy': 'colonoscopy',
                'priorRt': 'prior_rt',
                'chemotherapy': 'chemotherapy_prescribed',
                'hormoneTherapy': 'hormone_therapy_prescribed'
            }
            
            for js_field, py_field in categorical_fields.items():
                if js_field in ranges and ranges[js_field] != 'random':
                    note_params[py_field] = ranges[js_field]

            note = ConsultNote(**note_params)
            generated_notes.append({
                'text': note.get_text(),
                'data': convert_numpy_types(note.get_data_fields())
            })

        return jsonify({'notes': generated_notes, 'count': len(generated_notes)})

    except Exception as e:
        print("Error generating bulk notes:", e)
        print(traceback.format_exc())
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

# ---------- Main ----------
if __name__ == '__main__':
    app.run(debug=True)
