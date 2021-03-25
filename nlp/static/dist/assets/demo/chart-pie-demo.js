// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var overall = JSON.parse("{{ overallJSON|escapejs }}");
console.log(overall);

alert(overall);

var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["a","a","a","a"],
    datasets: [{
      data: [0,1,2,3],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
