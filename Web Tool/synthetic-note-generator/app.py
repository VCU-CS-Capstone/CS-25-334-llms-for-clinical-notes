from flask import Flask, render_template, request, jsonify
from note import ConsultNote

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_note', methods=['POST'])
def generate_note():
    note = ConsultNote()
    return jsonify({
        'text': note.get_text(),
        'data': note.get_data_fields()
    })

if __name__ == '__main__':
    app.run(debug=True)