class RangeManager {
    constructor() {
        this.ranges = {};
        this.generatedNotes = [];
        this.setupEventListeners();
    }

    async initialize() {
        // Fetch preset ranges from server
        const response = await fetch('/get_ranges');
        const data = await response.json();
        this.ranges = data;
        this.setupRangeSelectors();
    }

    setupEventListeners() {
        // Generate notes button
        document.getElementById('generateBulkNotes').addEventListener('click', () => this.generateNotes());

        // Note selector
        document.getElementById('noteSelector').addEventListener('change', (e) => {
            this.displayNote(parseInt(e.target.value));
        });
    }

    setupRangeSelectors() {
        // Setup each range selector based on the fetched ranges
        Object.keys(this.ranges).forEach(field => {
            const container = document.getElementById(`${field}Section`);
            if (!container) return;

            const rangeGroup = this.createRangeGroup(field);
            container.appendChild(rangeGroup);
        });
    }

    createRangeGroup(field) {
        const group = document.createElement('div');
        group.className = 'range-group';

        const label = document.createElement('label');
        label.textContent = this.formatFieldName(field);
        group.appendChild(label);

        const selection = document.createElement('div');
        selection.className = 'range-selection';

        // Create preset selector
        const preset = document.createElement('select');
        preset.className = 'range-preset';
        preset.id = `${field}Preset`;

        // Add custom option
        const customOption = document.createElement('option');
        customOption.value = 'custom';
        customOption.textContent = 'Custom Range';
        preset.appendChild(customOption);

        // Add preset options
        this.ranges[field].forEach(({label, range}) => {
            const option = document.createElement('option');
            option.value = range.join('-');
            option.textContent = `${label} (${range[0]}-${range[1]})`;
            preset.appendChild(option);
        });

        // Create custom range inputs
        const customRange = document.createElement('div');
        customRange.className = 'custom-range';
        customRange.id = `${field}CustomRange`;

        const minInput = document.createElement('input');
        minInput.type = 'number';
        minInput.id = `${field}Min`;
        minInput.placeholder = 'Min';

        const maxInput = document.createElement('input');
        maxInput.type = 'number';
        maxInput.id = `${field}Max`;
        maxInput.placeholder = 'Max';

        const separator = document.createElement('span');
        separator.textContent = 'to';

        customRange.appendChild(minInput);
        customRange.appendChild(separator);
        customRange.appendChild(maxInput);

        // Add event listeners
        preset.addEventListener('change', () => {
            if (preset.value === 'custom') {
                customRange.style.display = 'flex';
            } else {
                customRange.style.display = 'none';
                const [min, max] = preset.value.split('-');
                minInput.value = min;
                maxInput.value = max;
            }
        });

        selection.appendChild(preset);
        selection.appendChild(customRange);
        group.appendChild(selection);

        return group;
    }

    formatFieldName(field) {
        return field
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    getSelectedRanges() {
        const ranges = {};
        Object.keys(this.ranges).forEach(field => {
            const preset = document.getElementById(`${field}Preset`);
            if (!preset) return;

            if (preset.value === 'custom') {
                const min = document.getElementById(`${field}Min`).value;
                const max = document.getElementById(`${field}Max`).value;
                if (min && max) {
                    ranges[field] = [parseFloat(min), parseFloat(max)];
                }
            } else {
                const [min, max] = preset.value.split('-');
                ranges[field] = [parseFloat(min), parseFloat(max)];
            }
        });
        return ranges;
    }

    async generateNotes() {
        const numNotes = document.getElementById('numberOfNotes').value;
        const ranges = this.getSelectedRanges();

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
                return;
            }

            this.generatedNotes = data.notes;
            this.updateNoteSelector(data.notes.length);
            this.displayNote(0);

        } catch (error) {
            alert(`Error generating notes: ${error.message}`);
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