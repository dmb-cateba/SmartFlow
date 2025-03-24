"use strict";

document.addEventListener("DOMContentLoaded", function() {
  const scannerInput = document.getElementById('scannerInput');
  if (scannerInput) {
    scannerInput.addEventListener("keydown", processScan);
  }
});

function processScan(event) {
  if (event.key === "Enter") {
    const scanValue = event.target.value;
    const feedback = document.getElementById('scanFeedback');
    if (feedback) {
      feedback.innerText = `Scanned: ${scanValue}`;
    }
    event.target.value = '';
  }
}

// Expose the function if needed
window.processScan = processScan;
