(function () {
  'use strict';
  var D = window.DATA, KEY = 'azubi-vertrag-v1', L = ['A', 'B', 'C', 'D'];
  var root = document.getElementById('app');
  var page = document.body.getAttribute('data-page');

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function put(k, v) { var o = load(); o[k] = v; try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  function wipe() { try { localStorage.removeItem(KEY); } catch (e) {} }

  function h(tag, attrs) {
    var e = document.createElement(tag), k, i, c;
    if (attrs) for (k in attrs) {
      if (k === 'class') e.className = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    for (i = 2; i < arguments.length; i++) {
      c = arguments[i]; if (c == null) continue;
      if (Array.isArray(c)) c.forEach(function (x) { e.appendChild(x.nodeType ? x : document.createTextNode(x)); });
      else e.appendChild(c.nodeType ? c : document.createTextNode(c));
    }
    return e;
  }
  function clear() { while (root.firstChild) root.removeChild(root.firstChild); }
  function focusFirst(node) { var f = node.querySelector('[data-focus]'); if (f) { f.setAttribute('tabindex', '-1'); f.focus(); } }
  function home() { return h('a', { class: 'btn ghost', href: 'index.html' }, 'Zur Startseite'); }

  /* ------------------------------------------------ Rote/Gruene Karte */
  function rg() {
    var st = { i: 0, score: 0, res: [] }, items = D.rg;
    function render() {
      clear();
      var it = items[st.i], n = items.length, box = h('section', null);
      box.appendChild(h('p', { class: 'step' }, 'Aussage ' + (st.i + 1) + ' von ' + n));
      box.appendChild(h('h2', { class: 'card q', 'data-focus': '1' }, it.t));
      var fbox = h('div', { role: 'status' });
      var bYes = h('button', { class: 'btn ok', type: 'button', onclick: function () { answer(true); } }, '✓ Stimmt');
      var bNo = h('button', { class: 'btn bad', type: 'button', onclick: function () { answer(false); } }, '✗ Stimmt nicht');
      box.appendChild(h('div', { class: 'row2' }, bYes, bNo));
      box.appendChild(fbox);
      root.appendChild(box); focusFirst(box);
      function answer(val) {
        var good = val === it.ok;
        bYes.disabled = bNo.disabled = true;
        (val ? bYes : bNo).classList.add('sel');
        if (good) st.score++;
        st.res.push(good);
        var last = st.i === n - 1;
        fbox.appendChild(h('div', { class: 'fb ' + (good ? 'good' : 'bad') },
          h('h3', null, good ? '✓ Richtig!' : '✗ Leider falsch.'),
          h('p', null, h('strong', null, 'Lösung: '), (it.ok ? 'Stimmt – ' : 'Stimmt nicht – ') + it.b)));
        var nx = h('button', { class: 'btn', type: 'button', onclick: function () { if (last) finish(); else { st.i++; render(); } } }, last ? 'Ergebnis ansehen' : 'Weiter');
        fbox.appendChild(nx); nx.focus();
      }
    }
    function finish() {
      clear(); put('rg', { score: st.score, total: items.length });
      var box = h('section', null,
        h('div', { class: 'result' }, h('h2', { 'data-focus': '1' }, 'Ergebnis'), h('div', { class: 'big' }, st.score + ' von ' + items.length), h('div', { class: 'sub' }, 'Aussagen richtig')),
        h('ul', { class: 'sumlist' }, items.map(function (it, i) { return h('li', null, (st.res[i] ? '✓ ' : '✗ ') + (i + 1) + '. ' + it.t + ' – ' + (it.ok ? 'Stimmt' : 'Stimmt nicht')); })),
        h('div', { class: 'row' }, h('button', { class: 'btn', type: 'button', onclick: function () { st = { i: 0, score: 0, res: [] }; render(); } }, 'Noch einmal'), home()));
      root.appendChild(box); focusFirst(box);
    }
    render();
  }

  /* ------------------------------------------------ Auswahl-Quiz (IHK-Faelle, Mini-Quiz) */
  function choice(items, key, opt) {
    var st = { i: 0, score: 0, res: [] };
    function render() {
      clear();
      var it = items[st.i], n = items.length, box = h('section', null);
      box.appendChild(h('p', { class: 'step' }, opt.step(st.i, n)));
      box.appendChild(h('h2', { 'data-focus': '1' }, opt.head(it, st.i)));
      box.appendChild(h('p', { class: 'card q' }, it.q));
      var list = h('div', { class: 'answers' }), fbox = h('div', { role: 'status' }), btns = [];
      it.a.forEach(function (t, j) {
        var b = h('button', { class: 'ans', type: 'button', onclick: function () { pick(j); } }, h('span', { class: 'l', 'aria-hidden': 'true' }, L[j]), h('span', { class: 'at' }, h('span', { class: 'sr' }, 'Antwort ' + L[j] + ': '), t));
        btns.push(b); list.appendChild(b);
      });
      box.appendChild(list); box.appendChild(fbox);
      root.appendChild(box); focusFirst(box);
      function pick(j) {
        var good = j === it.c;
        btns.forEach(function (b, x) {
          b.disabled = true;
          if (x === it.c) { b.classList.add('right'); b.querySelector('.at').appendChild(h('span', { class: 'mark' }, '✓ Richtig')); }
          else if (x === j) { b.classList.add('wrong'); b.querySelector('.at').appendChild(h('span', { class: 'mark' }, '✗ Deine Antwort')); }
        });
        if (good) st.score++;
        st.res.push(good);
        var last = st.i === n - 1;
        fbox.appendChild(h('div', { class: 'fb ' + (good ? 'good' : 'bad') },
          h('h3', null, good ? '✓ Richtig!' : '✗ Leider falsch.'),
          h('p', null, h('strong', null, 'Richtig ist ' + L[it.c] + ': '), it.a[it.c]),
          h('p', null, h('strong', null, opt.fbLabel), it.fb)));
        var nx = h('button', { class: 'btn', type: 'button', onclick: function () { if (last) finish(); else { st.i++; render(); } } }, last ? 'Ergebnis ansehen' : 'Weiter');
        fbox.appendChild(nx); nx.focus();
      }
    }
    function finish() {
      clear(); put(key, { score: st.score, total: items.length });
      var box = h('section', null,
        h('div', { class: 'result' }, h('h2', { 'data-focus': '1' }, 'Ergebnis'), h('div', { class: 'big' }, st.score + ' von ' + items.length), h('div', { class: 'sub' }, opt.unit)),
        h('ul', { class: 'sumlist' }, items.map(function (it, i) { return h('li', null, (st.res[i] ? '✓ ' : '✗ ') + opt.head(it, i) + ' – richtig: ' + L[it.c]); })),
        h('div', { class: 'row' }, h('button', { class: 'btn', type: 'button', onclick: function () { st = { i: 0, score: 0, res: [] }; render(); } }, 'Noch einmal'), home()));
      root.appendChild(box); focusFirst(box);
    }
    render();
  }

  /* ------------------------------------------------ Vertrags-Detektiv */
  function det() {
    var sel = {}, ja = {}, max = 5;
    function count() { return Object.keys(sel).filter(function (k) { return sel[k]; }).length; }
    function kopf() {
      return D.kopf.map(function (t, i) { return h('p', { class: 'kopf' + (i === 0 ? ' t' : '') }, t); });
    }
    function play() {
      clear();
      var info = h('p', { class: 'step', role: 'status' }, 'Markiert: ' + count() + ' von höchstens ' + max);
      var doc = h('div', { class: 'doc', role: 'group', 'aria-label': 'Vertragsauszug, Zeilen 1 bis 7' }, kopf(), h('hr'));
      D.zeilen.forEach(function (z, i) {
        var b = h('button', { class: 'zeile', type: 'button', 'aria-pressed': sel[i] ? 'true' : 'false' },
          h('span', { class: 'n', 'aria-hidden': 'true' }, String(i + 1)),
          h('span', { class: 'zt' }, h('span', { class: 'sr' }, 'Zeile ' + (i + 1) + ': '), z.t, h('span', { class: 'pm' }, sel[i] ? '◉ markiert' : '')));
        b.addEventListener('click', function () {
          if (!sel[i] && count() >= max) { info.textContent = 'Du kannst höchstens ' + max + ' Zeilen markieren. Tippe eine markierte Zeile an, um sie abzuwählen.'; return; }
          sel[i] = !sel[i];
          b.setAttribute('aria-pressed', sel[i] ? 'true' : 'false');
          b.querySelector('.pm').textContent = sel[i] ? '◉ markiert' : '';
          info.textContent = 'Markiert: ' + count() + ' von höchstens ' + max;
        });
        doc.appendChild(b);
      });
      var box = h('section', null, h('h2', { 'data-focus': '1' }, 'Vertragsauszug'), doc, info,
        h('div', { class: 'row' }, h('button', { class: 'btn', type: 'button', onclick: check }, 'Prüfen'),
          h('button', { class: 'btn ghost', type: 'button', onclick: function () { sel = {}; play(); } }, 'Markierungen löschen')));
      root.appendChild(box); focusFirst(box);
    }
    function found() { var f = 0; D.zeilen.forEach(function (z, i) { if (z.f && sel[i]) f++; }); return f; }
    function regeln() { var r = 0; for (var k in ja) if (ja[k] === true) r++; return r; }
    function check() {
      clear(); ja = {};
      var doc = h('div', { class: 'doc', role: 'group', 'aria-label': 'Vertragsauszug mit Lösung' }, kopf(), h('hr'));
      D.zeilen.forEach(function (z, i) {
        var cls = 'zeile static', tag = '';
        if (z.f) { cls += sel[i] ? ' err' : ' miss'; tag = (sel[i] ? '✓ Gefunden' : '✗ Nicht gefunden') + ' · [Fehler ' + z.f + ']'; }
        else if (sel[i]) { cls += ' nope'; tag = '✗ Markiert, aber hier steckt kein Fehler'; }
        doc.appendChild(h('div', { class: cls }, h('span', { class: 'n', 'aria-hidden': 'true' }, String(i + 1)),
          h('span', { class: 'zt' }, h('span', { class: 'sr' }, 'Zeile ' + (i + 1) + ': '), z.t, tag ? h('span', { class: 'tag' }, tag) : null)));
      });
      var pts = h('div', { class: 'points', role: 'status' });
      function upd() {
        var f = found(), r = regeln(), p = f + r;
        pts.textContent = '';
        pts.appendChild(document.createTextNode('Punkte: '));
        pts.appendChild(h('span', { class: 'big' }, p + ' von 10'));
        pts.appendChild(document.createTextNode(' (gefunden: ' + f + ' von 5, Regeln: ' + r + ' von 5)'));
        put('det', { points: p, found: f, total: 10 });
      }
      var cards = [];
      Object.keys(D.fehler).forEach(function (n) {
        var fe = D.fehler[n], lineIdx = -1;
        D.zeilen.forEach(function (z, i) { if (String(z.f) === n) lineIdx = i; });
        var got = !!sel[lineIdx];
        var yes = h('button', { class: 'btn ghost', type: 'button', 'aria-pressed': 'false' }, '✓ Ja');
        var no = h('button', { class: 'btn ghost', type: 'button', 'aria-pressed': 'false' }, '✗ Nein');
        function set(v) { ja[n] = v; yes.setAttribute('aria-pressed', v ? 'true' : 'false'); no.setAttribute('aria-pressed', v ? 'false' : 'true'); yes.classList.toggle('sel', v); no.classList.toggle('sel', !v); upd(); }
        yes.addEventListener('click', function () { set(true); }); no.addEventListener('click', function () { set(false); });
        cards.push(h('div', { class: 'fehlercard' },
          h('h3', null, 'Fehler ' + n + ' · ' + fe.stelle),
          h('p', null, h('strong', null, got ? '✓ Gefunden' : '✗ Nicht gefunden')),
          h('p', null, h('strong', null, 'Regel: '), fe.regel),
          h('p', null, h('strong', null, 'Hatte ich auch die Regel?')),
          h('div', { class: 'row' }, yes, no)));
      });
      var box = h('section', null, h('h2', { 'data-focus': '1' }, 'Lösung'), doc, h('h2', null, 'Die 5 Fehler mit Regel'), cards,
        h('p', { class: 'note' }, 'Bewertung: je gefundenem Fehler 1 Punkt, je Regel 1 Punkt, höchstens 10 Punkte.'), pts,
        h('div', { class: 'row' }, h('button', { class: 'btn', type: 'button', onclick: function () { sel = {}; ja = {}; play(); } }, 'Noch einmal'), home()));
      root.appendChild(box); focusFirst(box); upd();
    }
    play();
  }

  /* ------------------------------------------------ Experten-Karten */
  function experten() {
    D.experten.forEach(function (c, i) {
      var id = 'ex' + i, ans = h('div', { class: 'reveal', id: id + 'l', hidden: '' }, h('strong', null, 'Lösung: '), c.loesung);
      var btn = h('button', { class: 'btn', type: 'button', 'aria-expanded': 'false', 'aria-controls': id + 'l' }, 'Lösung aufdecken');
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        btn.textContent = open ? 'Lösung aufdecken' : 'Lösung verbergen';
        if (open) ans.setAttribute('hidden', ''); else { ans.removeAttribute('hidden'); put('experten', { opened: true }); }
      });
      root.appendChild(h('section', { class: 'card', 'aria-labelledby': id }, h('h2', { id: id, style: 'margin-top:0' }, c.t),
        h('ul', { class: 'kern' }, c.kern.map(function (k) { return h('li', null, k); })),
        h('p', null, h('strong', null, 'Frage an die Klasse: '), c.frage), btn, ans));
    });
  }

  /* ------------------------------------------------ Merkblatt, Quellen */
  function merk() {
    var rows = D.merk.map(function (m) {
      return h('tr', null, h('td', { class: 'th', 'data-l': 'Thema' }, m.thema), h('td', { 'data-l': 'Das müsst ihr wissen' }, m.text), h('td', { 'data-l': 'Paragraf' }, m.para));
    });
    root.appendChild(h('table', { class: 'merk' }, h('caption', { class: 'sr' }, 'Merkblatt: Das Wichtigste auf einer Seite'),
      h('thead', null, h('tr', null, h('th', { scope: 'col' }, 'Thema'), h('th', { scope: 'col' }, 'Das müsst ihr wissen'), h('th', { scope: 'col' }, 'Paragraf'))), h('tbody', null, rows)));
    var p = document.getElementById('print'); if (p) p.addEventListener('click', function () { window.print(); });
  }
  function quellen() {
    root.appendChild(h('ul', { class: 'links' }, D.quellen.map(function (q) { return h('li', null, h('a', { href: q.u, target: '_blank', rel: 'noopener noreferrer' }, q.t)); })));
    root.appendChild(h('p', { class: 'note' }, 'Die Links öffnen externe Seiten. Rechtsstand: Oktober 2026.'));
  }

  /* ------------------------------------------------ Startseite */
  function start() {
    function status() {
      var o = load(), t = {
        rg: o.rg && '✓ ' + o.rg.score + ' von ' + o.rg.total,
        det: o.det && '✓ ' + o.det.points + ' von 10 Punkten',
        faelle: o.faelle && '✓ ' + o.faelle.score + ' von ' + o.faelle.total,
        quiz: o.quiz && '✓ ' + o.quiz.score + ' von ' + o.quiz.total,
        experten: o.experten && '✓ angesehen'
      };
      Array.prototype.forEach.call(document.querySelectorAll('[data-tile]'), function (a) { a.querySelector('.ts').textContent = t[a.getAttribute('data-tile')] || ''; });
    }
    status();
    var r = document.getElementById('reset');
    if (r) r.addEventListener('click', function () { wipe(); status(); r.textContent = 'Zurückgesetzt ✓'; setTimeout(function () { r.textContent = 'Zurücksetzen'; }, 2500); });
  }

  if (page === 'home') start();
  else if (page === 'rg') rg();
  else if (page === 'det') det();
  else if (page === 'faelle') choice(D.faelle, 'faelle', { step: function (i, n) { return 'Fall ' + (i + 1) + ' von ' + n; }, head: function (it) { return it.label; }, fbLabel: 'Begründung: ', unit: 'Fälle richtig' });
  else if (page === 'quiz') choice(D.quiz, 'quiz', { step: function (i, n) { return 'Frage ' + (i + 1) + ' von ' + n; }, head: function (it, i) { return 'Frage ' + (i + 1); }, fbLabel: 'Regel: ', unit: 'Fragen richtig' });
  else if (page === 'experten') experten();
  else if (page === 'merk') merk();
  else if (page === 'quellen') quellen();
})();
