/*! jquery-jeditable https://github.com/NicolasCARPi/jquery_jeditable#readme */

!(function ($) {
  'use strict';
  (($.fn.editableAriaShim = function () {
    return (this.attr({ role: 'button', tabindex: 0 }), this);
  }),
    ($.fn.editable = function (target, options) {
      if ('disable' !== target)
        if ('enable' !== target) {
          if ('destroy' !== target) {
            var settings = $.extend(
                {},
                $.fn.editable.defaults,
                { target: target },
                options
              ),
              plugin = $.editable.types[settings.type].plugin || function () {},
              submit = $.editable.types[settings.type].submit || function () {},
              buttons =
                $.editable.types[settings.type].buttons ||
                $.editable.types.defaults.buttons,
              content =
                $.editable.types[settings.type].content ||
                $.editable.types.defaults.content,
              element =
                $.editable.types[settings.type].element ||
                $.editable.types.defaults.element,
              reset =
                $.editable.types[settings.type].reset ||
                $.editable.types.defaults.reset,
              destroy =
                $.editable.types[settings.type].destroy ||
                $.editable.types.defaults.destroy,
              callback = settings.callback || function () {},
              intercept =
                settings.intercept ||
                function (s) {
                  return s;
                },
              onedit = settings.onedit || function () {},
              onsubmit = settings.onsubmit || function () {},
              onreset = settings.onreset || function () {},
              onerror = settings.onerror || reset;
            settings.before;
            return (
              settings.tooltip && $(this).attr('title', settings.tooltip),
              this.each(function () {
                var self = this;
                ($(this).data('event.editable', settings.event),
                  $.trim($(this).html()) || $(this).html(settings.placeholder),
                  'destroy' !== target
                    ? ($(this).on(settings.event, function (e) {
                        if (
                          !0 !== $(this).data('disabled.editable') &&
                          9 !== e.which &&
                          !self.editing &&
                          !1 !== onedit.apply(this, [settings, self, e])
                        ) {
                          if (
                            settings.before &&
                            jQuery.isFunction(settings.before)
                          )
                            settings.before(e);
                          else if (
                            settings.before &&
                            !jQuery.isFunction(settings.before)
                          )
                            throw "The 'before' option needs to be provided as a function!";
                          (e.preventDefault(),
                            e.stopPropagation(),
                            settings.tooltip && $(self).removeAttr('title'),
                            $(this)
                              .html()
                              .toLowerCase()
                              .replace(/(;|"|\/)/g, '') ===
                              settings.placeholder
                                .toLowerCase()
                                .replace(/(;|"|\/)/g, '') && $(this).html(''),
                            (self.editing = !0),
                            (self.revert = $(self).text()),
                            $(self).html(''));
                          var form = $('<form />');
                          (settings.cssclass &&
                            ('inherit' === settings.cssclass
                              ? form.attr('class', $(self).attr('class'))
                              : form.attr('class', settings.cssclass)),
                            settings.style &&
                              ('inherit' === settings.style
                                ? (form.attr('style', $(self).attr('style')),
                                  form.css('display', $(self).css('display')))
                                : form.attr('style', settings.style)),
                            settings.label &&
                              form.append(
                                '<label>' + settings.label + '</label>'
                              ),
                            settings.formid &&
                              form.attr('id', settings.formid));
                          var input_content,
                            t,
                            input = element.apply(form, [settings, self]);
                          settings.inputcssclass &&
                            ('inherit' === settings.inputcssclass
                              ? input.attr('class', $(self).attr('class'))
                              : input.attr('class', settings.inputcssclass));
                          var isSubmitting = !1;
                          if (settings.loadurl) {
                            ((t = self.setTimeout(function () {
                              input.disabled = !0;
                            }, 100)),
                              $(self).html(settings.loadtext));
                            var loaddata = {};
                            ((loaddata[settings.id] = self.id),
                              $.isFunction(settings.loaddata)
                                ? $.extend(
                                    loaddata,
                                    settings.loaddata.apply(self, [
                                      self.revert,
                                      settings,
                                    ])
                                  )
                                : $.extend(loaddata, settings.loaddata),
                              $.ajax({
                                type: settings.loadtype,
                                url: settings.loadurl,
                                data: loaddata,
                                async: !1,
                                cache: !1,
                                success: function (result) {
                                  (self.clearTimeout(t),
                                    (input_content = result),
                                    (input.disabled = !1));
                                },
                              }));
                          } else
                            settings.data
                              ? ((input_content = settings.data),
                                $.isFunction(settings.data) &&
                                  (input_content = settings.data.apply(self, [
                                    self.revert,
                                    settings,
                                  ])))
                              : (input_content = self.revert);
                          if (
                            (content.apply(form, [
                              input_content,
                              settings,
                              self,
                            ]),
                            input.attr('name', settings.name),
                            'none' !== settings.width)
                          ) {
                            var adj_width =
                              settings.width -
                              (input.outerWidth(!0) - settings.width);
                            input.width(adj_width);
                          }
                          (buttons.apply(form, [settings, self]),
                            settings.showfn &&
                              $.isFunction(settings.showfn) &&
                              form.hide(),
                            $(self).html(''),
                            $(self).append(form),
                            settings.showfn &&
                              $.isFunction(settings.showfn) &&
                              settings.showfn(form),
                            plugin.apply(form, [settings, self]),
                            form
                              .find(':input:visible:enabled:first')
                              .trigger('focus'),
                            settings.select && input.select(),
                            $(this).on('keydown', function (e) {
                              27 === e.which &&
                                (e.preventDefault(),
                                reset.apply(form, [settings, self]));
                            }),
                            'cancel' === settings.onblur
                              ? input.blur(function (e) {
                                  t = self.setTimeout(function () {
                                    reset.apply(form, [settings, self]);
                                  }, 500);
                                })
                              : 'submit' === settings.onblur
                                ? input.blur(function (e) {
                                    t = self.setTimeout(function () {
                                      form.trigger('submit');
                                    }, 200);
                                  })
                                : $.isFunction(settings.onblur) &&
                                  input.blur(function (e) {
                                    !1 ===
                                      settings.onblur.apply(self, [
                                        input.val(),
                                        settings,
                                        form,
                                      ]) && reset.apply(form, [settings, self]);
                                  }),
                            form.on('submit', function (e) {
                              if (
                                (e.preventDefault(),
                                e.stopPropagation(),
                                isSubmitting)
                              )
                                return !1;
                              if (
                                ((isSubmitting = !0),
                                t && self.clearTimeout(t),
                                (isSubmitting =
                                  !1 !==
                                  onsubmit.apply(form, [settings, self])) &&
                                  (isSubmitting =
                                    !1 !==
                                    submit.apply(form, [settings, self])))
                              )
                                if ($.isFunction(settings.target)) {
                                  var responseHandler = function (
                                      value,
                                      complete
                                    ) {
                                      ((isSubmitting = !1),
                                        !1 !== complete &&
                                          ($(self).html(value),
                                          (self.editing = !1),
                                          callback.apply(self, [
                                            self.innerHTML,
                                            settings,
                                          ]),
                                          $.trim($(self).html()) ||
                                            $(self).html(
                                              settings.placeholder
                                            )));
                                    },
                                    userTarget = settings.target.apply(self, [
                                      input.val(),
                                      settings,
                                      responseHandler,
                                    ]);
                                  !1 !== userTarget &&
                                    void 0 !== userTarget &&
                                    responseHandler(userTarget, userTarget);
                                } else {
                                  var submitdata = {};
                                  ((submitdata[settings.name] = input.val()),
                                    (submitdata[settings.id] = self.id),
                                    $.isFunction(settings.submitdata)
                                      ? $.extend(
                                          submitdata,
                                          settings.submitdata.apply(self, [
                                            self.revert,
                                            settings,
                                            submitdata,
                                          ])
                                        )
                                      : $.extend(
                                          submitdata,
                                          settings.submitdata
                                        ),
                                    'PUT' === settings.method &&
                                      (submitdata._method = 'put'),
                                    $(self).html(settings.indicator));
                                  var ajaxoptions = {
                                    type: 'POST',
                                    complete: function (xhr, status) {
                                      isSubmitting = !1;
                                    },
                                    data: submitdata,
                                    dataType: 'html',
                                    url: settings.target,
                                    success: function (result, status) {
                                      ((result = intercept.apply(self, [
                                        result,
                                        status,
                                      ])),
                                        'html' === ajaxoptions.dataType &&
                                          $(self).html(result),
                                        (self.editing = !1),
                                        callback.apply(self, [
                                          result,
                                          settings,
                                          submitdata,
                                        ]),
                                        $.trim($(self).html()) ||
                                          $(self).html(settings.placeholder));
                                    },
                                    error: function (xhr, status, error) {
                                      onerror.apply(form, [
                                        settings,
                                        self,
                                        xhr,
                                      ]);
                                    },
                                  };
                                  ($.extend(ajaxoptions, settings.ajaxoptions),
                                    $.ajax(ajaxoptions));
                                }
                              return (
                                $(self).attr('title', settings.tooltip),
                                !1
                              );
                            }));
                        }
                      }),
                      (self.reset = function (form) {
                        self.editing &&
                          !1 !== onreset.apply(form, [settings, self]) &&
                          ($(self).text(self.revert),
                          (self.editing = !1),
                          $.trim($(self).html()) ||
                            $(self).html(settings.placeholder),
                          settings.tooltip &&
                            $(self).attr('title', settings.tooltip));
                      }),
                      (self.destroy = function (form) {
                        ($(self)
                          .off($(self).data('event.editable'))
                          .removeData('disabled.editable')
                          .removeData('event.editable'),
                          self.clearTimeouts(),
                          self.editing && reset.apply(form, [settings, self]));
                      }),
                      (self.clearTimeout = function (t) {
                        var timeouts = $(self).data('timeouts');
                        if ((clearTimeout(t), timeouts)) {
                          var i = timeouts.indexOf(t);
                          i > -1
                            ? (timeouts.splice(i, 1),
                              timeouts.length <= 0 &&
                                $(self).removeData('timeouts'))
                            : console.warn(
                                'jeditable clearTimeout could not find timeout ' +
                                  t
                              );
                        }
                      }),
                      (self.clearTimeouts = function () {
                        var timeouts = $(self).data('timeouts');
                        if (timeouts) {
                          for (var i = 0, n = timeouts.length; i < n; ++i)
                            clearTimeout(timeouts[i]);
                          ((timeouts.length = 0),
                            $(self).removeData('timeouts'));
                        }
                      }),
                      (self.setTimeout = function (callback, time) {
                        var timeouts = $(self).data('timeouts'),
                          t = setTimeout(function () {
                            (callback(), self.clearTimeout(t));
                          }, time);
                        return (
                          timeouts ||
                            ((timeouts = []),
                            $(self).data('timeouts', timeouts)),
                          timeouts.push(t),
                          t
                        );
                      }))
                    : destroy.apply($(this).find('form'), [settings, self]));
              })
            );
          }
          $(this)
            .off($(this).data('event.editable'))
            .removeData('disabled.editable')
            .removeData('event.editable');
        } else $(this).data('disabled.editable', !1);
      else $(this).data('disabled.editable', !0);
    }));
  var _supportInType = function (type) {
    var i = document.createElement('input');
    return (i.setAttribute('type', type), 'text' !== i.type ? type : 'text');
  };
  (($.editable = {
    types: {
      defaults: {
        element: function (settings, original) {
          var input = $('<input type="hidden"></input>');
          return ($(this).append(input), input);
        },
        content: function (string, settings, original) {
          $(this).find(':input:first').val(string);
        },
        reset: function (settings, original) {
          original.reset(this);
        },
        destroy: function (settings, original) {
          original.destroy(this);
        },
        buttons: function (settings, original) {
          var submit,
            cancel,
            form = this;
          (settings.submit &&
            (settings.submit.match(/>$/)
              ? (submit = $(settings.submit).on('click', function () {
                  'submit' !== submit.attr('type') && form.trigger('submit');
                }))
              : ((submit = $('<button type="submit" />')).html(settings.submit),
                settings.submitcssclass &&
                  submit.addClass(settings.submitcssclass)),
            $(this).append(submit)),
          settings.cancel) &&
            (settings.cancel.match(/>$/)
              ? (cancel = $(settings.cancel))
              : ((cancel = $('<button type="cancel" />')).html(settings.cancel),
                settings.cancelcssclass &&
                  cancel.addClass(settings.cancelcssclass)),
            $(this).append(cancel),
            $(cancel).on('click', function (event) {
              return (
                ($.isFunction($.editable.types[settings.type].reset)
                  ? $.editable.types[settings.type].reset
                  : $.editable.types.defaults.reset
                ).apply(form, [settings, original]),
                !1
              );
            }));
        },
      },
      text: {
        element: function (settings, original) {
          var input = $('<input />').attr({
            autocomplete: 'off',
            list: settings.list,
            maxlength: settings.maxlength,
            pattern: settings.pattern,
            placeholder: settings.placeholder,
            tooltip: settings.tooltip,
            type: 'text',
          });
          return (
            'none' !== settings.width && input.css('width', settings.width),
            'none' !== settings.height && input.css('height', settings.height),
            settings.size && input.attr('size', settings.size),
            settings.maxlength && input.attr('maxlength', settings.maxlength),
            $(this).append(input),
            input
          );
        },
      },
      textarea: {
        element: function (settings, original) {
          var textarea = $('<textarea></textarea>');
          return (
            settings.rows
              ? textarea.attr('rows', settings.rows)
              : 'none' !== settings.height && textarea.height(settings.height),
            settings.cols
              ? textarea.attr('cols', settings.cols)
              : 'none' !== settings.width && textarea.width(settings.width),
            settings.maxlength &&
              textarea.attr('maxlength', settings.maxlength),
            $(this).append(textarea),
            textarea
          );
        },
      },
      select: {
        element: function (settings, original) {
          var select = $('<select />');
          return (
            settings.multiple && select.attr('multiple', 'multiple'),
            $(this).append(select),
            select
          );
        },
        content: function (data, settings, original) {
          var json;
          json = String === data.constructor ? JSON.parse(data) : data;
          var key,
            option,
            tuples = [];
          if (Array.isArray(json) && json.every(Array.isArray))
            ((tuples = json),
              (json = {}),
              tuples.forEach(function (e) {
                json[e[0]] = e[1];
              }));
          else for (key in json) tuples.push([key, json[key]]);
          settings.sortselectoptions &&
            tuples.sort(function (a, b) {
              return (a = a[1]) < (b = b[1]) ? -1 : a > b ? 1 : 0;
            });
          for (var i = 0; i < tuples.length; i++) {
            key = tuples[i][0];
            var value = tuples[i][1];
            json.hasOwnProperty(key) &&
              'selected' !== key &&
              ((option = $('<option />').val(key).append(value)),
              (json.selected !== key && key !== $.trim(original.revert)) ||
                $(option).prop('selected', 'selected'),
              $(this).find('select').append(option));
          }
          if (!settings.submit) {
            var form = this;
            $(this)
              .find('select')
              .change(function () {
                form.trigger('submit');
              });
          }
        },
      },
      number: {
        element: function (settings, original) {
          var input = $('<input />').attr({
            maxlength: settings.maxlength,
            placeholder: settings.placeholder,
            min: settings.min,
            max: settings.max,
            step: settings.step,
            tooltip: settings.tooltip,
            type: _supportInType('number'),
          });
          return (
            'none' !== settings.width && input.css('width', settings.width),
            $(this).append(input),
            input
          );
        },
      },
      email: {
        element: function (settings, original) {
          var input = $('<input />').attr({
            maxlength: settings.maxlength,
            placeholder: settings.placeholder,
            tooltip: settings.tooltip,
            type: _supportInType('email'),
          });
          return (
            'none' !== settings.width && input.css('width', settings.width),
            $(this).append(input),
            input
          );
        },
      },
      url: {
        element: function (settings, original) {
          var input = $('<input />').attr({
            maxlength: settings.maxlength,
            pattern: settings.pattern,
            placeholder: settings.placeholder,
            tooltip: settings.tooltip,
            type: _supportInType('url'),
          });
          return (
            'none' !== settings.width && input.css('width', settings.width),
            $(this).append(input),
            input
          );
        },
      },
    },
    addInputType: function (name, input) {
      $.editable.types[name] = input;
    },
  }),
    ($.fn.editable.defaults = {
      name: 'value',
      id: 'id',
      type: 'text',
      width: 'auto',
      height: 'auto',
      event: 'click.editable keydown.editable',
      onblur: 'cancel',
      tooltip: 'Click to edit',
      loadtype: 'GET',
      loadtext: 'Loading...',
      placeholder: 'Click to edit',
      sortselectoptions: !1,
      loaddata: {},
      submitdata: {},
      ajaxoptions: {},
    }));
})(jQuery);
