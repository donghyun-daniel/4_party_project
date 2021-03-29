// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var total = JSON.parse(document.getElementById('total_json').value);

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: Object.keys(total),
    datasets: [{
      data: Object.values(total),
      backgroundColor: ['#00FF00', '#FF0000'],
    }],
  },
});
