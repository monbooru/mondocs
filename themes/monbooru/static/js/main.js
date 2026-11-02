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

var themeIcon = document.querySelector('link[rel="icon"]');
var darkIcon = themeIcon && themeIcon.getAttribute('href');
function applyTheme(pick) {
  var light = pick === 'light';
  document.documentElement.dataset.theme = light ? 'light' : 'dark';
  document.querySelectorAll('#theme-switch button').forEach(function (b) {
    b.setAttribute('aria-pressed', String((b.dataset.pick === 'light') === light));
  });
  if (themeIcon) themeIcon.setAttribute('href', light ? darkIcon.replace(/favicon\.png$/, 'light/favicon.png') : darkIcon);
}
var storedTheme = null;
try { storedTheme = localStorage.getItem('mondocs-theme'); } catch (e) {}
applyTheme(storedTheme);
addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('#theme-switch button');
  if (!b) return;
  try { localStorage.setItem('mondocs-theme', b.dataset.pick); } catch (err) {}
  applyTheme(b.dataset.pick);
});

var siteRoot = new URL('../', document.currentScript.src).href;
var searchInput = document.getElementById('search-input');
var searchResults = document.getElementById('search-results');
var searchSelected = -1;
var searchLoading = false;

function loadSearchIndex() {
  if (window.searchIndex || searchLoading) return;
  searchLoading = true;
  var script = document.createElement('script');
  script.src = siteRoot + 'search-index.js';
  script.onload = function () { showSearchResults(); };
  script.onerror = function () { searchLoading = false; };
  document.head.appendChild(script);
}

function searchTerms() {
  return searchInput.value.toLowerCase().split(/\s+/).filter(Boolean);
}

// 2 when the term starts a word, 1 when it is inside one, 0 when it is absent.
function termScore(text, term) {
  var at = text.indexOf(term);
  if (at < 0) return 0;
  return at === 0 || !/[a-z0-9]/.test(text.charAt(at - 1)) ? 2 : 1;
}

function runSearch(terms) {
  var hits = [];
  window.searchIndex.forEach(function (page) {
    var title = page.t.toLowerCase();
    var best = [];
    page.s.forEach(function (section) {
      var heading = section.h.toLowerCase();
      var text = section.x.toLowerCase();
      var score = section.i ? 0 : 1;
      var all = terms.every(function (term) {
        var inTitle = termScore(title, term);
        var inHeading = termScore(heading, term);
        var inText = termScore(text, term);
        score += inTitle * 8 + inHeading * 4 + inText;
        return inTitle || inHeading || inText;
      });
      if (all) best.push({ page: page, section: section, score: score });
    });
    best.sort(function (a, b) { return b.score - a.score; });
    hits = hits.concat(best.slice(0, 2));
  });
  hits.sort(function (a, b) { return b.score - a.score; });
  return hits.slice(0, 8);
}

function appendMarked(parent, text, terms) {
  var pattern = terms.map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|');
  text.split(new RegExp('(' + pattern + ')', 'gi')).forEach(function (part, i) {
    if (i % 2) {
      var mark = document.createElement('mark');
      mark.textContent = part;
      parent.appendChild(mark);
    } else if (part) {
      parent.appendChild(document.createTextNode(part));
    }
  });
}

function searchSnippet(text, terms) {
  var lower = text.toLowerCase();
  var at = -1;
  terms.forEach(function (term) {
    var found = lower.indexOf(term);
    if (found >= 0 && (at < 0 || found < at)) at = found;
  });
  var start = Math.max(0, at - 40);
  if (start > 0) start = text.indexOf(' ', start) + 1;
  var end = start + 140;
  return (start > 0 ? '...' : '') + text.slice(start, end) + (end < text.length ? '...' : '');
}

function searchSpan(className, text, terms) {
  var span = document.createElement('span');
  span.className = className;
  if (terms) appendMarked(span, text, terms);
  else span.textContent = text;
  return span;
}

function closeSearch() {
  searchResults.hidden = true;
  searchInput.setAttribute('aria-expanded', 'false');
  searchInput.removeAttribute('aria-activedescendant');
  searchSelected = -1;
}

function showSearchResults() {
  var terms = searchTerms();
  if (!terms.length || !window.searchIndex) return closeSearch();
  searchResults.textContent = '';
  searchSelected = -1;
  searchInput.removeAttribute('aria-activedescendant');
  var hits = runSearch(terms);
  hits.forEach(function (hit, i) {
    var link = document.createElement('a');
    link.className = 'search-hit';
    link.id = 'search-hit-' + i;
    link.setAttribute('role', 'option');
    link.setAttribute('aria-selected', 'false');
    link.href = siteRoot + hit.page.u + (hit.section.i ? '#' + hit.section.i : '');
    var title = hit.page.t + (hit.section.h ? ' > ' + hit.section.h : '');
    link.appendChild(searchSpan('search-hit-title', title, terms));
    if (hit.page.p && hit.page.p.length) link.appendChild(searchSpan('search-hit-path', hit.page.p.join(' > ')));
    if (hit.section.x) link.appendChild(searchSpan('search-hit-text', searchSnippet(hit.section.x, terms), terms));
    searchResults.appendChild(link);
  });
  if (!hits.length) {
    var empty = document.createElement('div');
    empty.className = 'search-empty';
    empty.textContent = 'nothing found';
    searchResults.appendChild(empty);
  }
  searchResults.hidden = false;
  searchInput.setAttribute('aria-expanded', 'true');
}

function selectSearchHit(step) {
  var hits = searchResults.querySelectorAll('.search-hit');
  if (!hits.length) return;
  if (searchSelected >= 0) hits[searchSelected].setAttribute('aria-selected', 'false');
  searchSelected = searchSelected < 0 && step < 0 ? hits.length - 1 : (searchSelected + step + hits.length) % hits.length;
  var hit = hits[searchSelected];
  hit.setAttribute('aria-selected', 'true');
  hit.scrollIntoView({ block: 'nearest' });
  searchInput.setAttribute('aria-activedescendant', hit.id);
}

searchInput.addEventListener('focus', function () {
  loadSearchIndex();
  showSearchResults();
});
searchInput.addEventListener('input', showSearchResults);
searchInput.addEventListener('keydown', function (e) {
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    if (searchResults.hidden) showSearchResults();
    selectSearchHit(e.key === 'ArrowDown' ? 1 : -1);
  } else if (e.key === 'Enter') {
    var hit = searchResults.querySelectorAll('.search-hit')[Math.max(searchSelected, 0)];
    if (hit && !searchResults.hidden) {
      closeSearch();
      location.href = hit.href;
    }
  } else if (e.key === 'Escape') {
    if (searchResults.hidden) searchInput.blur();
    closeSearch();
  }
});
searchResults.addEventListener('click', function () { closeSearch(); });
addEventListener('click', function (e) {
  if (!e.target.closest('#search')) closeSearch();
});
addEventListener('keydown', function (e) {
  if ((e.key !== 's' && e.key !== '/') || e.ctrlKey || e.metaKey || e.altKey) return;
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
  e.preventDefault();
  searchInput.focus();
  searchInput.select();
});
