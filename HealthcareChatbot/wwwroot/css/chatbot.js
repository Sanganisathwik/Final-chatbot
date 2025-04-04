window.backendUrl = "http://127.0.0.1:8000"; // Ensure your backend URL is correct

// Function to scroll chat window to bottom
window.scrollToBottom = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollTop = element.scrollHeight;
    }
};

// Function to load sample queries from the API
async function loadSampleQueries() {
    try {
        const response = await fetch(`${window.backendUrl}/generate-sample-queries`, {
            method: "POST", // Changed to POST as requested
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({}) // Sending an empty JSON body for POST request
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const queriesContainer = document.getElementById("sample-queries");

        if (queriesContainer) {
            queriesContainer.innerHTML = ""; // Clear previous entries
            data.sample_queries.forEach(query => {
                let button = document.createElement("button");
                button.textContent = query;
                button.className = "query-btn btn btn-outline-primary m-1";
                button.onclick = () => sendMessage(query);
                queriesContainer.appendChild(button);
            });
        }
    } catch (error) {
        console.error("Error loading sample queries:", error);
    }
}

// Function to send a message
async function sendMessage(message) {
    const userInput = document.getElementById("user-input");
    const text = message || userInput.value.trim();

    if (!text) return; // Prevent sending empty messages

    appendMessage("user", text);
    userInput.value = ""; // Clear input field

    try {
        const response = await fetch(`${window.backendUrl}/generate-response`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: text }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        appendMessage("bot", data.output || "No response received.");
    } catch (error) {
        console.error("Error fetching response:", error);
        appendMessage("bot", "Error fetching response. Please try again later.");
    }

    window.scrollToBottom("chat-box");
}

// Function to append messages to the chatbox
function appendMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    
    messageDiv.className = sender === "user" ? "user-message text-end p-2" : "bot-message text-start p-2";
    messageDiv.innerHTML = `<span>${text}</span>`;

    chatBox.appendChild(messageDiv);
    window.scrollToBottom("chat-box");
}

// Load sample queries when the document is ready
document.addEventListener("DOMContentLoaded", loadSampleQueries);
