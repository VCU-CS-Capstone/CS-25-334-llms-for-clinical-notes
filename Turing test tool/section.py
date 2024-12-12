from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI

app = Flask(__name__)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DIRECTORY = "/Users/shashanksinha/Desktop/synthetic note generator"
SAVE_DIRECTORY = "/Users/shashanksinha/Desktop/synthetic note generator/responses"

def split_clinical_notes(notes, section):
    prompt = f"Using this note: {notes} Show me the information associated with the {section} section. Do not summarize it, do not add anything else, just repeat the text that is shown."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are showing me the {section} section of a clinical note."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                return file.read()  
    return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-section', methods=['GET'])
def generate_section():
    try:
        notes = process_files(DIRECTORY)
        if not notes:
            return jsonify({'section': 'Error: No notes found in the directory.'}), 500

        # Edits soon to be made such that the section is generated randomly
        section = "Medical History" 
        generated_section = split_clinical_notes(notes, section)
        
        return jsonify({'section': generated_section})
    except Exception as e:
        return jsonify({'section': f'Error: {str(e)}'}), 500


@app.route('/submit-response', methods=['POST'])
def submit_response():
    try:
        data = request.get_json()
        note_type = data.get('noteType')
        reasoning = data.get('reasoning')

        if not note_type or not reasoning:
            return jsonify({'message': 'Invalid input'}), 400

        filename = f"response_{note_type}_{len(os.listdir(SAVE_DIRECTORY)) + 1}.txt"
        file_path = os.path.join(SAVE_DIRECTORY, filename)

        with open(file_path, "w") as file:
            file.write(f"Note Type: {note_type}\n")
            file.write(f"Reasoning: {reasoning}\n")

        return jsonify({'message': 'Response saved successfully!'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
