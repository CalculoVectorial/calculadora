const startButton = document.getElementById('startButton');
const cameraStream = document.getElementById('cameraStream');

// Function to start the camera stream
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraStream.srcObject = stream;
    } catch (error) {
        console.error('Error accessing the camera:', error);
    }
}

// Add event listener to the button
startButton.addEventListener('click', startCamera);
