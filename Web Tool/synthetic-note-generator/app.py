from flask import Flask, render_template, request, jsonify
from note import ConsultNote
import traceback
from datetime import datetime
import numpy as np
import json
from constants import medication_list, allergy_list, problem_list, surgery_list
from constants import PRESET_RANGES, LIST_QUANTITY_RANGES
import random

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
        # Convert to datetime.date instead of datetime.datetime
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.date()  # Return just the date portion
    except ValueError:
        return None

@app.route('/')
def index():
    """Landing page to choose between single or bulk generation"""
    return render_template('landing.html')

@app.route('/single')
def single_note():
    """Original single note generation page"""
    return render_template('index.html')  

@app.route('/bulk')
def bulk_notes():
    """New bulk note generation page"""
    return render_template('bulk.html') 

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
        
        # Extract all nested data (from note.py)
        patient = data.get('patient', {})
        note_type = data.get('noteType', {})
        include_sections = data.get('includeSections', {})
        vitals = data.get('vitals', {})
        staging = data.get('staging', {})
        social_history = data.get('social_history', {})
        prior_treatment = data.get('prior_treatment', {})
        regenerate = data.get('regenSections', {})

        # Process the data with validation
        processed_data = {
            # Note type settings
            'note_generation_type': note_type.get('generation'),
            'clinical_note_type': note_type.get('clinical'),
                
            # Patient demographics
            'patient_age': safe_int(patient.get('age'), None, 18, 100),
            'patient_sex': patient.get('sex'),
            'patient_race': patient.get('race'),
            'patient_ethnicity': patient.get('ethnicity'),
            'patient_first_name': patient.get('first_name'),
            'patient_last_name': patient.get('last_name'),
                
            # Authors - Fixed field names to match form
            'note_author': data.get('note_author'),
            'note_cosigner': data.get('note_cosigner'),
            
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
            
            # Social history
            'alcohol_history': social_history.get('alcohol_history'),
            'smoking_history': social_history.get('smoking_history'),
            
            # Section toggles
            'include_hpi': include_sections.get('hpi', True),
            'include_vitals': include_sections.get('vitals', True),
            'include_social': include_sections.get('social', True),
            'include_medical': include_sections.get('medical', True),
            'include_exam': include_sections.get('exam', True),
            'include_imaging': include_sections.get('imaging', True),
            'include_plan': include_sections.get('plan', True),
            
            # Regeneration options
            'regen_hpi':regenerate.get('regenerate_hpi', False),
            # NOTE: regenerate_assmplan is not properly received from js, not sure why (sent as True and received as False)
            'regen_assmplan': regenerate.get('regenerate_assmplan', True),
        }

        print(f"regen_hpi: {processed_data['regen_hpi']}")
        print(f"regen_assmplan: {processed_data['regen_assmplan']}")

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

@app.route('/get_ranges')
def get_ranges():
    """Return all preset ranges for the frontend"""
    return jsonify({
        **PRESET_RANGES,
        **LIST_QUANTITY_RANGES
    })

