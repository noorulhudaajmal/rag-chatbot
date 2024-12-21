function toggleChat() {
    const chatBox = document.getElementById('chatBox');
    chatBox.classList.toggle('active');
    addMessage('bot', 'Hello, How can I help you today?');
}

const API_URL = 'http://localhost:8000/chat';
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const showContext = document.getElementById('show-context');

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage('user', message);
    userInput.value = '';

    try {
        const loadingId = addMessage('bot', 'Typing...');
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();
        document.getElementById(loadingId).remove();
        addMessage('bot', data.response);

    } catch (error) {
        console.error('Error:', error);
        addMessage('bot', 'Sorry, something went wrong. Please try again.');
    }
}

function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    const id = `msg-${Date.now()}`;
    messageDiv.id = id;
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});