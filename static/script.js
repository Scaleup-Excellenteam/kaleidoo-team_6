// Validate if files are uploaded before form submission
function validateUpload() {
    var filesInput = document.getElementById('files');

    if (!filesInput.files.length) {
        // If no file is selected, add invalid class and prevent form submission
        filesInput.classList.add('invalid');
        alert('Please upload at least one file.');
        return false;
    }

    // If the file input is not empty, remove any previous 'invalid' class
    filesInput.classList.remove('invalid');
    return true;
}

// Function to copy text to the clipboard
function copyToClipboard(text) {
    // Create a temporary text area element to hold the text to copy
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = text;
    document.body.appendChild(tempTextArea);

    // Select the text
    tempTextArea.select();
    tempTextArea.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text to the clipboard
    document.execCommand('copy');

    // Remove the temporary text area from the DOM
    document.body.removeChild(tempTextArea);

    // Optionally, you can give some feedback to the user
    alert("Copied: " + text);
}

// Process file upload and show progress
function processFiles(event) {
    event.preventDefault();

    // Validate files before proceeding
    if (!validateUpload()) {
        return;
    }

    // Show processing message
    document.getElementById('processing-message').style.display = 'block';

    var formData = new FormData(document.getElementById('uploadForm'));

    // Send files via Fetch API
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('processing-message').style.display = 'none';
        // Reset the form after successful upload
        document.getElementById('uploadForm').reset();
    })
    .catch(error => {
        console.error('Error uploading files:', error);
        alert('Failed to upload files.');
        document.getElementById('processing-message').style.display = 'none';
    });
}

// Handle question submissions and display answer
function submitQuestion(event) {
    event.preventDefault();  // Prevent form from submitting normally

    let question = document.getElementById('question').value;

    // Send question to Flask server via Fetch API
    fetch('/submit_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        // Update the answer section with the returned answer
        document.getElementById('answer').textContent = `Q: ${data.question} - A: ${data.answer}`;
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    const questionForm = document.getElementById('question-form');
    const chatBox = document.getElementById('chat-box');

    questionForm.addEventListener('submit', submitQuestion);

    function submitQuestion(event) {
        event.preventDefault(); // Prevent the form from submitting traditionally

        const questionInput = document.getElementById('question');
        const question = questionInput.value;

        if (question) {
            fetch('/submit_question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Update the chat box with the new question and answer
                    const userMessage = `
                        <div class="chat-message user-message">
                            <strong>You:</strong> ${data.question}
                            <button class="copy-btn" onclick="copyToClipboard('${data.question}')">Copy</button>
                        </div>`;
                    const botMessage = `
                        <div class="chat-message bot-message">
                            <strong>StudyBuddy:</strong> ${data.answer}
                            <button class="copy-btn" onclick="copyToClipboard('${data.answer}')">Copy</button>
                        </div>`;

                    chatBox.innerHTML += userMessage + botMessage;
                    questionInput.value = ''; // Clear the input field
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
});