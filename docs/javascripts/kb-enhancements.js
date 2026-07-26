(function () {
  function currentArticle() {
    return document.querySelector('.md-content article.md-content__inner');
  }

  function openSearchWithTopic() {
    var toggle = document.getElementById('__search');
    var input = document.querySelector('[data-md-component="search-query"]');
    var title = document.querySelector('.md-content h1');
    if (!toggle || !input) return;
    toggle.checked = true;
    input.value = title ? title.textContent.trim() : '';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    window.setTimeout(function () { input.focus(); }, 30);
  }

  function addNextActions() {
    var article = currentArticle();
    if (!article || article.querySelector('.kb-next')) return;
    if (location.pathname.replace(/\/+$/, '').endsWith('/cl_maverick_kb')) return;

    var relatedHeading = Array.prototype.slice.call(article.querySelectorAll('h2')).find(function (heading) {
      return /связанн/i.test(heading.textContent || '');
    });

    var section = document.createElement('section');
    section.className = 'kb-next';
    section.setAttribute('aria-labelledby', 'kb-next-title');
    section.innerHTML =
      '<h2 id="kb-next-title">Что дальше</h2>' +
      '<p>Продолжите по связанным материалам или найдите другую инструкцию по этой теме.</p>' +
      '<div class="kb-next__actions"></div>';

    var actions = section.querySelector('.kb-next__actions');

    if (relatedHeading && relatedHeading.id) {
      var related = document.createElement('a');
      related.className = 'kb-next__button';
      related.href = '#' + relatedHeading.id;
      related.textContent = 'Связанные страницы';
      actions.appendChild(related);
    }

    var search = document.createElement('button');
    search.className = 'kb-next__button';
    search.type = 'button';
    search.textContent = 'Искать по теме';
    search.addEventListener('click', openSearchWithTopic);
    actions.appendChild(search);

    var top = document.createElement('a');
    top.className = 'kb-next__button';
    top.href = '#';
    top.textContent = 'К началу';
    actions.appendChild(top);

    var home = document.createElement('a');
    home.className = 'kb-next__button';
    home.href = new URL('./', document.querySelector('script[src*="/assets/javascripts/"]').src.split('/assets/javascripts/')[0] + '/').href;
    home.textContent = 'На главную';
    actions.appendChild(home);

    article.appendChild(section);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addNextActions);
  } else {
    addNextActions();
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(addNextActions);
  }
})();
