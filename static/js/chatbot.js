// Open Chatbot Popup
function openChatbot() {
  document.getElementById("chatbot-popup").style.display = "block";
  document.getElementById("chatbot-icon").style.display = "none";
}

// Close Chatbot Popup
function closeChatbot() {
  document.getElementById("chatbot-popup").style.display = "none";
  document.getElementById("chatbot-icon").style.display = "block";
}

// Send Message
function sendMessage() {
  const userInput = document.getElementById("user-input").value.trim();
  const chatbotBody = document.getElementById("chatbot-body");

  if (userInput === "") {
      // If input is empty, display an error message
      chatbotBody.innerHTML += `<div class='chatbot-chat'><div>Please enter a valid question!</div></div>`;
      return;  // Stop the execution if input is empty
  }

  // Proceed with sending the valid input to the backend
  chatbotBody.innerHTML += `<div class='user-chat'><img class="user-icon-img" src="static/img/User-icon.png" alt="User Icon" style="width: 70px;"><div>${userInput}</div></div>`;
  document.getElementById("user-input").value = "";  // Clear input field

  // Scroll to the bottom of the chat window
  chatbotBody.scrollTop = chatbotBody.scrollHeight;

  // Make an AJAX request to the Flask server
  $.ajax({
      url: "/chat",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ message: userInput }),
      success: function(response) {
          setTimeout(() => {
              chatbotBody.innerHTML += `<div class='chatbot-chat'><img class="chatbot-icon-img" src="static/img/chatbot-icon.png" alt="Chatbot Icon" style="width: 70px;"><div>${response.message}</div></div>`;
              chatbotBody.scrollTop = chatbotBody.scrollHeight;  // Scroll down
          }, 1000);
      },
      error: function() {
          chatbotBody.innerHTML += `<div class='chatbot-chat'><div>Sorry, an error occurred. Please try again later.</div></div>`;
      }
  });
}

