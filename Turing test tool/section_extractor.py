import re
import os

SECTION_LABELS = {
    "History of Present Illness": [r"HPI", r"History of Present Illness", r"History"],
    "Past Medical History": [r"PMH", r"Past Medical History", r"Medical History"],
}

def create_section_patterns(section_labels):
    section_patterns = {}
    for section, labels in section_labels.items():
        pattern = r"(" + "|".join(labels) + r")\s*:"
        section_patterns[section] = pattern
    return section_patterns

def extract_sections(note, section_patterns):
    extracted_sections = {}
    
    for section_name, section_pattern in section_patterns.items():
        match = re.search(section_pattern, note, re.IGNORECASE)
        
        if match:
            start_index = match.end() 
            
            next_section = re.search(r"\n[A-Z ]+:\n", note[start_index:])
            
            if next_section:
                end_index = start_index + next_section.start()
                extracted_sections[section_name] = note[start_index:end_index].strip()
            else:
                extracted_sections[section_name] = note[start_index:].strip()
        else:
            extracted_sections[section_name] = "Section not found."
    
    return extracted_sections

def process_files(directory):
    section_patterns = create_section_patterns(SECTION_LABELS)
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"): 
            file_path = os.path.join(directory, filename)
            
            with open(file_path, "r") as file:
                note_content = file.read()
            
            extracted_sections = extract_sections(note_content, section_patterns)
            
            print(f"Extracted sections from {filename}:")
            for section_name, content in extracted_sections.items():
                print(f"{section_name}:\n{content}\n")


directory = "/Users/shashanksinha/Desktop/synthetic note generator"
process_files(directory)

