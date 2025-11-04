function onHCaptchaSuccess(token) {
  // CAPTCHA solved — show landing content
  document.getElementById('recaptcha-container').style.display = 'none';
  document.getElementById('content').style.display = 'block';
}

function sayHello() {
  alert("Hello! You passed hCaptcha.");
}
