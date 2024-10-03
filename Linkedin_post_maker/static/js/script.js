document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('post-form');
    const resultDiv = document.getElementById('result');
    const linkedinPostDiv = document.getElementById('linkedin-post');
    const imagePromptDiv = document.getElementById('image-prompt');
    const copyPostButton = document.getElementById('copy-post');
    const copyPromptButton = document.getElementById('copy-prompt');
    const shortPrompts = document.querySelectorAll('.short-prompt');
    const inputText = document.getElementById('input-text');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            linkedinPostDiv.innerHTML = data.linkedin_post;
            imagePromptDiv.innerHTML = data.image_prompt;
            resultDiv.classList.remove('hidden');
        })
        .catch(error => console.error('Error:', error));
    });

    copyPostButton.addEventListener('click', function() {
        copyToClipboard(linkedinPostDiv.innerText);
    });

    copyPromptButton.addEventListener('click', function() {
        copyToClipboard(imagePromptDiv.innerText);
    });

    shortPrompts.forEach(button => {
        button.addEventListener('click', function() {
            inputText.value = this.innerText;
        });
    });

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    }
});