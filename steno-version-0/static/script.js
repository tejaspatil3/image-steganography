function hideMessage() {
    let fileInput = document.getElementById('fileInput').files[0];
    let message = document.getElementById('message').value;
    let outputFileName = document.getElementById('outputFileName').value || "hidden_image";

    let formData = new FormData();
    formData.append("file", fileInput);
    formData.append("message", message);

    fetch("/stego/hide/image", { method: "POST", body: formData })
        .then(response => response.blob())
        .then(blob => {
            let link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = outputFileName + ".png";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => console.error("Error:", error));
}

function extractMessage() {
    let fileInput = document.getElementById('fileInput').files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("/stego/extract/image", { method: "POST", body: formData })
        .then(response => response.text())
        .then(text => {
            document.getElementById('outputMessage').innerText = "Hidden Message: " + text;
        })
        .catch(error => console.error("Error:", error));
}
