/*!
 * FooTable - Awesome Responsive Tables
 * Version : 2.0.3
 * http://fooplugins.com/plugins/footable-jquery/
 *
 * Requires jQuery - http://jquery.com/
 *
 * Copyright 2014 Steven Usher & Brad Vincent
 * Released under the MIT license
 * You are free to use FooTable in commercial projects as long as this copyright header is left intact.
 *
 * Date: 11 Nov 2014
 */
(function (e, t) {
  function a() {
    var e = this;
    ((e.id = null),
      (e.busy = !1),
      (e.start = function (t, a) {
        e.busy ||
          (e.stop(),
          (e.id = setTimeout(function () {
            (t(), (e.id = null), (e.busy = !1));
          }, a)),
          (e.busy = !0));
      }),
      (e.stop = function () {
        null !== e.id && (clearTimeout(e.id), (e.id = null), (e.busy = !1));
      }));
  }
  function i(i, o, n) {
    var r = this;
    ((r.id = n),
      (r.table = i),
      (r.options = o),
      (r.breakpoints = []),
      (r.breakpointNames = ''),
      (r.columns = {}),
      (r.plugins = t.footable.plugins.load(r)));
    var l = r.options,
      d = l.classes,
      s = l.events,
      u = l.triggers,
      f = 0;
    return (
      (r.timers = {
        resize: new a(),
        register: function (e) {
          return ((r.timers[e] = new a()), r.timers[e]);
        },
      }),
      (r.init = function () {
        var a = e(t),
          i = e(r.table);
        if ((t.footable.plugins.init(r), i.hasClass(d.loaded)))
          return (r.raise(s.alreadyInitialized), undefined);
        (r.raise(s.initializing),
          i.addClass(d.loading),
          i.find(l.columnDataSelector).each(function () {
            var e = r.getColumnData(this);
            r.columns[e.index] = e;
          }));
        for (var o in l.breakpoints)
          (r.breakpoints.push({ name: o, width: l.breakpoints[o] }),
            (r.breakpointNames += o + ' '));
        (r.breakpoints.sort(function (e, t) {
          return e.width - t.width;
        }),
          i
            .unbind(u.initialize)
            .bind(u.initialize, function () {
              (i.removeData('footable_info'),
                i.data('breakpoint', ''),
                i.trigger(u.resize),
                i.removeClass(d.loading),
                i.addClass(d.loaded).addClass(d.main),
                r.raise(s.initialized));
            })
            .unbind(u.redraw)
            .bind(u.redraw, function () {
              r.redraw();
            })
            .unbind(u.resize)
            .bind(u.resize, function () {
              r.resize();
            })
            .unbind(u.expandFirstRow)
            .bind(u.expandFirstRow, function () {
              i.find(l.toggleSelector)
                .first()
                .not('.' + d.detailShow)
                .trigger(u.toggleRow);
            })
            .unbind(u.expandAll)
            .bind(u.expandAll, function () {
              i.find(l.toggleSelector)
                .not('.' + d.detailShow)
                .trigger(u.toggleRow);
            })
            .unbind(u.collapseAll)
            .bind(u.collapseAll, function () {
              i.find('.' + d.detailShow).trigger(u.toggleRow);
            }),
          i.trigger(u.initialize),
          a.bind('resize.footable', function () {
            (r.timers.resize.stop(),
              r.timers.resize.start(function () {
                r.raise(u.resize);
              }, l.delay));
          }));
      }),
      (r.addRowToggle = function () {
        if (l.addRowToggle) {
          var t = e(r.table),
            a = !1;
          t.find('span.' + d.toggle).remove();
          for (var i in r.columns) {
            var o = r.columns[i];
            if (o.toggle) {
              a = !0;
              var n =
                '> tbody > tr:not(.' +
                d.detail +
                ',.' +
                d.disabled +
                ') > td:nth-child(' +
                (parseInt(o.index, 10) + 1) +
                '),' +
                '> tbody > tr:not(.' +
                d.detail +
                ',.' +
                d.disabled +
                ') > th:nth-child(' +
                (parseInt(o.index, 10) + 1) +
                ')';
              return (
                t
                  .find(n)
                  .not('.' + d.detailCell)
                  .prepend(e(l.toggleHTMLElement).addClass(d.toggle)),
                undefined
              );
            }
          }
          a ||
            t
              .find(
                '> tbody > tr:not(.' +
                  d.detail +
                  ',.' +
                  d.disabled +
                  ') > td:first-child'
              )
              .add(
                '> tbody > tr:not(.' +
                  d.detail +
                  ',.' +
                  d.disabled +
                  ') > th:first-child'
              )
              .not('.' + d.detailCell)
              .prepend(e(l.toggleHTMLElement).addClass(d.toggle));
        }
      }),
      (r.setColumnClasses = function () {
        var t = e(r.table);
        for (var a in r.columns) {
          var i = r.columns[a];
          if (null !== i.className) {
            var o = '',
              n = !0;
            (e.each(i.matches, function (e, t) {
              (n || (o += ', '),
                (o +=
                  '> tbody > tr:not(.' +
                  d.detail +
                  ') > td:nth-child(' +
                  (parseInt(t, 10) + 1) +
                  ')'),
                (n = !1));
            }),
              t
                .find(o)
                .not('.' + d.detailCell)
                .addClass(i.className));
          }
        }
      }),
      (r.bindToggleSelectors = function () {
        var t = e(r.table);
        r.hasAnyBreakpointColumn() &&
          (t
            .find(l.toggleSelector)
            .unbind(u.toggleRow)
            .bind(u.toggleRow, function () {
              var t = e(this).is('tr') ? e(this) : e(this).parents('tr:first');
              r.toggleDetail(t);
            }),
          t
            .find(l.toggleSelector)
            .unbind('click.footable')
            .bind('click.footable', function (a) {
              t.is('.breakpoint') &&
                e(a.target).is('td,th,.' + d.toggle) &&
                e(this).trigger(u.toggleRow);
            }));
      }),
      (r.parse = function (e, t) {
        var a = l.parsers[t.type] || l.parsers.alpha;
        return a(e);
      }),
      (r.getColumnData = function (t) {
        var a = e(t),
          i = a.data('hide'),
          o = a.index();
        ((i = i || ''),
          (i = jQuery.map(i.split(','), function (e) {
            return jQuery.trim(e);
          })));
        var n = {
          index: o,
          hide: {},
          type: a.data('type') || 'alpha',
          name: a.data('name') || e.trim(a.text()),
          ignore: a.data('ignore') || !1,
          toggle: a.data('toggle') || !1,
          className: a.data('class') || null,
          matches: [],
          names: {},
          group: a.data('group') || null,
          groupName: null,
          isEditable: a.data('editable'),
        };
        if (null !== n.group) {
          var d = e(r.table)
            .find(
              '> thead > tr.footable-group-row > th[data-group="' +
                n.group +
                '"], > thead > tr.footable-group-row > td[data-group="' +
                n.group +
                '"]'
            )
            .first();
          n.groupName = r.parse(d, { type: 'alpha' });
        }
        var u = parseInt(a.prev().attr('colspan') || 0, 10);
        f += u > 1 ? u - 1 : 0;
        var p = parseInt(a.attr('colspan') || 0, 10),
          c = n.index + f;
        if (p > 1) {
          var b = a.data('names');
          ((b = b || ''), (b = b.split(',')));
          for (var g = 0; p > g; g++)
            (n.matches.push(g + c), b.length > g && (n.names[g + c] = b[g]));
        } else n.matches.push(c);
        n.hide['default'] =
          'all' === a.data('hide') || e.inArray('default', i) >= 0;
        var h = !1;
        for (var m in l.breakpoints)
          ((n.hide[m] = 'all' === a.data('hide') || e.inArray(m, i) >= 0),
            (h = h || n.hide[m]));
        n.hasBreakpoint = h;
        var v = r.raise(s.columnData, { column: { data: n, th: t } });
        return v.column.data;
      }),
      (r.getViewportWidth = function () {
        return (
          window.innerWidth || (document.body ? document.body.offsetWidth : 0)
        );
      }),
      (r.calculateWidth = function (e, t) {
        return jQuery.isFunction(l.calculateWidthOverride)
          ? l.calculateWidthOverride(e, t)
          : (t.viewportWidth < t.width && (t.width = t.viewportWidth),
            t.parentWidth < t.width && (t.width = t.parentWidth),
            t);
      }),
      (r.hasBreakpointColumn = function (e) {
        for (var t in r.columns)
          if (r.columns[t].hide[e]) {
            if (r.columns[t].ignore) continue;
            return !0;
          }
        return !1;
      }),
      (r.hasAnyBreakpointColumn = function () {
        for (var e in r.columns) if (r.columns[e].hasBreakpoint) return !0;
        return !1;
      }),
      (r.resize = function () {
        var t = e(r.table);
        if (t.is(':visible')) {
          if (!r.hasAnyBreakpointColumn())
            return (t.trigger(u.redraw), undefined);
          var a = {
            width: t.width(),
            viewportWidth: r.getViewportWidth(),
            parentWidth: t.parent().width(),
          };
          a = r.calculateWidth(t, a);
          var i = t.data('footable_info');
          if (
            (t.data('footable_info', a),
            r.raise(s.resizing, { old: i, info: a }),
            !i || (i && i.width && i.width !== a.width))
          ) {
            for (var o, n = null, l = 0; r.breakpoints.length > l; l++)
              if (
                ((o = r.breakpoints[l]), o && o.width && a.width <= o.width)
              ) {
                n = o;
                break;
              }
            var d = null === n ? 'default' : n.name,
              f = r.hasBreakpointColumn(d),
              p = t.data('breakpoint');
            (t
              .data('breakpoint', d)
              .removeClass('default breakpoint')
              .removeClass(r.breakpointNames)
              .addClass(d + (f ? ' breakpoint' : '')),
              d !== p &&
                (t.trigger(u.redraw),
                r.raise(s.breakpoint, { breakpoint: d, info: a })));
          }
          r.raise(s.resized, { old: i, info: a });
        }
      }),
      (r.redraw = function () {
        (r.addRowToggle(), r.bindToggleSelectors(), r.setColumnClasses());
        var t = e(r.table),
          a = t.data('breakpoint'),
          i = r.hasBreakpointColumn(a);
        (t
          .find('> tbody > tr:not(.' + d.detail + ')')
          .data('detail_created', !1)
          .end()
          .find('> thead > tr:last-child > th')
          .each(function () {
            var i = r.columns[e(this).index()],
              o = '',
              n = !0;
            (e.each(i.matches, function (e, t) {
              n || (o += ', ');
              var a = t + 1;
              ((o +=
                '> tbody > tr:not(.' +
                d.detail +
                ') > td:nth-child(' +
                a +
                ')'),
                (o +=
                  ', > tfoot > tr:not(.' +
                  d.detail +
                  ') > td:nth-child(' +
                  a +
                  ')'),
                (o += ', > colgroup > col:nth-child(' + a + ')'),
                (n = !1));
            }),
              (o +=
                ', > thead > tr[data-group-row="true"] > th[data-group="' +
                i.group +
                '"]'));
            var l = t.find(o).add(this);
            if (
              ('' !== a &&
                (i.hide[a] === !1
                  ? l.addClass('footable-visible').show()
                  : l.removeClass('footable-visible').hide()),
              1 === t.find('> thead > tr.footable-group-row').length)
            ) {
              var s = t.find(
                  '> thead > tr:last-child > th[data-group="' +
                    i.group +
                    '"]:visible, > thead > tr:last-child > th[data-group="' +
                    i.group +
                    '"]:visible'
                ),
                u = t.find(
                  '> thead > tr.footable-group-row > th[data-group="' +
                    i.group +
                    '"], > thead > tr.footable-group-row > td[data-group="' +
                    i.group +
                    '"]'
                ),
                f = 0;
              (e.each(s, function () {
                f += parseInt(e(this).attr('colspan') || 1, 10);
              }),
                f > 0 ? u.attr('colspan', f).show() : u.hide());
            }
          })
          .end()
          .find('> tbody > tr.' + d.detailShow)
          .each(function () {
            r.createOrUpdateDetailRow(this);
          }),
          t.find('[data-bind-name]').each(function () {
            r.toggleInput(this);
          }),
          t.find('> tbody > tr.' + d.detailShow + ':visible').each(function () {
            var t = e(this).next();
            t.hasClass(d.detail) && (i ? t.show() : t.hide());
          }),
          t
            .find(
              '> thead > tr > th.footable-last-column, > tbody > tr > td.footable-last-column'
            )
            .removeClass('footable-last-column'),
          t
            .find(
              '> thead > tr > th.footable-first-column, > tbody > tr > td.footable-first-column'
            )
            .removeClass('footable-first-column'),
          t
            .find('> thead > tr, > tbody > tr')
            .find('> th.footable-visible:last, > td.footable-visible:last')
            .addClass('footable-last-column')
            .end()
            .find('> th.footable-visible:first, > td.footable-visible:first')
            .addClass('footable-first-column'),
          r.raise(s.redrawn));
      }),
      (r.toggleDetail = function (t) {
        var a = t.jquery ? t : e(t),
          i = a.next();
        a.hasClass(d.detailShow)
          ? (a.removeClass(d.detailShow),
            i.hasClass(d.detail) && i.hide(),
            r.raise(s.rowCollapsed, { row: a[0] }))
          : (r.createOrUpdateDetailRow(a[0]),
            a.addClass(d.detailShow).next().show(),
            r.raise(s.rowExpanded, { row: a[0] }));
      }),
      (r.removeRow = function (t) {
        var a = t.jquery ? t : e(t);
        a.hasClass(d.detail) && (a = a.prev());
        var i = a.next();
        (a.data('detail_created') === !0 && i.remove(),
          a.remove(),
          r.raise(s.rowRemoved));
      }),
      (r.appendRow = function (t) {
        var a = t.jquery ? t : e(t);
        (e(r.table).find('tbody').append(a), r.redraw());
      }),
      (r.getColumnFromTdIndex = function (t) {
        var a = null;
        for (var i in r.columns)
          if (e.inArray(t, r.columns[i].matches) >= 0) {
            a = r.columns[i];
            break;
          }
        return a;
      }),
      (r.createOrUpdateDetailRow = function (t) {
        var a,
          i = e(t),
          o = i.next(),
          n = [];
        if (i.data('detail_created') === !0) return !0;
        if (i.is(':hidden')) return !1;
        if (
          (r.raise(s.rowDetailUpdating, { row: i, detail: o }),
          i.find('> td:hidden').each(function () {
            var t = e(this).index(),
              a = r.getColumnFromTdIndex(t),
              i = a.name;
            if (a.ignore === !0) return !0;
            t in a.names && (i = a.names[t]);
            var o = e(this).attr('data-bind-name');
            if (null != o && e(this).is(':empty')) {
              var l = e(
                '.' + d.detailInnerValue + '[' + 'data-bind-value="' + o + '"]'
              );
              e(this).html(e(l).contents().detach());
            }
            var s;
            return (
              a.isEditable !== !1 &&
                (a.isEditable || e(this).find(':input').length > 0) &&
                (null == o &&
                  ((o = 'bind-' + e.now() + '-' + t),
                  e(this).attr('data-bind-name', o)),
                (s = e(this).contents().detach())),
              s || (s = e(this).contents().clone(!0, !0)),
              n.push({
                name: i,
                value: r.parse(this, a),
                display: s,
                group: a.group,
                groupName: a.groupName,
                bindName: o,
              }),
              !0
            );
          }),
          0 === n.length)
        )
          return !1;
        var u = i.find('> td:visible').length,
          f = o.hasClass(d.detail);
        return (
          f ||
            ((o = e(
              '<tr class="' +
                d.detail +
                '"><td class="' +
                d.detailCell +
                '"><div class="' +
                d.detailInner +
                '"></div></td></tr>'
            )),
            i.after(o)),
          o.find('> td:first').attr('colspan', u),
          (a = o.find('.' + d.detailInner).empty()),
          l.createDetail(a, n, l.createGroupedDetail, l.detailSeparator, d),
          i.data('detail_created', !0),
          r.raise(s.rowDetailUpdated, { row: i, detail: o }),
          !f
        );
      }),
      (r.raise = function (t, a) {
        (r.options.debug === !0 &&
          e.isFunction(r.options.log) &&
          r.options.log(t, 'event'),
          (a = a || {}));
        var i = { ft: r };
        e.extend(!0, i, a);
        var o = e.Event(t, i);
        return (o.ft || e.extend(!0, o, i), e(r.table).trigger(o), o);
      }),
      (r.reset = function () {
        var t = e(r.table);
        (t
          .removeData('footable_info')
          .data('breakpoint', '')
          .removeClass(d.loading)
          .removeClass(d.loaded),
          t.find(l.toggleSelector).unbind(u.toggleRow).unbind('click.footable'),
          t.find('> tbody > tr').removeClass(d.detailShow),
          t.find('> tbody > tr.' + d.detail).remove(),
          r.raise(s.reset));
      }),
      (r.toggleInput = function (t) {
        var a = e(t).attr('data-bind-name');
        if (null != a) {
          var i = e(
            '.' + d.detailInnerValue + '[' + 'data-bind-value="' + a + '"]'
          );
          null != i &&
            (e(t).is(':visible')
              ? e(i).is(':empty') || e(t).html(e(i).contents().detach())
              : e(t).is(':empty') || e(i).html(e(t).contents().detach()));
        }
      }),
      r.init(),
      r
    );
  }
  t.footable = {
    options: {
      delay: 100,
      breakpoints: { phone: 480, tablet: 1024 },
      parsers: {
        alpha: function (t) {
          return e(t).data('value') || e.trim(e(t).text());
        },
        numeric: function (t) {
          var a =
            e(t).data('value') ||
            e(t)
              .text()
              .replace(/[^0-9.\-]/g, '');
          return ((a = parseFloat(a)), isNaN(a) && (a = 0), a);
        },
      },
      addRowToggle: !0,
      calculateWidthOverride: null,
      toggleSelector: ' > tbody > tr:not(.footable-row-detail)',
      columnDataSelector:
        '> thead > tr:last-child > th, > thead > tr:last-child > td',
      detailSeparator: ':',
      toggleHTMLElement: '<span />',
      createGroupedDetail: function (e) {
        for (
          var t = { _none: { name: null, data: [] } }, a = 0;
          e.length > a;
          a++
        ) {
          var i = e[a].group;
          null !== i
            ? (i in t ||
                (t[i] = { name: e[a].groupName || e[a].group, data: [] }),
              t[i].data.push(e[a]))
            : t._none.data.push(e[a]);
        }
        return t;
      },
      createDetail: function (t, a, i, o, n) {
        var r = i(a);
        for (var l in r)
          if (0 !== r[l].data.length) {
            '_none' !== l &&
              t.append(
                '<div class="' +
                  n.detailInnerGroup +
                  '">' +
                  r[l].name +
                  '</div>'
              );
            for (var d = 0; r[l].data.length > d; d++) {
              var s = r[l].data[d].name ? o : '';
              t.append(
                e('<div></div>')
                  .addClass(n.detailInnerRow)
                  .append(
                    e('<div></div>')
                      .addClass(n.detailInnerName)
                      .append(r[l].data[d].name + s)
                  )
                  .append(
                    e('<div></div>')
                      .addClass(n.detailInnerValue)
                      .attr('data-bind-value', r[l].data[d].bindName)
                      .append(r[l].data[d].display)
                  )
              );
            }
          }
      },
      classes: {
        main: 'footable',
        loading: 'footable-loading',
        loaded: 'footable-loaded',
        toggle: 'footable-toggle',
        disabled: 'footable-disabled',
        detail: 'footable-row-detail',
        detailCell: 'footable-row-detail-cell',
        detailInner: 'footable-row-detail-inner',
        detailInnerRow: 'footable-row-detail-row',
        detailInnerGroup: 'footable-row-detail-group',
        detailInnerName: 'footable-row-detail-name',
        detailInnerValue: 'footable-row-detail-value',
        detailShow: 'footable-detail-show',
      },
      triggers: {
        initialize: 'footable_initialize',
        resize: 'footable_resize',
        redraw: 'footable_redraw',
        toggleRow: 'footable_toggle_row',
        expandFirstRow: 'footable_expand_first_row',
        expandAll: 'footable_expand_all',
        collapseAll: 'footable_collapse_all',
      },
      events: {
        alreadyInitialized: 'footable_already_initialized',
        initializing: 'footable_initializing',
        initialized: 'footable_initialized',
        resizing: 'footable_resizing',
        resized: 'footable_resized',
        redrawn: 'footable_redrawn',
        breakpoint: 'footable_breakpoint',
        columnData: 'footable_column_data',
        rowDetailUpdating: 'footable_row_detail_updating',
        rowDetailUpdated: 'footable_row_detail_updated',
        rowCollapsed: 'footable_row_collapsed',
        rowExpanded: 'footable_row_expanded',
        rowRemoved: 'footable_row_removed',
        reset: 'footable_reset',
      },
      debug: !1,
      log: null,
    },
    version: {
      major: 0,
      minor: 5,
      toString: function () {
        return t.footable.version.major + '.' + t.footable.version.minor;
      },
      parse: function (e) {
        var t = /(\d+)\.?(\d+)?\.?(\d+)?/.exec(e);
        return {
          major: parseInt(t[1], 10) || 0,
          minor: parseInt(t[2], 10) || 0,
          patch: parseInt(t[3], 10) || 0,
        };
      },
    },
    plugins: {
      _validate: function (a) {
        if (!e.isFunction(a))
          return (
            t.footable.options.debug === !0 &&
              console.error(
                'Validation failed, expected type "function", received type "{0}".',
                typeof a
              ),
            !1
          );
        var i = new a();
        return 'string' != typeof i.name
          ? (t.footable.options.debug === !0 &&
              console.error(
                'Validation failed, plugin does not implement a string property called "name".',
                i
              ),
            !1)
          : e.isFunction(i.init)
            ? (t.footable.options.debug === !0 &&
                console.log(
                  'Validation succeeded for plugin "' + i.name + '".',
                  i
                ),
              !0)
            : (t.footable.options.debug === !0 &&
                console.error(
                  'Validation failed, plugin "' +
                    i.name +
                    '" does not implement a function called "init".',
                  i
                ),
              !1);
      },
      registered: [],
      register: function (a, i) {
        t.footable.plugins._validate(a) &&
          (t.footable.plugins.registered.push(a),
          'object' == typeof i && e.extend(!0, t.footable.options, i));
      },
      load: function (e) {
        var a,
          i,
          o = [];
        for (i = 0; t.footable.plugins.registered.length > i; i++)
          try {
            ((a = t.footable.plugins.registered[i]), o.push(new a(e)));
          } catch (n) {
            t.footable.options.debug === !0 && console.error(n);
          }
        return o;
      },
      init: function (e) {
        for (var a = 0; e.plugins.length > a; a++)
          try {
            e.plugins[a].init(e);
          } catch (i) {
            t.footable.options.debug === !0 && console.error(i);
          }
      },
    },
  };
  var o = 0;
  e.fn.footable = function (a) {
    a = a || {};
    var n = e.extend(!0, {}, t.footable.options, a);
    return this.each(function () {
      o++;
      var t = new i(this, n, o);
      e(this).data('footable', t);
    });
  };
})(jQuery, window);
