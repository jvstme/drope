const body = document.querySelector("body");
const dropArea = document.getElementById("drop-area");
const filesArea = document.getElementById("files-area");
const filesList = document.getElementById("files-list");
const fileInputField = document.getElementById("file-input-field");
const fileChoiceForm = document.getElementById("file-choice-form");
const templates = document.getElementById("templates");
const fileContainerTemplate = templates.querySelector(".file-container");

let dragCounter = 0;

fileInputField.addEventListener("change", fileChosen, false);
dropArea.addEventListener("dragenter", dragEntered, false);
dropArea.addEventListener("dragleave", dragLeft, false);
dropArea.addEventListener("dragover", ignoreEvent, false);
dropArea.addEventListener("drop", itemDropped, false);
body.addEventListener("dragover", ignoreEvent, false);
body.addEventListener("drop", ignoreEvent, false);

function ignoreEvent(e) {
    e.preventDefault();
}

function fileChosen() {
    doFilesUpload(fileInputField.files);
}

function doFilesUpload(files) {
    for (let i = 0; i < files.length; i++) {
        doFileUpload(files[i]);
    }
}

function doFileUpload(file) {
    const container = fileContainerTemplate.cloneNode(true);
    container.querySelector(".file-name").innerText = file.name;
    filesList.insertBefore(container, filesList.firstChild);
    filesArea.classList.remove("nodisplay");
    
    const statusIndicator = container.querySelector(".status-indicator");
    const progressValueNode = container.querySelector(".progress-value");

    uploadFile(
        file,
        function(e) { uploadProgressed(e, progressValueNode); },
        function(e) { uploadReadyStateChanged(e, statusIndicator); },
    );
}

function uploadFile(file, progressListener, readyStateChangeListener) {
    const data = new FormData();
    data.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", ".");

    xhr.upload.addEventListener("progress", progressListener, false);
    xhr.addEventListener("readystatechange", readyStateChangeListener, false);

    xhr.send(data);
}

function uploadReadyStateChanged(evt, statusIndicator) {
    const xhr = evt.target;

    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
            uploadSuccessFul(statusIndicator);
        } else {
            uploadFailed(statusIndicator);
        }
    }
}

function uploadSuccessFul(indicator) {
    indicator.querySelector(".progress-indicator").classList.add("nodisplay");
    indicator.querySelector(".success-indicator").classList.remove("nodisplay");
}

function uploadFailed(indicator) {
    indicator.querySelector(".progress-indicator").classList.add("nodisplay");
    indicator.querySelector(".error-indicator").classList.remove("nodisplay");
}

function uploadProgressed(evt, progressValueNode) {
    const progress = evt.loaded / evt.total * 100;
    progressValueNode.textContent = progress.toFixed(1);
}

function updateDropAreaStatus() {
    if (dragCounter > 0) {
        dropArea.classList.add("drag-active");
    } else {
        dropArea.classList.remove("drag-active");
    }
}

function handleDtItem(dtItem) {
    if (dtItem.webkitGetAsEntry !== undefined) {
        const entry = dtItem.webkitGetAsEntry();
        if (entry && entry.isFile) {
            entry.file(doFileUpload);
        }
    } else if (dtItem.kind === "file") {
        const file = dtItem.getAsFile();
        if (file !== null) {
            doFileUpload(file);
        }
    }
}

function handleDt(dt) {
    for (let i = 0; i < dt.items.length; i++) {
        handleDtItem(dt.items[i]);
    }
}

function dragEntered(e) {
    dragCounter++;
    updateDropAreaStatus();
}

function dragLeft(e) {
    dragCounter--;
    updateDropAreaStatus();
}

function itemDropped(e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    
    dragCounter = 0;
    updateDropAreaStatus();

    handleDt(e.dataTransfer);
}
