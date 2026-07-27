console.log("script.js loaded");

let selectedFile = null;
const API_BASE = "http://127.0.0.1:8000";

const pdfFile = document.getElementById("pdfFile");
const selectedFileText = document.getElementById("selectedFile");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");
const currentDocument = document.getElementById("currentDocument");
const documentList = document.getElementById("documentList");

console.log("uploadBtn element found?", uploadBtn);

pdfFile.addEventListener("change", () => {
    console.log("STEP A: file input changed");
    if (pdfFile.files.length > 0) {
        selectedFile = pdfFile.files[0];
        selectedFileText.innerHTML = selectedFile.name;
        console.log("STEP B: file selected ->", selectedFile.name);
    }
});

uploadBtn.addEventListener("click", async () => {
    console.log("STEP 1: upload button clicked");

    if (!selectedFile) {
        console.log("STEP 2: no file selected, stopping here");
        uploadStatus.innerHTML = "⚠️ No file selected";
        return;
    }

    console.log("STEP 3: file exists, proceeding to upload:", selectedFile.name);

    uploadStatus.innerHTML = "Uploading...";
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        console.log("STEP 4: sending fetch request");
        const response = await fetch(`${API_BASE}/upload/`, {
            method: "POST",
            body: formData
        });
        console.log("STEP 5: got response, status =", response.status);

        const data = await response.json();
        console.log("STEP 6: parsed data =", data);

        uploadStatus.innerHTML = "✅ Uploaded Successfully";
        currentDocument.innerText = data.filename;

        const li = document.createElement("li");
        li.innerHTML = data.filename;
        documentList.appendChild(li);

        console.log("STEP 7: UI updated successfully");

    } catch (err) {
        console.log("STEP ERROR:", err);
        uploadStatus.innerHTML = "❌ Upload Failed: " + err.message;
    }
});
// =========================
// Chat with PDF
// =========================

const askBtn = document.getElementById("askBtn");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chatBox");

askBtn.addEventListener("click", async () => {

    console.log("STEP CHAT 1: Send button clicked");

    const question = questionInput.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    const documentId = currentDocument.innerText.trim();

    if (!documentId || documentId === "None") {
        alert("Please upload or process a document first.");
        return;
    }

    console.log("Question:", question);
    console.log("Document:", documentId);

    try {

        const response = await fetch(`${API_BASE}/chat/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                document_id: documentId,
                question: question
            })
        });

        console.log("Chat Status:", response.status);

        const data = await response.json();

        console.log(data);

        chatBox.innerHTML += `
            <div><b>You:</b> ${question}</div>
            <div><b>AI:</b> ${data.answer}</div>
            <hr>
        `;

        questionInput.value = "";

    } catch (err) {

        console.error(err);

        alert("Chat Error: " + err.message);

    }

});

// =========================
// Upload PDF from URL
// =========================

const pdfUrlInput = document.getElementById("pdfUrl");
const downloadPdfBtn = document.getElementById("downloadPdfBtn");

downloadPdfBtn.addEventListener("click", async () => {

    const url = pdfUrlInput.value.trim();

    if (!url) {
        alert("Please enter a PDF URL.");
        return;
    }

    uploadStatus.innerHTML = "Downloading PDF...";

    try {

        const response = await fetch(`${API_BASE}/upload/url`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Download failed");
        }

        uploadStatus.innerHTML = "✅ PDF Downloaded Successfully";

        currentDocument.innerText = data.filename;

        const li = document.createElement("li");
        li.innerHTML = data.filename;
        documentList.appendChild(li);

        pdfUrlInput.value = "";

        alert("PDF downloaded successfully!");

    } catch (err) {

        console.error(err);

        uploadStatus.innerHTML = "❌ Download Failed";

        alert(err.message);

    }

});

// =========================
// Process YouTube Video
// =========================

const youtubeBtn = document.getElementById("youtubeBtn");
const youtubeUrl = document.getElementById("youtubeUrl");

youtubeBtn.addEventListener("click", async () => {

    const url = youtubeUrl.value.trim();

    if (!url) {
        alert("Please enter a YouTube URL.");
        return;
    }

    uploadStatus.innerHTML = "🎥 Fetching transcript...";

    try {

        const response = await fetch(`${API_BASE}/youtube/upload`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to process YouTube video.");
        }

        uploadStatus.innerHTML = "✅ YouTube video indexed successfully";

        currentDocument.innerText = data.document_id;

        const li = document.createElement("li");
        li.innerHTML = `🎥 ${data.document_id}`;

        documentList.appendChild(li);

        youtubeUrl.value = "";

        alert("YouTube video indexed successfully!");

    } catch (err) {

        console.error(err);

        uploadStatus.innerHTML = "❌ Failed to process YouTube video";

        alert(err.message);

    }

});

// =========================
// Paste Text
// =========================

const pasteText = document.getElementById("pasteText");
const submitTextBtn = document.getElementById("submitTextBtn");

submitTextBtn.addEventListener("click", async () => {

    const text = pasteText.value.trim();

    if (!text) {
        alert("Please paste some text.");
        return;
    }

    uploadStatus.innerHTML = "Processing text...";

    try {

        const response = await fetch(`${API_BASE}/text/process`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to process text.");
        }

        uploadStatus.innerHTML = "✅ Text processed successfully";

        currentDocument.innerText = data.document_id;

        const li = document.createElement("li");
        li.innerHTML = `📝 ${data.document_id}`;
        documentList.appendChild(li);

        pasteText.value = "";

        alert("Text processed successfully!");

    } catch (err) {

        console.error(err);

        uploadStatus.innerHTML = "❌ Failed to process text";

        alert(err.message);

    }

});