const debtData = [52, 55, 57, 61, 64, 68, 71, 72, 73, 76, 79, 83, 87, 94, 101];
const growthData = [5.2, 4.8, 4.2, 3.9, 3.5, 3.1, 2.8, 2.6, 2.4, 2.0, 1.5, 1.1, 0.8, 0.2, -0.7];
const years = Array.from({ length: 15 }, (_, index) => 2010 + index);
const mean = debtData.reduce((sum, value) => sum + value, 0) / debtData.length;
const sorted = [...debtData].sort((a, b) => a - b);
const median = sorted[Math.floor(sorted.length / 2)];
const variance = debtData.reduce((sum, value) => sum + (value - mean) ** 2, 0) / debtData.length;
const standardDeviation = Math.sqrt(variance);

const format = (value, decimals = 1) => value.toFixed(decimals);
const setText = (id, value) => { document.getElementById(id).textContent = value; };
setText('heroMean', format(mean));
setText('meanValue', `${format(mean)}%`);
setText('medianValue', `${format(median)}%`);
setText('stdValue', format(standardDeviation));
setText('countValue', debtData.length);

function chartScales(width, height, min, max, values) {
  const pad = { left: 34, right: 14, top: 15, bottom: 27 };
  const x = index => pad.left + (index / (values.length - 1)) * (width - pad.left - pad.right);
  const y = value => pad.top + ((max - value) / (max - min)) * (height - pad.top - pad.bottom);
  return { pad, x, y };
}

function drawLineChart() {
  const svg = document.getElementById('lineChart');
  const width = 760; const height = 300; const { pad, x, y } = chartScales(width, height, 40, 110, debtData);
  const points = debtData.map((value, index) => `${x(index)},${y(value)}`).join(' ');
  const area = `${pad.left},${height - pad.bottom} ${points} ${x(debtData.length - 1)},${height - pad.bottom}`;
  const grid = [40, 60, 80, 100].map(value => `<line class="chart-grid" x1="${pad.left}" x2="${width - pad.right}" y1="${y(value)}" y2="${y(value)}"/><text class="chart-label" x="3" y="${y(value) + 3}">${value}</text>`).join('');
  const labels = years.map((year, index) => index % 3 === 0 ? `<text class="chart-label" x="${x(index)}" y="${height - 6}" text-anchor="middle">${year}</text>` : '').join('');
  const dots = debtData.map((value, index) => `<circle class="chart-point" cx="${x(index)}" cy="${y(value)}" r="3.2"/>`).join('');
  svg.innerHTML = `${grid}${labels}<line class="mean-line" x1="${pad.left}" x2="${width - pad.right}" y1="${y(mean)}" y2="${y(mean)}"/><polygon class="chart-area" points="${area}"/><polyline class="chart-path" points="${points}"/>${dots}`;
}

function drawHistogram() {
  const bins = [debtData.filter(value => value < 60).length, debtData.filter(value => value >= 60 && value < 75).length, debtData.filter(value => value >= 75 && value < 90).length, debtData.filter(value => value >= 90 && value < 105).length, debtData.filter(value => value >= 105).length];
  document.getElementById('histogram').innerHTML = bins.map(count => `<div class="hist-bar" data-count="${count}" style="height:${Math.max(count * 20, 10)}%"></div>`).join('');
  const intervals = ['< 60', '60–74', '75–89', '90–104', '≥ 105'];
  document.getElementById('frequencyTable').innerHTML = bins.map((count, index) => `<tr><td>${intervals[index]}</td><td>${count}</td><td>${format((count / debtData.length) * 100)}%</td></tr>`).join('');
}

function regression() {
  const xMean = growthData.reduce((sum, value) => sum + value, 0) / growthData.length;
  const covariance = growthData.reduce((sum, value, index) => sum + (value - xMean) * (debtData[index] - mean), 0);
  const xVariance = growthData.reduce((sum, value) => sum + (value - xMean) ** 2, 0);
  const slope = covariance / xVariance; const intercept = mean - slope * xMean;
  const correlation = covariance / Math.sqrt(xVariance * debtData.reduce((sum, value) => sum + (value - mean) ** 2, 0));
  setText('slopeValue', `${slope < 0 ? '−' : ''}${format(Math.abs(slope), 2)}x + ${format(intercept)}`);
  setText('correlationValue', format(correlation, 2)); setText('rSquaredValue', `${format(correlation ** 2 * 100)}%`);
  drawScatter(slope, intercept);
}

function drawScatter(slope, intercept) {
  const svg = document.getElementById('scatterChart'); const width = 760; const height = 300;
  const { pad, x, y } = chartScales(width, height, 40, 110, debtData);
  const xMin = -1; const xMax = 6; const xScale = value => pad.left + ((value - xMin) / (xMax - xMin)) * (width - pad.left - pad.right);
  const grid = [40, 60, 80, 100].map(value => `<line class="chart-grid" x1="${pad.left}" x2="${width - pad.right}" y1="${y(value)}" y2="${y(value)}"/><text class="chart-label" x="3" y="${y(value) + 3}">${value}</text>`).join('');
  const points = growthData.map((value, index) => `<circle class="chart-point" cx="${xScale(value)}" cy="${y(debtData[index])}" r="4"/>`).join('');
  const lineStart = slope * xMin + intercept; const lineEnd = slope * xMax + intercept;
  svg.innerHTML = `${grid}<line class="mean-line" style="stroke:var(--coral);stroke-width:2" x1="${xScale(xMin)}" y1="${y(lineStart)}" x2="${xScale(xMax)}" y2="${y(lineEnd)}"/>${points}<text class="chart-label" x="${pad.left}" y="${height - 7}">growth rate %</text>`;
}

function normalCdf(value) { return 0.5 * (1 + Math.erf(value / Math.sqrt(2))); }
function calculateZ() {
  const value = Number(document.getElementById('zInput').value); const z = (value - mean) / standardDeviation; const probability = normalCdf(z);
  const tailProbability = 1 - probability;
  const riskBand = tailProbability >= 0.35 ? 'Higher exposure' : tailProbability >= 0.15 ? 'Watch closely' : 'Lower exposure';
  setText('zScore', `${z < 0 ? '−' : ''}${format(Math.abs(z), 2)}`);
  setText('riskProbability', `${format(tailProbability * 100)}%`);
  setText('riskBand', riskBand);
}

// Math.erf is not supported in every browser, so use a compact normal-CDF approximation.
Math.erf = Math.erf || function (x) { const sign = x < 0 ? -1 : 1; x = Math.abs(x); const a1 = 0.254829592; const a2 = -0.284496736; const a3 = 1.421413741; const a4 = -1.453152027; const a5 = 1.061405429; const p = 0.3275911; const t = 1 / (1 + p * x); return sign * (1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x)); };
drawLineChart(); drawHistogram(); regression(); calculateZ();
document.getElementById('calculateButton').addEventListener('click', calculateZ);
document.getElementById('zInput').addEventListener('keydown', event => { if (event.key === 'Enter') calculateZ(); });
