
/********************************* form step desktop bar  ********************************/
var currentStep = 1;
let is_metric = true
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
  adaptPlaceholder();
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
  if (progressText){
    progressText.textContent = `${Math.min(currentStep, 4)}/${Math.min(steps.length, 4)}`;

  }
}


function moveToNextStep (){
  if (currentStep < steps.length) {
    showStep(currentStep + 1);
  }

}



function adaptPlaceholder (){
  const input_hrs = document.getElementsByClassName("mobile-text1");
  const input_mins = document.getElementsByClassName("mobile-text2");
  const carbPlaceholder = document.getElementById("carbs_consumed");
  const waterPlaceholder = document.getElementById("water_consumed");
  const sodiumPlaceholder = document.getElementById("sodium_consumed");
  const waterUnit = waterPlaceholder ? waterPlaceholder.getAttribute("data-water-unit") : "milliliters";

  // Adjust placeholders for inputs based on window width
    if (input_hrs){
      for (let input of input_hrs) {
        if (window.innerWidth <= 768) {
          input.placeholder = "Duration (Hrs)";
          input.style.fontSize = "14px";
        } else {
          input.placeholder = "Hours";
          input.style.fontSize = "14px";
        }
      }
    }

    if (input_mins){
      for (let input of input_mins) {
        if (window.innerWidth <= 768) {
          input.placeholder = "Duration (Mins)";
          input.style.fontSize = "14px";
        } else {
          input.placeholder = "Mins";
          input.style.fontSize = "14px";
        }
      }
    }

    if (carbPlaceholder){
          if (window.innerWidth <= 768) {
            carbPlaceholder.placeholder = "Amount of carbohydrates (in grams) consumed";
          } else {
            carbPlaceholder.placeholder = "Enter amount of carbohydrates...";
          }
          carbPlaceholder.style.fontSize = "14px";
    }

    if (waterPlaceholder){
          if (window.innerWidth <= 768) {
            waterPlaceholder.placeholder = `Volume of water (in ${waterUnit}) consumed`;

          } else {
            waterPlaceholder.placeholder = `Enter volume of water...`;
          }
          waterPlaceholder.style.fontSize = "14px";
    }

    if (sodiumPlaceholder){
          if (window.innerWidth <= 768) {
            sodiumPlaceholder.placeholder = "Amount of sodium (in milligrams) consumed";
          } else {
            sodiumPlaceholder.placeholder = "Enter amount of sodium...";
          }
          sodiumPlaceholder.style.fontSize = "14px";
    }
}



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
const workoutUpdateConfirm = document.getElementById('workoutUpdateConfirm');
const workout_log_thank_you = document.getElementById('workout_log_thank_you');
const alert_close_btn = document.getElementById('close-message');
const signupForm = document.getElementById("signup-form");
const loginForm = document.getElementById("login-form");
const birth_date_element = document.getElementById("birth_date");
const plannedDate_element = document.getElementById("plannedDate");
const workout_date_element = document.getElementById("workout_date");


function getFuelPlan(){

  const workoutName = document.getElementById('workoutName').value.trim();
  const sport = document.getElementById('sport').value;
  const plannedDate = document.getElementById('plannedDate').value;
  const duration_hours = document.getElementById('duration_hours').value;
  const duration_minutes = document.getElementById('duration_minutes').value;
  const training_stress_element = document.getElementById('trainingStressScore');
  const trainingStressScore = training_stress_element ? training_stress_element.value : null;
  const intensityFactor_element = document.getElementById('intensityFactor');
  const intensityFactor = intensityFactor_element ? intensityFactor_element.value : null;


  // Validation
  if (!workoutName || workoutName.trim() === "") {
    showMessage('Workout Name field cannot be empty');
    return;
  }

  if (!sport) {
    showMessage('Please select a sport');
    return;
  }


  if (!plannedDate) {
    showMessage('Please select a planned date');
    return;
  }

  let currentDate = new Date();
  currentDate.setHours(0, 0, 0, 0);
  let plannedDateObj = new Date(plannedDate);
  plannedDateObj.setHours(0, 0, 0, 0);


  if (plannedDateObj < currentDate) {
    showMessage('Planned date cannot be in the past');
    return;
  }

  if ((!duration_hours && !duration_minutes) || (duration_hours == 0 && duration_minutes == 0)) {
    showMessage('Please specify duration');
    return;
  }

  if (duration_hours && (!isNumber(duration_hours) || duration_hours < 0)) {
    showMessage('Duration hours must be a number greater than 0');
    return;
  }

  if (duration_minutes  && (!isNumber(duration_minutes) || duration_minutes < 0)) {
    showMessage('Duration minutes must be a number greater than 0');
    return;
  }


  if (sport === "cycling" || sport === "mountain_biking") {
    if (!trainingStressScore) {
      showMessage('Please enter the training stress score');
      return;
    }

    if (!isNumber(trainingStressScore) || trainingStressScore > 10000 || trainingStressScore <= 0) {
      showMessage('Training stress score must be a number between 0 and 10000');
      return;
    }

    if (!intensityFactor) {
      showMessage('Please enter the Intensity Factor');
      return;
    }

    if (!isNumber(intensityFactor) || intensityFactor > 2 || intensityFactor <= 0) {
      showMessage('Intensity factor must be a number between 0 and 2');
      return;
    }

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
        document.getElementById('waterUnit').textContent = fuelingRequirements.water_unit;
        document.getElementById('sodiumPlan').textContent = fuelingRequirements.sodium;
        moveToNextStep();
      }
      else{
        showMessage(response.error);
        return

      }
    },
    error: function(error) {
        showMessage(error.responseJSON.error);
        return
    }
  });

}


