import datetime
import random
from groq import Groq
import os
import calendar
import re
from constants import hpi_command_phrases, asmplan_command_phrases
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GROQ_API_KEY")

def regenerate(note, temp=1.05, commandType='hpi'):
    # Different sections require different command types when regenerating
    if commandType == 'asmplan':
        request = random.choice(asmplan_command_phrases)
    else:
        request = random.choice(hpi_command_phrases)

    request += note
    client = Groq(
    api_key=key
    )
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": request
            }
        ],
        temperature=temp,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""
    return result

def replace_placeholders(text, mappings):
    # Replace bracketed numbers with mappings, such as {1} -> patient.last_name -> Smith
    def replacement(match):
        index = int(match.group(1))
        return str(mappings.get(index, match.group(0)))

    # Last resort, delete unmapped bracketed numbers such as {32}
    # This code cleanly deletes them without removing any '\n's
    cleaned_lines = []
    for line in text.splitlines():
        # Split line into sentences
        sentences = re.split(r'(?<=[.!?])\s+', line)
        valid_sentences = []
        for sentence in sentences:
            # Find {x}'s
            placeholders = re.findall(r'\{(\d+)\}', sentence)
            # Replace and save mappings only if they are valid
            if all(int(p) in mappings for p in placeholders):
                valid_sentences.append(sentence)
        cleaned_lines.append(' '.join(valid_sentences))

    cleaned_text = '\n'.join(cleaned_lines)
    return re.sub(r'\{(\d+)\}', replacement, cleaned_text)

def regen_validation(text, hpi=True):
    # Checks for numbers inside brackets, followed by a percentage sign, or bulleted such as '3.'
    pattern = r'(?<!\{)\b\d+\b(?!\})(?!\s*%)(?!\.)'
    newTemp = 1.0
    type = ''
    
    # Perform regeneration based on command type
    if hpi:
        type = 'hpi'
        regenerated_text = regenerate(text, commandType='hpi')
    else:
        type = 'asmplan'
        regenerated_text = regenerate(text, commandType='asmplan')

    while (1):
        # Makes sure that bracketed values in the regenerated text match the original text
        t1 = set(re.findall(r'\{(\d+)\}', text))
        t2 = set(re.findall(r'\{(\d+)\}', regenerated_text))

        outside_values = re.findall(pattern, regenerated_text)

        if not outside_values and t2.issubset(t1):
                print("\nProper regeneration without alterations")
                break
        else:
            print("\n*****Anomaly detected******")
            print("Regenerating Text:", regenerated_text)
            # Decrease temperature to prevent infinite loop regeneration
            regenerated_text = regenerate(text, newTemp - 0.01, type)

    # Clean unwanted helper sentences. They appear even when specified not to.
    cleaned_text = clean_sentences(regenerated_text)
    return cleaned_text

def clean_sentences(text):
    # This deletes sentences such as "Here is your note"
    cleaned_lines = []
    for line in text.splitlines():
        sentences = re.split(r'(?<=[.!?])\s+', line)
        cleaned = [s for s in sentences if not re.search(r'\b(here|rewritten|note|rephrased)\b', s, re.IGNORECASE)]
        cleaned_lines.append(' '.join(cleaned))
    return '\n'.join(cleaned_lines)

def get_feature_probabilities():
    probabilities = {
        'note_cosigner': 1.0,
        'problem_list': 1.0,
        'medication_list': 1.0,
        'allergies_list': 1.0,
        'ct': 1.0,
        'mri': 1.0,
        'bone_scan': 1.0,
        'alcohol_status': [0.0, 1/3., 1/3., 1/3.],
        'smoking_status': [0.0, 1/3., 1/3., 1/3.],
    }
    return probabilities


def random_time_period(min_period=1, max_period=2, time_period='month'):
    if time_period == 'month':
        single = 'month'
        multiple = 'months'
    elif time_period == 'week':
        single = 'week'
        multiple = 'weeks'
    elif time_period == 'year':
        single = 'year'
        multiple = 'years'
    else:
        single = ''
        multiple = ''
        assert f'Invalid time period {time_period}'

    period = random.randint(min_period, max_period)
    if period < 1:
        period = 1
    if period == 1:
        return f'{period} {single}'
    else:
        return f'{period} {multiple}'


def format_date(dt, date_format=None):
    if dt is None:
        return None
    else:
        if date_format is None:
            date_format_index = random.randint(0, 3)
        else:
            date_format_index = date_format
        if date_format_index == 0:
            return dt.strftime('%m/%d/%Y')
        elif date_format_index == 1:
            return dt.strftime('%m-%d-%Y')
        elif date_format_index == 2:
            return dt.strftime('%Y-%m-%d')
        else:
            return dt.strftime('%b %d, %Y')


def date_offset(years=0, months=0, days=0):
    return datetime.timedelta(days=years * 365 + months * 30 + days)