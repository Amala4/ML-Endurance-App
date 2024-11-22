// document.addEventListener("DOMContentLoaded", () => {
//   const menuTrigger = document.querySelector(".menu-trigger");
//   const sidebar = document.querySelector(".sidebar");
//   const body = document.body;
//   // Toggle sidebar classes on click
//   menuTrigger.addEventListener("click", () => {
//     sidebar.classList.toggle("menuClosed");
//     setTimeout(() => {
//       sidebar.classList.toggle("sidebar-h");
//     }, 500);
//   });

//   // Apply classes automatically for small screens
//   if (window.innerWidth < 992) {
//     body.classList.add("bodyClosed");
//     sidebar.classList.add("menuClosed", "sidebar-h");
//   }
// });

// document.addEventListener("DOMContentLoaded", () => {
//   const currentPath = window.location.pathname;
//   const sidebarLinks = document.querySelectorAll(".sidebar-list a");

//   sidebarLinks.forEach((link) => {
//     const href = link.getAttribute("href");

//     // Check if the href is valid (not null, empty, or "#")
//     if (href && href !== "#" && href.includes(currentPath)) {
//       link.closest(".sidebar-list").classList.add("active");
//     } else {
//       link.closest(".sidebar-list").classList.remove("active");
//     }
//   });
// });

// step form
/********************************* form step desktop bar  ********************************/
document.addEventListener("DOMContentLoaded", () => {
  let currentStep = 1;
  const steps = document.querySelectorAll(".form-step");
  const indicators = document.querySelectorAll(".step-nav-item");

  function showStep(step) {
    // Ensure step is within valid range
    if (step < 1 || step > steps.length) return;

    // Mark the previous step as completed
    if (step > 1) {
      const previousIndicator = document.querySelector(
        `.step-nav-item[data-step="${step - 1}"] .step-tab-count`
      );
      previousIndicator.classList.add("completed");
    }

    if (step < currentStep) {
      const currentIndicator = document.querySelector(
        `.step-nav-item[data-step="${currentStep - 1}"] .step-tab-count`
      );
      currentIndicator.classList.remove("completed");
    }
    currentStep = step;
    // Toggle visibility of form steps
    steps.forEach((formStep) => {
      formStep.classList.toggle("active", formStep.dataset.step == step);
    });
    // Toggle active class on step indicators
    indicators.forEach((indicator) => {
      indicator.classList.toggle("active", indicator.dataset.step == step);
    });
  }
  // Handle Next button clicks
  document.querySelectorAll(".step-btn-next").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep < steps.length) {
        showStep(currentStep + 1);
      }
    });
  });
  // Handle Previous button clicks
  document.querySelectorAll(".step-btn-prev").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep > 1) {
        showStep(currentStep - 1);
      }
    });
  });
  // Handle step indicator clicks
  indicators.forEach((indicator) => {
    indicator.addEventListener("click", () => {
      const step = parseInt(indicator.dataset.step);
      showStep(step);
    });
  });
});

/********************************* mobile progress bar  ********************************/
// Select all relevant elements
const steps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");
const nextButtons = document.querySelectorAll(".step-btn-next");
const prevButtons = document.querySelectorAll(".step-btn-prev"); // Optional if you want a 'Previous' button
const progressText1 = document.querySelector(".progress-text1");

let currentStep = 0;

// Function to update step visibility
function updateStep() {
  // Show/hide steps based on current step
  steps.forEach((step, index) => {
    step.classList.toggle("active", index === currentStep);
  });

  // Update the progress steps
  progressSteps.forEach((progressStep, index) => {
    // Only show the first four steps visually
    if (index < 4) {
      progressStep.classList.toggle("completed", index <= currentStep);
    } else {
      // Ensure the last two steps are not shown as completed and are hidden
      progressStep.classList.remove("completed");
    }
  });

  // Update the progress text to show total of 4
  progressText1.textContent = `${Math.min(currentStep + 1, 3)}/3`; // Show steps as 1/4, 2/4, etc.
}

// Event listeners for Next buttons
nextButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (currentStep < steps.length - 1) {
      currentStep++;
      updateStep();
    }
  });
});

// Optional: Event listeners for Previous buttons
prevButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;
      updateStep();
    }
  });
});

function adjustPlaceholder() {
  const inputs = document.getElementsByClassName("mobile-text1");
  const texts = document.getElementsByClassName("mobile-text2");

  for (let input of inputs) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      input.placeholder = "Duration (Hrs)";
      input.style.fontSize = "14px";
    } else {
      // For desktop devices
      input.placeholder = " Hours";
      input.style.fontSize = "14px";
    }
  }

  for (let text of texts) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      text.placeholder = "Duration (Mins)";
      text.style.fontSize = "14px";
    } else {
      // For desktop devices
      text.placeholder = " Mins";
      text.style.fontSize = "14px";
    }
  }
}
// Initialize the form on page load
updateStep();
adjustPlaceholder();

// Adjust placeholder text on window resize
window.onresize = adjustPlaceholder;

/********************************* vaidation  ********************************/
