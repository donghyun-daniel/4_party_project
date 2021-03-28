// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var overall = document.getElementById('overall_json').value;
var overall = JSON.parse(overall);

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: Object.keys(overall),
    datasets: [{
      data: Object.values(overall),
      backgroundColor: ['#00FF00', '#FF0000'],
    }],
  },
});
