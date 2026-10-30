addEventListener('keydown', function (e) {
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.lightbox-state:checked').forEach(function (c) { c.checked = false; });
});

function selectAndCopy(text) {
  var field = document.createElement('textarea');
  field.value = text;
  field.setAttribute('readonly', '');
  field.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0';
  document.body.appendChild(field);
  field.select();
  var copied = false;
  try { copied = document.execCommand('copy'); } catch (e) { copied = false; }
  document.body.removeChild(field);
  return copied ? Promise.resolve() : Promise.reject();
}

function copy(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(text).catch(function () { return selectAndCopy(text); });
  }
  return selectAndCopy(text);
}

addEventListener('click', function (e) {
  var link = e.target.closest && e.target.closest('a.anchor');
  if (!link) return;
  e.preventDefault();
  copy(link.href).then(function () {
    link.classList.add('copied');
    setTimeout(function () { link.classList.remove('copied'); }, 1200);
  }, function () {});
  try { history.replaceState(null, '', link.getAttribute('href')); } catch (e) {}
});

var themeIcons = Array.prototype.map.call(document.querySelectorAll('link[rel="icon"]'), function (l) { return l.getAttribute('href'); });
function applyTheme(pick) {
  var light = pick ? pick === 'light' : matchMedia('(prefers-color-scheme: light)').matches;
  if (pick) document.documentElement.dataset.theme = pick;
  document.querySelectorAll('#theme-switch button').forEach(function (b) {
    b.setAttribute('aria-pressed', String((b.dataset.pick === 'light') === light));
  });
  if (pick) document.querySelectorAll('link[rel="icon"]').forEach(function (l) {
    l.setAttribute('href', themeIcons[light ? 1 : 0]);
  });
}
var storedTheme = null;
try { storedTheme = localStorage.getItem('mondocs-theme'); } catch (e) {}
applyTheme(storedTheme);
matchMedia('(prefers-color-scheme: light)').addEventListener('change', function () {
  if (!document.documentElement.dataset.theme) applyTheme(null);
});
addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('#theme-switch button');
  if (!b) return;
  try { localStorage.setItem('mondocs-theme', b.dataset.pick); } catch (err) {}
  applyTheme(b.dataset.pick);
});