function validateWorkoutDetails(){
  const workout_date = document.getElementById('workout_date').value;
  const duration_hours = document.getElementById('duration_hours').value;
  const duration_minutes = document.getElementById('duration_minutes').value;
  const calories = document.getElementById('calories').value;
  const training_stress_element = document.getElementById('training_stress');

  // Validation
  if (!workout_date) {
    showMessage('Please fill in workout date');
    return;
  }

  let currentDate = new Date();
  currentDate.setHours(0, 0, 0, 0);
  let workoutDateObj = new Date(workout_date);
  workoutDateObj.setHours(0, 0, 0, 0);


  if (currentDate < workoutDateObj) {
    showMessage('Workout date cannot be in the future');
    return;
  }

  if ((!duration_hours && !duration_minutes) || (duration_hours == 0 && duration_minutes == 0)) {
    showMessage('Please specify duration');
    return;
  }

  if (duration_hours && (!isNumber(duration_hours) || duration_hours < 0)) {
    showMessage('Duration hours must be a number greater than 0');
    return;
  }

  if (duration_minutes  && (!isNumber(duration_minutes) || duration_minutes < 0)) {
    showMessage('Duration minutes must be a number greater than 0');
    return;
  }




  if (training_stress_element) {
    const training_stress_value = document.getElementById('training_stress').value;
    if (!training_stress_value) {
      showMessage('Please enter the training stress score');
      return;
    }

    if (!isNumber(training_stress_value) || training_stress_value > 10000 || training_stress_value <= 0) {
      showMessage('Training stress score must be a number between 0 and 10000');
      return;
    }
  }



  if (!calories) {
    showMessage('Please enter the amount of work in Calories');
    return;
  }

  if (!isNumber(calories) || calories <= 0) {
    showMessage('Amount of work must be a number greater than 0');
    return;
  }

  moveToNextStep();
}


function validateFuelLog(){
  const carbs_consumed = document.getElementById('carbs_consumed').value;
  const water_consumed = document.getElementById('water_consumed').value;
  const sodium_consumed = document.getElementById('sodium_consumed').value;


  // Validation
  //Carbs
  if (!carbs_consumed) {
    showMessage('Please fill in the carbohydrate consumed');
    return;
  }


  if (carbs_consumed && (!isNumber(carbs_consumed) || carbs_consumed < 0)) {
    showMessage('Carbohydrate consumed must be a number greater than 0');
    return;
  }



  //Water
  if (!water_consumed) {
    showMessage('Please fill in the water consumed');
    return;
  }


  if (water_consumed && (!isNumber(water_consumed) || water_consumed < 0)) {
    showMessage('Water consumed must be a number greater than 0');
    return;
  }



  //Sodium
  if (!sodium_consumed) {
    showMessage('Please fill in the sodium consumed');
    return;
  }


  if (sodium_consumed && (!isNumber(sodium_consumed) || sodium_consumed < 0)) {
    showMessage('Sodium consumed must be a number greater than 0');
    return;
  }


  moveToNextStep();
}



