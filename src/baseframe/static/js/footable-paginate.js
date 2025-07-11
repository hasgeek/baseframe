/*!
 * FooTable Paginate
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
 * Date: 25 Apr 2014
 */
!(function (a, e, t) {
  function i(e) {
    var t = a(e.table),
      i = t.data();
    ((this.pageNavigation = i.pageNavigation || e.options.pageNavigation),
      (this.pageSize = i.pageSize || e.options.pageSize),
      (this.firstText = i.firstText || e.options.firstText),
      (this.previousText = i.previousText || e.options.previousText),
      (this.nextText = i.nextText || e.options.nextText),
      (this.lastText = i.lastText || e.options.lastText),
      (this.limitNavigation = parseInt(
        i.limitNavigation || e.options.limitNavigation || o.limitNavigation,
        10
      )),
      (this.limitPreviousText =
        i.limitPreviousText || e.options.limitPreviousText),
      (this.limitNextText = i.limitNextText || e.options.limitNextText),
      (this.limit = this.limitNavigation > 0),
      (this.currentPage = i.currentPage || 0),
      (this.pages = []),
      (this.control = !1));
  }
  function n() {
    var e = this;
    ((e.name = 'Footable Paginate'),
      (e.init = function (t) {
        if (t.options.paginate === !0) {
          if (a(t.table).data('page') === !1) return;
          ((e.footable = t),
            a(t.table)
              .unbind('.paging')
              .bind({
                'footable_initialized.paging footable_row_removed.paging footable_redrawn.paging footable_sorted.paging footable_filtered.paging':
                  function () {
                    e.setupPaging();
                  },
              })
              .data('footable-paging', e));
        }
      }),
      (e.setupPaging = function () {
        var t = e.footable,
          n = a(t.table).find('> tbody');
        ((t.pageInfo = new i(t)),
          e.createPages(t, n),
          e.createNavigation(t, n),
          e.fillPage(t, n, t.pageInfo.currentPage));
      }),
      (e.createPages = function (e, t) {
        var i = 1,
          n = e.pageInfo,
          o = i * n.pageSize,
          l = [],
          g = [];
        n.pages = [];
        var s = t.find('> tr:not(.footable-filtered,.footable-row-detail)');
        (s.each(function (a, e) {
          (l.push(e),
            a === o - 1
              ? (n.pages.push(l), i++, (o = i * n.pageSize), (l = []))
              : a >= s.length - (s.length % n.pageSize) && g.push(e));
        }),
          g.length > 0 && n.pages.push(g),
          n.currentPage >= n.pages.length &&
            (n.currentPage = n.pages.length - 1),
          n.currentPage < 0 && (n.currentPage = 0),
          1 === n.pages.length
            ? a(e.table).addClass('no-paging')
            : a(e.table).removeClass('no-paging'));
      }),
      (e.createNavigation = function (t, i) {
        var n = a(t.table).find(t.pageInfo.pageNavigation);
        if (0 === n.length) {
          if (
            ((n = a(t.pageInfo.pageNavigation)),
            n.parents('table:first').length > 0 &&
              n.parents('table:first') !== a(t.table))
          )
            return;
          n.length > 1 &&
            t.options.debug === !0 &&
            console.error('More than one pagination control was found!');
        }
        if (0 !== n.length) {
          (n.is('ul') ||
            (0 === n.find('ul:first').length && n.append('<ul />'),
            (n = n.find('ul'))),
            n.find('li').remove());
          var o = t.pageInfo;
          ((o.control = n),
            o.pages.length > 0 &&
              (n.append(
                '<li class="footable-page-arrow"><a data-page="first" href="#first">' +
                  t.pageInfo.firstText +
                  '</a>'
              ),
              n.append(
                '<li class="footable-page-arrow"><a data-page="prev" href="#prev">' +
                  t.pageInfo.previousText +
                  '</a></li>'
              ),
              o.limit &&
                n.append(
                  '<li class="footable-page-arrow"><a data-page="limit-prev" href="#limit-prev">' +
                    t.pageInfo.limitPreviousText +
                    '</a></li>'
                ),
              o.limit ||
                a.each(o.pages, function (a, e) {
                  e.length > 0 &&
                    n.append(
                      '<li class="footable-page"><a data-page="' +
                        a +
                        '" href="#">' +
                        (a + 1) +
                        '</a></li>'
                    );
                }),
              o.limit &&
                (n.append(
                  '<li class="footable-page-arrow"><a data-page="limit-next" href="#limit-next">' +
                    t.pageInfo.limitNextText +
                    '</a></li>'
                ),
                e.createLimited(n, o, 0)),
              n.append(
                '<li class="footable-page-arrow"><a data-page="next" href="#next">' +
                  t.pageInfo.nextText +
                  '</a></li>'
              ),
              n.append(
                '<li class="footable-page-arrow"><a data-page="last" href="#last">' +
                  t.pageInfo.lastText +
                  '</a></li>'
              )),
            n
              .off('click', 'a[data-page]')
              .on('click', 'a[data-page]', function (i) {
                i.preventDefault();
                var l = a(this).data('page'),
                  g = o.currentPage;
                if ('first' === l) g = 0;
                else if ('prev' === l) g > 0 && g--;
                else if ('next' === l) g < o.pages.length - 1 && g++;
                else if ('last' === l) g = o.pages.length - 1;
                else if ('limit-prev' === l) {
                  g = -1;
                  var s = n.find('.footable-page:first a').data('page');
                  (e.createLimited(n, o, s - o.limitNavigation),
                    e.setPagingClasses(n, o.currentPage, o.pages.length));
                } else if ('limit-next' === l) {
                  g = -1;
                  var r = n.find('.footable-page:last a').data('page');
                  (e.createLimited(n, o, r + 1),
                    e.setPagingClasses(n, o.currentPage, o.pages.length));
                } else g = l;
                if (g >= 0) {
                  if (o.limit && o.currentPage != g) {
                    for (var p = g; p % o.limitNavigation !== 0; ) p -= 1;
                    e.createLimited(n, o, p);
                  }
                  e.paginate(t, g);
                }
              }),
            e.setPagingClasses(n, o.currentPage, o.pages.length));
        }
      }),
      (e.createLimited = function (a, e, t) {
        ((t = t || 0), a.find('li.footable-page').remove());
        var i,
          n,
          o = a
            .find('li.footable-page-arrow > a[data-page="limit-prev"]')
            .parent(),
          l = a
            .find('li.footable-page-arrow > a[data-page="limit-next"]')
            .parent();
        for (i = e.pages.length - 1; i >= 0; i--)
          ((n = e.pages[i]),
            i >= t &&
              i < t + e.limitNavigation &&
              n.length > 0 &&
              o.after(
                '<li class="footable-page"><a data-page="' +
                  i +
                  '" href="#">' +
                  (i + 1) +
                  '</a></li>'
              ));
        (0 === t ? o.hide() : o.show(),
          t + e.limitNavigation >= e.pages.length ? l.hide() : l.show());
      }),
      (e.paginate = function (t, i) {
        var n = t.pageInfo;
        if (n.currentPage !== i) {
          var o = a(t.table).find('> tbody'),
            l = t.raise('footable_paging', { page: i, size: n.pageSize });
          if (l && l.result === !1) return;
          (e.fillPage(t, o, i),
            n.control.find('li').removeClass('active disabled'),
            e.setPagingClasses(n.control, n.currentPage, n.pages.length));
        }
      }),
      (e.setPagingClasses = function (a, e, t) {
        (a
          .find('li.footable-page > a[data-page=' + e + ']')
          .parent()
          .addClass('active'),
          e >= t - 1 &&
            (a
              .find('li.footable-page-arrow > a[data-page="next"]')
              .parent()
              .addClass('disabled'),
            a
              .find('li.footable-page-arrow > a[data-page="last"]')
              .parent()
              .addClass('disabled')),
          1 > e &&
            (a
              .find('li.footable-page-arrow > a[data-page="first"]')
              .parent()
              .addClass('disabled'),
            a
              .find('li.footable-page-arrow > a[data-page="prev"]')
              .parent()
              .addClass('disabled')));
      }),
      (e.fillPage = function (t, i, n) {
        ((t.pageInfo.currentPage = n),
          a(t.table).data('currentPage', n),
          i.find('> tr').hide(),
          a(t.pageInfo.pages[n]).each(function () {
            e.showRow(this, t);
          }),
          t.raise('footable_page_filled'));
      }),
      (e.showRow = function (e, t) {
        var i = a(e),
          n = i.next(),
          o = a(t.table);
        o.hasClass('breakpoint') &&
        i.hasClass('footable-detail-show') &&
        n.hasClass('footable-row-detail')
          ? (i.add(n).show(), t.createOrUpdateDetailRow(e))
          : i.show();
      }));
  }
  if (e.footable === t || null === e.footable)
    throw new Error(
      'Please check and make sure footable.js is included in the page and is loaded prior to this script.'
    );
  var o = {
    paginate: !0,
    pageSize: 10,
    pageNavigation: '.pagination',
    firstText: '&laquo;',
    previousText: '&lsaquo;',
    nextText: '&rsaquo;',
    lastText: '&raquo;',
    limitNavigation: 0,
    limitPreviousText: '...',
    limitNextText: '...',
  };
  e.footable.plugins.register(n, o);
})(jQuery, window);
