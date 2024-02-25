let data = null;
// let img = document.querySelector('.variation-ton');
let chart0;
let chart1;
let chart2;

const select0 = document.querySelector('.select-0');
const select1 = document.querySelector('.select-1');
const select2 = document.querySelector('.select-2');

const ctx0 = document.getElementById('myChart0');
const ctx1 = document.getElementById('myChart1');
const ctx2 = document.getElementById('myChart2');
const _url = 'http://127.0.0.1:5000/chart-data-viennoiseries';

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
  chart0 = createChart("week", ctx0, "Pain au chocolat", chart0);
  chart1 = createChart("week", ctx1, "Croissant", chart1);
  chart2 = createChart("week", ctx2, "Pains suisses", chart2);
  
};
main();

//events
select0.addEventListener("change", e => {
  chart0 = createChart(e.target.value, ctx0, "Pain au chocolat", chart0);
});
select1.addEventListener("change", async e => {
  chart1 = createChart(e.target.value, ctx1, "Croissant", chart1);
});
select2.addEventListener("change", e => {
  chart2 = createChart(e.target.value, ctx2, "Pains suisses", chart2);
});
