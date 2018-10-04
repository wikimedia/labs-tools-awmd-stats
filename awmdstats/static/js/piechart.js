/* Generate our beautiful pie and bar charts */
/* Author: Derick N. Alangi */

window.onload = function() {
    var i, pie_dp = [], bar_dp = [];
    data_points = return_data();
    ps = return_patch_sum();

    for(i = 0; i < data_points.length; i++){
        // populate the pie chart data with it's values
        pie_dp.push({
            y: (parseInt(data_points[i]['patches'])/ps)*100,
            label: data_points[i]['name']
        });

        // populate the bar chart data with it's values
        bar_dp.push({
            y: parseInt(data_points[i]['patches']),
            label: data_points[i]['name']
        });
    }

    var pie_chat = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: ""
        },
        data: [{
            type: "pie",
            startAngle: 240,
            yValueFormatString: "##0.00\"%\"",
            indexLabel: "{label} {y}",
            dataPoints: pie_dp
        }]
    });

    var bar_chat = new CanvasJS.Chart("chartContainer1", {
        animationEnabled: true,

        title:{
            text: ""
        },
        axisX:{
            interval: 1
        },
        axisY2:{
            interlacedColor: "rgba(1,77,101,.2)",
            gridColor: "rgba(1,77,101,.1)",
            title: "Number of Patches"
        },
        data: [{
            type: "bar",
            name: "patches",
            axisYType: "secondary",
            color: "#007bff",
            dataPoints: bar_dp
        }]
    });

    pie_chat.render();
    bar_chat.render();
}

/* Return contributor data */
function return_data() {
    return data;
}

function return_patch_sum() {
    return patchsum;
}
