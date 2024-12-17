let mediaRecorder;
let audioChunks = [];

// Función para iniciar la grabación
document.getElementById("start").addEventListener("click", async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            if (audioChunks.length === 0) {
                alert("No se grabó audio. Inténtalo de nuevo.");
                updateStatus("No se grabó audio.", "error");
                return;
            }

            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            const formData = new FormData();
            formData.append("audio", audioBlob, "recording.webm");

            uploadAudio(formData, "/upload-recording", "status");
        };

        mediaRecorder.start();
        updateStatus("Grabando...", "recording");
        toggleRecordingButtons(true);
    } catch (err) {
        console.error("Error al acceder al micrófono:", err);
        alert("Permisos del micrófono denegados. Habilítalos en tu navegador.");
    }
});

// Función para detener la grabación
document.getElementById("stop").addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        updateStatus("Procesando grabación...", "processing");
        toggleRecordingButtons(false);
    } else {
        alert("No hay una grabación activa para detener.");
    }
});

// Función para manejar la subida de un archivo MP3, WAV, M4A o FLAC
document.getElementById("uploadForm").addEventListener("submit", (event) => {
    event.preventDefault();

    const fileInput = document.getElementById("audioFile");
    const file = fileInput.files[0];

    if (!file) {
        updateStatus("Por favor, selecciona un archivo.", "error");
        return;
    }

    if (!isValidAudioFile(file)) {
        updateStatus("Formato no soportado. Usa MP3, WAV, M4A o FLAC.", "error");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    updateStatus("Subiendo archivo... Por favor espera.", "uploading");
    uploadAudio(formData, "/upload-file", "fileStatus");
});

// Función unificada para subir audio al servidor
async function uploadAudio(formData, url, statusElementId) {
    const statusElement = document.getElementById(statusElementId);

    try {
        updateStatus("Enviando datos al servidor...", "processing");
        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            statusElement.textContent = "Transcripción completada!";
            statusElement.className = "status completed"; // Agregar la clase 'completed'
            document.getElementById("transcription").textContent = data.text || "Sin texto disponible.";
        } else {
            const errorData = await response.text();
            statusElement.textContent = `Error: ${errorData}`;
            statusElement.className = "status error"; // Clase 'error' en caso de fallo
            console.error("Error del servidor:", errorData);
        }
    } catch (error) {
        statusElement.textContent = "Error en la conexión al servidor.";
        console.error("Error en fetch:", error);
    }
}

// Función para validar el formato del archivo
function isValidAudioFile(file) {
    const allowedExtensions = ["mp3", "wav", "m4a", "flac"];
    const fileExtension = file.name.split(".").pop().toLowerCase();
    return allowedExtensions.includes(fileExtension);
}

// Actualizar el estado del sistema
function updateStatus(message, className) {
    const statusElement = document.getElementById("status");
    statusElement.textContent = message;
    statusElement.className = `status ${className}`;
}

// Activar o desactivar botones de grabación
function toggleButton(buttonId, isDisabled) {
    document.getElementById(buttonId).disabled = isDisabled;
}

function toggleRecordingButtons(isRecording) {
    toggleButton("start", isRecording);
    toggleButton("stop", !isRecording);
}

// Mostrar el nombre del archivo seleccionado
const fileInput = document.getElementById("audioFile");
const fileNameDisplay = document.getElementById("fileName");

fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
        fileNameDisplay.textContent = "Ningún archivo seleccionado";
    }
});

document.getElementById("copyButton").addEventListener("click", function () {
    const transcriptionText = document.getElementById("transcription").innerText;

    if (transcriptionText.trim() === "") {
        alert("No hay texto para copiar.");
        return;
    }

    navigator.clipboard.writeText(transcriptionText).then(() => {
        alert("Texto copiado al portapapeles.");
    }).catch(err => {
        console.error("Error al copiar el texto: ", err);
    });
});