const $ = selector => document.querySelector(selector);
const number = new Intl.NumberFormat('pt-BR');
const state = { snapshot: null, visible: 8 };

function create(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function filtered() {
  const query = $('#search').value.trim().toUpperCase();
  const status = $('#status').value;
  return state.snapshot.control.filter(row => row.sourceKey.toUpperCase().includes(query) &&
    (status === 'all' || row.status === status));
}

function renderTable() {
  const records = filtered();
  const tbody = $('#rows');
  tbody.replaceChildren();
  for (const item of records.slice(0, state.visible)) {
    const tr = create('tr');
    for (const value of [item.sourceKey, item.entity, item.unit, item.history.join(' → ')]) tr.append(create('td', value));
    const status = create('td');
    status.append(create('span', item.status === 'EXECUTADO' ? 'Executado' : 'Para revisão', `status-pill ${item.status === 'EXECUTADO' ? 'ok' : 'error'}`));
    tr.append(status);
    const action = create('td');
    const button = create('button', 'Ver trilha ↗', 'detail-button');
    button.addEventListener('click', () => showDetail(item));
    action.append(button);
    tr.append(action);
    tbody.append(tr);
  }
  if (!records.length) {
    const tr = create('tr');
    const td = create('td', 'Nenhum registro corresponde aos filtros selecionados.');
    td.colSpan = 6;
    tr.append(td);
    tbody.append(tr);
  }
  $('#count').textContent = `${Math.min(state.visible, records.length)} de ${records.length} registros`;
  $('#more').hidden = state.visible >= records.length;
}

function showDetail(item) {
  const root = $('#detail-content');
  root.replaceChildren(create('h2', item.sourceKey), create('p', `${item.entity} · ${item.unit} · dado 100% fictício`));
  root.append(create('h3', 'Histórico de estados'));
  const history = create('div', undefined, 'history');
  for (const step of item.history) history.append(create('span', step));
  root.append(history, create('h3', 'Resultado registrado'), create('div', item.message || 'Sem mensagem adicional.', 'message'));
  root.append(create('h3', 'Payload ilustrativo'));
  root.append(create('pre', item.payload ? JSON.stringify(item.payload, null, 2) : 'Nenhum payload gerado: registro bloqueado pela validação.'));
  $('#detail').showModal();
}

function render() {
  const data = state.snapshot;
  const metrics = data.metrics;
  for (const key of ['extracted', 'validated', 'completed', 'errors', 'batches']) $(`#${key}`).textContent = number.format(metrics[key]);
  const rate = metrics.completed / metrics.extracted * 100;
  $('#rate').textContent = `${number.format(Math.round(rate))}%`;
  $('#donut').style.setProperty('--done', `${rate}%`);
  $('#legend-completed').textContent = number.format(metrics.completed);
  $('#legend-errors').textContent = number.format(metrics.errors);
  $('#equation').textContent = `${number.format(metrics.extracted)} extraídos = ${number.format(metrics.completed)} executados + ${number.format(metrics.errors)} para revisão`;
  const phases = $('#phases');
  phases.replaceChildren();
  for (const [index, phaseName] of data.phases.entries()) {
    const phase = create('div', undefined, 'phase');
    phase.append(create('div', '✓', 'phase-circle'), create('b', phaseName), create('small', `Etapa 0${index + 1}`));
    phases.append(phase);
  }
  const entities = $('#entity-list');
  entities.replaceChildren();
  for (const item of data.byEntity) {
    const article = create('article', undefined, 'entity');
    const heading = create('div', undefined, 'entity-head');
    heading.append(create('b', item.entity), create('span', `${number.format(item.completed)} / ${number.format(item.extracted)}`));
    const track = create('div', undefined, 'track');
    const fill = create('div');
    fill.style.width = `${item.completed / item.extracted * 100}%`;
    track.append(fill);
    article.append(heading, create('p', `${item.errors} para revisão · ${item.extracted} extraídos`), track);
    entities.append(article);
  }
  renderTable();
}

async function init() {
  try {
    const response = await fetch('data/snapshot.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.snapshot = await response.json();
    $('#search').addEventListener('input', () => { state.visible = 8; renderTable(); });
    $('#status').addEventListener('change', () => { state.visible = 8; renderTable(); });
    $('#more').addEventListener('click', () => { state.visible += 8; renderTable(); });
    $('#close').addEventListener('click', () => $('#detail').close());
    render();
  } catch (error) {
    $('#rows').replaceChildren(create('tr'));
    $('#count').textContent = 'Falha ao carregar os dados da demonstração.';
    console.error(error);
  }
}

init();
