from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
import time

app = Flask(__name__)

SAVE_DIRECTORY = "/app/responses"

# Ensure the save directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="mysql",
            port="3306",
            user="root",
            password="client_section1",
            database="section_db"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-section', methods=['GET'])
def generate_section():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'section': 'Error: Database connection failed.'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, label, content, section_type FROM clinical_note_sections ORDER BY RAND() LIMIT 1;")
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return jsonify({'section': 'Error: No notes found in the database.'}), 500

        return jsonify({'id': row['id'], 'label': row['label'], 'section': row['content'], 'actual_type': row['section_type']})
    except Exception as e:
        return jsonify({'section': f'Error: {str(e)}'}), 500

@app.route('/submit-response', methods=['POST'])
def submit_response():
    try:
        data = request.get_json()
        note_type = data.get('noteType')
        reasoning = data.get('reasoning')
        actual_note_type = data.get('actualNoteType')

        if not note_type or not reasoning or not actual_note_type:
            return jsonify({'message': 'Invalid input'}), 400

        # Generate a unique filename using a timestamp
        timestamp = int(time.time())
        filename = f"response_{timestamp}.txt"
        file_path = os.path.join(SAVE_DIRECTORY, filename)

        # Save response in a separate text file
        with open(file_path, "w") as file:
            file.write(f"User note type guess: {note_type}\n")
            file.write(f"Reasoning: {reasoning}\n")
            file.write(f"Actual note type: {actual_note_type}\n")

        return jsonify({'message': f'Response saved as {filename}!'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
