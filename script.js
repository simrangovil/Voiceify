function speakText() {
  const text = document.getElementById("text-input").value;
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}

document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const fileInput = document.getElementById("doc-file");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("/upload", {
    method: "POST",
    body: formData
  })
    .then(res => res.blob())
    .then(blob => {
      const audio = document.getElementById("audio");
      audio.src = URL.createObjectURL(blob);
      audio.hidden = false;
      audio.play();
    })
    .catch(err => console.error("Error:", err));
});
