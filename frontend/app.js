const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const fileInfo = document.getElementById("file-info");
const fileNameSpan = document.getElementById("file-name");
const analyzeBtn = document.getElementById("analyze-btn");
const loadingState = document.getElementById("loading-state");
const resultSection = document.getElementById("result-section");
const markdownResult = document.getElementById("markdown-result"); // Initial assistant message
const chatHistory = document.getElementById("chat-history");
const chatInputContainer = document.getElementById("chat-input-container");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

let selectedFile = null;
let currentSessionId = null;

// Allow clicking on drop zone to open file picker
dropZone.addEventListener("click", () => fileInput.click());

// Handle file selection
fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) handleFileSelect(e.target.files[0]);
});

// Drag and drop
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
        if (e.dataTransfer.files[0].type === "application/pdf") {
            handleFileSelect(e.dataTransfer.files[0]);
        } else {
            alert("Please upload a valid PDF file.");
        }
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    fileNameSpan.textContent = file.name;
    fileInfo.style.display = "inline-flex";
    analyzeBtn.disabled = false;
    resultSection.style.display = "none";
}

// Ensure links in parsed markdown open securely
function processLinks(container) {
    const links = container.querySelectorAll('a');
    links.forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
}

// Step 1: Analyze Resume
analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
    loadingState.style.display = "flex";
    resultSection.style.display = "none";
    dropZone.style.display = "none";
    chatHistory.innerHTML = '<div id="markdown-result" class="chat-message assistant-message markdown-body"></div>'; // reset

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze-resume", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        loadingState.style.display = "none";
        
        currentSessionId = data.session_id;

        const mdContainer = document.getElementById("markdown-result");
        if (data.result) {
            mdContainer.innerHTML = marked.parse(data.result);
            processLinks(mdContainer);
            resultSection.style.display = "block";
            chatInputContainer.style.display = "flex"; // Show chat interface!
        } else {
            mdContainer.innerHTML = "<p>Error: No result received.</p>";
            resultSection.style.display = "block";
        }
        
    } catch (error) {
        console.error("Error analyzing:", error);
        loadingState.style.display = "none";
        document.getElementById("markdown-result").innerHTML = `<p style="color: #ef4444;">Error processing: ${error.message}</p>`;
        resultSection.style.display = "block";
    } finally {
        analyzeBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze Another Resume';
        analyzeBtn.disabled = false;
        dropZone.style.display = "block";
        fileInfo.style.display = "none";
        selectedFile = null;
        fileInput.value = "";
    }
});

// Step 2: Multi-Turn Chatting
async function submitChat() {
    const text = chatInput.value.trim();
    if (!text || !currentSessionId) return;

    // Append human message
    const userBubble = document.createElement('div');
    userBubble.className = "chat-message user-message markdown-body";
    userBubble.innerHTML = marked.parse(text);
    chatHistory.appendChild(userBubble);
    
    chatInput.value = "";
    chatInput.disabled = true;
    sendBtn.disabled = true;
    
    // Auto-scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // Loading bubble
    const loadingBubble = document.createElement('div');
    loadingBubble.className = "chat-message assistant-message markdown-body";
    loadingBubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Thinking...';
    chatHistory.appendChild(loadingBubble);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                message: text
            })
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        
        loadingBubble.innerHTML = marked.parse(data.result || "No answer.");
        processLinks(loadingBubble);
        
    } catch (error) {
        loadingBubble.innerHTML = `<p style="color: #ef4444;">Error: ${error.message}</p>`;
    } finally {
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

sendBtn.addEventListener("click", submitChat);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") submitChat();
});
