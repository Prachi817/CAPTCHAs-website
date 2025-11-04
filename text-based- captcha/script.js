function verifyCaptcha() {
  const userInput = document.getElementById('captcha-input').value.trim().toLowerCase();
  const correctText = "WOYEE700"; // Match this to your image

  if (userInput === correctText.toLowerCase()) {
    document.getElementById('captcha-container').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  } else {
    alert("Incorrect CAPTCHA. Please try again.");
  }
}

