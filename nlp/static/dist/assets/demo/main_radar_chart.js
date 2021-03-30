// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("main_radar_chart");
var category = JSON.parse(document.getElementById('category_json').value);

var pos_score = JSON.parse(document.getElementById('pos_score_json').value);
var myRadarChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: category["category"],
        datasets: [{
            labels: "positive",
            data: category["pos_score_scaled"]
        }],
        datasets: [{
            labels: "negative",
            data: category["neg_score_scaled"]
        }],

    }
});