
let pie_data = [{
    values: [15, 10, 20, 30, 10, 15],
    labels: ['Sience', 'IT', 'Music', 'Design & Art', 'Politics', 'Comedy' ],
    hoverinfo: 'label+percent',
    hole: .4,
    type: 'pie'
  }];
  
  let pie_layout = {
    title: 'Category pie chart',
    annotations: [
      {
        font: {
          size: 15
        },
        showarrow: false,
        text: ""
      }
    ],
    height: 400,
    width: 400,
    showlegend: false
  };
  
  Plotly.newPlot('pieDiv', pie_data, pie_layout);   