const dropArea = document.getElementById("drop-area");
const fileInputField = document.getElementById("file-input-field");
const uploadForm = document.getElementById("upload-form");
const loadingArea = document.getElementById("loading-area");
const messageArea = document.getElementById("message-area");
const uploadProgressIndicator = document.getElementById(
    "upload-progress-indicator",
);
const messageText = document.getElementById("message-text");
const messageCloseButton = document.getElementById("message-close-button");

let dragCounter = 0;
let activeArea = dropArea;

fileInputField.addEventListener("change", fileChosen);
dropArea.addEventListener("dragenter", dragEntered, false);
dropArea.addEventListener("dragleave", dragLeft, false);
dropArea.addEventListener("dragover", dragOver, false);
dropArea.addEventListener("drop", itemDropped, false);
messageCloseButton.addEventListener("click", messageCloseButtonClicked);


function activateArea(area) {
    activeArea.classList.add("nodisplay");
    activeArea = area;
    activeArea.classList.remove("nodisplay");
}

function displayMessage(text) {
    messageText.textContent = text;
    activateArea(messageArea);
}

function setUploadProgress(value) {
    uploadProgressIndicator.textContent = Number(value).toFixed(1);
}

function messageCloseButtonClicked() {
    activateArea(dropArea);
}


function fileChosen() {
    setUploadProgress(0);
    activateArea(loadingArea);
    submitForm();
}

function submitForm() {
    const data = new FormData(uploadForm);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", ".");

    xhr.upload.addEventListener("progress", uploadProgressed);
    xhr.addEventListener("readystatechange", uploadReadyStateChanged);

    xhr.send(data);
}

function uploadReadyStateChanged(e) {
    const xhr = e.target;

    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
            uploadSuccessful();
        } else {
            uploadFailed();
        }
    }
}

function filesNumberDescription() {
    const n = fileInputField.files.length;
    const noun = n === 1 ? "file" : "files";
    return n + " " + noun;
}

function uploadSuccessful() {
    displayMessage("Uploaded " + filesNumberDescription() + " :)");
}

function uploadFailed() {
    displayMessage("Upload failed :(");
}

function uploadProgressed(e) {
    const progress = e.loaded / e.total * 100;
    setUploadProgress(progress);
}

function updateDropAreaStatus() {
    if (dragCounter > 0) {
        dropArea.classList.add("drag-active");
    } else {
        dropArea.classList.remove("drag-active");
    }
}

function isFile(dtItem) {
    return dtItem.kind === "file" && dtItem.type;
}

function getFiles(dt) {
    const filteredDt = new DataTransfer();

    for (let i = 0; i < dt.items.length; i++) {
        if (isFile(dt.items[i])) {
            const file = dt.items[i].getAsFile();
            if (file !== null) {
                filteredDt.items.add(file);
            }
        }
    }

    return filteredDt.files;
}

function hasFiles(dt) {
    for (let i = 0; i < dt.items.length; i++) {
        if (isFile(dt.items[i])) {
            return true;
        }
    }

    return false;
}

function dragEntered(e) {
    if (hasFiles(e.dataTransfer)) {
        dragCounter++;
        updateDropAreaStatus();
    }
}

function dragLeft(e) {
    if (hasFiles(e.dataTransfer)) {
        dragCounter--;
        updateDropAreaStatus();
    }
}

function dragOver(e) {
    e.preventDefault();
}

function itemDropped(e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    
    if (hasFiles(e.dataTransfer)) {
        dragCounter = 0;
        updateDropAreaStatus();

        fileInputField.files = getFiles(e.dataTransfer);
        fileChosen();
    }
}