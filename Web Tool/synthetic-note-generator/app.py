from flask import Flask, render_template, request, jsonify
from note import ConsultNote
import traceback
from datetime import datetime

app = Flask(__name__)

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

@app.route('/generate_note', methods=['POST'])
def generate_note():
    try:
        data = request.get_json()
        
        # Extract data from the new structure
        patient = data.get('patient', {})
        note_type = data.get('noteType', {})
        include_sections = data.get('includeSections', {})
        
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
            
            # Staging information
            'risk_level': data.get('staging', {}).get('risk'),
            
            # Section toggles
            'include_hpi': include_sections.get('hpi', True),
            'include_vitals': include_sections.get('vitals', True),
            'include_social': include_sections.get('social', True),
            'include_medical': include_sections.get('medical', True),
            'include_exam': include_sections.get('exam', True),
            'include_imaging': include_sections.get('imaging', True),
            'include_plan': include_sections.get('plan', True),
            
            # Additional data that might be needed by the note generator
            'base_date': parse_date(data.get('base_date')),
            'note_author': data.get('note_author'),
            'note_cosigner': data.get('note_cosigner'),
            
            # Treatment information
            'prostatectomy': data.get('prostatectomy'),
            'colonoscopy': data.get('colonoscopy'),
            
            # Social history
            'social_history': data.get('social_history'),

            # Regeneration options
            'regen_hpi': data.get('regenSections', {}).get('regenerate_hpi', False),
            'regen_assmplan': data.get('regenSections', {}).get('regenerate_assmplan', False),
            
            # Lists
            'medications': data.get('medications', []),
            'allergies': data.get('allergies', []),
            'problem_list': data.get('problem_list', {})
        }

        # Generate the note with the processed data
        note = ConsultNote(**processed_data)
        
        return jsonify({
            'text': note.get_text(),
            'data': note.get_data_fields()
        })
    except Exception as e:
        print(f"Error generating note: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)