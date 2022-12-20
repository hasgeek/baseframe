/*
 * validate.js 2.0.1
 * Copyright (c) 2011 - 2015 Rick Harrison, http://rickharrison.me
 * validate.js is open sourced under the MIT license.
 * Portions of validate.js are inspired by CodeIgniter.
 * http://rickharrison.github.com/validate.js
 */
(function (r, t, l) {
  var u = {
      required: 'The %s field is required.',
      matches: 'The %s field does not match the %s field.',
      default: 'The %s field is still set to default, please change.',
      valid_email: 'The %s field must contain a valid email address.',
      valid_emails: 'The %s field must contain all valid email addresses.',
      min_length: 'The %s field must be at least %s characters in length.',
      max_length: 'The %s field must not exceed %s characters in length.',
      exact_length: 'The %s field must be exactly %s characters in length.',
      greater_than: 'The %s field must contain a number greater than %s.',
      less_than: 'The %s field must contain a number less than %s.',
      alpha: 'The %s field must only contain alphabetical characters.',
      alpha_numeric: 'The %s field must only contain alpha-numeric characters.',
      alpha_dash:
        'The %s field must only contain alpha-numeric characters, underscores, and dashes.',
      numeric: 'The %s field must contain only numbers.',
      integer: 'The %s field must contain an integer.',
      decimal: 'The %s field must contain a decimal number.',
      is_natural: 'The %s field must contain only positive numbers.',
      is_natural_no_zero:
        'The %s field must contain a number greater than zero.',
      valid_ip: 'The %s field must contain a valid IP.',
      valid_base64: 'The %s field must contain a base64 string.',
      valid_credit_card:
        'The %s field must contain a valid credit card number.',
      is_file_type: 'The %s field must contain only %s files.',
      valid_url: 'The %s field must contain a valid URL.',
      greater_than_date:
        'The %s field must contain a more recent date than %s.',
      less_than_date: 'The %s field must contain an older date than %s.',
      greater_than_or_equal_date:
        "The %s field must contain a date that's at least as recent as %s.",
      less_than_or_equal_date:
        "The %s field must contain a date that's %s or older.",
    },
    v = function (a) {},
    w = /^(.+?)\[(.+)\]$/,
    g = /^[0-9]+$/,
    x = /^\-?[0-9]+$/,
    m = /^\-?[0-9]*\.?[0-9]+$/,
    q =
      /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
    y = /^[a-z]+$/i,
    z = /^[a-z0-9]+$/i,
    A = /^[a-z0-9_\-]+$/i,
    B = /^[0-9]+$/i,
    C = /^[1-9][0-9]*$/i,
    D =
      /^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})$/i,
    E = /[^a-zA-Z0-9\/\+=]/i,
    F = /^[\d\-\s]+$/,
    G =
      /^((http|https):\/\/(\w+:{0,1}\w*@)?(\S+)|)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?$/,
    H = /\d{4}-\d{1,2}-\d{1,2}/,
    f = function (a, c, b) {
      this.callback = b || v;
      this.errors = [];
      this.fields = {};
      this.form = this._formByNameOrNode(a) || {};
      this.messages = {};
      this.handlers = {};
      this.conditionals = {};
      a = 0;
      for (b = c.length; a < b; a++) {
        var d = c[a];
        if ((d.name || d.names) && d.rules)
          if (d.names)
            for (var n = 0, f = d.names.length; n < f; n++)
              this._addField(d, d.names[n]);
          else this._addField(d, d.name);
        else
          console.warn(
            'validate.js: The following field is being skipped due to a misconfiguration:'
          ),
            console.warn(d),
            console.warn(
              'Check to ensure you have properly configured a name and rules for this field'
            );
      }
      var e = this.form.onsubmit;
      this.form.onsubmit = (function (a) {
        return function (b) {
          try {
            return a._validateForm(b) && (e === l || e());
          } catch (c) {}
        };
      })(this);
    },
    p = function (a, c) {
      var b;
      if (0 < a.length && ('radio' === a[0].type || 'checkbox' === a[0].type))
        for (b = 0, elementLength = a.length; b < elementLength; b++) {
          if (a[b].checked) return a[b][c];
        }
      else return a[c];
    };
  f.prototype.setMessage = function (a, c) {
    this.messages[a] = c;
    return this;
  };
  f.prototype.registerCallback = function (a, c) {
    a &&
      'string' === typeof a &&
      c &&
      'function' === typeof c &&
      (this.handlers[a] = c);
    return this;
  };
  f.prototype.registerConditional = function (a, c) {
    a &&
      'string' === typeof a &&
      c &&
      'function' === typeof c &&
      (this.conditionals[a] = c);
    return this;
  };
  f.prototype._formByNameOrNode = function (a) {
    return 'object' === typeof a ? a : t.forms[a];
  };
  f.prototype._addField = function (a, c) {
    this.fields[c] = {
      name: c,
      display: a.display || c,
      rules: a.rules,
      depends: a.depends,
      id: null,
      element: null,
      type: null,
      value: null,
      checked: null,
    };
  };
  f.prototype._validateForm = function (a) {
    this.errors = [];
    for (var c in this.fields)
      if (this.fields.hasOwnProperty(c)) {
        var b = this.fields[c] || {},
          d = this.form[b.name];
        d &&
          d !== l &&
          ((b.id = p(d, 'id')),
          (b.element = d),
          (b.type = 0 < d.length ? d[0].type : d.type),
          (b.value = p(d, 'value')),
          (b.checked = p(d, 'checked')),
          b.depends && 'function' === typeof b.depends
            ? b.depends.call(this, b) && this._validateField(b)
            : b.depends &&
              'string' === typeof b.depends &&
              this.conditionals[b.depends]
            ? this.conditionals[b.depends].call(this, b) &&
              this._validateField(b)
            : this._validateField(b));
      }
    'function' === typeof this.callback && this.callback(this.errors, a);
    0 < this.errors.length &&
      (a && a.preventDefault
        ? a.preventDefault()
        : event && (event.returnValue = !1));
    return !0;
  };
  f.prototype._validateField = function (a) {
    var c,
      b,
      d = a.rules.split('|'),
      f = a.rules.indexOf('required'),
      I = !a.value || '' === a.value || a.value === l;
    c = 0;
    for (ruleLength = d.length; c < ruleLength; c++) {
      var e = d[c];
      b = null;
      var h = !1,
        k = w.exec(e);
      if (-1 !== f || -1 !== e.indexOf('!callback_') || !I)
        if (
          (k && ((e = k[1]), (b = k[2])),
          '!' === e.charAt(0) && (e = e.substring(1, e.length)),
          'function' === typeof this._hooks[e]
            ? this._hooks[e].apply(this, [a, b]) || (h = !0)
            : 'callback_' === e.substring(0, 9) &&
              ((e = e.substring(9, e.length)),
              'function' === typeof this.handlers[e] &&
                !1 === this.handlers[e].apply(this, [a.value, b, a]) &&
                (h = !0)),
          h)
        ) {
          k = this.messages[a.name + '.' + e] || this.messages[e] || u[e];
          h = 'An error has occurred with the ' + a.display + ' field.';
          k &&
            ((h = k.replace('%s', a.display)),
            b &&
              (h = h.replace(
                '%s',
                this.fields[b] ? this.fields[b].display : b
              )));
          var g;
          for (b = 0; b < this.errors.length; b += 1)
            a.id === this.errors[b].id && (g = this.errors[b]);
          e = g || {
            id: a.id,
            display: a.display,
            element: a.element,
            name: a.name,
            message: h,
            messages: [],
            rule: e,
          };
          e.messages.push(h);
          g || this.errors.push(e);
        }
    }
  };
  f.prototype._getValidDate = function (a) {
    if (!a.match('today') && !a.match(H)) return !1;
    var c = new Date();
    a.match('today') ||
      ((a = a.split('-')),
      c.setFullYear(a[0]),
      c.setMonth(a[1] - 1),
      c.setDate(a[2]));
    return c;
  };
  f.prototype._hooks = {
    required: function (a) {
      var c = a.value;
      return 'checkbox' === a.type || 'radio' === a.type
        ? !0 === a.checked
        : null !== c && '' !== c;
    },
    default: function (a, c) {
      return a.value !== c;
    },
    matches: function (a, c) {
      var b = this.form[c];
      return b ? a.value === b.value : !1;
    },
    valid_email: function (a) {
      return q.test(a.value);
    },
    valid_emails: function (a) {
      a = a.value.split(/\s*,\s*/g);
      for (var c = 0, b = a.length; c < b; c++) if (!q.test(a[c])) return !1;
      return !0;
    },
    min_length: function (a, c) {
      return g.test(c) ? a.value.length >= parseInt(c, 10) : !1;
    },
    max_length: function (a, c) {
      return g.test(c) ? a.value.length <= parseInt(c, 10) : !1;
    },
    exact_length: function (a, c) {
      return g.test(c) ? a.value.length === parseInt(c, 10) : !1;
    },
    greater_than: function (a, c) {
      return m.test(a.value) ? parseFloat(a.value) > parseFloat(c) : !1;
    },
    less_than: function (a, c) {
      return m.test(a.value) ? parseFloat(a.value) < parseFloat(c) : !1;
    },
    alpha: function (a) {
      return y.test(a.value);
    },
    alpha_numeric: function (a) {
      return z.test(a.value);
    },
    alpha_dash: function (a) {
      return A.test(a.value);
    },
    numeric: function (a) {
      return g.test(a.value);
    },
    integer: function (a) {
      return x.test(a.value);
    },
    decimal: function (a) {
      return m.test(a.value);
    },
    is_natural: function (a) {
      return B.test(a.value);
    },
    is_natural_no_zero: function (a) {
      return C.test(a.value);
    },
    valid_ip: function (a) {
      return D.test(a.value);
    },
    valid_base64: function (a) {
      return E.test(a.value);
    },
    valid_url: function (a) {
      return G.test(a.value);
    },
    valid_credit_card: function (a) {
      if (!F.test(a.value)) return !1;
      var c = 0,
        b = 0,
        d = !1;
      a = a.value.replace(/\D/g, '');
      for (var f = a.length - 1; 0 <= f; f--)
        (b = a.charAt(f)),
          (b = parseInt(b, 10)),
          d && 9 < (b *= 2) && (b -= 9),
          (c += b),
          (d = !d);
      return 0 === c % 10;
    },
    is_file_type: function (a, c) {
      if ('file' !== a.type) return !0;
      var b = a.value.substr(a.value.lastIndexOf('.') + 1),
        d = c.split(','),
        f = !1,
        g = 0,
        e = d.length;
      for (g; g < e; g++) b.toUpperCase() == d[g].toUpperCase() && (f = !0);
      return f;
    },
    greater_than_date: function (a, c) {
      var b = this._getValidDate(a.value),
        d = this._getValidDate(c);
      return d && b ? b > d : !1;
    },
    less_than_date: function (a, c) {
      var b = this._getValidDate(a.value),
        d = this._getValidDate(c);
      return d && b ? b < d : !1;
    },
    greater_than_or_equal_date: function (a, c) {
      var b = this._getValidDate(a.value),
        d = this._getValidDate(c);
      return d && b ? b >= d : !1;
    },
    less_than_or_equal_date: function (a, c) {
      var b = this._getValidDate(a.value),
        d = this._getValidDate(c);
      return d && b ? b <= d : !1;
    },
  };
  r.FormValidator = f;
})(window, document);
'undefined' !== typeof module &&
  module.exports &&
  (module.exports = FormValidator);
