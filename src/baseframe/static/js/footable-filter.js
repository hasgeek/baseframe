/*!
 * FooTable Filter
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
!(function (t, e, i) {
  function a() {
    var e = this;
    (e.name = 'Footable Filter'),
      (e.init = function (i) {
        if (((e.footable = i), i.options.filter.enabled === !0)) {
          if (t(i.table).data('filter') === !1) return;
          i.timers.register('filter'),
            t(i.table)
              .unbind('.filtering')
              .bind({
                'footable_initialized.filtering': function (a) {
                  var r = t(i.table),
                    l = {
                      input: r.data('filter') || i.options.filter.input,
                      timeout:
                        r.data('filter-timeout') || i.options.filter.timeout,
                      minimum:
                        r.data('filter-minimum') || i.options.filter.minimum,
                      disableEnter:
                        r.data('filter-disable-enter') ||
                        i.options.filter.disableEnter,
                    };
                  l.disableEnter &&
                    t(l.input).keypress(function (t) {
                      return window.event
                        ? 13 !== window.event.keyCode
                        : 13 !== t.which;
                    }),
                    r.bind('footable_clear_filter', function () {
                      t(l.input).val(''), e.clearFilter();
                    }),
                    r.bind('footable_filter', function (t, i) {
                      e.filter(i.filter);
                    }),
                    t(l.input).keyup(function (a) {
                      i.timers.filter.stop(),
                        27 === a.which && t(l.input).val(''),
                        i.timers.filter.start(function () {
                          var i = t(l.input).val() || '';
                          e.filter(i);
                        }, l.timeout);
                    });
                },
                'footable_redrawn.filtering': function (a) {
                  var r = t(i.table),
                    l = r.data('filter-string');
                  l && e.filter(l);
                },
              })
              .data('footable-filter', e);
        }
      }),
      (e.filter = function (i) {
        var a = e.footable,
          r = t(a.table),
          l = r.data('filter-minimum') || a.options.filter.minimum,
          o = !i,
          n = a.raise('footable_filtering', { filter: i, clear: o });
        if (!((n && n.result === !1) || (n.filter && n.filter.length < l)))
          if (n.clear) e.clearFilter();
          else {
            var f = n.filter.split(' ');
            r.find('> tbody > tr').hide().addClass('footable-filtered');
            var s = r.find('> tbody > tr:not(.footable-row-detail)');
            t.each(f, function (t, e) {
              e &&
                e.length > 0 &&
                (r.data('current-filter', e),
                (s = s.filter(a.options.filter.filterFunction)));
            }),
              s.each(function () {
                e.showRow(this, a), t(this).removeClass('footable-filtered');
              }),
              r.data('filter-string', n.filter),
              a.raise('footable_filtered', { filter: n.filter, clear: !1 });
          }
      }),
      (e.clearFilter = function () {
        var i = e.footable,
          a = t(i.table);
        a
          .find('> tbody > tr:not(.footable-row-detail)')
          .removeClass('footable-filtered')
          .each(function () {
            e.showRow(this, i);
          }),
          a.removeData('filter-string'),
          i.raise('footable_filtered', { clear: !0 });
      }),
      (e.showRow = function (e, i) {
        var a = t(e),
          r = a.next(),
          l = t(i.table);
        l.hasClass('breakpoint') &&
        a.hasClass('footable-detail-show') &&
        r.hasClass('footable-row-detail')
          ? (a.add(r).show(), i.createOrUpdateDetailRow(e))
          : a.show();
      });
  }
  if (e.footable === i || null === e.footable)
    throw new Error(
      'Please check and make sure footable.js is included in the page and is loaded prior to this script.'
    );
  var r = {
    filter: {
      enabled: !0,
      input: '.footable-filter',
      timeout: 300,
      minimum: 2,
      disableEnter: !1,
      filterFunction: function (e) {
        var i = t(this),
          a = i.parents('table:first'),
          r = a.data('current-filter').toUpperCase(),
          l = i.find('td').text();
        return (
          a.data('filter-text-only') ||
            i.find('td[data-value]').each(function () {
              l += t(this).data('value');
            }),
          l.toUpperCase().indexOf(r) >= 0
        );
      },
    },
  };
  e.footable.plugins.register(a, r);
})(jQuery, window);
