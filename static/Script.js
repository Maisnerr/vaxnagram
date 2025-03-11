const currentIP = "https://9113-185-186-196-91.ngrok-free.app"
// local: http://192.168.1.138:5000
// ngrok: https://9113-185-186-196-91.ngrok-free.app

// Function to handle getting a random image post
function loadRandom() {
    fetch(currentIP+'/random-image')  // Use PC's IP address
        .then(response => response.json())
        .then(data => {
            if (data.file_url) {
                document.getElementById("titlepost").innerHTML = data.description;
                let imageElement = document.getElementById('resultpost');
                let imageSource = currentIP+`${data.file_url}`;
                imageElement.src = imageSource;
                document.getElementById("aResultpost").href = imageSource;
                imageElement.style.display = "block";
            } else {
                console.error('No image data received.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching random image.');
        });
}

// Function to handle uploading an image
function uploadImage() {
    const input = document.getElementById('third');
    const file = input.files[0];
    const title = document.getElementById("first").value;

    if (!file) {
        alert('Please select an image to upload.');
        return;
    }

    // Check if the file is an image
    if (!file.type.startsWith('image/')) {
        alert('Please upload a valid image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('title', title);

    fetch(currentIP+'/upload', {  // Use PC's IP address
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);

        if (data.file_url) {
            document.getElementById("title").innerHTML = data.description;
            let imageElement = document.getElementById('result');
            let imageSource = currentIP+`${data.file_url}`;
            document.getElementById('result').src = imageSource;
            document.getElementById("aResult").href = imageSource;
            imageElement.style.display = "block";  // Ensure image is visible
        } else {
            console.error('No file URL received.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading image.');
    });
}
