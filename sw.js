const CACHE_NAME = 'stlite-cache-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './app.py',
  './manifest.json',
  'https://cdn.jsdelivr.net/npm/@stlite/mountable/build/stlite.css',
  'https://cdn.jsdelivr.net/npm/@stlite/mountable/build/stlite.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});