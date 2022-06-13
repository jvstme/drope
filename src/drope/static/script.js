const body = document.querySelector("body");
const dropArea = document.getElementById("drop-area");
const filesArea = document.getElementById("files-area");
const activeUploadsSec = document.getElementById("active-uploads-section");
const activeFilesList = document.getElementById("active-uploads-file-list");
const finishedUploadsSec = document.getElementById("finished-uploads-section");
const finishedFilesList = document.getElementById("finished-uploads-file-list");
const fileInputField = document.getElementById("file-input-field");
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
    activeFilesList.insertBefore(container, activeFilesList.firstChild);
    activeUploadsSec.classList.remove("nodisplay");
    filesArea.classList.remove("nodisplay");
    
    const progressValueNode = container.querySelector(".progress-value");

    uploadFile(
        file,
        function(e) { uploadProgressed(e, container, progressValueNode); },
        function(e) { uploadReadyStateChanged(e, container); },
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

function uploadProgressed(evt, fileContainer, progressValueNode) {
    const progress = evt.loaded / evt.total * 100;
    setProgressBar(fileContainer, progress);
    progressValueNode.textContent = progress.toFixed(1);
}

function uploadReadyStateChanged(evt, fileContainer) {
    const xhr = evt.target;

    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
            uploadSuccessful(fileContainer);
        } else {
            uploadFailed(fileContainer);
        }
    }
}

function uploadSuccessful(fileCont) {
    fileCont.querySelector(".progress-indicator").classList.add("nodisplay");
    fileCont.querySelector(".success-indicator").classList.remove("nodisplay");
    moveToFinished(fileCont);
}

function uploadFailed(fileCont) {
    fileCont.querySelector(".progress-indicator").classList.add("nodisplay");
    fileCont.querySelector(".error-indicator").classList.remove("nodisplay");
    moveToFinished(fileCont);
}

function moveToFinished(fileContainer) {
    fileContainer.parentElement.removeChild(fileContainer);
    setProgressBar(fileContainer, 0);
    finishedFilesList.insertBefore(fileContainer, finishedFilesList.firstChild);
    finishedUploadsSec.classList.remove("nodisplay");

    if (activeFilesList.children.length === 0) {
        activeUploadsSec.classList.add("nodisplay");
    }
}

function setProgressBar(element, progress) {
    element.style.setProperty("--progress", progress + "%");
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
