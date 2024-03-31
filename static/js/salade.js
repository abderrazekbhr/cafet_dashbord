let data = null;
// let img = document.querySelector('.variation-ton');
let chartTon;
let chartPoulet;
const thon = document.querySelector('.salade-ton');
const poulet = document.querySelector('.salade-poulet');
const ctx0 = document.getElementById('myChart0');
const ctx1 = document.getElementById('myChart1');
const _url = 'http://127.0.0.1:5000/chart-data-salade';

const fetchData = async () => {
  if (data === null) {
    const response = await fetch(_url);
    data = await response.json();
  }
};

const createChart = (periode, ctx, column, chart) => {
  let localData;
  if (chart != undefined) {
    console.log('destroying');
    chart.destroy();
  }
  if (periode == 'semaine') {
    localData = {
      x: data.map(d => d['Date']).slice(data.length - 5, data.length),
      y: data.map(d => d[column]).slice(data.length - 5, data.length),
    };
  } else if (periode == 'mois') {
    localData = {
      x: data.map(d => d['Date']).slice(data.length - 30, data.length),
      y: data.map(d => d[column]).slice(data.length - 30, data.length),
    };
  } else {
    localData = {
      x: data.map(d => d['Date']),
      y: data.map(d => d[column]),
    };
  }
  console.log(localData);
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: localData.x,
      datasets: [
        {
          label: column + ' Quantité',
          labelColor: 'rgb(106,86,61)',
          data: localData.y,
          borderWidth: 1,
          borderColor: 'rgb(106,86,61)',
          backgroundColor: 'rgba(106,86,61, 0.2)',
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      
      plugins: {
        tooltip: {
          backgroundColor: 'rgba(106,86,61, 0.2)',
          titleColor: 'black',
          bodyColor: 'black',
          titleFont: {
            size: 16,
          },
          bodyFont: {
            size: 14,
          },
        },
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false,
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Date',
          },
          ticks: {
            color: '#000',
          },
        },
        y: {
          stacked: true,
          title: {
            display: true,
            text: 'Quantité',
          },
          ticks: {
            color: '#000',
          },
        },
      },
    },
  });
};
//intialize the chart and fetch data
const main = async () => {
  await fetchData();
  chartTon = createChart('semaine', ctx0, 'Salade Thon', chartTon);
  chartPoulet = createChart('semaine', ctx1, 'Salade Poulet', chartPoulet);
};
main();
//events
thon.addEventListener('change', e => {
  chartTon = createChart(e.target.value, ctx0, 'Salade Thon', chartTon);
});
poulet.addEventListener('change', async e => {
    chartPoulet = createChart(e.target.value, ctx1, 'Salade Poulet', chartPoulet);
});
