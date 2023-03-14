window.onload = function () {

    var d = new Date("July 21, 1983 01:15:00");
    var chart = new CanvasJS.Chart("chart", {
        title: {
            text: "Sensor Node Temperature"
        },
        //Time
        axisX: {
            valueFormatString: "hh mm"
        },
        // Temperature
        axisY2: {
            title: "Temperature (C)",
            suffix: "C"
        },
        toolTip: {
            shared: true
        },
        legend: {
            
            cursor: "pointer",
            verticalAlign: "top",
            horizontalAlign: "center",
            dockInsidePlotArea: true,
            itemclick: toogleDataSeries
        },

        
        data: [{
            type:"line",
            axisYType: "secondary",
            name: "Node 1",
            showInLegend: true,
            markerSize: 0,
            yValueFormatString: "##.#C",
            dataPoints: [		
                {x:  d.getHours() + d.getMinutes() , y: 23.6}
                //{x:  new Date("July 21, 1983 03:15:00").getHours().getMinutes() , y: 24.2},
                //{x:  new Date("July 21, 1983 05:15:00").getHours().getMinutes() , y: 23.2},
               // {x:  new Date("July 21, 1983 07:15:00").getHours().getMinutes() , y: 22.2}


                
                

               
            ]
        },
        {
            type: "line",
            axisYType: "secondary",
            name: "Node 2",
            showInLegend: true,
            markerSize: 0,
            yValueFormatString: "##.#C",
            dataPoints: [
                
            ]
        },
        {
            type: "line",
            axisYType: "secondary",
            name: "Node 3",
            showInLegend: true,
            markerSize: 0,
            yValueFormatString: "##.#C",
            dataPoints: [
                
            ]
        },
        {
            type: "line",
            axisYType: "secondary",
            name: "Node 4",
            showInLegend: true,
            markerSize: 0,
            yValueFormatString: "##.#C",
            dataPoints: [
                
            ]
        }]
    });
    chart.render();
    
    function toogleDataSeries(e){
        if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
        } else{
            e.dataSeries.visible = true;
        }
        chart.render();
    }
    
    }