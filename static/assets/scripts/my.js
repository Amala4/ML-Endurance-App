
/********************************* form step desktop bar  ********************************/
var currentStep = 1;
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
  updateStepOnMobile(currentStep);
}

/********************************* mobile progress bar  ********************************/
const progressSteps = document.querySelectorAll(".progress-step");
const nextButtons = document.querySelectorAll(".step-btn-next");
const prevButtons = document.querySelectorAll(".step-btn-prev");
const progressText = document.querySelector(".progress-text");



// Function to update step visibility
function updateStepOnMobile(currentStep) {

  // Update the progress steps
  progressSteps.forEach((progressStep, index) => {
    // Only show the first four steps visually
    if (index < 4) {
      progressStep.classList.toggle("completed", index <= currentStep-1);
    } else {
      // Ensure the last two steps are not shown as completed and are hidden
      progressStep.classList.remove("completed");
    }
  });
  
  // Update the progress texts
  progressText.textContent = `${Math.min(currentStep, 4)}/${Math.min(steps.length, 4)}`;
}


function moveToNextStep (){
  if (currentStep < steps.length) {
    showStep(currentStep + 1);
  }

}



function adjustPlaceholder() {
  const inputs = document.getElementsByClassName("mobile-text1");
  const texts = document.getElementsByClassName("mobile-text2");
  const placeholder1 = document.getElementsByClassName(
    "placeholder-responsive1"
  );
  const placeholder2 = document.getElementsByClassName(
    "placeholder-responsive2"
  );
  const placeholder3 = document.getElementsByClassName(
    "placeholder-responsive3"
  );

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

  for (let place1 of placeholder1) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      place1.placeholder = "Total carbohydrates";
      place1.style.fontSize = "14px";
    } else {
      // For desktop devices
      place1.placeholder = " Enter number of carbohydrates...";
      place1.style.fontSize = "14px";
    }
  }

  for (let place2 of placeholder2) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      place2.placeholder = "Volume of water (in milliliters) ";
      place2.style.fontSize = "14px";
    } else {
      // For desktop devices
      place2.placeholder = "Enter volume of water...";
      place2.style.fontSize = "14px";
    }
  }

  for (let place3 of placeholder3) {
    if (window.innerWidth <= 768) {
      // For mobile devices
      place3.placeholder = "Amount of sodium (in milligrams) consumed";
      place3.style.fontSize = "14px";
    } else {
      // For desktop devices
      place3.placeholder = "Enter amount of sodium...";
      place3.style.fontSize = "14px";
    }
  }
}



// Adjust placeholder text on window resize
window.onresize = adjustPlaceholder;

/********************************* password Visibility  ********************************/

function togglePasswordVisibility() {
  const passwordField = document.getElementById("password-field");
  const hideIcon = document.getElementById("hide-icon");
  const showIcon = document.getElementById("show-icon");

  if (passwordField.type === "password") {
    passwordField.type = "text";
    hideIcon.style.display = "none"; 
    showIcon.style.display = "inline"; 
  } else {
    passwordField.type = "password";
    hideIcon.style.display = "inline"; 
    showIcon.style.display = "none"; 
  }
}


/********************************* Data Submission  ********************************/
const workout_submit_btn = document.getElementById('workout_submit_btn');
const workout_plan_btn = document.getElementById('workout_plan_btn');
const workout_log_details = document.getElementById('workout_log_details');
const workout_log_fuel = document.getElementById('workout_log_fuel');
const workout_log_conditions = document.getElementById('workout_log_conditions');
const workout_log_submit = document.getElementById('workout_log_submit');
const workout_log_thank_you = document.getElementById('workout_log_thank_you');


