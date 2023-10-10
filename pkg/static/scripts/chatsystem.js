function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
  
    if (message !== '') {
      const chatBox = document.getElementById('chat-box');
      const messageElement = document.createElement('div');
      messageElement.classList.add('message');
      messageElement.textContent = `You: ${message}`;
      chatBox.appendChild(messageElement);
  
      // Clear the input after sending the message
      messageInput.value = '';
      messageInput.focus();
  
      // Optional: Scroll to the bottom of the chat box to always show the latest message
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }
  