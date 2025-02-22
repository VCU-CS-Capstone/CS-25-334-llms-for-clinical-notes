// Define the ExportButtons component
const ExportButtons = () => {
    const downloadNote = () => {
        const noteOutput = document.querySelector('#noteOutput .output-section:first-child pre');
        if (!noteOutput || !noteOutput.textContent) {
            alert('No note data available to export');
            return;
        }

        const blob = new Blob([noteOutput.textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `synthetic_note_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const downloadJson = () => {
        const jsonOutput = document.querySelector('#noteOutput .output-section:nth-child(2) pre');
        if (!jsonOutput || !jsonOutput.textContent) {
            alert('No JSON data available to export');
            return;
        }
    
        try {
            // Parse and re-stringify to ensure valid JSON
            const jsonData = JSON.parse(jsonOutput.textContent);
            const formattedJson = JSON.stringify(jsonData, null, 2);
            const blob = new Blob([formattedJson], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `note_data_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            alert('Error processing JSON data: ' + error.message);
        }
    };

    return React.createElement('div', { className: 'flex gap-4 mt-4' },
        React.createElement('button', {
            onClick: downloadNote,
            className: 'bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors',
            type: 'button'
        }, 'Export Note'),
        React.createElement('button', {
            onClick: downloadJson,
            className: 'bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded transition-colors',
            type: 'button'
        }, 'Export JSON')
    );
};

// Define the options (these will be loaded from the backend)
const OPTIONS = {
    medication: [],
    allergy: [],
    problem: [],
    surgery: []
};

// Fetch options from backend when page loads
function loadOptions() {
    fetch('/get_options')
        .then(response => response.json())
        .then(data => {
            OPTIONS.medication = data.medications;
            OPTIONS.allergy = data.allergies;
            OPTIONS.problem = data.problem_list;
            OPTIONS.surgery = data.surgery_list;
            console.log('Loaded options:', OPTIONS); // Debug log
        })
        .catch(error => console.error('Error loading options:', error));
}

// Create dropdown instead of text input
function createDropdown(options) {
    const select = document.createElement('select');
    select.className = 'form-select';
    
    // Add empty option
    const emptyOption = document.createElement('option');
    emptyOption.value = '';
    emptyOption.textContent = '-- Select --';
    select.appendChild(emptyOption);
    
    // Add all options
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
    
    return select;
}

// Helper function to create a dynamic field group
function createDynamicFieldGroup(containerId, fieldType) {
    console.log('Creating field group:', fieldType, 'Options:', OPTIONS[fieldType]); // Debug log
    const container = document.getElementById(containerId);
    const wrapper = document.createElement('div');
    wrapper.className = 'dynamic-field-wrapper';
    
    // Create dropdown instead of text input
    const dropdown = createDropdown(OPTIONS[fieldType]);
    dropdown.className = `${fieldType}-input`;
    
    // Create remove button
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-field';
    removeBtn.textContent = 'Remove';
    removeBtn.onclick = function() {
        container.removeChild(wrapper);
    };
    
    wrapper.appendChild(dropdown);
    wrapper.appendChild(removeBtn);
    container.appendChild(wrapper);
}

// Add event listeners for the dynamic field buttons
document.addEventListener('DOMContentLoaded', function() {
    // Load options when page loads
    loadOptions();
    
    const addMedicationBtn = document.getElementById('addMedication');
    const addAllergyBtn = document.getElementById('addAllergy');
    const addProblemBtn = document.getElementById('addProblem');
    const addSurgeryBtn = document.getElementById('addSurgery');

    if (addMedicationBtn) {
        addMedicationBtn.addEventListener('click', () => createDynamicFieldGroup('medicationsContainer', 'medication'));
    }
    if (addAllergyBtn) {
        addAllergyBtn.addEventListener('click', () => createDynamicFieldGroup('allergiesContainer', 'allergy'));
    }
    if (addProblemBtn) {
        addProblemBtn.addEventListener('click', () => createDynamicFieldGroup('problemsContainer', 'problem'));
    }
    if (addSurgeryBtn) {
        addSurgeryBtn.addEventListener('click', () => createDynamicFieldGroup('surgicalHistoryContainer', 'surgery'));
    }
});

// Function to get value from input, with type conversion if needed
function getInputValue(elementId, type = 'string') {
    const element = document.getElementById(elementId);
    if (!element) return null;
    
    const value = element.value.trim();
    if (!value) return null;
    
    switch (type) {
        case 'number':
            return Number(value);
        case 'boolean':
            return value === 'true';
        default:
            return value;
    }
}

// Function to collect TNM staging
function getTNMStaging() {
    const t = getInputValue('stageT');
    const n = getInputValue('stageN');
    const m = getInputValue('stageM');
    return t && n && m ? `${t}${n}${m}` : null;
}

// Function to collect vitals
function getVitals() {
    return {
        temperature: getInputValue('temperature', 'number'),
        blood_pressure: {
            systolic: getInputValue('systolic', 'number'),
            diastolic: getInputValue('diastolic', 'number')
        },
        pulse: getInputValue('pulse', 'number'),
        respiration: getInputValue('respiration', 'number'),
        weight: getInputValue('weight', 'number'),
        pain: getInputValue('pain', 'number')
    };
}

// Function to collect social history
function getSocialHistory() {
    return {
        alcohol_history: getInputValue('alcoholHistory'),
        smoking_history: {
            smoking_status: getInputValue('smokingStatus'),
            years_smoked: getInputValue('yearsSmoked', 'number'),
            packs_per_year: getInputValue('packsPerYear', 'number'),
            years_ago_stopped: getInputValue('yearsAgoStopped', 'number')
        }
    };
}

// Function to collect all form data
function collectFormData() {
    const formData = {
        // Regeneration options
        regenSections: {
            regenerate_hpi: document.getElementById('regenerateHPI')?.checked ?? false,
            regenerate_assmplan: document.getElementById('regenerateAssmPlan')?.checked ?? false
        },
        noteType: {
            generation: getInputValue('noteGenerationType'),
            clinical: getInputValue('clinicalNoteType')
        },
        
        patient: {
            age: getInputValue('patientAge', 'number'),
            sex: getInputValue('patientSex'),
            race: getInputValue('patientRace'),
            ethnicity: getInputValue('ethnicity'),
            first_name: getInputValue('firstName'),
            last_name: getInputValue('lastName')
        },
        
        // Authors
        note_author: getInputValue('noteAuthor'),
        note_cosigner: getInputValue('noteCosigner'),
        
        // Medical values
        aua: getInputValue('aua', 'number'),
        ipss: getInputValue('ipss', 'number'),
        shim: getInputValue('shim', 'number'),
        ecog: getInputValue('ecog', 'number'),
        psa: {
            score: getInputValue('psaScore', 'number')
        },
        performance_score: getInputValue('performanceScore', 'number'),
        
        // Dates
        base_date: getInputValue('baseDate'),
        mri_date: getInputValue('mriDate'),
        pelvic_ct: getInputValue('pelvicCtDate'),
        pelvic_mri: getInputValue('pelvicMriDate'),
        bone_scan: getInputValue('boneScanDate'),
        
        // Dynamic lists
        medications: Array.from(document.querySelectorAll('#medicationsContainer .medication-input'))
            .map(select => select.value)
            .filter(Boolean),
            
        allergies: Array.from(document.querySelectorAll('#allergiesContainer .allergy-input'))
            .map(select => select.value)
            .filter(Boolean),
            
        problem_list: {
            active_problems: Array.from(document.querySelectorAll('#problemsContainer .problem-input'))
                .map(select => select.value)
                .filter(Boolean),
            surgical_history: Array.from(document.querySelectorAll('#surgicalHistoryContainer .surgery-input'))
                .map(select => select.value)
                .filter(Boolean)
        },
        
        // Vitals
        vitals: getVitals(),
        
        // Staging
        staging: {
            tnm: getTNMStaging(),
            group_stage: getInputValue('groupStage'),
            risk: getInputValue('riskLevel'),
            histology: getInputValue('histology')
        },
        
        // Treatment
        prostatectomy: getInputValue('prostatectomy'),
        colonoscopy: getInputValue('colonoscopy', 'boolean'),
        prior_treatment: {
            prior_rt: getInputValue('priorRt', 'boolean'),
            prior_rt_date: getInputValue('priorRtDate'),
            chemotherapy_prescribed: getInputValue('chemoPrescribed', 'boolean'),
            hormone_therapy_prescribed: getInputValue('hormonePrescribed', 'boolean')
        },
        
        // Include/Exclude Sections
        includeSections: {
            hpi: document.getElementById('includeHPI')?.checked ?? true,
            vitals: document.getElementById('includeVitals')?.checked ?? true,
            social: document.getElementById('includeSocial')?.checked ?? true,
            medical: document.getElementById('includeMedical')?.checked ?? true,
            exam: document.getElementById('includeExam')?.checked ?? true,
            imaging: document.getElementById('includeImaging')?.checked ?? true,
            plan: document.getElementById('includePlan')?.checked ?? true
        },

        // Social History
        social_history: getSocialHistory()
    };

    return formData;
}

// Event handler for form submission
document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generateNote');
    if (generateButton) {
        generateButton.addEventListener('click', function() {
            const formData = collectFormData();
            
            fetch('/generate_note', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('noteOutput').innerHTML = `
                        <div class="error">
                            <h3>Error:</h3>
                            <pre>${data.error}</pre>
                            <h3>Stack Trace:</h3>
                            <pre>${data.trace}</pre>
                        </div>
                    `;
                } else {
                    document.getElementById('noteOutput').innerHTML = `
                        <div class="output-section">
                            <h3>Generated Note:</h3>
                            <pre>${data.text}</pre>
                        </div>
                        <div class="output-section">
                            <h3>Note Data:</h3>
                            <pre>${JSON.stringify(data.data, null, 2)}</pre>
                        </div>
                        <div id="export-buttons-root"></div>
                    `;
            
                    // Render the export buttons
                    const root = ReactDOM.createRoot(document.getElementById('export-buttons-root'));
                    root.render(React.createElement(ExportButtons));
                }
            })
            .catch(error => {
                document.getElementById('noteOutput').innerHTML = `
                    <div class="error">
                        <h3>Error:</h3>
                        <pre>Failed to generate note: ${error}</pre>
                    </div>
                `;
            });
        });
    }
});