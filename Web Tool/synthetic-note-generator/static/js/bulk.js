class RangeManager {
    constructor() {
        this.ranges = {};
        this.generatedNotes = [];
        this.setupEventListeners();
    }

    async initialize() {
        // Fetch preset ranges from server
        try {
            const response = await fetch('/get_ranges');
            const data = await response.json();
            this.ranges = data;
            
            // Populate dropdowns with options from the server
            this.populateRangeOptions();
            
            // Initialize the custom range display state
            this.initializeCustomRangeDisplay();
        } catch (error) {
            console.error('Error loading ranges:', error);
        }
    }

    setupEventListeners() {
        // Generate notes button
        document.getElementById('generateBulkNotes').addEventListener('click', () => this.generateNotes());

        // Note selector
        const noteSelector = document.getElementById('noteSelector');
        if (noteSelector) {
            noteSelector.addEventListener('change', (e) => {
                this.displayNote(parseInt(e.target.value));
            });
        }

        // Handle preset selection changes - We'll set this up after populating the dropdowns
    }

    // New method to populate range options from server data
    populateRangeOptions() {
        // For each numerical field, populate its dropdown with options from the ranges
        Object.keys(this.ranges).forEach(field => {
            const selectElement = document.getElementById(`${field}Preset`);
            if (!selectElement) return;
            
            // Clear existing options (except the first one if it's a categorical field)
            if (field.endsWith('Select')) {
                // For categorical fields, keep the existing options
            } else {
                // For numeric fields with custom ranges
                selectElement.innerHTML = '';
                
                // Add custom range option
                const customOption = document.createElement('option');
                customOption.value = 'custom';
                customOption.textContent = 'Custom Range';
                selectElement.appendChild(customOption);
                
                // Add options from server data
                if (this.ranges[field]) {
                    this.ranges[field].forEach(({label, range}) => {
                        const option = document.createElement('option');
                        option.value = range.join('-');
                        option.textContent = `${label} (${range[0]}-${range[1]})`;
                        selectElement.appendChild(option);
                    });
                }
                
                // Add event listener for this dropdown
                selectElement.addEventListener('change', (e) => {
                    const fieldId = e.target.id.replace('Preset', '');
                    const customRange = document.getElementById(`${fieldId}CustomRange`);
                    
                    if (customRange) {
                        if (e.target.value === 'custom') {
                            customRange.style.display = 'flex';
                        } else {
                            customRange.style.display = 'none';
                            if (e.target.value.includes('-')) {
                                const [min, max] = e.target.value.split('-');
                                const minInput = document.getElementById(`${fieldId}Min`);
                                const maxInput = document.getElementById(`${fieldId}Max`);
                                
                                if (minInput && maxInput) {
                                    minInput.value = min;
                                    maxInput.value = max;
                                }
                            }
                        }
                    }
                });
            }
        });
    }

    // Initialize custom range display
    initializeCustomRangeDisplay() {
        // Hide all custom range inputs by default
        document.querySelectorAll('.custom-range').forEach(range => {
            range.style.display = 'none';
        });
        
        // Show custom ranges only for those with 'custom' selected
        document.querySelectorAll('.range-preset').forEach(preset => {
            if (preset.value === 'custom') {
                const fieldId = preset.id.replace('Preset', '');
                const customRange = document.getElementById(`${fieldId}CustomRange`);
                if (customRange) {
                    customRange.style.display = 'flex';
                }
            }
        });
    }

    formatFieldName(field) {
        return field
            .replace(/_/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    getSelectedRanges() {
        const ranges = {};
        
        // Get numeric ranges from preset fields
        document.querySelectorAll('.range-preset').forEach(preset => {
            if (preset.id.endsWith('Select')) {
                // Skip categorical fields, they're handled separately
                return;
            }
            
            // Extract field name from the preset id
            const field = preset.id.replace('Preset', '');
            
            if (preset.value === 'custom') {
                // Get min/max from custom inputs
                const minInput = document.getElementById(`${field}Min`);
                const maxInput = document.getElementById(`${field}Max`);
                
                if (minInput && maxInput && minInput.value && maxInput.value) {
                    ranges[field] = [parseFloat(minInput.value), parseFloat(maxInput.value)];
                }
            } else if (preset.value.includes('-')) {
                // Get min/max from preset value
                const [min, max] = preset.value.split('-');
                ranges[field] = [parseFloat(min), parseFloat(max)];
            }
        });
        
        // Get categorical selections
        const categoryFields = [
            'sexSelect', 'raceSelect', 'ethnicitySelect', 'tnmSelect', 
            'riskLevelSelect', 'groupStageSelect', 'alcoholHistorySelect', 
            'smokingStatusSelect', 'prostatectomySelect', 'colonoscopySelect',
            'priorRtSelect', 'chemotherapySelect', 'hormoneTherapySelect'
        ];
        
        categoryFields.forEach(fieldId => {
            const select = document.getElementById(fieldId);
            if (select && select.value !== 'random') {
                const fieldName = fieldId.replace('Select', '');
                ranges[fieldName] = select.value;
            }
        });
        
        return ranges;
    }

    async generateNotes() {
        const numNotes = document.getElementById('numberOfNotes').value;
        const ranges = this.getSelectedRanges();
        
        // Show loading indicator
        document.getElementById('generateBulkNotes').textContent = 'Generating...';
        document.getElementById('generateBulkNotes').disabled = true;

        try {
            const response = await fetch('/generate_bulk_notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num_notes: numNotes,
                    ranges: ranges
                })
            });

            const data = await response.json();
            
            if (data.error) {
                alert(`Error generating notes: ${data.error}`);
                document.getElementById('generateBulkNotes').textContent = 'Generate Notes';
                document.getElementById('generateBulkNotes').disabled = false;
                return;
            }

            this.generatedNotes = data.notes;
            this.updateNoteSelector(data.notes.length);
            this.displayNote(0);

            // Show success message
            document.getElementById('generateBulkNotes').textContent = `Generated ${data.notes.length} Notes Successfully`;
            setTimeout(() => {
                document.getElementById('generateBulkNotes').textContent = 'Generate Notes';
                document.getElementById('generateBulkNotes').disabled = false;
            }, 3000);

        } catch (error) {
            alert(`Error generating notes: ${error.message}`);
            document.getElementById('generateBulkNotes').textContent = 'Generate Notes';
            document.getElementById('generateBulkNotes').disabled = false;
        }
    }

    updateNoteSelector(numNotes) {
        const selector = document.getElementById('noteSelector');
        selector.innerHTML = '';
        
        for (let i = 0; i < numNotes; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `Note ${i + 1}`;
            selector.appendChild(option);
        }
        
        selector.disabled = false;
    }

    displayNote(index) {
        const noteContent = document.getElementById('noteContent');
        const noteData = document.getElementById('noteData');
        const note = this.generatedNotes[index];
        
        if (!note) {
            noteContent.textContent = 'No note selected';
            noteData.textContent = '';
            return;
        }

        // Display note text
        noteContent.textContent = note.text;
        
        // Display note data
        noteData.textContent = JSON.stringify(note.data, null, 2);
    }
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const rangeManager = new RangeManager();
    rangeManager.initialize();
});