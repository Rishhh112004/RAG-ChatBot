const BASE_URL = "http://127.0.0.1:8000";

const fileInput = document.getElementById("fileInput");
const chatBox = document.getElementById("chatBox");
const status = document.getElementById("uploadStatus");

let currentSessionId = null;

/* ── File upload ── */
fileInput.addEventListener("change", async function () {
    const files = fileInput.files;
    for (let file of files) {
        status.innerText = "Uploading " + file.name + "...";
        const formData = new FormData();
        formData.append("file", file);
        try {
            const res = await fetch(`${BASE_URL}/upload-file`, {
                method: "POST",
                body: formData
            });
            const data = await res.json();
            status.innerText = data.message;
        } catch (err) {
            status.innerText = "Upload failed";
        }
    }
    fileInput.value = "";      // Reset so the same file can be re-uploaded if needed
});

/* ── Send question ── */
async function sendMessage() {
    const input = document.getElementById("userInput");
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    const loadingId = addLoadingMessage();     // Show a loading indicator while waiting for the (slow) LLM

    try {
        const res = await fetch(`${BASE_URL}/ask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, session_id: currentSessionId })
        });
        const data = await res.json();
        currentSessionId = data.session_id;

        removeLoadingMessage(loadingId);
        addMessage(data.answer, "bot");

        loadSessions();        // Refresh session list so new chat appears with its title

    } catch (err) {
        removeLoadingMessage(loadingId);
        addMessage("Backend not reachable. Is the server running?", "bot");
    }
}

/* ── Add a chat bubble ── */
function addMessage(text, type) {
    const msg = document.createElement("div");
    msg.classList.add("message", type);
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}

/* ── Loading indicator ── */
function addLoadingMessage() {
    const id = "loading-" + Date.now();
    const msg = document.createElement("div");
    msg.classList.add("message", "bot", "loading");
    msg.id = id;
    msg.innerText = "Fetching Answer...";
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeLoadingMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

/* ── Enter key to send ── */
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

/* ── Clear visible chat (keeps session) ── */
function clearChat() {
    chatBox.innerHTML = "";
}

/* ── Start a new session ── */
function newChat() {
    currentSessionId = null;
    chatBox.innerHTML = "";
}

/* ── Upload paragraph text ── */
async function uploadParagraph() {
    const text = document.getElementById("paragraphInput").value.trim();
    if (!text) {
        alert("Enter a paragraph first");
        return;
    }
    status.innerText = "Uploading paragraph...";
    try {
        const res = await fetch(`${BASE_URL}/upload-text`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ paragraph: text })
        });
        const data = await res.json();
        status.innerText = data.message;
        document.getElementById("paragraphInput").value = "";
    } catch (err) {
        status.innerText = "Upload failed";
    }
}

/* ── Load session list (shows titles) ── */
function addLoadingMessage() {
    const id = "loading-" + Date.now();
    const msg = document.createElement("div");
    msg.classList.add("message", "bot", "loading");
    msg.id = id;
    msg.innerText = "Thinking...";
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}
 
function removeLoadingMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
 
/* ── Enter key to send ── */
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});
 
/* ── Clear visible chat (keeps session) ── */
function clearChat() {
    chatBox.innerHTML = "";
}
 
/* ── Start a new session ── */
function newChat() {
    currentSessionId = null;
    chatBox.innerHTML = "";
}
 
/* ── Upload paragraph text ── */
async function uploadParagraph() {
    const text = document.getElementById("paragraphInput").value.trim();
    if (!text) {
        alert("Enter a paragraph first");
        return;
    }
    status.innerText = "Uploading paragraph...";
    try {
        const res = await fetch(`${BASE_URL}/upload-text`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ paragraph: text })
        });
        const data = await res.json();
        status.innerText = data.message;
        document.getElementById("paragraphInput").value = "";
    } catch (err) {
        status.innerText = "Upload failed";
    }
}
 
/* ── Load session list ── */
async function loadSessions() {
    try {
        const res = await fetch(`${BASE_URL}/sessions`);
        const data = await res.json();
 
        const list = document.getElementById("sessionList");
        list.innerHTML = "";
 
        data.forEach(s => {
            // Wrapper row: title + delete button side by side
            const row = document.createElement("div");
            row.classList.add("session-row");
 
            // Title area — click to load chat
            const item = document.createElement("div");
            item.classList.add("session-item");
            item.innerText = s.title || s.id;
            if (s.id === currentSessionId) {
                item.classList.add("active-session");
            }
            item.onclick = () => loadChat(s.id);
 
            // Delete button — click to delete this session
            const del = document.createElement("button");
            del.classList.add("delete-btn");
            del.innerText = "✕";
            del.title = "Delete this chat";
            del.onclick = (e) => {
                e.stopPropagation(); // don't trigger loadChat
                deleteSession(s.id);
            };
 
            row.appendChild(item);
            row.appendChild(del);
            list.appendChild(row);
        });
    } catch (err) {
        console.error("Could not load sessions:", err);
    }
}
 
/* ── Delete a session ── */
async function deleteSession(sessionId) {
    if (!confirm("Delete this chat? This cannot be undone.")) return;
 
    try {
        await fetch(`${BASE_URL}/chat/${sessionId}`, { method: "DELETE" });
 
        // If the deleted session was open, clear the chat area
        if (sessionId === currentSessionId) {
            currentSessionId = null;
            chatBox.innerHTML = "";
        }
 
        loadSessions(); // refresh list
    } catch (err) {
        alert("Could not delete chat.");
    }
}

/* ── Load a past chat ── */
async function loadChat(sessionId) {
    currentSessionId = sessionId;

    const res = await fetch(`${BASE_URL}/chat/${sessionId}`);
    const data = await res.json();

    chatBox.innerHTML = "";
    data.forEach(m => {
        addMessage(m.question, "user");
        addMessage(m.answer, "bot");
    });

    // Highlight active session
    loadSessions();
}

// Load sessions on page open
loadSessions();
