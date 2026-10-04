const sampleElection = {
  candidates: [
    { id: 'C-01', name: 'Anudeep', party: 'GREEN FUTURE', description: 'Building greener streets and stronger neighbourhoods.', symbol: '✳' },
    { id: 'C-02', name: 'Hrithil', party: 'PEOPLE FIRST', description: 'Making public services work for everyone.', symbol: '◉' },
    { id: 'C-03', name: 'Nihara', party: 'COMMON GROUND', description: 'Bringing fresh ideas and open conversations.', symbol: '↗' }
  ], voters: ['VOTER-001', 'VOTER-002', 'VOTER-003', 'VOTER-004', 'VOTER-005', 'VOTER-006']
};
const STORAGE_KEY = 'janmat-election-v1';
let election = loadElection();
function loadElection() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved?.candidates?.length && Array.isArray(saved.voters) && Array.isArray(saved.votes)) return saved;
  } catch (error) { /* Start with the sample election if local data is unavailable. */ }
  return { ...structuredClone(sampleElection), votes: [] };
}
function saveElection() { localStorage.setItem(STORAGE_KEY, JSON.stringify(election)); }
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]); }
function render() {
  const grid = document.querySelector('#candidateGrid');
  const options = document.querySelector('#voteOptions');
  if (!election.candidates.length) {
    grid.innerHTML = '<div class="empty-card">The ballot is being prepared. The election organiser can add candidates below.</div>';
    options.innerHTML = '<p class="card-sub">No candidates are on the ballot yet.</p>';
  } else {
    grid.innerHTML = election.candidates.map((candidate, i) => `<article class="candidate-card"><div class="candidate-top"><span class="candidate-number">CANDIDATE No. ${String(i + 1).padStart(2, '0')}</span><span class="candidate-symbol">${escapeHtml(candidate.symbol || '✳')}</span></div><h3>${escapeHtml(candidate.name)}</h3><div class="candidate-party">${escapeHtml(candidate.party)}</div><p class="candidate-desc">${escapeHtml(candidate.description)}</p><span class="candidate-id">${escapeHtml(candidate.id)}</span></article>`).join('');
    options.innerHTML = election.candidates.map((candidate, i) => `<label class="vote-option"><input type="radio" name="candidate" value="${escapeHtml(candidate.id)}" required><span>${escapeHtml(candidate.name)}</span><small>${escapeHtml(candidate.party)}</small></label>`).join('');
  }
  const counts = Object.fromEntries(election.candidates.map(c => [c.id, 0]));
  election.votes.forEach(vote => { if (counts[vote.candidateId] !== undefined) counts[vote.candidateId]++; });
  const max = Math.max(0, ...Object.values(counts));
  document.querySelector('#resultsList').innerHTML = election.candidates.length ? election.candidates.map(candidate => {
    const count = counts[candidate.id];
    const width = max ? Math.max(count ? 5 : 0, Math.round(count / max * 100)) : 0;
    return `<div class="result-row"><div class="result-name">${escapeHtml(candidate.name)}<small>${escapeHtml(candidate.party)}</small></div><div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div><div class="result-count">${count}</div></div>`;
  }).join('') : '<div class="empty-card">No candidates to count yet.</div>';
  document.querySelector('#totalVotes').textContent = `${election.votes.length} ${election.votes.length === 1 ? 'VOTE' : 'VOTES'} CAST`;
  const leaders = election.candidates.filter(c => counts[c.id] === max && max > 0);
  document.querySelector('#winnerLine').textContent = !election.votes.length ? 'Waiting for the first vote…' : leaders.length > 1 ? `Currently tied: ${leaders.map(c => c.name).join(' and ')}` : `${leaders[0].name} is currently leading`;
  document.querySelector('#setupCandidates').value = election.candidates.map(c => [c.id, c.name, c.party, c.description].join(', ')).join('\n');
  document.querySelector('#setupVoters').value = election.voters.join('\n');
}
document.querySelector('#voteForm').addEventListener('submit', event => {
  event.preventDefault();
  const voterId = document.querySelector('#voterId').value.trim();
  const candidateId = document.querySelector('input[name="candidate"]:checked')?.value;
  const receipt = document.querySelector('#receipt');
  let message;
  if (!election.voters.some(id => id.toLowerCase() === voterId.toLowerCase())) message = 'Voter ID not recognised. Please check with your election organiser.';
  else if (election.votes.some(vote => vote.voterId.toLowerCase() === voterId.toLowerCase())) message = 'This voter ID has already been used. Each person may vote once.';
  else if (!candidateId) message = 'Please select one candidate before submitting your ballot.';
  else {
    const receiptCode = `JM-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
    election.votes.push({ voterId, candidateId, receiptCode, time: new Date().toISOString() });
    saveElection(); render();
    receipt.innerHTML = `<strong>✓ Your vote has been recorded.</strong><br>Receipt: ${receiptCode} · Your choice remains private.`;
    receipt.classList.add('visible'); event.target.reset();
    showToast('Your voice has been counted. Thank you.');
    return;
  }
  receipt.textContent = message; receipt.classList.add('visible');
});
document.querySelector('#setupForm').addEventListener('submit', event => {
  event.preventDefault();
  const candidates = document.querySelector('#setupCandidates').value.split(/\r?\n/).map(line => line.trim()).filter(Boolean).map(line => {
    const [id, name, party, ...description] = line.split(',').map(part => part.trim());
    return { id, name, party, description: description.join(', ') || 'A candidate in this election.', symbol: '✳' };
  });
  const voters = [...new Set(document.querySelector('#setupVoters').value.split(/\r?\n/).map(id => id.trim()).filter(Boolean))];
  if (candidates.some(c => !c.id || !c.name || !c.party) || new Set(candidates.map(c => c.id.toLowerCase())).size !== candidates.length) { showToast('Check each candidate line: ID, Name, Party, description.'); return; }
  if (candidates.length < 1 || voters.length < 1) { showToast('Add at least one candidate and one voter ID.'); return; }
  election = { candidates, voters, votes: election.votes.filter(vote => voters.some(id => id.toLowerCase() === vote.voterId.toLowerCase()) && candidates.some(c => c.id === vote.candidateId)) };
  saveElection(); render(); showToast('Election setup saved on this device.');
});
document.querySelector('#resetDemo').addEventListener('click', () => {
  election = { ...structuredClone(sampleElection), votes: [] }; saveElection(); render(); showToast('Sample election restored.');
});
let toastTimer;
function showToast(message) {
  const toast = document.querySelector('#toast'); toast.textContent = message; toast.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}
render();
