// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("main_pie_chart");
var total = JSON.parse(document.getElementById('total_json').value);

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: Object.keys(total),
    datasets: [{
        data: Object.values(total),
        backgroundColor: ['#00FF88', '#FF8800'],
        }],
        }
   options: {
    responsive: true,
   }
				legend: {
					position: 'top',
				},
				title: {
					display: true,
					text: 'Chart.js Doughnut Chart'
				},
				animation: {
					animateScale: true,
					animateRotate: true
				}
});