def get_random_value_in_range(range_values):
    """Get a random value within the specified range"""
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
        regen_sections = data.get('regenSections', {}) or data.get('ranges', {})

        if num_notes < 1 or num_notes > 1000:
            return jsonify({
                'error': 'Number of notes must be between 1 and 1000'
            }), 400
        
        generated_notes = []
        for _ in range(num_notes):
            # Create note parameters based on ranges
            note_params = {}
            
            # Handle basic numeric ranges
            if 'age' in ranges:
                note_params['patient_age'] = get_random_value_in_range(ranges['age'])
            
            if 'aua' in ranges:
                note_params['aua'] = get_random_value_in_range(ranges['aua'])
                
            if 'ipss' in ranges:
                note_params['ipss'] = get_random_value_in_range(ranges['ipss'])
                
            if 'shim' in ranges:
                note_params['shim'] = get_random_value_in_range(ranges['shim'])
                
            if 'ecog' in ranges:
                note_params['ecog'] = get_random_value_in_range(ranges['ecog'])
                
            if 'psa' in ranges:
                note_params['psa_score'] = get_random_value_in_range(ranges['psa'])
                
            if 'performance_score' in ranges:
                note_params['performance_score'] = get_random_value_in_range(ranges['performance_score'])
                
            if 'temperature' in ranges:
                note_params['temperature'] = get_random_value_in_range(ranges['temperature'])
                
            if 'systolic' in ranges:
                note_params['blood_pressure_systolic'] = get_random_value_in_range(ranges['systolic'])
                
            if 'diastolic' in ranges:
                note_params['blood_pressure_diastolic'] = get_random_value_in_range(ranges['diastolic'])
                
            if 'pulse' in ranges:
                note_params['pulse'] = get_random_value_in_range(ranges['pulse'])
                
            if 'respiration' in ranges:
                note_params['respiration'] = get_random_value_in_range(ranges['respiration'])
                
            if 'weight' in ranges:
                note_params['weight'] = get_random_value_in_range(ranges['weight'])
                
            if 'pain' in ranges:
                note_params['pain'] = get_random_value_in_range(ranges['pain'])

            # Handle categorical fields
            if 'sexSelect' in ranges:
                note_params['patient_sex'] = ranges['sexSelect']
                
            if 'raceSelect' in ranges:
                note_params['patient_race'] = ranges['raceSelect']
                
            if 'ethnicitySelect' in ranges:
                note_params['patient_ethnicity'] = ranges['ethnicitySelect']
                
            if 'tnmSelect' in ranges:
                note_params['tnm'] = ranges['tnmSelect']
                
            if 'riskLevelSelect' in ranges:
                note_params['risk_level'] = ranges['riskLevelSelect']
                
            if 'groupStageSelect' in ranges:
                note_params['group_stage'] = ranges['groupStageSelect']
                
            if 'alcoholHistorySelect' in ranges:
                note_params['alcohol_history'] = ranges['alcoholHistorySelect']
                
            if 'smokingStatusSelect' in ranges:
                note_params['smoking_history'] = {'smoking_status': ranges['smokingStatusSelect']}
                
            if 'prostatectomySelect' in ranges:
                note_params['prostatectomy'] = ranges['prostatectomySelect']
                
            if 'colonoscopySelect' in ranges:
                note_params['colonoscopy'] = ranges['colonoscopySelect'] == 'true'
                
            if 'priorRtSelect' in ranges:
                note_params['prior_rt'] = ranges['priorRtSelect'] == 'true'
                
            if 'chemotherapySelect' in ranges:
                note_params['chemotherapy_prescribed'] = ranges['chemotherapySelect'] == 'true'
                
            if 'hormoneTherapySelect' in ranges:
                note_params['hormone_therapy_prescribed'] = ranges['hormoneTherapySelect'] == 'true'

            # Handle list quantities
            if 'medications' in ranges:
                quantity = int(get_random_value_in_range(ranges['medications']))
                if quantity > 0:
                    note_params['medications'] = random.sample(medication_list, min(quantity, len(medication_list)))
            
            if 'allergies' in ranges:
                quantity = int(get_random_value_in_range(ranges['allergies']))
                if quantity > 0:
                    note_params['allergies'] = random.sample(allergy_list, min(quantity, len(allergy_list)))
            
            if 'problems' in ranges:
                quantity = int(get_random_value_in_range(ranges['problems']))
                if quantity > 0:
                    note_params['problem_list'] = random.sample(problem_list, min(quantity, len(problem_list)))
            
            if 'surgeries' in ranges:
                quantity = int(get_random_value_in_range(ranges['surgeries']))
                if quantity > 0:
                    note_params['surgical_history'] = random.sample(surgery_list, min(quantity, len(surgery_list)))

            regen_sections = data.get('regenSections', {}) or data.get('ranges', {})

            note_params['regen_hpi'] = regen_sections.get('regenerate_hpi') or regen_sections.get('regenerateHPI', False)
            note_params['regen_assmplan'] = regen_sections.get('regenerate_assmplan') or regen_sections.get('regenerateAssmPlan', False)

            # Debugging
            print(f"DEBUG: regen_hpi = {note_params['regen_hpi']}, Type: {type(note_params['regen_hpi'])}")
            print(f"DEBUG: regen_assmplan = {note_params['regen_assmplan']}, Type: {type(note_params['regen_assmplan'])}")

            # Generate the note using the ConsultNote class
            note = ConsultNote(**note_params)
            generated_notes.append({
                'text': note.get_text(),
                'data': convert_numpy_types(note.get_data_fields())
            })

        return jsonify({
            'notes': generated_notes,
            'count': len(generated_notes)
        })

    except Exception as e:
        print(f"Error generating bulk notes: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)