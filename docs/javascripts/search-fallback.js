(function () {
  var input = document.querySelector('[data-md-component="search-query"]');
  var result = document.querySelector('[data-md-component="search-result"]');
  if (!input || !result) return;

  var meta = result.querySelector('.md-search-result__meta');
  var list = result.querySelector('.md-search-result__list');
  if (!meta || !list) return;

  var bundle = Array.prototype.slice.call(document.scripts).find(function (s) {
    return s.src && s.src.indexOf('/assets/javascripts/') !== -1;
  });
  var baseUrl = bundle ? bundle.src.split('/assets/javascripts/')[0] + '/' : new URL('./', location.href).href;
  var docsPromise = fetch(baseUrl + 'search/search_index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { return data.docs || []; })
    .catch(function () { return []; });

  function normalize(value) {
    return String(value || '')
      .toLowerCase()
      .replace(/ё/g, 'е')
      .replace(/[\s\u00a0]+/g, ' ')
      .trim();
  }

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, function (ch) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch];
    });
  }

  function stripHtml(value) {
    return String(value || '')
      .replace(/<[^>]*>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'");
  }

  function excerpt(text, token) {
    var clean = stripHtml(text).replace(/\s+/g, ' ').trim();
    if (!clean) return '';
    var lower = normalize(clean);
    var idx = lower.indexOf(token);
    if (idx < 0) return clean.slice(0, 170) + (clean.length > 170 ? '…' : '');
    var start = Math.max(0, idx - 70);
    var end = Math.min(clean.length, idx + 130);
    return (start ? '…' : '') + clean.slice(start, end) + (end < clean.length ? '…' : '');
  }

  function score(doc, tokens) {
    var title = normalize(doc.title);
    var location = normalize(decodeURIComponent(doc.location || ''));
    var text = normalize(doc.text);
    var total = 0;
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (!t) continue;
      if (title.indexOf(t) >= 0) total += 12;
      if (location.indexOf(t) >= 0) total += 8;
      if (text.indexOf(t) >= 0) total += 2;
      if (title === t) total += 20;
    }
    return total;
  }

  function render(docs, query) {
    var q = normalize(query);
    list.innerHTML = '';
    if (q.length < 2) {
      meta.textContent = 'Начните печатать для поиска';
      return;
    }
    var tokens = q.split(' ').filter(Boolean);
    var matches = docs
      .map(function (doc) { return { doc: doc, score: score(doc, tokens) }; })
      .filter(function (item) { return item.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 10);

    if (!matches.length) {
      meta.textContent = 'Ничего не найдено';
      return;
    }

    meta.textContent = 'Найдено: ' + matches.length;
    matches.forEach(function (item) {
      var doc = item.doc;
      var href = new URL(doc.location || '.', baseUrl).href;
      var li = document.createElement('li');
      li.className = 'md-search-result__item';
      li.innerHTML =
        '<a class="md-search-result__link" href="' + escapeHtml(href) + '">' +
          '<article class="md-search-result__article md-typeset">' +
            '<h1>' + escapeHtml(doc.title || doc.location || 'Страница') + '</h1>' +
            '<p>' + escapeHtml(excerpt(doc.text || '', tokens[0])) + '</p>' +
          '</article>' +
        '</a>';
      list.appendChild(li);
    });
  }

  var timer = null;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      docsPromise.then(function (docs) { render(docs, input.value); });
    }, 80);
  }, true);

  input.addEventListener('focus', function () {
    if (input.value) docsPromise.then(function (docs) { render(docs, input.value); });
  }, true);
})();
