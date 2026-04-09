const BASE_URL = "http://127.0.0.1:8000";

const fileInput = document.getElementById("fileInput");
const chatBox = document.getElementById("chatBox");
const status = document.getElementById("uploadStatus");

/* Upload files */
fileInput.addEventListener("change", async function () {

    const files = fileInput.files;

    for (let file of files) {

        status.innerText = "Uploading " + file.name;

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
});

/* Send question */
async function sendMessage() {

    const input = document.getElementById("userInput");
    const question = input.value.trim();

    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    try {
        const res = await fetch(`${BASE_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await res.json();

        addMessage(data.answer, "bot");

    } catch (err) {
        addMessage("Backend not reachable", "bot");
    }
}

/* UI message */
function addMessage(text, type) {

    const msg = document.createElement("div");
    msg.classList.add("message", type);
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* Enter key */
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

/* Clear chat */
function clearChat() {
    chatBox.innerHTML = "";
}

async function uploadParagraph() {

    const text = document.getElementById("paragraphInput").value.trim();

    if (!text) {
        alert("Enter paragraph first");
        return;
    }

    try {
        const res = await fetch(`${BASE_URL}/upload-text`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ paragraph: text })
        });

        const data = await res.json();

        alert(data.message);

        document.getElementById("paragraphInput").value = "";

    } catch (err) {
        alert("Upload failed");
    }
}