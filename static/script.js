
async function generateImage() {

    const prompt = document.getElementById("prompt").value.trim();

    const button = document.getElementById("generateBtn");
    const status = document.getElementById("status");
    const result = document.getElementById("result");

    if (!prompt) {
        status.textContent = "Please enter an image description.";
        return;
    }

    button.disabled = true;
    button.textContent = "Generating...";
    status.textContent = "AI is creating your image. Please wait...";
    result.style.display = "none";

    try {

        const response = await fetch("/generate", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                prompt: prompt
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        const image = document.getElementById("generatedImage");
        const download = document.getElementById("downloadBtn");

        image.src = data.image_url;
        download.href = data.image_url;

        result.style.display = "block";
        status.textContent = data.message;

    } catch (error) {

        status.textContent = "Error: " + error.message;

    } finally {

        button.disabled = false;
        button.textContent = "Generate Image";
    }
}
