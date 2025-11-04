let correctAnswer = null;

function generateMathCaptcha() {
  const num1 = Math.floor(Math.random() * 10 + 1); // 1–10
  const num2 = Math.floor(Math.random() * 10 + 1);
  const operators = ['+', '-', '*'];
  const operator = operators[Math.floor(Math.random() * operators.length)];

  let expression = `${num1} ${operator} ${num2}`;
  correctAnswer = eval(expression); // Simple math evaluation
  document.getElementById('math-question').innerText = `What is ${expression}?`;
}

function verifyMathCaptcha() {
  const userAnswer = parseInt(document.getElementById('math-answer').value.trim());

  if (userAnswer === correctAnswer) {
    document.getElementById('captcha-container').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  } else {
    alert("Incorrect. Try again.");
    document.getElementById('math-answer').value = '';
    generateMathCaptcha(); // Refresh question
  }
}

function sayHello() {
  alert("Hello! You passed the math CAPTCHA.");
}

// Generate one on page load
window.onload = generateMathCaptcha;
