
window.onload = function () {

var chart = new CanvasJS.Chart("chartContainer", {
	exportEnabled: true,
	animationEnabled: true,
	theme: "light2",
	title:{
		text: "Temperature Variation - Ladakh vs Chandigarh"
	},
	axisX: {
		title: "April 2017",
		valueFormatString: "DD MMM"
	},
	axisY: {
		suffix: " °C"
	},     
	toolTip: {
		shared: true
	},
	legend: {
		cursor: "pointer",
		horizontalAlign: "right",
		itemclick: toggleDataSeries
	},
	data: [{
		type: "rangeArea",
		showInLegend: true,
		name: "Ladakh",
		markerSize: 0,
		yValueFormatString: "#0.## °C",
		dataPoints: [
			{ x: new Date(2017, 3, 1), y: [5, 21] },
			{ x: new Date(2017, 3, 2), y: [7, 15] },
			{ x: new Date(2017, 3, 3), y: [7, 18] },
			{ x: new Date(2017, 3, 4), y: [9, 16] },
			{ x: new Date(2017, 3, 5), y: [10, 17] },
			{ x: new Date(2017, 3, 6), y: [8, 13] },
			{ x: new Date(2017, 3, 7), y: [6, 10] },
			{ x: new Date(2017, 3, 8), y: [6, 15] },
			{ x: new Date(2017, 3, 9), y: [6, 20] },
			{ x: new Date(2017, 3, 10), y: [5, 21] },
			{ x: new Date(2017, 3, 11), y: [6, 21] },
			{ x: new Date(2017, 3, 12), y: [7, 14] },
			{ x: new Date(2017, 3, 13), y: [7, 17] },
			{ x: new Date(2017, 3, 14), y: [5, 20] },
			{ x: new Date(2017, 3, 15), y: [7, 18] },
			{ x: new Date(2017, 3, 16), y: [7, 15] },
			{ x: new Date(2017, 3, 17), y: [8, 15] },
			{ x: new Date(2017, 3, 18), y: [7, 13] },
			{ x: new Date(2017, 3, 19), y: [7, 13] },
			{ x: new Date(2017, 3, 20), y: [, 18] },
			{ x: new Date(2017, 3, 21), y: [6, 20] },
			{ x: new Date(2017, 3, 22), y: [9, 23] },
			{ x: new Date(2017, 3, 23), y: [9, 24] },
			{ x: new Date(2017, 3, 24), y: [8, 23] },
			{ x: new Date(2017, 3, 25), y: [12, 24] },
			{ x: new Date(2017, 3, 26), y: [10, 21] },
			{ x: new Date(2017, 3, 27), y: [7, 24] },
			{ x: new Date(2017, 3, 28), y: [10, 27] },
			{ x: new Date(2017, 3, 29), y: [10, 26] },
			{ x: new Date(2017, 3, 30), y: [12, 27] } 
		]
	},
	{
		type: "rangeArea",
		showInLegend: true,
		name: "Chandigarh",
		markerSize: 0,
		yValueFormatString: "#0.## °C",
		dataPoints: [
			{ x: new Date(2017, 2, 1), y: [15, 31] },
			{ x: new Date(2017, 3, 2), y: [16, 30] },
			{ x: new Date(2017, 3, 3), y: [14, 30] },
			{ x: new Date(2017, 3, 4), y: [15, 30] },
			{ x: new Date(2017, 3, 5), y: [17, 33] },
			{ x: new Date(2017, 3, 6), y: [19, 35] },
			{ x: new Date(2017, 3, 7), y: [20, 30] },
			{ x: new Date(2017, 3, 8), y: [15, 31] },
			{ x: new Date(2017, 3, 9), y: [16, 32] },
			{ x: new Date(2017, 3, 10), y: [16, 33] },
			{ x: new Date(2017, 3, 11), y: [16, 35] },
			{ x: new Date(2017, 3, 12), y: [17, 36] },
			{ x: new Date(2017, 3, 13), y: [20, 32] },
			{ x: new Date(2017, 3, 14), y: [17, 35] },
			{ x: new Date(2017, 3, 15), y: [18, 36] },
			{ x: new Date(2017, 3, 16), y: [20, 34] },
			{ x: new Date(2017, 3, 17), y: [17, 30] },
			{ x: new Date(2017, 3, 18), y: [19, 29] },
			{ x: new Date(2017, 3, 19), y: [16, 32] },
			{ x: new Date(2017, 3, 20), y: [17, 33] },
			{ x: new Date(2017, 3, 21), y: [16, 35] },
			{ x: new Date(2017, 3, 22), y: [19, 36] },
			{ x: new Date(2017, 3, 23), y: [20, 36] },
			{ x: new Date(2017, 3, 24), y: [21, 37] },
			{ x: new Date(2017, 3, 25), y: [21, 38] },
			{ x: new Date(2017, 3, 26), y: [21, 39] },
			{ x: new Date(2017, 3, 27), y: [22, 39] },
			{ x: new Date(2017, 3, 28), y: [22, 39] },
			{ x: new Date(2017, 3, 29), y: [22, 41] },
			{ x: new Date(2017, 3, 30), y: [23, 42] }
		
        ]}]
});
chart.render();

function toggleDataSeries(e) {
	if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;
	} else {
		e.dataSeries.visible = true;
	}
	e.chart.render();
}

}