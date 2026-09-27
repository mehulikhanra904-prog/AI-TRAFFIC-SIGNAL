const $ = id => document.getElementById(id);
const lanes = ['A','B','C','D'].map((id,i)=>({id, vehicles:[47,8,31,4][i], queue_length:[29,6,20,3][i], avg_speed:8, avg_wait:20}));
const base = location.port === '8000' ? '' : 'http://127.0.0.1:8000';
let emergency = {active:false}, greens = [], phase = 0, remaining = 0, online = false, busy = false;
async function request(path, data) {
  const response = await fetch(base + path, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data || {}), signal:AbortSignal.timeout(5000)});
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}
function render() {
  const active = online ? (emergency.active ? emergency.lane : lanes[phase].id) : null;
  $('lanes').innerHTML = lanes.map((lane,i)=>`<div class="lane"><div class="lane-name">LANE ${lane.id}<small>${lane.vehicles} vehicles</small></div><div class="bar"><span style="width:${lane.vehicles/70*100}%"></span></div><div class="timing">${emergency.active ? (active===lane.id?'GREEN':'RED') : (greens[i] || '—')+' SEC'}</div></div>`).join('');
  ['North','East','South','West'].forEach((name,i)=>$('light'+name).classList.toggle('active', active===lanes[i].id));
  $('modeLabel').textContent = !online ? 'OFFLINE' : emergency.active ? 'EMERGENCY' : 'OPTIMIZED';
  $('modeCaption').textContent = online ? 'Trained model connected' : 'API unavailable — controls paused';
  $('signalTag').textContent = !online ? 'NO CONNECTION' : emergency.active ? 'PRIORITY' : 'NORMAL AI';
  $('phase').textContent = active ? `LANE ${active}` : 'PAUSED';
  $('remaining').textContent = emergency.active ? 'PRIORITY' : remaining+'s';
  $('emergencyText').textContent = emergency.active ? `Simulated ambulance on Lane ${emergency.lane}, ${emergency.distance} m away. Click Clear emergency after passage.` : 'No active emergency. Simulated traffic inputs feed the trained model.';
  $('emergencyBtn').textContent = emergency.active ? 'Clear emergency' : 'Simulate ambulance';
  $('emergencyBtn').classList.toggle('active', emergency.active);
  $('emergencyBtn').disabled = busy || !online;
  $('emergencyLane').disabled = busy || emergency.active;
}
async function refresh() {
  if (busy) return;
  busy = true;
  try {
    const result = await request('/api/optimize', {lanes});
    greens = result.green_seconds; emergency = result.emergency; online = true;
    if (remaining <= 0) remaining = greens[phase];
    $('eventLog').textContent = 'Model prediction received: '+new Date().toLocaleTimeString();
  } catch(error) { online = false; $('eventLog').textContent = error.message+' — start backend on port 8000'; }
  finally { busy = false; render(); }
}
$('emergencyBtn').onclick = async () => {
  if (busy || !online) return;
  busy = true; render();
  try {
    const clearing = emergency.active;
    const result = await request(clearing ? '/api/emergency/clear' : '/api/emergency/activate', {lane:$('emergencyLane').value, distance:120, vehicle:'Ambulance'});
    emergency = result.emergency;
    if (clearing) remaining = greens[phase];
    $('eventLog').textContent = result.message;
  } catch(error) { online = false; $('eventLog').textContent = error.message; }
  finally { busy = false; render(); }
};
setInterval(()=>{
  $('clock').textContent = new Date().toLocaleTimeString();
  if (online && !emergency.active && --remaining <= 0) {phase=(phase+1)%4; remaining=greens[phase];}
  render();
},1000);
setInterval(refresh,5000);
render(); refresh();
