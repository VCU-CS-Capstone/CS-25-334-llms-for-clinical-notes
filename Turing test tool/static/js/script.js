let currentQuestion = 0;
let correctAnswers = 0;
const totalQuestions = 5;
let responses = [];

async function generateSection() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('generate-button').style.display = 'none';
    document.getElementById('next-button').style.display = 'none';

    try {
        const response = await fetch('/generate-section');
        if (!response.ok) throw new Error(`Error: ${response.status}, ${response.statusText}`);

        const data = await response.json();
        const formattedContent = data.section.replace(/\n/g, '<br>');

        document.getElementById('generated-section').innerHTML = `
            <div id="section-label"><strong>${data.label}:</strong></div>
            <div id="section-content">${formattedContent}</div>`;

        document.getElementById('next-button').style.display = 'block';
        document.getElementById('next-button').dataset.actualType = data.actual_type;

    } catch (error) {
        document.getElementById('generated-section').innerText = 'Error: ' + error.message;
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

async function submitResponse() {
    const noteType = document.querySelector('input[name="note-type"]:checked')?.value;
    const reasoning = document.getElementById('reason-input').value;
    const actualType = document.getElementById('next-button').dataset.actualType;

    if (!noteType || !reasoning.trim()) {
        alert('Please select a note type and provide your reasoning.');
        return;
    }

    const isCorrect = noteType === actualType;
    if (isCorrect) correctAnswers++;

    responses.push({ question: currentQuestion + 1, guessed: noteType, actual: actualType, reasoning });

    try {
        const backendResponse = await fetch('/submit-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ noteType, reasoning, actualNoteType: actualType })
        });

        const result = await backendResponse.json();
        if (!backendResponse.ok) alert(`Failed to save response: ${result.message}`);
    } catch (error) {
        console.error('Error submitting response:', error);
        alert('Error saving response to the server.');
    }

    currentQuestion++;

    if (currentQuestion < totalQuestions) {
        document.querySelectorAll('input[name="note-type"]').forEach(input => input.checked = false);
        document.getElementById('reason-input').value = '';
        generateSection();
    } else {
        showResults();
    }
}

function showResults() {
    let resultsHTML = `<h2>Quiz Completed!</h2>`;
    resultsHTML += `<p>You got <strong>${correctAnswers}/${totalQuestions}</strong> correct.</p>`;
    resultsHTML += `<h3>Review Your Answers:</h3><ul>`;

    responses.forEach(response => {
        resultsHTML += `<li>Question ${response.question}: You guessed <strong>${response.guessed}</strong>, Actual: <strong>${response.actual}</strong>. <br>Reasoning: ${response.reasoning}</li>`;
    });

    resultsHTML += `</ul>`;

    document.getElementById('results').innerHTML = resultsHTML;
    document.getElementById('results').style.display = 'block';
    document.querySelector('.controls').style.display = 'none';
}

document.getElementById('generate-button').addEventListener('click', generateSection);
document.getElementById('next-button').addEventListener('click', submitResponse);
