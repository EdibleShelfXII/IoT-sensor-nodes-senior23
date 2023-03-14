window.onload = function() {
    console.log("LOADED");

    //Configuration variables
    var updateInterval = 1000 //in ms
    var numberElements = 200;

    //Globals
    var updateCount = 0;

    // Chart Objects
    var node1Temperature = $("#node1Temperature");
    var node1Humidity = $("#node1Humidity");
    var node2Temperature = $("#node2Temperature");
    var node2Humidity = $("#node2Humidity");
    
    
    //chart instances & configuration

    var commonOptions = {
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              displayFormats: {
                millisecond: 'mm:ss:SSS'
              }
            }
          }],
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        legend: {display: false},
        tooltips:{ 
          enabled: false
        }
    };
    var node1ChartInstance_temp = new Chart(node1Temperature, {
        type: 'line',
        data: {
          datasets: [{
              label: "Node 1 Temperature",
              data: 0,
              fill: false,
              borderColor: '#343e9a',
              borderWidth: 1
          }]
        },
        options: Object.assign({}, commonOptions, {
          title:{
            display: true,
            text: "Node 1 - Temperature",
            fontSize: 18
          }
        })
    });
    var node1ChartInstance_humd = new Chart(node1Humidity, {
        type: 'line',
        data: {
          datasets: [{
              label: "Node 1 Humidity",
              data: 0,
              fill: false,
              borderColor: '#343e9a',
              borderWidth: 1
          }]
        },
        options: Object.assign({}, commonOptions, {
          title:{
            display: true,
            text: "Node 1 - Humidity ",
            fontSize: 18
          }
        })
    });

    var node2ChartInstance_temp = new Chart(node2Temperature, {
        type: 'line',
        data: {
          datasets: [{
              label: "Node 2 Temperature",
              data: 0,
              fill: false,
              borderColor: '#343e9a',
              borderWidth: 1
          }]
        },
        options: Object.assign({}, commonOptions, {
          title:{
            display: true,
            text: "Node 2 - Temperature",
            fontSize: 18
          }
        })    });

        var node2ChartInstance_humd = new Chart(node2Humidity, {
            type: 'line',
            data: {
              datasets: [{
                  label: "Node 2 Humidity",
                  data: 0,
                  fill: false,
                  borderColor: '#343e9a',
                  borderWidth: 1
              }]
            },
            options: Object.assign({}, commonOptions, {
              title:{
                display: true,
                text: "Node 2 - Humidity",
                fontSize: 18
              }
            })    });

   

    function addData(data) {
      if(data){
       
        if(data['adr']== 1){
        node1ChartInstance_temp.data.labels.push(new Date());
        node1ChartInstance_temp.data.datasets.forEach((dataset) => {dataset.data.push(data['temp'])});
        node1ChartInstance_humd.data.labels.push(new Date());
        node1ChartInstance_humd.data.datasets.forEach((dataset) => {dataset.data.push(data['humd'])});
        }
        else if (data['adr'] == 2){
        node2ChartInstance_temp.data.labels.push(new Date());
        node2ChartInstance_temp.data.datasets.forEach((dataset) => {dataset.data.push(data['temp'])});
        node2ChartInstance_humd.data.labels.push(new Date());
        node2ChartInstance_humd.data.datasets.forEach((dataset) => {dataset.data.push(data['humd'])});
        }

        if(updateCount > numberElements){
          node1ChartInstance_temp.data.label.shift();
          node1ChartInstance_temp.data.datasets[0].data.shift();
          node1ChartInstance_humd.data.label.shift();
          node1ChartInstance_humd.data.datasets[0].data.shift();
          node2ChartInstance_temp.data.label.shift();
          node2ChartInstance_temp.data.datasets[0].data.shift();
          node2ChartInstance_humd.data.label.shift();
          node2ChartInstance_humd.data.datasets[0].data.shift();
        }
        else updateCount++;
        node1ChartInstance_temp.update();
        node1ChartInstance_humd.update();
        node2ChartInstance_temp.update();
        node2ChartInstance_humd.update();

      }
    };

    function updateData() {
      console.log("Update Data");
      addData({"adr": 1,"temp" : 73,"humd" : 24});
      addData({"adr": 2,"temp" : 75,"humd" : 60});
      $.getJSON("TempHumGenerator.py", addData);
      setTimeout(updateData,updateInterval);
    }

    updateData();
  }