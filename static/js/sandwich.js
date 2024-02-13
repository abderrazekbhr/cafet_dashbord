let data = null;
// let img = document.querySelector('.variation-ton');
let chart0;
let chart1;
let chart2;
let chart3;
let chart4;
let chart5;
let chart6;
let chart7;
let chart8;
const select0 = document.querySelector('.select-0');
const select1 = document.querySelector('.select-1');
const select2 = document.querySelector('.select-2');
const select3 = document.querySelector('.select-3');
const select4 = document.querySelector('.select-4');
const select5 = document.querySelector('.select-5');
const select6 = document.querySelector('.select-6');
const select7 = document.querySelector('.select-7');
const select8 = document.querySelector('.select-8');

const ctx0 = document.getElementById('myChart0');
const ctx1 = document.getElementById('myChart1');
const ctx2 = document.getElementById('myChart2');
const ctx3 = document.getElementById('myChart3');
const ctx4 = document.getElementById('myChart4');
const ctx5 = document.getElementById('myChart5');
const ctx6 = document.getElementById('myChart6');
const ctx7 = document.getElementById('myChart7');
const ctx8 = document.getElementById('myChart8');
const _url = 'http://127.0.0.1:5000/chart-data-sandwich';

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
  if (periode == 'week') {
    localData = {
      x: data.map(d => d['Date']).slice(data.length - 5, data.length),
      y: data.map(d => d[column]).slice(data.length - 5, data.length),
    };
  } else if (periode == 'month') {
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
  console.log(data);
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: localData.x,
      datasets: [
        {
          label: column + ' quantity',
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
      animations: {
        tension: {
          duration: 2000,
          easing: 'linear',
          from: 0.5,
          to: 0,
          loop: true,
        },
      },
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
            text: 'Quantity',
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
  chart0 = createChart('week', ctx0, 'Sandwiches poulet crudités', chart0);
  chart1 = createChart('week', ctx1, 'Sandwiches thon cruditès', chart1);
  chart2 = createChart('week', ctx2, 'Sandwiches végétarien', chart2);
  chart3 = createChart('week', ctx3, 'Sandwiches poulet mexicain', chart3);
  chart4 = createChart('week', ctx4, 'Sandwiches chèvre miel crudités', chart4);
  chart5 = createChart('week', ctx5, 'Sandwiches poulet curry', chart5);
  chart6 = createChart('week', ctx6, 'Sandwiches saumon', chart6);
  chart7 = createChart('week', ctx7, 'Panini 4 fromages', chart7);
  chart8 = createChart('week', ctx8, 'Panini poulet Kebab', chart8);
};
main();

//events
select0.addEventListener('change', e => {
  chart0 = createChart(e.target.value, ctx0, 'Sandwiches poulet crudités', chart0);
});
select1.addEventListener('change', async e => {
  chart1 = createChart(e.target.value, ctx1, 'Sandwiches thon cruditès', chart1);
});
select2.addEventListener('change', e => {
  chart2 = createChart(e.target.value, ctx2, 'Sandwiches végétarien', chart2);
});
select3.addEventListener('change', async e => {
  chart3 = createChart(e.target.value, ctx3, 'Sandwiches poulet mexicain', chart3);
});
select4.addEventListener('change', e => {
  chart4 = createChart(e.target.value, ctx4, 'Sandwiches chèvre miel crudités', chart4);
});
select5.addEventListener('change', async e => {
  chart5 = createChart(e.target.value, ctx5, 'Sandwiches poulet curry', chart5);
});
select6.addEventListener('change', e => {
  chart6 = createChart(e.target.value, ctx6, 'Sandwiches saumon', chart6);
});
select7.addEventListener('change', async e => {
  chart7 = createChart(e.target.value, ctx7, 'Panini 4 fromages', chart7);
});
select8.addEventListener('change', async e => {
  chart8 = createChart(e.target.value, ctx8, 'Panini poulet Kebab', chart8);
});
