
radar_data = [{
    type: 'scatterpolar',
    r: [39, 28, 8, 7, 28, 39],
    theta: ['Sience', 'IT', 'Music', 'Design & Art', 'Politics', 'Comedy'],
    fill: 'toself',
    marker: {
      color: color
    }
  }]
  
  radar_layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 50]
      }
    },
    showlegend: false,
    title: 'Like counts of categories',
    height: 400,
    width: 500
  }
  
  Plotly.newPlot("radarDiv", radar_data, radar_layout)