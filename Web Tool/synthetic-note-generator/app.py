from flask import Flask, render_template, request, jsonify
from note import ConsultNote

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_note', methods=['POST'])
def generate_note():
    data = request.get_json()
    aua_value = int(data.get('aua')) if data.get('aua') else None
    ipss_value = int(data.get('ipss')) if data.get('ipss') else None
    shim_value = int(data.get('shim')) if data.get('shim') else None
    ecog_value = int(data.get('ecog')) if data.get('ecog') else None

    note = ConsultNote(aua=aua_value, ipss=ipss_value, shim=shim_value, ecog=ecog_value)  # Pass values to ConsultNote
    return jsonify({
        'text': note.get_text(),
        'data': note.get_data_fields()
    })

if __name__ == '__main__':
    app.run(debug=True)
