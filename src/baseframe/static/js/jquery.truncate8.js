/**!
 * trunk8 v1.3.3
 * https://github.com/rviscomi/trunk8
 *
 * Copyright 2012 Rick Viscomi
 * Released under the MIT License.
 *
 * Date: September 26, 2012
 */
!(function (t) {
  function e(e) {
    ((this.$element = t(e)),
      (this.original_text = this.$element.html().trim()),
      (this.settings = t.extend({}, t.fn.trunk8.defaults)));
  }
  function n(t) {
    var e = document.createElement('DIV');
    return (
      (e.innerHTML = t),
      'undefined' != typeof e.textContent ? e.textContent : e.innerText
    );
  }
  function r(t) {
    if (n(t) === t) return t.split(/\s/g);
    for (
      var e,
        i,
        a = [],
        s =
          /<([a-z]+)([^<]*)(?:>(.*?(?!<\1>)*)<\/\1>|\s+\/>)(['.?!,]*)|((?:[^<>\s])+['.?!,]*\w?|<br\s?\/?>)/gi,
        o = s.exec(t);
      o && e !== s.lastIndex;

    )
      ((e = s.lastIndex),
        o[5]
          ? a.push(o[5])
          : o[1] &&
            a.push({ tag: o[1], attribs: o[2], content: o[3], after: o[4] }),
        (o = s.exec(t)));
    for (i = 0; i < a.length; i++)
      'string' != typeof a[i] &&
        a[i].content &&
        (a[i].content = r(a[i].content));
    return a;
  }
  function i(e, n, r) {
    e = e.replace(r, '');
    var i = function (n, a) {
        var s,
          o,
          l,
          h,
          u = '';
        for (h = 0; h < n.length; h++)
          ((s = n[h]),
            (l = t.trim(e).split(' ').length),
            t.trim(e).length &&
              ('string' == typeof s
                ? (/<br\s*\/?>/.test(s) ||
                    (1 === l && t.trim(e).length <= s.length
                      ? ((s = e),
                        ('p' === a || 'div' === a) && (s += r),
                        (e = ''))
                      : (e = e.replace(s, ''))),
                  (u += t.trim(s) + (h === n.length - 1 || 1 >= l ? '' : ' ')))
                : ((o = i(s.content, s.tag)),
                  s.after && (e = e.replace(s.after, '')),
                  o &&
                    (s.after || (s.after = ' '),
                    (u +=
                      '<' +
                      s.tag +
                      s.attribs +
                      '>' +
                      o +
                      '</' +
                      s.tag +
                      '>' +
                      s.after)))));
        return u;
      },
      a = i(n);
    return (a.slice(a.length - r.length) === r && (a += r), a);
  }
  function a() {
    var e,
      a,
      s,
      l,
      u,
      c,
      f = this.data('trunk8'),
      g = f.settings,
      p = g.width,
      d = g.side,
      m = g.fill,
      v = g.parseHTML,
      y = o.getLineHeight(this) * g.lines,
      S = f.original_text,
      x = S.length,
      b = '';
    if (
      (this.html(S),
      (u = this.text()),
      v && n(S) !== S && ((c = r(S)), (S = n(S)), (x = S.length)),
      p === h.auto)
    ) {
      if (this.height() <= y) return;
      for (e = 0, a = x - 1; a >= e; )
        ((s = e + ((a - e) >> 1)),
          (l = o.eatStr(S, d, x - s, m)),
          v && c && (l = i(l, c, m)),
          this.html(l),
          this.height() > y
            ? (a = s - 1)
            : ((e = s + 1), (b = b.length > l.length ? b : l)));
      (this.html(''), this.html(b), g.tooltip && this.attr('title', u));
    } else {
      if (isNaN(p)) return void t.error('Invalid width "' + p + '".');
      ((s = x - p),
        (l = o.eatStr(S, d, s, m)),
        this.html(l),
        g.tooltip && this.attr('title', S));
    }
    g.onTruncate();
  }
  var s,
    o,
    l = { center: 'center', left: 'left', right: 'right' },
    h = { auto: 'auto' };
  ((e.prototype.updateSettings = function (e) {
    this.settings = t.extend(this.settings, e);
  }),
    (s = {
      init: function (n) {
        return this.each(function () {
          var r = t(this),
            i = r.data('trunk8');
          (i || r.data('trunk8', (i = new e(this))),
            i.updateSettings(n),
            a.call(r));
        });
      },
      update: function (e) {
        return this.each(function () {
          var n = t(this);
          (e && (n.data('trunk8').original_text = e), a.call(n));
        });
      },
      revert: function () {
        return this.each(function () {
          var e = t(this).data('trunk8').original_text;
          t(this).html(e);
        });
      },
      getSettings: function () {
        return t(this.get(0)).data('trunk8').settings;
      },
    }),
    (o = {
      eatStr: function (e, n, r, i) {
        var a,
          s,
          h = e.length,
          u = o.eatStr.generateKey.apply(null, arguments);
        if (o.eatStr.cache[u]) return o.eatStr.cache[u];
        if (
          (('string' != typeof e || 0 === h) &&
            t.error('Invalid source string "' + e + '".'),
          0 > r || r > h)
        )
          t.error('Invalid bite size "' + r + '".');
        else if (0 === r) return e;
        switch (
          ('string' != typeof (i + '') &&
            t.error('Fill unable to be converted to a string.'),
          n)
        ) {
          case l.right:
            return (o.eatStr.cache[u] = t.trim(e.substr(0, h - r)) + i);
          case l.left:
            return (o.eatStr.cache[u] = i + t.trim(e.substr(r)));
          case l.center:
            return (
              (a = h >> 1),
              (s = r >> 1),
              (o.eatStr.cache[u] =
                t.trim(o.eatStr(e.substr(0, h - a), l.right, r - s, '')) +
                i +
                t.trim(o.eatStr(e.substr(h - a), l.left, s, '')))
            );
          default:
            t.error('Invalid side "' + n + '".');
        }
      },
      getLineHeight: function (e) {
        var n = t(e).css('float');
        'none' !== n && t(e).css('float', 'none');
        var r = t(e).css('position');
        'absolute' === r && t(e).css('position', 'static');
        var i,
          a = t(e).html(),
          s = 'line-height-test';
        return (
          t(e)
            .html('i')
            .wrap('<div id="' + s + '" />'),
          (i = t('#' + s).innerHeight()),
          t(e).html(a).css({ float: n, position: r }).unwrap(),
          i
        );
      },
    }),
    (o.eatStr.cache = {}),
    (o.eatStr.generateKey = function () {
      return Array.prototype.join.call(arguments, '');
    }),
    (t.fn.trunk8 = function (e) {
      return s[e]
        ? s[e].apply(this, Array.prototype.slice.call(arguments, 1))
        : 'object' != typeof e && e
          ? void t.error('Method ' + e + ' does not exist on jQuery.trunk8')
          : s.init.apply(this, arguments);
    }),
    (t.fn.trunk8.defaults = {
      fill: '&hellip;',
      lines: 1,
      side: l.right,
      tooltip: !0,
      width: h.auto,
      parseHTML: !1,
      onTruncate: function () {},
    }));
})(jQuery);
