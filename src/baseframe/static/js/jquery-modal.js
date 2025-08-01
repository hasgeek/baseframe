/*
    A simple jQuery modal (http://github.com/kylefox/jquery-modal)
    jQuery Modal is distributed under the MIT License.
    Version 0.8.2
*/
!(function (o) {
  'object' == typeof module && 'object' == typeof module.exports
    ? o(require('jquery'), window, document)
    : o(jQuery, window, document);
})(function (o, t, e, i) {
  var s = [],
    l = function () {
      return s.length ? s[s.length - 1] : null;
    },
    n = function () {
      var o,
        t = !1;
      for (o = s.length - 1; o >= 0; o--)
        s[o].$blocker &&
          (s[o].$blocker.toggleClass('current', !t).toggleClass('behind', t),
          (t = !0));
    };
  ((o.modal = function (t, e) {
    var i, n;
    if (
      ((this.$body = o('body')),
      (this.options = o.extend({}, o.modal.defaults, e)),
      (this.options.doFade = !isNaN(parseInt(this.options.fadeDuration, 10))),
      (this.$blocker = null),
      this.options.closeExisting)
    )
      for (; o.modal.isActive(); ) o.modal.close();
    if ((s.push(this), t.is('a')))
      if (((n = t.attr('href')), /^#/.test(n))) {
        if (((this.$elm = o(n)), 1 !== this.$elm.length)) return null;
        (this.$body.append(this.$elm), this.open());
      } else
        ((this.$elm = o('<div>')),
          this.$body.append(this.$elm),
          (i = function (o, t) {
            t.elm.remove();
          }),
          this.showSpinner(),
          t.trigger(o.modal.AJAX_SEND),
          o
            .get(n)
            .done(function (e) {
              if (o.modal.isActive()) {
                t.trigger(o.modal.AJAX_SUCCESS);
                var s = l();
                (s.$elm.empty().append(e).on(o.modal.CLOSE, i),
                  s.hideSpinner(),
                  s.open(),
                  t.trigger(o.modal.AJAX_COMPLETE));
              }
            })
            .fail(function () {
              t.trigger(o.modal.AJAX_FAIL);
              var e = l();
              (e.hideSpinner(), s.pop(), t.trigger(o.modal.AJAX_COMPLETE));
            }));
    else ((this.$elm = t), this.$body.append(this.$elm), this.open());
  }),
    (o.modal.prototype = {
      constructor: o.modal,
      open: function () {
        var t = this;
        (this.block(),
          this.options.doFade
            ? setTimeout(function () {
                t.show();
              }, this.options.fadeDuration * this.options.fadeDelay)
            : this.show(),
          o(e)
            .off('keydown.modal')
            .on('keydown.modal', function (o) {
              var t = l();
              27 == o.which && t.options.escapeClose && t.close();
            }),
          this.options.clickClose &&
            this.$blocker.click(function (t) {
              t.target == this && o.modal.close();
            }));
      },
      close: function () {
        (s.pop(),
          this.unblock(),
          this.hide(),
          o.modal.isActive() || o(e).off('keydown.modal'));
      },
      block: function () {
        (this.$elm.trigger(o.modal.BEFORE_BLOCK, [this._ctx()]),
          this.$body.css('overflow', 'hidden'),
          (this.$blocker = o(
            '<div class="' +
              this.options.blockerClass +
              ' blocker current"></div>'
          ).appendTo(this.$body)),
          n(),
          this.options.doFade &&
            this.$blocker
              .css('opacity', 0)
              .animate({ opacity: 1 }, this.options.fadeDuration),
          this.$elm.trigger(o.modal.BLOCK, [this._ctx()]));
      },
      unblock: function (t) {
        !t && this.options.doFade
          ? this.$blocker.fadeOut(
              this.options.fadeDuration,
              this.unblock.bind(this, !0)
            )
          : (this.$blocker.children().appendTo(this.$body),
            this.$blocker.remove(),
            (this.$blocker = null),
            n(),
            o.modal.isActive() || this.$body.css('overflow', ''));
      },
      show: function () {
        (this.$elm.trigger(o.modal.BEFORE_OPEN, [this._ctx()]),
          this.options.showClose &&
            ((this.closeButton = o(
              '<a href="#close-modal" rel="modal:close" class="close-modal ' +
                this.options.closeClass +
                '">' +
                this.options.closeText +
                '</a>'
            )),
            this.$elm.append(this.closeButton)),
          this.$elm.addClass(this.options.modalClass).appendTo(this.$blocker),
          this.options.doFade
            ? this.$elm
                .css('opacity', 0)
                .show()
                .animate({ opacity: 1 }, this.options.fadeDuration)
            : this.$elm.show(),
          this.$elm.trigger(o.modal.OPEN, [this._ctx()]));
      },
      hide: function () {
        (this.$elm.trigger(o.modal.BEFORE_CLOSE, [this._ctx()]),
          this.closeButton && this.closeButton.remove());
        var t = this;
        (this.options.doFade
          ? this.$elm.fadeOut(this.options.fadeDuration, function () {
              t.$elm.trigger(o.modal.AFTER_CLOSE, [t._ctx()]);
            })
          : this.$elm.hide(0, function () {
              t.$elm.trigger(o.modal.AFTER_CLOSE, [t._ctx()]);
            }),
          this.$elm.trigger(o.modal.CLOSE, [this._ctx()]));
      },
      showSpinner: function () {
        this.options.showSpinner &&
          ((this.spinner =
            this.spinner ||
            o(
              '<div class="' + this.options.modalClass + '-spinner"></div>'
            ).append(this.options.spinnerHtml)),
          this.$body.append(this.spinner),
          this.spinner.show());
      },
      hideSpinner: function () {
        this.spinner && this.spinner.remove();
      },
      _ctx: function () {
        return {
          elm: this.$elm,
          $elm: this.$elm,
          $blocker: this.$blocker,
          options: this.options,
        };
      },
    }),
    (o.modal.close = function (t) {
      if (o.modal.isActive()) {
        t && t.preventDefault();
        var e = l();
        return (e.close(), e.$elm);
      }
    }),
    (o.modal.isActive = function () {
      return s.length > 0;
    }),
    (o.modal.getCurrent = l),
    (o.modal.defaults = {
      closeExisting: !0,
      escapeClose: !0,
      clickClose: !0,
      closeText: 'Close',
      closeClass: '',
      modalClass: 'modal',
      blockerClass: 'jquery-modal',
      spinnerHtml: null,
      showSpinner: !0,
      showClose: !0,
      fadeDuration: null,
      fadeDelay: 1,
    }),
    (o.modal.BEFORE_BLOCK = 'modal:before-block'),
    (o.modal.BLOCK = 'modal:block'),
    (o.modal.BEFORE_OPEN = 'modal:before-open'),
    (o.modal.OPEN = 'modal:open'),
    (o.modal.BEFORE_CLOSE = 'modal:before-close'),
    (o.modal.CLOSE = 'modal:close'),
    (o.modal.AFTER_CLOSE = 'modal:after-close'),
    (o.modal.AJAX_SEND = 'modal:ajax:send'),
    (o.modal.AJAX_SUCCESS = 'modal:ajax:success'),
    (o.modal.AJAX_FAIL = 'modal:ajax:fail'),
    (o.modal.AJAX_COMPLETE = 'modal:ajax:complete'),
    (o.fn.modal = function (t) {
      return (1 === this.length && new o.modal(this, t), this);
    }),
    o(e).on('click.modal', 'a[rel~="modal:close"]', o.modal.close),
    o(e).on('click.modal', 'a[rel~="modal:open"]', function (t) {
      (t.preventDefault(), o(this).modal());
    }));
});
