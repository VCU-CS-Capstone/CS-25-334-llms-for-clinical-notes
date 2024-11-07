from flask import Flask, render_template, request, jsonify
from note import ConsultNote
import traceback

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_note', methods=['POST'])
def generate_note():
    try:
        data = request.get_json()
        
        # Extract and validate medical values
        medical_values = data.get('medicalValues', {})
        demographics = data.get('demographics', {})
        note_type = data.get('noteType', {})
        include_sections = data.get('includeSections', {})
        regen_sections = data.get('regenSections', {})

        regen_hpi = regen_sections.get('regenerate_hpi', False)
        regen_assmplan = regen_sections.get('regenerate_assmplan', False)

        # Debug: Print the values of regen_hpi and regen_assmplan
        print("Regenerate HPI in app.py:", regen_hpi)
        print("Regenerate Assessment Plan in app.py:", regen_assmplan)

        # Process the data with validation
        processed_data = {
            # Note type settings
            'note_generation_type': note_type.get('generation'),
            'clinical_note_type': note_type.get('clinical'),
            
            # Demographics with validation
            'patient_age': safe_int(demographics.get('age'), None, 18, 100),
            'patient_sex': demographics.get('sex'),
            'patient_race': demographics.get('race'),
            'patient_first_name': demographics.get('firstName'),
            'patient_last_name': demographics.get('lastName'),
            
            # Medical values with validation
            'aua': safe_int(medical_values.get('aua'), None, 0, 35),
            'ipss': safe_int(medical_values.get('ipss'), None, 0, 35),
            'shim': safe_int(medical_values.get('shim'), None, 1, 25),
            'ecog': safe_int(medical_values.get('ecog'), None, 0, 4),
            'psa_score': safe_float(medical_values.get('psaScore'), None, 0),
            'disease_site': medical_values.get('diseaseSite'),
            'risk_level': medical_values.get('riskLevel'),
            'gleason_primary': safe_int(medical_values.get('gleasonPrimary'), None, 3, 5),
            'gleason_secondary': safe_int(medical_values.get('gleasonSecondary'), None, 3, 5),
            
            # Section toggles
            'include_hpi': include_sections.get('hpi', True),
            'include_vitals': include_sections.get('vitals', True),
            'include_social': include_sections.get('social', True),
            'include_medical': include_sections.get('medical', True),
            'include_exam': include_sections.get('exam', True),
            'include_imaging': include_sections.get('imaging', True),
            'include_plan': include_sections.get('plan', True),

            # Groq regeneration
            'regen_hpi': regen_sections.get('regenerate_hpi', False),
            'regen_assmplan': regen_sections.get('regenerate_assmplan', False)
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