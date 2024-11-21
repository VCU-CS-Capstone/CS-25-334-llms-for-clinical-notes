from flask import Flask, render_template, request, jsonify
from note import ConsultNote
import traceback
from datetime import datetime
import numpy as np
import json
from constants import medication_list, allergy_list, problem_list, surgery_list

app = Flask(__name__)

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
        return super(CustomJSONEncoder, self).default(obj)

# Configure Flask to use custom JSON encoder
app.json_encoder = CustomJSONEncoder

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

def safe_int(value, default=None, min_val=None, max_val=None):
    """Safely convert value to integer with bounds checking"""
    if not value:
        return default
    try:
        result = int(value)
        if min_val is not None and result < min_val:
            return default
        if max_val is not None and result > max_val:
            return default
        return result
    except ValueError:
        return default

def safe_float(value, default=None, min_val=None, max_val=None):
    """Safely convert value to float with bounds checking"""
    if not value:
        return default
    try:
        result = float(value)
        if min_val is not None and result < min_val:
            return default
        if max_val is not None and result > max_val:
            return default
        return result
    except ValueError:
        return default

def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_options')
def get_options():
    """Endpoint to provide options for dropdowns"""
    return jsonify({
        'medications': medication_list,
        'allergies': allergy_list,
        'problem_list': problem_list,
        'surgery_list': surgery_list
    })

@app.route('/generate_note', methods=['POST'])
def generate_note():
    try:
        data = request.get_json()
        
        # Extract and validate medical values
        patient = data.get('patient', {})
        note_type = data.get('noteType', {})
        include_sections = data.get('includeSections', {})
        vitals = data.get('vitals', {})
        staging = data.get('staging', {})
        social_history = data.get('social_history', {})
        prior_treatment = data.get('prior_treatment', {})
        
        # Process the data with validation
        processed_data = {
            # Note type settings
            'note_generation_type': note_type.get('generation'),
            'clinical_note_type': note_type.get('clinical'),
            
            # Patient demographics
            'patient_age': safe_int(patient.get('age'), None, 18, 100),
            'patient_sex': patient.get('sex'),
            'patient_race': patient.get('race'),
            'patient_first_name': patient.get('first_name'),
            'patient_last_name': patient.get('last_name'),
            
            # Medical values
            'aua': safe_int(data.get('aua')),
            'ipss': safe_int(data.get('ipss')),
            'shim': safe_int(data.get('shim')),
            'ecog': safe_int(data.get('ecog')),
            'psa_score': safe_float(data.get('psa', {}).get('score')),
            'performance_score': safe_int(data.get('performance_score')),
            
            # Lists
            'medications': data.get('medications', []),
            'allergies': data.get('allergies', []),
            'problem_list': data.get('problem_list', {}).get('active_problems', []),
            'surgical_history': data.get('problem_list', {}).get('surgical_history', []),
            
            # Dates
            'base_date': parse_date(data.get('base_date')),
            'mri_date': parse_date(data.get('mri_date')),
            'pelvic_ct_date': parse_date(data.get('pelvic_ct')),
            'pelvic_mri_date': parse_date(data.get('pelvic_mri')),
            'bone_scan_date': parse_date(data.get('bone_scan')),
            
            # Vitals
            'temperature': safe_float(vitals.get('temperature')),
            'blood_pressure_systolic': safe_int(vitals.get('blood_pressure', {}).get('systolic')),
            'blood_pressure_diastolic': safe_int(vitals.get('blood_pressure', {}).get('diastolic')),
            'pulse': safe_int(vitals.get('pulse')),
            'respiration': safe_int(vitals.get('respiration')),
            'weight': safe_int(vitals.get('weight')),
            'pain': safe_int(vitals.get('pain')),
            
            # Staging
            'risk_level': staging.get('risk'),
            'tnm': staging.get('tnm'),
            'group_stage': staging.get('group_stage'),
            'histology': staging.get('histology'),
            
            # Treatment
            'prostatectomy': data.get('prostatectomy'),
            'colonoscopy': data.get('colonoscopy'),
            
            # Prior treatment
            'prior_rt': prior_treatment.get('prior_rt'),
            'prior_rt_date': parse_date(prior_treatment.get('prior_rt_date')),
            'chemotherapy_prescribed': prior_treatment.get('chemotherapy_prescribed'),
            'hormone_therapy_prescribed': prior_treatment.get('hormone_therapy_prescribed'),
            
            # Section toggles
            'include_hpi': include_sections.get('hpi', True),
            'include_vitals': include_sections.get('vitals', True),
            'include_social': include_sections.get('social', True),
            'include_medical': include_sections.get('medical', True),
            'include_exam': include_sections.get('exam', True),
            'include_imaging': include_sections.get('imaging', True),
            'include_plan': include_sections.get('plan', True),
            
            # Regeneration options
            'regen_hpi': data.get('regenSections', {}).get('regenerate_hpi', False),
            'regen_assmplan': data.get('regenSections', {}).get('regenerate_assmplan', False),
        }

        # Generate the note with the processed data
        note = ConsultNote(**processed_data)
        
        # Convert any numpy types to Python native types
        note_data = convert_numpy_types(note.get_data_fields())
        note_text = note.get_text()

        return jsonify({
            'text': note_text,
            'data': note_data
        })
    except Exception as e:
        print(f"Error generating note: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

# Make sure the JSON encoder is properly configured
app.json.encoder = CustomJSONEncoder

if __name__ == '__main__':
    app.run(debug=True)