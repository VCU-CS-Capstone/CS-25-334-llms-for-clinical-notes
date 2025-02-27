
## Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- Pip (Python package manager)

After cloning, update the directory path in section.py for the clinical notes in the code to point to the correct location on your local machine where the notes are stored.

## Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key to the file, API key can be created here -  https://platform.openai.com/api-keys :
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python section.py
   ```

2. **Access the interface**:
   Open a web browser and navigate to `http://127.0.0.1:5000/`.
