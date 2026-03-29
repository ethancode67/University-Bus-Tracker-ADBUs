const API_URL = 'http://127.0.0.1:8000/api/bus/1/';
const TICK_MS = 10000;

let STOPS = [];
let segmentIdx = 0;
let segmentT   = 0;
let routeInitialized = false;

// ─── Leaflet map ───────────────────────────────────────────────────────────────
const map = L.map('map', {
  zoomControl: true,
  attributionControl: false,
}).setView([26.103373, 91.593815], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

// Placeholders — built after first API response
let routeLine    = null;
let stopMarkers  = [];
let busMarker    = null;

// ─── Icon helpers ──────────────────────────────────────────────────────────────
function makeStopIcon(passed, current) {
  const bg     = passed  ? '#00e5a0' : current ? '#ffffff' : '#1e2128';
  const border = passed  ? '#00e5a0' : current ? '#00e5a0' : '#6b7280';
  return L.divIcon({
    className: '',
    html: `<div style="
      width:12px;height:12px;border-radius:50%;
      background:${bg};border:2.5px solid ${border};
      box-shadow:0 1px 6px rgba(0,0,0,0.6);
    "></div>`,
    iconAnchor: [6, 6],
  });
}

function makeBusIcon() {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:36px;height:36px;border-radius:50%;
      background:rgba(0,229,160,0.15);
      border:2px solid rgba(0,229,160,0.5);
      display:flex;align-items:center;justify-content:center;
      box-shadow:0 0 16px rgba(0,229,160,0.3);
    ">
      <div style="
        width:24px;height:24px;border-radius:50%;
        background:#00e5a0;border:2px solid #fff;
        display:flex;align-items:center;justify-content:center;
        font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,0.4);
      ">🚌</div>
    </div>`,
    iconAnchor: [18, 18],
  });
}

// ─── Build map elements once on first load ─────────────────────────────────────
function initRoute() {
  // Route polyline
  const routeCoords = STOPS.map(s => [s.lat, s.lng]);
  if (routeLine) map.removeLayer(routeLine);
  routeLine = L.polyline(routeCoords, {
    color: '#00e5a0',
    weight: 4,
    opacity: 0.7,
    dashArray: '8, 6',
  }).addTo(map);
  map.fitBounds(routeLine.getBounds(), { padding: [40, 40] });

  // Stop markers
  stopMarkers.forEach(m => map.removeLayer(m));
  stopMarkers = STOPS.map((stop, i) =>
    L.marker([stop.lat, stop.lng], { icon: makeStopIcon(false, i === 0) })
      .addTo(map)
      .bindTooltip(stop.name, { direction: 'top', offset: [0, -8] })
  );

  // Bus marker
  if (busMarker) map.removeLayer(busMarker);
  busMarker = L.marker([STOPS[0].lat, STOPS[0].lng], {
    icon: makeBusIcon(),
    zIndexOffset: 1000,
  }).addTo(map);

  routeInitialized = true;
}

// ─── Position helper ───────────────────────────────────────────────────────────
function lerp(a, b, t) { return a + (b - a) * t; }

function getBusLatLng() {
  const from = STOPS[segmentIdx];
  const to   = STOPS[Math.min(segmentIdx + 1, STOPS.length - 1)];
  return [
    lerp(from.lat, to.lat, segmentT),
    lerp(from.lng, to.lng, segmentT),
  ];
}

// ─── Fetch from Django API ─────────────────────────────────────────────────────
async function fetchBusData() {
  try {
    const res  = await fetch(API_URL);
    if (!res.ok) throw new Error(`Server returned ${res.status}`);
    const data = await res.json();

    STOPS      = data.stops;
    segmentIdx = data.location.segment_index;
    segmentT   = data.location.segment_t;

    if (!routeInitialized) {
      initRoute();
    }

    // Update bus marker position
    const pos = getBusLatLng();
    busMarker.setLatLng(pos);
    map.panTo(pos, { animate: true, duration: 1.2 });

    // Update stop marker icons
    stopMarkers.forEach((m, i) => {
      m.setIcon(makeStopIcon(i < segmentIdx, i === segmentIdx));
    });

    updatePanel();
    document.getElementById('last-updated').textContent = 'just now';

  } catch (err) {
    console.error('Failed to fetch bus data:', err);
    document.getElementById('last-updated').textContent = 'connection error';
  }
}

// ─── Panel ─────────────────────────────────────────────────────────────────────
function updatePanel() {
  const nextIdx  = Math.min(segmentIdx + 1, STOPS.length - 1);
  const nextStop = STOPS[nextIdx];
  const remaining = 1 - segmentT;
  const etaMin   = Math.max(1, Math.round(remaining * 5 + 1));

  document.getElementById('next-stop-name').textContent = nextStop.name;
  document.getElementById('eta-time').innerHTML = `${etaMin}<span>min away</span>`;
  document.getElementById('next-stop-dist').textContent = `~${(remaining * 0.6).toFixed(1)} km away`;

  // Stops list
  const list = document.getElementById('stops-list');
  list.innerHTML = '';
  STOPS.forEach((stop, i) => {
    const isDone    = i < segmentIdx;
    const isCurrent = i === segmentIdx;
    const isNext    = i === segmentIdx + 1;
    const isLast    = i === STOPS.length - 1;

    let badge = '';
    if (isDone)         badge = '<span class="stop-badge badge-done">Passed</span>';
    else if (isCurrent) badge = '<span class="stop-badge badge-current">At stop</span>';
    else if (isNext)    badge = '<span class="stop-badge badge-next">Next</span>';

    const item = document.createElement('div');
    item.className = 'stop-item';
    item.innerHTML = `
      <div class="stop-marker-col">
        <div class="stop-dot ${isDone ? 'done' : isCurrent ? 'current' : ''}"></div>
        ${!isLast ? `<div class="stop-line ${isDone ? 'done' : ''}"></div>` : ''}
      </div>
      <div class="stop-info">
        <div class="stop-name ${isDone ? 'muted' : isCurrent ? 'active' : ''}">${stop.name}</div>
        <div class="stop-time">${stop.eta}</div>
        ${badge}
      </div>
    `;
    list.appendChild(item);
  });
}

// ─── Toast ──────────────────────────────────────────────────────────────────────
let toastTimer;
function showToast(msg) {
  document.getElementById('toast-msg').textContent = msg;
  const el = document.getElementById('toast');
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 3000);
}

// ─── Init ───────────────────────────────────────────────────────────────────────
fetchBusData();
setInterval(fetchBusData, TICK_MS);