function checkWorkoutLog(){

  const check_workout_log_url = $("#check_workout_log_url").data("check_workout_log_url");

  $.ajax({
    url: check_workout_log_url,
    method: 'GET',
    success: function(log) {
        if (log.exists) {
          $('#confirmLogUpdateModal').modal('show');

          // When the user clicks 'Yes' to update
          $('#workoutUpdateConfirm').click(function() {
            $('#confirmLogUpdateModal').modal('hide');
            submitWorkoutLog();
          });

        } else {
          submitWorkoutLog();
        }
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});


}


function submitWorkoutLog(){

  // Workout Details
  const workout_date = document.getElementById('workout_date').value;
  const training_stress_element = document.getElementById('training_stress');
  const training_stress = training_stress_element ? training_stress_element.value : null;
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
  const gastro = document.querySelector('input[name="gastro"]:checked')?.value || '0';
  const muscle = document.querySelector('input[name="muscle"]:checked')?.value || '0';
  const bonking = document.querySelector('input[name="bonking"]:checked')?.value || '0';

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
        showMessage(response.error);
        return

      }
    },
    error: function(error) {
        showMessage(error.responseJSON.error);
        return
    }
  });


}


let timeout_Id;
function showMessage(message) {
  const messageBox = document.getElementById('alert-message');
  const messageText = document.getElementById('message-text');

  messageText.textContent = message || 'Something went wrong.';
  messageBox.style.display = 'block';
  messageBox.scrollIntoView({ behavior: 'smooth', block: 'center' });

  if (timeout_Id) {
    clearTimeout(timeout_Id);
  }


  timeout_Id = setTimeout(function() {
  messageBox.style.display = 'none';
  }, 4000);
}



function isNumber(value) {
    return /^\d+(\.\d+)?$/.test(value.toString());
}


/********************************* Chart Section  ********************************/

var backendData;

function createChart(indexAxis = "x", chartData = { labels: [], datasets: [] }, is_metric = is_metric) {
  var ctx = document.getElementById("myChart").getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    data: chartData,
    options: {
      responsive: true,
      indexAxis: indexAxis,
      animation: false,
      plugins: {
        legend: {
          display: true,
          position: "top",
          labels: {
            color: "white",
            usePointStyle: true,
            pointStyle: "circle",
            boxHeight: 8,
            font: { size: 15 },
            padding: 0,
          },
        },
        tooltip: {
          backgroundColor: "#2A2D3E",
          titleColor: "white",
          bodyColor: "white",
          callbacks: {
            label: function (tooltipItem) {
              let unit = "";

              if (tooltipItem.label === "Water") unit = is_metric ? "ml" : "oz";
              else if (tooltipItem.label === "Carbs") unit = "g";
              else if (tooltipItem.label === "Sodium") unit = "mg";
              else unit = "";
              return `${tooltipItem.dataset.label}: ${tooltipItem.raw}${unit}`;
            },
          },
        },
      },
      scales: {
        x: {
          ticks: {
            color: "white",
            font: { size: 12 },
          },
          grid: {
            display: false,
          },
        },
        y: {
          ticks: {
            color: "white",
            font: { size: 12 },
            // display: false,
          },
          grid: {
            display: false,
          },
        },
      },
    },
  });
}

// Function to update chart layout based on screen size
function adaptChartLayout() {
  if  (backendData){

    const isMobile = window.innerWidth >= 320 && window.innerWidth <= 767;
    const newIndexAxis = isMobile ? "y" : "x";

    // Only update if the axis has changed
    if (chart.options.indexAxis !== newIndexAxis) {
      chart.destroy();
      chart = createChart(newIndexAxis, backendData, is_metric);
    }
  }

}

// Debounce the resize event
let resizeTimeout;

function debounceResize() {
    adaptPlaceholder();
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    adaptChartLayout();
  }, 200);
}

// Function to update the chart data
function updateChartData() {
  const chart_url = $("#chart_url").data("chart_url");

  $.ajax({
    url: chart_url,
    method: 'GET',
    data: [],
    success: function(response) {
      if (response.success) {

        if (window.chart) {
          window.chart.destroy();
        }

        // Create a new chart with the updated data
        backendData = response.chart_data
        is_metric = response.is_metric
        window.chart = createChart("x", backendData, is_metric);
        adaptChartLayout();
        moveToNextStep();
      }
      else{
        showMessage("Something went wrong, contact Admin");
        return

      }
    },
    error: function(error) {
        showMessage("Something went wrong, contact Admin");
        return
    }
  });
}


