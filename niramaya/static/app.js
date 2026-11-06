'use strict';
const byId = id => document.getElementById(id);
const history = [];
const tabs = [...document.querySelectorAll('[data-panel]')];
function show(panel) {
  for (const tab of tabs) {
    const active = tab.dataset.panel === panel;
    tab.setAttribute('aria-pressed', String(active));
    byId(tab.dataset.panel).hidden = !active;
  }
}
tabs.forEach(tab => tab.onclick = () => show(tab.dataset.panel));

async function api(path, options) {
  const response = await fetch(path, {...options, signal: AbortSignal.timeout(30000)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'The service could not respond.');
  return data;
}
api('/healthz').then(data => {
  byId('model-status').textContent = data.chat_configured ? 'Live model configured' : 'Live chat unavailable';
}).catch(() => { byId('model-status').textContent = 'Service unavailable'; });

function element(tag, text, parent) {
  const node = document.createElement(tag);
  node.textContent = text;
  parent.append(node);
  return node;
}
function save(label, text, parent) {
  const button = element('button', label, parent);
  button.type = 'button';
  button.onclick = () => {
    byId('notes').value += '\n' + text + '\n';
    show('visit');
    byId('notes').focus();
  };
}
function paperCard(paper, i, container) {
  const card = element('article', '', container);
  card.className = 'paper';
  element('strong', `[${i + 1}] ${paper.title}`, card);
  element('p', [paper.journal, paper.year].filter(Boolean).join(' · '), card);
  const details = element('details', '', card);
  element('summary', 'Read abstract', details);
  element('p', paper.abstract || 'No abstract provided.', details);
  const link = element('a', 'Open PubMed record ↗', card);
  link.href = paper.url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  card.append(document.createTextNode('  '));
  save('Add source to notes', paper.title + ' — ' + paper.url, card);
}
let chatVersion = 0;
const chatMode = byId('chat-mode');
chatMode.onchange = () => {
  const evidence = chatMode.value === 'evidence';
  byId('topic-field').hidden = !evidence;
  byId('topic').disabled = !evidence;
  byId('topic').required = evidence;
  byId('clear').click();
};
byId('ask').onsubmit = async event => {
  event.preventDefault();
  const question = byId('question').value.trim();
  const form = event.currentTarget;
  const button = form.querySelector('[type=submit]');
  const version = chatVersion;
  button.disabled = true;
  byId('chat-status').textContent = chatMode.value === 'direct' ? 'Preparing a response…' : 'Searching literature and preparing a response…';
  try {
    const data = await api('/api/chat', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question, mode: chatMode.value, topic: byId('topic').value.trim(), language: byId('language').value, history: history.slice(-4)})});
    if (version !== chatVersion) return;
    const message = element('article', '', byId('messages'));
    message.className = 'message';
    element('strong', question, message);
    element('p', 'Response · ' + data.model, message);
    element('p', data.answer, message);
    save('Add question to visit notes', question, message);
    if (data.papers.length) {
      element('h3', 'Retrieved evidence', message);
      data.papers.forEach((paper, i) => paperCard(paper, i, message));
    }
    history.push({role:'user',text:question},{role:'assistant',text:data.answer.slice(0,1800)});
    byId('question').value = '';
    byId('chat-status').textContent = 'Response ready.';
  } catch (error) {
    if (version === chatVersion) byId('chat-status').textContent = error.message;
  } finally {
    button.disabled = false;
  }
};
byId('clear').onclick = () => {
  chatVersion++;
  history.length = 0;
  byId('messages').replaceChildren();
  byId('chat-status').textContent = '';
};
byId('search').onsubmit = async event => {
  event.preventDefault();
  const button = event.currentTarget.querySelector('button');
  const results = byId('papers');
  button.disabled = true;
  results.textContent = 'Searching…';
  try {
    const data = await api('/api/research?q=' + encodeURIComponent(byId('query').value.trim()));
    results.textContent = data.papers.length ? '' : 'No papers found. Try different search terms.';
    data.papers.forEach((paper, i) => paperCard(paper, i, results));
  } catch (error) {
    results.textContent = error.message;
  } finally {
    button.disabled = false;
  }
};
byId('download').onclick = () => {
  const url = URL.createObjectURL(new Blob([byId('notes').value], {type:'text/plain;charset=utf-8'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'niramaya-visit-notes.txt';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
