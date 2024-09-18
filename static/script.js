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

function processFiles(event) {
    event.preventDefault();

    // Show processing message
    document.getElementById('processing-message').style.display = 'block';

    var formData = new FormData(document.getElementById('uploadForm'));

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