function getFuelPlan(){

  const workoutName = document.getElementById('workoutName').value.trim();
  const sport = document.getElementById('sport').value;
  const plannedDate = document.getElementById('plannedDate').value;
  const duration_hours = document.getElementById('duration_hours').value;
  const duration_minutes = document.getElementById('duration_minutes').value;
  const trainingStressScore = document.getElementById('trainingStressScore').value;
  const intensityFactor = document.getElementById('intensityFactor').value;

  // Validation
  if (!plannedDate || (!duration_hours && !duration_minutes) || !trainingStressScore || !intensityFactor) {
    alert('Please ensure all fields are selected');
    return
  }

  const formData = {
    workoutName,
    sport,
    plannedDate,
    duration_hours,
    duration_minutes,
    trainingStressScore,
    intensityFactor,
  };

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const fuel_planner_url = $("#fuel_planner_url").data("fuel_planner_url");


  $.ajax({
    url: fuel_planner_url,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    data: JSON.stringify(formData),
    success: function(response) {
      if (response.success) {
        const fuelingRequirements = response.fueling_requirements;
        document.getElementById('carbsPlan').textContent = fuelingRequirements.carbohydrate;
        document.getElementById('waterPlan').textContent = fuelingRequirements.water;
        document.getElementById('sodiumPlan').textContent = fuelingRequirements.sodium;
        moveToNextStep();
      }
      else{
        console.error('Error:', response.error);
        alert(response.error);
        return 

      }
    },
    error: function(error) {
        console.error('Error:', error.responseJSON.error);
        alert(error.responseJSON.error);
        return 
    }
  });

}


function validateWorkoutDetails(){
  const workout_date = document.getElementById('workout_date').value;
  const training_stress = document.getElementById('training_stress').value;
  const calories = document.getElementById('calories').value;
  const duration_hours = document.getElementById('duration_hours').value;

  if (!workout_date || !training_stress || !duration_hours || !calories) {
    alert('Please ensure all fields are selected');
    return
  }
  moveToNextStep();
}


function validateFuelLog(){
  const carbs_consumed = document.getElementById('carbs_consumed').value;
  const water_consumed = document.getElementById('water_consumed').value;
  const sodium_consumed = document.getElementById('sodium_consumed').value;

  if (!carbs_consumed || !water_consumed || !sodium_consumed) {
    alert('Please ensure all fields are selected');
    return
  }
  moveToNextStep();
}



function submitWorkoutLog(){

  // Workout Details
  const workout_date = document.getElementById('workout_date').value;
  const training_stress = document.getElementById('training_stress').value;
  const calories = document.getElementById('calories').value;
  const duration_hours = document.getElementById('duration_hours').value;
  const duration_minutes = document.getElementById('duration_minutes').value;

  // Fuel Log
  const carbs_consumed = document.getElementById('carbs_consumed').value;
  const water_consumed = document.getElementById('water_consumed').value;
  const sodium_consumed = document.getElementById('sodium_consumed').value;

  // Conditions
  const weather = document.querySelector('input[name="weather"]:checked').value;
  const indoor_workout = document.getElementById('indoor_workout').checked;
  
  // Issues
  const gastro = document.querySelector('input[name="gastro"]:checked').value;
  const muscle = document.querySelector('input[name="muscle"]:checked').value;
  const bonking = document.querySelector('input[name="bonking"]:checked').value;

  const formData = {
    workout_date,
    training_stress,
    calories,
    duration_hours,
    duration_minutes,
    carbs_consumed,
    water_consumed,
    sodium_consumed,
    weather,
    indoor_workout,
    gastro,
    muscle,
    bonking
  };


  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const workout_log_url = $("#workout_log_url").data("workout_log_url");


  $.ajax({
    url: workout_log_url,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    data: JSON.stringify(formData),
    success: function(response) {
      if (response.success) {
        moveToNextStep();
      }
      else{
        console.error('Error:', response.error);
        alert(response.error);
        return 

      }
    },
    error: function(error) {
        console.error('Error:', error.responseJSON.error);
        alert(error.responseJSON.error);
        return 
    }
  });


}


document.addEventListener("DOMContentLoaded", () => {

  // Initialize on page load
  updateStepOnMobile(1);
  adjustPlaceholder();

  if (workout_submit_btn) {
    workout_submit_btn.addEventListener("click", () => {
      getFuelPlan();
    });
  }

  if (workout_plan_btn) {
    workout_plan_btn.addEventListener("click", () => {
      moveToNextStep();
    });
  }

  if (workout_log_details) {
    workout_log_details.addEventListener("click", () => {
      validateWorkoutDetails();
    });
  }

  if (workout_log_fuel) {
    workout_log_fuel.addEventListener("click", () => {
      validateFuelLog();
    });
  }

  if (workout_log_conditions) {
    workout_log_conditions.addEventListener("click", () => {
      moveToNextStep();
    });
  }


  if (workout_log_submit) {
    workout_log_submit.addEventListener("click", () => {
      submitWorkoutLog();
    });
  }


  if (workout_log_thank_you) {
    workout_log_thank_you.addEventListener("click", () => {
      moveToNextStep();
    });
  }


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