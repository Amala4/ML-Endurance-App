function createChart(indexAxis = "x") {
  var ctx = document.getElementById("myChart").getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["TSS", "Carbs", "Water", "Sodium"],
      datasets: [
        {
          label: "Planned",
          data: [75, 90, 80, 90],
          backgroundColor: "#2F388D",
          barPercentage: 0.5,
          categoryPercentage: 0.4,
          borderRadius: 2,
        },
        {
          label: "Actual",
          data: [65, 80, 50, 75],
          backgroundColor: "#7983D9",
          barPercentage: 0.5,
          categoryPercentage: 0.4,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      indexAxis: indexAxis,
      animation: false,
      // maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: "top",
          labels: {
            color: "white",
            usePointStyle: true, // Makes the legend markers rounded
            pointStyle: "circle",
            boxHeight: 8,
            font: { size: 15 },
            padding: 0,
          },
          padding: 0,
        },
        tooltip: {
          backgroundColor: "#2A2D3E",
          titleColor: "white",
          bodyColor: "white",
          callbacks: {
            label: function (tooltipItem) {
              let unit = "";
              if (tooltipItem.label === "Water") unit = "l";
              else if (tooltipItem.label === "Sodium") unit = "mg";
              else unit = "g";
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
            // display: false,
          },
          grid: {
            display: false,
          },
        },
        y: {
          ticks: {
            color: "white",
            font: { size: 12 },
            display: false,
            callback: function (value) {
              return value;
            },
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
function updateChart() {
  if (window.innerWidth >= 320 && window.innerWidth <= 767) {
    chart.destroy(); // Destroy the existing chart
    chart = createChart("y"); // Create a new horizontal chart
  } else {
    chart.destroy();
    chart = createChart("x"); // Create a new vertical chart
  }
}

// Initialize chart
var chart = createChart();

// Add event listener for window resizing
window.addEventListener("resize", updateChart);

// Call the update function initially to handle current screen size
updateChart();
