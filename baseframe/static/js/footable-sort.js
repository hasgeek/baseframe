/*!
 * FooTable Sort
 * Version : 2.0.3
 * http://fooplugins.com/plugins/footable-jquery/
 * https://github.com/fooplugins/FooTable/tree/V2
 *
 * Requires jQuery - http://jquery.com/
 *
 * Copyright 2014 Steven Usher & Brad Vincent
 * Released under the MIT license
 * You are free to use FooTable in commercial projects as long as this copyright header is left intact.
 *
 * Date: 18 Jun 2015
 */
!(function (t, o, a) {
  function s() {
    var o = this;
    (o.name = 'Footable Sortable'),
      (o.init = function (a) {
        (o.footable = a),
          a.options.sort === !0 &&
            t(a.table)
              .unbind('.sorting')
              .bind({
                'footable_initialized.sorting': function (s) {
                  var e,
                    r,
                    n = t(a.table),
                    i = (n.find('> tbody'), a.options.classes.sort);
                  if (n.data('sort') !== !1) {
                    n
                      .find(
                        '> thead > tr:last-child > th, > thead > tr:last-child > td'
                      )
                      .each(function (o) {
                        var s = t(this),
                          e = a.columns[s.index()];
                        e.sort.ignore === !0 ||
                          s.hasClass(i.sortable) ||
                          (s.addClass(i.sortable),
                          t('<span />').addClass(i.indicator).appendTo(s));
                      }),
                      n
                        .find(
                          '> thead > tr:last-child > th.' +
                            i.sortable +
                            ', > thead > tr:last-child > td.' +
                            i.sortable
                        )
                        .unbind('click.footable')
                        .bind('click.footable', function (a) {
                          a.preventDefault(), (r = t(this));
                          var s = !r.hasClass(i.sorted);
                          return o.doSort(r.index(), s), !1;
                        });
                    var l = !1;
                    for (var d in a.columns)
                      if (((e = a.columns[d]), e.sort.initial)) {
                        var c = 'descending' !== e.sort.initial;
                        o.doSort(e.index, c);
                        break;
                      }
                    l && a.bindToggleSelectors();
                  }
                },
                'footable_redrawn.sorting': function (s) {
                  var e = t(a.table),
                    r = a.options.classes.sort;
                  e.data('sorted') >= 0 &&
                    e.find('> thead > tr:last-child > th').each(function (a) {
                      var s = t(this);
                      return s.hasClass(r.sorted) || s.hasClass(r.descending)
                        ? void o.doSort(a)
                        : void 0;
                    });
                },
                'footable_column_data.sorting': function (o) {
                  var a = t(o.column.th);
                  (o.column.data.sort = o.column.data.sort || {}),
                    (o.column.data.sort.initial = a.data('sort-initial') || !1),
                    (o.column.data.sort.ignore = a.data('sort-ignore') || !1),
                    (o.column.data.sort.selector =
                      a.data('sort-selector') || null);
                  var s = a.data('sort-match') || 0;
                  s >= o.column.data.matches.length && (s = 0),
                    (o.column.data.sort.match = o.column.data.matches[s]);
                },
              })
              .data('footable-sort', o);
      }),
      (o.doSort = function (s, e) {
        var r = o.footable;
        if (t(r.table).data('sort') !== !1) {
          var n = t(r.table),
            i = n.find('> tbody'),
            l = r.columns[s],
            d = n.find('> thead > tr:last-child > th:eq(' + s + ')'),
            c = r.options.classes.sort,
            u = r.options.events.sort;
          if (
            ((e =
              e === a
                ? d.hasClass(c.sorted)
                : 'toggle' === e
                ? !d.hasClass(c.sorted)
                : e),
            l.sort.ignore === !0)
          )
            return !0;
          var h = r.raise(u.sorting, {
            column: l,
            direction: e ? 'ASC' : 'DESC',
          });
          (h && h.result === !1) ||
            (n.data('sorted', l.index),
            n
              .find(
                '> thead > tr:last-child > th, > thead > tr:last-child > td'
              )
              .not(d)
              .removeClass(c.sorted + ' ' + c.descending),
            e === a && (e = d.hasClass(c.sorted)),
            e
              ? d.removeClass(c.descending).addClass(c.sorted)
              : d.removeClass(c.sorted).addClass(c.descending),
            o.sort(r, i, l, e),
            r.bindToggleSelectors(),
            r.raise(u.sorted, { column: l, direction: e ? 'ASC' : 'DESC' }));
        }
      }),
      (o.rows = function (o, s, e) {
        var r = [];
        return (
          s
            .find('> tr')
            .each(function () {
              var s = t(this),
                n = null;
              if (s.hasClass(o.options.classes.detail)) return !0;
              s.next().hasClass(o.options.classes.detail) &&
                (n = s.next().get(0));
              var i = { row: s, detail: n };
              return (
                e !== a && (i.value = o.parse(this.cells[e.sort.match], e)),
                r.push(i),
                !0
              );
            })
            .detach(),
          r
        );
      }),
      (o.sort = function (t, a, s, e) {
        var r = o.rows(t, a, s),
          n = t.options.sorters[s.type] || t.options.sorters.alpha;
        r.sort(function (t, o) {
          return e ? n(t.value, o.value) : n(o.value, t.value);
        });
        for (var i = 0; i < r.length; i++)
          a.append(r[i].row), null !== r[i].detail && a.append(r[i].detail);
      });
  }
  if (o.footable === a || null === o.footable)
    throw new Error(
      'Please check and make sure footable.js is included in the page and is loaded prior to this script.'
    );
  var e = {
    sort: !0,
    sorters: {
      alpha: function (t, o) {
        return (
          'string' == typeof t && (t = t.toLowerCase()),
          'string' == typeof o && (o = o.toLowerCase()),
          t === o ? 0 : o > t ? -1 : 1
        );
      },
      numeric: function (t, o) {
        return t - o;
      },
    },
    classes: {
      sort: {
        sortable: 'footable-sortable',
        sorted: 'footable-sorted',
        descending: 'footable-sorted-desc',
        indicator: 'footable-sort-indicator',
      },
    },
    events: {
      sort: { sorting: 'footable_sorting', sorted: 'footable_sorted' },
    },
  };
  o.footable.plugins.register(s, e);
})(jQuery, window);
