function adjustPlaceholder() {
  const text1 = document.getElementsByClassName("text-1");
  const text2 = document.getElementsByClassName("text-2");
  const text3 = document.getElementsByClassName("text-3");

  for (let value1 of text1) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      value1.placeholder = "Old password";
      value1.style.fontSize = "14px";
    }
  }

  for (let value2 of text2) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      value2.placeholder = "New password";
      value2.style.fontSize = "14px";
    }
  }

  for (let value3 of text3) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      value3.placeholder = "New password again";
      value3.style.fontSize = "14px";
    }
  }
}
// Initialize the form on page load
adjustPlaceholder();

// Adjust placeholder text on window resize
window.onresize = adjustPlaceholder;

/********************************* vaidation  ********************************/
