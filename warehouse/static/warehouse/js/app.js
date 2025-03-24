"use strict";

// Global variables
let currentUser = '';
let navigationStack = [];

// Update the logged-in user display on all headers/badges
function updateUserDisplay() {
  const userBadges = document.querySelectorAll('.user-badge');
  userBadges.forEach(badge => {
    badge.innerText = currentUser;
  });
}

// Hide all screens and clear scanner input/feedback
function hideAll() {
  const screens = ['loginScreen', 'mainMenu', 'subMenuScreen', 'workflowScreen'];
  screens.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });
  // Clear scanner input and feedback if present
  const scannerInput = document.getElementById('scannerInput');
  if (scannerInput) scannerInput.value = '';
  const scanFeedback = document.getElementById('scanFeedback');
  if (scanFeedback) scanFeedback.innerText = '';
}

// Login function
function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  if (username && password) {
    currentUser = username;
    updateUserDisplay();
    hideAll();
    document.getElementById('mainMenu').classList.remove('hidden');
  } else {
    document.getElementById('loginFeedback').innerText = 'Invalid username or password!';
  }
}

// Expose functions to global scope
window.login = login;
window.updateUserDisplay = updateUserDisplay;
window.hideAll = hideAll;