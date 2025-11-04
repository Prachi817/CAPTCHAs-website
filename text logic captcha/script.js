function verifyTextCaptcha() {
  const selected = document.getElementById('text-captcha').value;

  if (selected === "correct") {
    document.getElementById('captcha-container').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  } else {
    alert("Incorrect! Please try again.");
  }
}

function sayHello() {
  alert("Hello! You passed the CAPTCHA.");
}
