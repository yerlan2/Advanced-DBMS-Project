// let line_trace = {
//   x: ["2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08",],
//   y: [10, 15, 13, 17, 18, 19],
//   type: 'scatter',
//   marker: {
//     color: color
//   }
// };

let line_layout = {
  title: 'How much posts created by month',
  height: 400,
  width: 500,
  showlegend: false
};

let line_data = [line_trace];

Plotly.newPlot('lineDiv', line_data, line_layout);