/********************************* Event Listeners  ********************************/
const sport_option = document.getElementById('sport');

window.addEventListener("resize", debounceResize);

document.addEventListener("DOMContentLoaded", () => {

  // Initialize on page load
  updateStepOnMobile(1);
  adaptPlaceholder();


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
      checkWorkoutLog();
    });
  }



  if (workout_log_thank_you) {
    workout_log_thank_you.addEventListener("click", () => {
      updateChartData();
    });
  }


  if (alert_close_btn) {
    alert_close_btn.addEventListener("click", () => {
      document.getElementById('alert-message').style.display = 'none';

    });
  }


  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (validateSignupForm()) {
        signupForm.submit();
      }
    });
  }


  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (validateLoginForm()) {
        this.submit();
      }
    });
  }


  if (sport_option) {
    sport_option.addEventListener("change", () => {
      const selectedSport = sport_option.value;
      const tssDiv = document.getElementById('tss_div');
      const IntFDiv = document.getElementById('intF_div');

      if (selectedSport === 'cycling' || selectedSport === 'mountain_biking') {
        tssDiv.style.display = 'block';
        IntFDiv.style.display = 'block';
      } else {
        tssDiv.style.display = 'none';
        IntFDiv.style.display = 'none';
      }
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






  if (birth_date_element) {
     flatpickr(birth_date_element, {
      dateFormat: "m/d/Y",
      disableMobile: true,
      maxDate: new Date(),
     });
  }

   if (plannedDate_element) {
     flatpickr(plannedDate_element, {
       dateFormat: "m/d/Y",
       disableMobile: true,
     });
   }

   if (workout_date_element) {
     flatpickr(workout_date_element, {
       dateFormat: "m/d/Y",
       disableMobile: true,
     });
   }



});





function validateSignupForm() {
  const fullname = document.querySelector("input[name='fullname']").value.trim();
  const email = document.querySelector("input[name='email']").value.trim();
  const password = document.querySelector("input[name='password']").value;
  const terms = document.querySelector("input[name='terms']").checked;

  if (!fullname) {
    showMessage("Name is required.");
    return false;
  }
  if (!email || !validateEmail(email)) {
    showMessage("A valid email is required.");
    return false;
  }
  if (!password || password.length < 4) {
    showMessage("Password must be at least 4 characters.");
    return false;
  }
  if (!terms) {
    showMessage("You must agree to the Terms and Privacy Policy.");
    return false;
  }

  return true;
}


function validateLoginForm() {
  const email = document.querySelector("input[name='email']").value.trim();
  const password = document.querySelector("input[name='password']").value;


  if (!email || !validateEmail(email)) {
    showMessage("Please enter a valid email address.");
    return false;
  }
  if (!password) {
    showMessage("Password is required.");
    return false;
  }

  return true;
}



function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}


function previewImage(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
      const imageUrl = e.target.result;
      document.getElementById('profile-image-placeholder').src = imageUrl;
  };

  if (file) {
      reader.readAsDataURL(file);
  }
}



function convertWeight(unit) {
  const weightInput = document.getElementById('weight');
  const weightLabel = document.getElementById('weight-label');

  let currentPlaceholder = weightInput.placeholder;
  let numericMatch = currentPlaceholder.match(/\d+(\.\d+)?/);
  let currentWeight = numericMatch ? parseFloat(numericMatch[0]) : null;
  const isMetric = currentPlaceholder.includes('kg');

  if (currentWeight !== null) {
      if (unit === 'Metric' && !isMetric) {
          const convertedWeight = (currentWeight / 2.20462).toFixed(1);
          weightInput.placeholder = `${convertedWeight}kg`;
      } else if (unit === 'Imperial' && isMetric) {
          const convertedWeight = (currentWeight * 2.20462).toFixed(1);
          weightInput.placeholder = `${convertedWeight}lb`;
      }
  }

  weightLabel.textContent = unit === 'Metric' ? 'Weight (kgs)' : 'Weight (lbs)';
}



document.querySelectorAll('input[name="units"]').forEach(radio => {
  radio.addEventListener('change', function () {
      const selectedUnit = this.id;
      convertWeight(selectedUnit);
  });
});




