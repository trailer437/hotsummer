// JavaScript code for handling file upload and sending it to the server
function handleFileUpload() {
    var fileInput = document.getElementById('imageUpload');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);
    
    // Disable the detect button during processing
    var detectBtn = document.getElementById('detectBtn');
    detectBtn.disabled = true;
  
    // Show the loading message
    var resultText = document.getElementById('resultText');
    resultText.innerText = 'Detecting...';
    
    // Send the file to the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/detect', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var result = JSON.parse(xhr.responseText);
        displayResult(result);
      } else {
        console.log('Error:', xhr.status);
      }
  
      // Enable the detect button after processing
      detectBtn.disabled = false;
    };
    xhr.send(formData);
  }
  
  // JavaScript code to display the prediction result
  function displayResult(result) {
    var resultDiv = document.getElementById('result');
    var resultText = document.getElementById('resultText');
    
    if (result.success) {
      resultText.innerText = result.label;
    } else {
      resultText.innerText = 'Error: ' + result.message;
    }
    
    resultDiv.style.display = 'block';
  }
  
  // JavaScript code to enable the detect button when an image is selected
  document.getElementById('imageUpload').addEventListener('change', function() {
    document.getElementById('detectBtn').disabled = false;
  });
  