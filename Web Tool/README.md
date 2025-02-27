#  Web Tool Readme
***
## Set Up

### Develop within a virtual environment
Please enter venv whenever changes are to be made.
1. To create a venv (within Web Tool directory): "python -m venv env"
2. To enter venv use command (powershell): 
    - ".\env\Scripts\activate"
2. To install requirements use command: "python -m pip install -r requirements.txt"
3. When done using venv exit using: "deactivate"
***
## Running

 1. **Navigate** into the "synthetic-note-generator" folder
 2. **Run** app.py: "python app.py"
 3. Click on given URL: "* Running on http://<url_name>"
***
## Documentation

### Note Generation code

Note generation code consists of the following files:
  - note.py
  - constants.py
  - data_elements.py
  - utils.py

app.py initializes Flask and handles endpoints.
