/*
  Ractive.js v0.7.3
  Sat Apr 25 2015 13:52:38 GMT-0400 (EDT) - commit da40f81c660ba2f09c45a09a9c20fdd34ee36d80

  http://ractivejs.org
  http://twitter.com/RactiveJS

  Released under the MIT License.
*/
!(function (t, e) {
  'object' == typeof exports && 'undefined' != typeof module
    ? (module.exports = e())
    : 'function' == typeof define && define.amd
      ? define(e)
      : (t.Ractive = e());
})(this, function () {
  'use strict';
  function t(t) {
    var e;
    if (t && 'boolean' != typeof t)
      return 'undefined' != typeof window && document && t
        ? t.nodeType
          ? t
          : 'string' == typeof t &&
              ((e = document.getElementById(t)),
              !e && document.querySelector && (e = document.querySelector(t)),
              e && e.nodeType)
            ? e
            : t[0] && t[0].nodeType
              ? t[0]
              : null
        : null;
  }
  function e(t) {
    return (
      t &&
        'unknown' != typeof t.parentNode &&
        t.parentNode &&
        t.parentNode.removeChild(t),
      t
    );
  }
  function n(t) {
    return null != t && t.toString ? t : '';
  }
  function i(t) {
    for (
      var e = arguments.length, n = Array(e > 1 ? e - 1 : 0), i = 1;
      e > i;
      i++
    )
      n[i - 1] = arguments[i];
    for (var r, s; (s = n.shift()); )
      for (r in s) Oa.call(s, r) && (t[r] = s[r]);
    return t;
  }
  function r(t) {
    for (
      var e = arguments.length, n = Array(e > 1 ? e - 1 : 0), i = 1;
      e > i;
      i++
    )
      n[i - 1] = arguments[i];
    return (
      n.forEach(function (e) {
        for (var n in e) !e.hasOwnProperty(n) || n in t || (t[n] = e[n]);
      }),
      t
    );
  }
  function s(t) {
    return '[object Array]' === Pa.call(t);
  }
  function o(t) {
    return Ta.test(Pa.call(t));
  }
  function a(t, e) {
    return null === t && null === e
      ? !0
      : 'object' == typeof t || 'object' == typeof e
        ? !1
        : t === e;
  }
  function u(t) {
    return !isNaN(parseFloat(t)) && isFinite(t);
  }
  function h(t) {
    return t && '[object Object]' === Pa.call(t);
  }
  function c(t, e) {
    return t.replace(/%s/g, function () {
      return e.shift();
    });
  }
  function l(t) {
    for (
      var e = arguments.length, n = Array(e > 1 ? e - 1 : 0), i = 1;
      e > i;
      i++
    )
      n[i - 1] = arguments[i];
    throw ((t = c(t, n)), new Error(t));
  }
  function f() {
    Qb.DEBUG && Aa.apply(null, arguments);
  }
  function d(t) {
    for (
      var e = arguments.length, n = Array(e > 1 ? e - 1 : 0), i = 1;
      e > i;
      i++
    )
      n[i - 1] = arguments[i];
    ((t = c(t, n)), Sa(t, n));
  }
  function p(t) {
    for (
      var e = arguments.length, n = Array(e > 1 ? e - 1 : 0), i = 1;
      e > i;
      i++
    )
      n[i - 1] = arguments[i];
    ((t = c(t, n)), Ra[t] || ((Ra[t] = !0), Sa(t, n)));
  }
  function m() {
    Qb.DEBUG && d.apply(null, arguments);
  }
  function v() {
    Qb.DEBUG && p.apply(null, arguments);
  }
  function g(t, e, n) {
    var i = y(t, e, n);
    return i ? i[t][n] : null;
  }
  function y(t, e, n) {
    for (; e; ) {
      if (n in e[t]) return e;
      if (e.isolated) return null;
      e = e.parent;
    }
  }
  function b(t) {
    return function () {
      return t;
    };
  }
  function w(t) {
    var e, n, i, r, s, o;
    for (
      e = t.split('.'),
        (n = Wa[e.length]) || (n = x(e.length)),
        s = [],
        i = function (t, n) {
          return t ? '*' : e[n];
        },
        r = n.length;
      r--;

    )
      ((o = n[r].map(i).join('.')),
        s.hasOwnProperty(o) || (s.push(o), (s[o] = !0)));
    return s;
  }
  function x(t) {
    var e,
      n,
      i,
      r,
      s,
      o,
      a,
      u,
      h = '';
    if (!Wa[t]) {
      for (i = []; h.length < t; ) h += 1;
      for (
        e = parseInt(h, 2),
          r = function (t) {
            return '1' === t;
          },
          s = 0;
        e >= s;
        s += 1
      ) {
        for (n = s.toString(2); n.length < t; ) n = '0' + n;
        for (u = [], a = n.length, o = 0; a > o; o++) u.push(r(n[o]));
        i[s] = u;
      }
      Wa[t] = i;
    }
    return Wa[t];
  }
  function k(t, e, n, i) {
    var r = t[e];
    if (!r || (!r.equalsOrStartsWith(i) && r.equalsOrStartsWith(n)))
      return ((t[e] = r ? r.replace(n, i) : i), !0);
  }
  function E(t) {
    var e = t.slice(2);
    return 'i' === t[1] && u(e) ? +e : e;
  }
  function _(t) {
    return null == t ? t : (qa.hasOwnProperty(t) || (qa[t] = new $a(t)), qa[t]);
  }
  function A(t, e) {
    function n(e, n) {
      var i, r, o;
      return (
        n.isRoot
          ? (o = [].concat(
              Object.keys(t.viewmodel.data),
              Object.keys(t.viewmodel.mappings),
              Object.keys(t.viewmodel.computations)
            ))
          : ((i = t.viewmodel.wrapped[n.str]),
            (r = i ? i.get() : t.viewmodel.get(n)),
            (o = r ? Object.keys(r) : null)),
        o &&
          o.forEach(function (t) {
            ('_ractive' === t && s(r)) || e.push(n.join(t));
          }),
        e
      );
    }
    var i, r, o;
    for (i = e.str.split('.'), o = [Za]; (r = i.shift()); )
      '*' === r
        ? (o = o.reduce(n, []))
        : o[0] === Za
          ? (o[0] = _(r))
          : (o = o.map(S(r)));
    return o;
  }
  function S(t) {
    return function (e) {
      return e.join(t);
    };
  }
  function C(t) {
    return t ? t.replace(za, '.$1') : '';
  }
  function O(t, e, n) {
    if ('string' != typeof e || !u(n)) throw new Error('Bad arguments');
    var i = void 0,
      r = void 0;
    if (/\*/.test(e))
      return (
        (r = {}),
        A(t, _(C(e))).forEach(function (e) {
          var i = t.viewmodel.get(e);
          if (!u(i)) throw new Error(Ka);
          r[e.str] = i + n;
        }),
        t.set(r)
      );
    if (((i = t.get(e)), !u(i))) throw new Error(Ka);
    return t.set(e, +i + n);
  }
  function P(t, e) {
    return Ha(this, t, void 0 === e ? 1 : +e);
  }
  function T(t) {
    ((this.event = t), (this.method = 'on' + t), (this.deprecate = tu[t]));
  }
  function F(t, e) {
    var n = t.indexOf(e);
    -1 === n && t.push(e);
  }
  function R(t, e) {
    for (var n = 0, i = t.length; i > n; n++) if (t[n] == e) return !0;
    return !1;
  }
  function j(t, e) {
    var n;
    if (!s(t) || !s(e)) return !1;
    if (t.length !== e.length) return !1;
    for (n = t.length; n--; ) if (t[n] !== e[n]) return !1;
    return !0;
  }
  function N(t) {
    return 'string' == typeof t ? [t] : void 0 === t ? [] : t;
  }
  function D(t) {
    return t[t.length - 1];
  }
  function I(t, e) {
    var n = t.indexOf(e);
    -1 !== n && t.splice(n, 1);
  }
  function L(t) {
    for (var e = [], n = t.length; n--; ) e[n] = t[n];
    return e;
  }
  function V(t) {
    setTimeout(t, 0);
  }
  function M(t, e) {
    return function () {
      for (var n; (n = t.shift()); ) n(e);
    };
  }
  function U(t, e, n, i) {
    var r;
    if (e === t)
      throw new TypeError(
        "A promise's fulfillment handler cannot return the same promise"
      );
    if (e instanceof eu) e.then(n, i);
    else if (!e || ('object' != typeof e && 'function' != typeof e)) n(e);
    else {
      try {
        r = e.then;
      } catch (s) {
        return void i(s);
      }
      if ('function' == typeof r) {
        var o, a, u;
        ((a = function (e) {
          o || ((o = !0), U(t, e, n, i));
        }),
          (u = function (t) {
            o || ((o = !0), i(t));
          }));
        try {
          r.call(e, a, u);
        } catch (s) {
          if (!o) return (i(s), void (o = !0));
        }
      } else n(e);
    }
  }
  function W(t, e, n) {
    var i;
    return (
      (e = C(e)),
      '~/' === e.substr(0, 2)
        ? ((i = _(e.substring(2))), q(t, i.firstKey, n))
        : '.' === e[0]
          ? ((i = z(au(n), e)), i && q(t, i.firstKey, n))
          : (i = B(t, _(e), n)),
      i
    );
  }
  function z(t, e) {
    var n;
    if ((void 0 != t && 'string' != typeof t && (t = t.str), '.' === e))
      return _(t);
    if (((n = t ? t.split('.') : []), '../' === e.substr(0, 3))) {
      for (; '../' === e.substr(0, 3); ) {
        if (!n.length)
          throw new Error(
            'Could not resolve reference - too many "../" prefixes'
          );
        (n.pop(), (e = e.substring(3)));
      }
      return (n.push(e), _(n.join('.')));
    }
    return _(t ? t + e.replace(/^\.\//, '.') : e.replace(/^\.\/?/, ''));
  }
  function B(t, e, n, i) {
    var r, s, o, a, u;
    if (e.isRoot) return e;
    for (s = e.firstKey; n; )
      if (
        ((r = n.context),
        (n = n.parent),
        r &&
          ((a = !0),
          (o = t.viewmodel.get(r)),
          o && ('object' == typeof o || 'function' == typeof o) && s in o))
      )
        return r.join(e.str);
    return $(t.viewmodel, s)
      ? e
      : t.parent &&
          !t.isolated &&
          ((a = !0),
          (n = t.component.parentFragment),
          (s = _(s)),
          (u = B(t.parent, s, n, !0)))
        ? (t.viewmodel.map(s, { origin: t.parent.viewmodel, keypath: u }), e)
        : i || a
          ? void 0
          : (t.viewmodel.set(e, void 0), e);
  }
  function q(t, e) {
    var n;
    !t.parent ||
      t.isolated ||
      $(t.viewmodel, e) ||
      ((e = _(e)),
      (n = B(t.parent, e, t.component.parentFragment, !0)) &&
        t.viewmodel.map(e, { origin: t.parent.viewmodel, keypath: n }));
  }
  function $(t, e) {
    return '' === e || e in t.data || e in t.computations || e in t.mappings;
  }
  function Q(t) {
    t.teardown();
  }
  function Z(t) {
    t.unbind();
  }
  function H(t) {
    t.unrender();
  }
  function K(t) {
    t.cancel();
  }
  function G(t) {
    t.detach();
  }
  function Y(t) {
    t.detachNodes();
  }
  function J(t) {
    !t.ready ||
      t.outros.length ||
      t.outroChildren ||
      (t.outrosComplete ||
        (t.parent ? t.parent.decrementOutros(t) : t.detachNodes(),
        (t.outrosComplete = !0)),
      t.intros.length ||
        t.totalChildren ||
        ('function' == typeof t.callback && t.callback(),
        t.parent && t.parent.decrementTotal()));
  }
  function X() {
    for (var t, e, n; cu.ractives.length; )
      ((e = cu.ractives.pop()),
        (n = e.viewmodel.applyChanges()),
        n && pu.fire(e, n));
    for (tt(), t = 0; t < cu.views.length; t += 1) cu.views[t].update();
    for (cu.views.length = 0, t = 0; t < cu.tasks.length; t += 1) cu.tasks[t]();
    return ((cu.tasks.length = 0), cu.ractives.length ? X() : void 0);
  }
  function tt() {
    var t, e, n, i;
    for (t = du.length; t--; )
      ((e = du[t]),
        e.keypath
          ? du.splice(t, 1)
          : (n = uu(e.root, e.ref, e.parentFragment)) &&
            ((i || (i = [])).push({ item: e, keypath: n }), du.splice(t, 1)));
    i && i.forEach(et);
  }
  function et(t) {
    t.item.resolve(t.keypath);
  }
  function nt(t, e, n) {
    var i, r, s, o, a, u, h, c, l, f, d, p, m, v;
    if (
      ((i = new ou(function (t) {
        return (r = t);
      })),
      'object' == typeof t)
    ) {
      ((n = e || {}),
        (u = n.easing),
        (h = n.duration),
        (a = []),
        (c = n.step),
        (l = n.complete),
        (c || l) &&
          ((d = {}),
          (n.step = null),
          (n.complete = null),
          (f = function (t) {
            return function (e, n) {
              d[t] = n;
            };
          })));
      for (s in t)
        t.hasOwnProperty(s) &&
          ((c || l) &&
            ((p = f(s)), (n = { easing: u, duration: h }), c && (n.step = p)),
          (n.complete = l ? p : Fa),
          a.push(it(this, s, t[s], n)));
      return (
        (v = { easing: u, duration: h }),
        c &&
          (v.step = function (t) {
            return c(t, d);
          }),
        l &&
          i.then(function (t) {
            return l(t, d);
          }),
        (v.complete = r),
        (m = it(this, null, null, v)),
        a.push(m),
        (i.stop = function () {
          for (var t; (t = a.pop()); ) t.stop();
          m && m.stop();
        }),
        i
      );
    }
    return (
      (n = n || {}),
      n.complete && i.then(n.complete),
      (n.complete = r),
      (o = it(this, t, e, n)),
      (i.stop = function () {
        return o.stop();
      }),
      i
    );
  }
  function it(t, e, n, i) {
    var r, s, o, u;
    return (
      e && (e = _(C(e))),
      null !== e && (u = t.viewmodel.get(e)),
      yu.abort(e, t),
      a(u, n)
        ? (i.complete && i.complete(i.to), ku)
        : (i.easing &&
            ((r =
              'function' == typeof i.easing ? i.easing : t.easing[i.easing]),
            'function' != typeof r && (r = null)),
          (s = void 0 === i.duration ? 400 : i.duration),
          (o = new wu({
            keypath: e,
            from: u,
            to: n,
            root: t,
            duration: s,
            easing: r,
            interpolator: i.interpolator,
            step: i.step,
            complete: i.complete,
          })),
          yu.add(o),
          t._animations.push(o),
          o)
    );
  }
  function rt() {
    return this.detached
      ? this.detached
      : (this.el && I(this.el.__ractive_instances__, this),
        (this.detached = this.fragment.detach()),
        _u.fire(this),
        this.detached);
  }
  function st(t) {
    return this.el ? this.fragment.find(t) : null;
  }
  function ot(t, e) {
    var n;
    return (
      (n = this._isComponentQuery
        ? !this.selector || t.name === this.selector
        : t.node
          ? fa(t.node, this.selector)
          : null),
      n ? (this.push(t.node || t.instance), e || this._makeDirty(), !0) : void 0
    );
  }
  function at(t) {
    var e;
    return (e = t.parentFragment)
      ? e.owner
      : t.component && (e = t.component.parentFragment)
        ? e.owner
        : void 0;
  }
  function ut(t) {
    var e, n;
    for (e = [t], n = at(t); n; ) (e.push(n), (n = at(n)));
    return e;
  }
  function ht(t, e, n, i) {
    var r = [];
    return (
      ka(r, {
        selector: { value: e },
        live: { value: n },
        _isComponentQuery: { value: i },
        _test: { value: Su },
      }),
      n
        ? (ka(r, {
            cancel: { value: Cu },
            _root: { value: t },
            _sort: { value: Tu },
            _makeDirty: { value: Fu },
            _remove: { value: Ru },
            _dirty: { value: !1, writable: !0 },
          }),
          r)
        : r
    );
  }
  function ct(t, e) {
    var n, i;
    return this.el
      ? ((e = e || {}),
        (n = this._liveQueries),
        (i = n[t])
          ? e && e.live
            ? i
            : i.slice()
          : ((i = ju(this, t, !!e.live, !1)),
            i.live && (n.push(t), (n['_' + t] = i)),
            this.fragment.findAll(t, i),
            i))
      : [];
  }
  function lt(t, e) {
    var n, i;
    return (
      (e = e || {}),
      (n = this._liveComponentQueries),
      (i = n[t])
        ? e && e.live
          ? i
          : i.slice()
        : ((i = ju(this, t, !!e.live, !0)),
          i.live && (n.push(t), (n['_' + t] = i)),
          this.fragment.findAllComponents(t, i),
          i)
    );
  }
  function ft(t) {
    return this.fragment.findComponent(t);
  }
  function dt(t) {
    return this.container
      ? this.container.component && this.container.component.name === t
        ? this.container
        : this.container.findContainer(t)
      : null;
  }
  function pt(t) {
    return this.parent
      ? this.parent.component && this.parent.component.name === t
        ? this.parent
        : this.parent.findParent(t)
      : null;
  }
  function mt(t, e) {
    var n = void 0 === arguments[2] ? {} : arguments[2];
    if (e) {
      n.event ? (n.event.name = e) : (n.event = { name: e, _noArg: !0 });
      var i = _(e).wildcardMatches();
      vt(t, i, n.event, n.args, !0);
    }
  }
  function vt(t, e, n, i) {
    var r,
      s,
      o = void 0 === arguments[4] ? !1 : arguments[4],
      a = !0;
    for (Uu.enqueue(t, n), s = e.length; s >= 0; s--)
      ((r = t._subs[e[s]]), r && (a = gt(t, r, n, i) && a));
    if ((Uu.dequeue(t), t.parent && a)) {
      if (o && t.component) {
        var u = t.component.name + '.' + e[e.length - 1];
        ((e = _(u).wildcardMatches()), n && (n.component = t));
      }
      vt(t.parent, e, n, i);
    }
  }
  function gt(t, e, n, i) {
    var r = null,
      s = !1;
    (n && !n._noArg && (i = [n].concat(i)), (e = e.slice()));
    for (var o = 0, a = e.length; a > o; o += 1)
      e[o].apply(t, i) === !1 && (s = !0);
    return (
      n &&
        !n._noArg &&
        s &&
        (r = n.original) &&
        (r.preventDefault && r.preventDefault(),
        r.stopPropagation && r.stopPropagation()),
      !s
    );
  }
  function yt(t) {
    var e = { args: Array.prototype.slice.call(arguments, 1) };
    Wu(this, t, e);
  }
  function bt(t) {
    var e;
    return (
      (t = _(C(t))),
      (e = this.viewmodel.get(t, qu)),
      void 0 === e &&
        this.parent &&
        !this.isolated &&
        uu(this, t.str, this.component.parentFragment) &&
        (e = this.viewmodel.get(t)),
      e
    );
  }
  function wt(e, n) {
    if (!this.fragment.rendered)
      throw new Error(
        'The API has changed - you must call `ractive.render(target[, anchor])` to render your Ractive instance. Once rendered you can use `ractive.insert()`.'
      );
    if (((e = t(e)), (n = t(n) || null), !e))
      throw new Error('You must specify a valid target to insert into');
    (e.insertBefore(this.detach(), n),
      (this.el = e),
      (e.__ractive_instances__ || (e.__ractive_instances__ = [])).push(this),
      (this.detached = null),
      xt(this));
  }
  function xt(t) {
    (Qu.fire(t),
      t.findAllComponents('*').forEach(function (t) {
        xt(t.instance);
      }));
  }
  function kt(t, e, n) {
    var i, r;
    return (
      (t = _(C(t))),
      (i = this.viewmodel.get(t)),
      s(i) && s(e)
        ? ((r = mu.start(this, !0)),
          this.viewmodel.merge(t, i, e, n),
          mu.end(),
          r)
        : this.set(t, e, n && n.complete)
    );
  }
  function Et(t, e) {
    var n, i;
    return (
      (n = A(t, e)),
      (i = {}),
      n.forEach(function (e) {
        i[e.str] = t.get(e.str);
      }),
      i
    );
  }
  function _t(t, e, n, i) {
    var r, s, o;
    ((e = _(C(e))),
      (i = i || ah),
      e.isPattern
        ? ((r = new sh(t, e, n, i)),
          t.viewmodel.patternObservers.push(r),
          (s = !0))
        : (r = new Gu(t, e, n, i)),
      r.init(i.init),
      t.viewmodel.register(e, r, s ? 'patternObservers' : 'observers'),
      (r.ready = !0));
    var a = {
      cancel: function () {
        var n;
        o ||
          (s
            ? ((n = t.viewmodel.patternObservers.indexOf(r)),
              t.viewmodel.patternObservers.splice(n, 1),
              t.viewmodel.unregister(e, r, 'patternObservers'))
            : t.viewmodel.unregister(e, r, 'observers'),
          (o = !0));
      },
    };
    return (t._observers.push(a), a);
  }
  function At(t, e, n) {
    var i, r, s, o;
    if (h(t)) {
      ((n = e), (r = t), (i = []));
      for (t in r)
        r.hasOwnProperty(t) && ((e = r[t]), i.push(this.observe(t, e, n)));
      return {
        cancel: function () {
          for (; i.length; ) i.pop().cancel();
        },
      };
    }
    if ('function' == typeof t)
      return ((n = e), (e = t), (t = ''), oh(this, t, e, n));
    if (((s = t.split(' ')), 1 === s.length)) return oh(this, t, e, n);
    for (i = [], o = s.length; o--; )
      ((t = s[o]), t && i.push(oh(this, t, e, n)));
    return {
      cancel: function () {
        for (; i.length; ) i.pop().cancel();
      },
    };
  }
  function St(t, e, n) {
    var i = this.observe(
      t,
      function () {
        (e.apply(this, arguments), i.cancel());
      },
      { init: !1, defer: n && n.defer }
    );
    return i;
  }
  function Ct(t, e) {
    var n,
      i = this;
    if (t)
      ((n = t.split(' ').map(ch).filter(lh)),
        n.forEach(function (t) {
          var n, r;
          (n = i._subs[t]) &&
            (e
              ? ((r = n.indexOf(e)), -1 !== r && n.splice(r, 1))
              : (i._subs[t] = []));
        }));
    else for (t in this._subs) delete this._subs[t];
    return this;
  }
  function Ot(t, e) {
    var n,
      i,
      r,
      s = this;
    if ('object' == typeof t) {
      n = [];
      for (i in t) t.hasOwnProperty(i) && n.push(this.on(i, t[i]));
      return {
        cancel: function () {
          for (var t; (t = n.pop()); ) t.cancel();
        },
      };
    }
    return (
      (r = t.split(' ').map(ch).filter(lh)),
      r.forEach(function (t) {
        (s._subs[t] || (s._subs[t] = [])).push(e);
      }),
      {
        cancel: function () {
          return s.off(t, e);
        },
      }
    );
  }
  function Pt(t, e) {
    var n = this.on(t, function () {
      (e.apply(this, arguments), n.cancel());
    });
    return n;
  }
  function Tt(t, e, n) {
    var i,
      r,
      s,
      o,
      a,
      u,
      h = [];
    if (((i = Ft(t, e, n)), !i)) return null;
    for (
      r = t.length,
        a = i.length - 2 - i[1],
        s = Math.min(r, i[0]),
        o = s + i[1],
        u = 0;
      s > u;
      u += 1
    )
      h.push(u);
    for (; o > u; u += 1) h.push(-1);
    for (; r > u; u += 1) h.push(u + a);
    return ((h.touchedFrom = 0 !== a ? i[0] : t.length), h);
  }
  function Ft(t, e, n) {
    switch (e) {
      case 'splice':
        for (
          void 0 !== n[0] &&
          n[0] < 0 &&
          (n[0] = t.length + Math.max(n[0], -t.length));
          n.length < 2;

        )
          n.push(0);
        return ((n[1] = Math.min(n[1], t.length - n[0])), n);
      case 'sort':
      case 'reverse':
        return null;
      case 'pop':
        return t.length ? [t.length - 1, 1] : [0, 0];
      case 'push':
        return [t.length, 0].concat(n);
      case 'shift':
        return [0, t.length ? 1 : 0];
      case 'unshift':
        return [0, 0].concat(n);
    }
  }
  function Rt(e, n) {
    var i,
      r,
      s,
      o = this;
    if (
      ((s = this.transitionsEnabled),
      this.noIntro && (this.transitionsEnabled = !1),
      (i = mu.start(this, !0)),
      mu.scheduleTask(function () {
        return Ch.fire(o);
      }, !0),
      this.fragment.rendered)
    )
      throw new Error(
        'You cannot call ractive.render() on an already rendered instance! Call ractive.unrender() first'
      );
    if (
      ((e = t(e) || this.el),
      (n = t(n) || this.anchor),
      (this.el = e),
      (this.anchor = n),
      !this.append && e)
    ) {
      var a = e.__ractive_instances__;
      (a && a.length && jt(a), (e.innerHTML = ''));
    }
    return (
      this.cssId && Ah.apply(),
      e &&
        ((r = e.__ractive_instances__)
          ? r.push(this)
          : (e.__ractive_instances__ = [this]),
        n
          ? e.insertBefore(this.fragment.render(), n)
          : e.appendChild(this.fragment.render())),
      mu.end(),
      (this.transitionsEnabled = s),
      i.then(function () {
        return Oh.fire(o);
      })
    );
  }
  function jt(t) {
    t.splice(0, t.length).forEach(Q);
  }
  function Nt(t, e) {
    for (var n = t.slice(), i = e.length; i--; )
      ~n.indexOf(e[i]) || n.push(e[i]);
    return n;
  }
  function Dt(t, e) {
    var n, i, r;
    return (
      (i = '[data-ractive-css~="{' + e + '}"]'),
      (r = function (t) {
        var e,
          n,
          r,
          s,
          o,
          a,
          u,
          h = [];
        for (e = []; (n = Nh.exec(t)); )
          e.push({ str: n[0], base: n[1], modifiers: n[2] });
        for (s = e.map(Lt), u = e.length; u--; )
          ((a = s.slice()),
            (r = e[u]),
            (a[u] = r.base + i + r.modifiers || ''),
            (o = s.slice()),
            (o[u] = i + ' ' + o[u]),
            h.push(a.join(' '), o.join(' ')));
        return h.join(', ');
      }),
      (n = Ih.test(t)
        ? t.replace(Ih, i)
        : t.replace(jh, '').replace(Rh, function (t, e) {
            var n, i;
            return Dh.test(e)
              ? t
              : ((n = e.split(',').map(It)),
                (i = n.map(r).join(', ') + ' '),
                t.replace(e, i));
          }))
    );
  }
  function It(t) {
    return t.trim ? t.trim() : t.replace(/^\s+/, '').replace(/\s+$/, '');
  }
  function Lt(t) {
    return t.str;
  }
  function Vt(t) {
    t &&
      t.constructor !== Object &&
      ('function' == typeof t ||
        ('object' != typeof t
          ? l(
              'data option must be an object or a function, `' +
                t +
                '` is not valid'
            )
          : m(
              'If supplied, options.data should be a plain JavaScript object - using a non-POJO as the root object may work, but is discouraged'
            )));
  }
  function Mt(t, e) {
    Vt(e);
    var n = 'function' == typeof t,
      i = 'function' == typeof e;
    return (
      e || n || (e = {}),
      n || i
        ? function () {
            var r = i ? Ut(e, this) : e,
              s = n ? Ut(t, this) : t;
            return Wt(r, s);
          }
        : Wt(e, t)
    );
  }
  function Ut(t, e) {
    var n = t.call(e);
    if (n)
      return (
        'object' != typeof n && l('Data function must return an object'),
        n.constructor !== Object &&
          v(
            'Data function returned something other than a plain JavaScript object. This might work, but is strongly discouraged'
          ),
        n
      );
  }
  function Wt(t, e) {
    if (t && e) {
      for (var n in e) n in t || (t[n] = e[n]);
      return t;
    }
    return t || e;
  }
  function zt(t) {
    var e, n, i;
    return t.matchString('=')
      ? ((e = t.pos),
        t.allowWhitespace(),
        (n = t.matchPattern(jc))
          ? t.matchPattern(Nc)
            ? (i = t.matchPattern(jc))
              ? (t.allowWhitespace(),
                t.matchString('=') ? [n, i] : ((t.pos = e), null))
              : ((t.pos = e), null)
            : null
          : ((t.pos = e), null))
      : null;
  }
  function Bt(t) {
    var e;
    return (e = t.matchPattern(Ic)) ? { t: pc, v: e } : null;
  }
  function qt(t) {
    var e, n;
    if (t.interpolate[t.inside] === !1) return null;
    for (n = 0; n < t.tags.length; n += 1) if ((e = $t(t, t.tags[n]))) return e;
  }
  function $t(t, e) {
    var n, i, r, s;
    if (((n = t.pos), t.matchString('\\' + e.open))) {
      if (0 === n || '\\' !== t.str[n - 1]) return e.open;
    } else if (!t.matchString(e.open)) return null;
    if ((i = Rc(t)))
      return t.matchString(e.close)
        ? ((e.open = i[0]), (e.close = i[1]), t.sortMustacheTags(), Vc)
        : null;
    if ((t.allowWhitespace(), t.matchString('/'))) {
      t.pos -= 1;
      var o = t.pos;
      Dc(t)
        ? (t.pos = o)
        : ((t.pos = o - e.close.length),
          t.error("Attempted to close a section that wasn't open"));
    }
    for (s = 0; s < e.readers.length; s += 1)
      if (((r = e.readers[s]), (i = r(t, e))))
        return (
          e.isStatic && (i.s = !0),
          t.includeLinePositions && (i.p = t.getLinePos(n)),
          i
        );
    return ((t.pos = n), null);
  }
  function Qt(t) {
    var e;
    return (e = t.matchPattern(zc)) ? { t: hc, v: e } : null;
  }
  function Zt(t) {
    var e = t.remaining();
    return 'true' === e.substr(0, 4)
      ? ((t.pos += 4), { t: dc, v: 'true' })
      : 'false' === e.substr(0, 5)
        ? ((t.pos += 5), { t: dc, v: 'false' })
        : null;
  }
  function Ht(t) {
    var e;
    return (e = Kc(t))
      ? Jc.test(e.v)
        ? e.v
        : '"' + e.v.replace(/"/g, '\\"') + '"'
      : (e = Wc(t))
        ? e.v
        : (e = t.matchPattern(Gc))
          ? e
          : void 0;
  }
  function Kt(t) {
    var e, n, i;
    return (
      (e = t.pos),
      t.allowWhitespace(),
      (n = Yc(t)),
      null === n
        ? ((t.pos = e), null)
        : (t.allowWhitespace(),
          t.matchString(':')
            ? (t.allowWhitespace(),
              (i = Ol(t)),
              null === i ? ((t.pos = e), null) : { t: vc, k: n, v: i })
            : ((t.pos = e), null))
    );
  }
  function Gt(t) {
    var e, n, i, r;
    return (
      (e = t.pos),
      (i = Xc(t)),
      null === i
        ? null
        : ((n = [i]),
          t.matchString(',')
            ? ((r = Gt(t)), r ? n.concat(r) : ((t.pos = e), null))
            : n)
    );
  }
  function Yt(t) {
    function e(t) {
      i.push(t);
    }
    var n, i, r, s;
    return (
      (n = t.pos),
      t.allowWhitespace(),
      (r = Ol(t)),
      null === r
        ? null
        : ((i = [r]),
          t.allowWhitespace(),
          t.matchString(',') &&
            ((s = Yt(t)), null === s && t.error(Mc), s.forEach(e)),
          i)
    );
  }
  function Jt(t) {
    return Wc(t) || Bc(t) || Kc(t) || el(t) || il(t) || Dc(t);
  }
  function Xt(t) {
    var e, n, i, r, s, o;
    return (
      (e = t.pos),
      (i = t.matchPattern(/^@(?:keypath|index|key)/)),
      i ||
        ((n = t.matchPattern(ol) || ''),
        (i =
          (!n && t.relaxedNames && t.matchPattern(cl)) || t.matchPattern(hl)),
        i || '.' !== n || ((n = ''), (i = '.'))),
      i
        ? n || t.relaxedNames || !$c.test(i)
          ? !n && qc.test(i)
            ? ((r = qc.exec(i)[0]), (t.pos = e + r.length), { t: mc, v: r })
            : ((s = (n || '') + C(i)),
              t.matchString('(') &&
                ((o = s.lastIndexOf('.')),
                -1 !== o
                  ? ((s = s.substr(0, o)), (t.pos = e + s.length))
                  : (t.pos -= 1)),
              { t: gc, n: s.replace(/^this\./, './').replace(/^this$/, '.') })
          : ((t.pos = e), null)
        : null
    );
  }
  function te(t) {
    var e, n;
    return (
      (e = t.pos),
      t.matchString('(')
        ? (t.allowWhitespace(),
          (n = Ol(t)),
          n || t.error(Mc),
          t.allowWhitespace(),
          t.matchString(')') || t.error(Uc),
          { t: xc, x: n })
        : null
    );
  }
  function ee(t) {
    var e, n, i;
    if (((e = t.pos), t.allowWhitespace(), t.matchString('.'))) {
      if ((t.allowWhitespace(), (n = t.matchPattern(Gc))))
        return { t: yc, n: n };
      t.error('Expected a property name');
    }
    return t.matchString('[')
      ? (t.allowWhitespace(),
        (i = Ol(t)),
        i || t.error(Mc),
        t.allowWhitespace(),
        t.matchString(']') || t.error("Expected ']'"),
        { t: yc, x: i })
      : null;
  }
  function ne(t) {
    var e, n, i, r;
    return (n = Sl(t))
      ? ((e = t.pos),
        t.allowWhitespace(),
        t.matchString('?')
          ? (t.allowWhitespace(),
            (i = Ol(t)),
            i || t.error(Mc),
            t.allowWhitespace(),
            t.matchString(':') || t.error('Expected ":"'),
            t.allowWhitespace(),
            (r = Ol(t)),
            r || t.error(Mc),
            { t: kc, o: [n, i, r] })
          : ((t.pos = e), n))
      : null;
  }
  function ie(t) {
    return Cl(t);
  }
  function re(t) {
    function e(t) {
      switch (t.t) {
        case dc:
        case mc:
        case hc:
        case pc:
          return t.v;
        case cc:
          return JSON.stringify(String(t.v));
        case lc:
          return '[' + (t.m ? t.m.map(e).join(',') : '') + ']';
        case fc:
          return '{' + (t.m ? t.m.map(e).join(',') : '') + '}';
        case vc:
          return t.k + ':' + e(t.v);
        case wc:
          return ('typeof' === t.s ? 'typeof ' : t.s) + e(t.o);
        case Ec:
          return (
            e(t.o[0]) +
            ('in' === t.s.substr(0, 2) ? ' ' + t.s + ' ' : t.s) +
            e(t.o[1])
          );
        case _c:
          return e(t.x) + '(' + (t.o ? t.o.map(e).join(',') : '') + ')';
        case xc:
          return '(' + e(t.x) + ')';
        case bc:
          return e(t.x) + e(t.r);
        case yc:
          return t.n ? '.' + t.n : '[' + e(t.x) + ']';
        case kc:
          return e(t.o[0]) + '?' + e(t.o[1]) + ':' + e(t.o[2]);
        case gc:
          return '_' + n.indexOf(t.n);
        default:
          throw new Error('Expected legal JavaScript');
      }
    }
    var n;
    return (se(t, (n = [])), { r: n, s: e(t) });
  }
  function se(t, e) {
    var n, i;
    if (
      (t.t === gc && -1 === e.indexOf(t.n) && e.unshift(t.n), (i = t.o || t.m))
    )
      if (h(i)) se(i, e);
      else for (n = i.length; n--; ) se(i[n], e);
    (t.x && se(t.x, e), t.r && se(t.r, e), t.v && se(t.v, e));
  }
  function oe(t, e) {
    var n;
    if (t) {
      for (; t.t === xc && t.x; ) t = t.x;
      return (
        t.t === gc
          ? (e.r = t.n)
          : t.t === hc && Fl.test(t.v)
            ? (e.r = t.v)
            : (n = ae(t))
              ? (e.rx = n)
              : (e.x = Pl(t)),
        e
      );
    }
  }
  function ae(t) {
    for (var e, n = []; t.t === bc && t.r.t === yc; )
      ((e = t.r),
        n.unshift(e.x ? (e.x.t === gc ? e.x : Pl(e.x)) : e.n),
        (t = t.x));
    return t.t !== gc ? null : { r: t.n, m: n };
  }
  function ue(t, e) {
    var n,
      i = Ol(t);
    return i
      ? (t.matchString(e.close) ||
          t.error("Expected closing delimiter '" + e.close + "'"),
        (n = { t: Kh }),
        Tl(i, n),
        n)
      : null;
  }
  function he(t, e) {
    var n, i;
    return t.matchString('&')
      ? (t.allowWhitespace(),
        (n = Ol(t))
          ? (t.matchString(e.close) ||
              t.error("Expected closing delimiter '" + e.close + "'"),
            (i = { t: Kh }),
            Tl(n, i),
            i)
          : null)
      : null;
  }
  function ce(t, e) {
    var n, i, r, s, o;
    return (
      (n = t.pos),
      t.matchString('>')
        ? (t.allowWhitespace(),
          (i = t.pos),
          (t.relaxedNames = !0),
          (r = Ol(t)),
          (t.relaxedNames = !1),
          t.allowWhitespace(),
          (s = Ol(t)),
          t.allowWhitespace(),
          r
            ? ((o = { t: tc }),
              Tl(r, o),
              t.allowWhitespace(),
              s && ((o = { t: Gh, n: Oc, f: [o] }), Tl(s, o)),
              t.matchString(e.close) ||
                t.error("Expected closing delimiter '" + e.close + "'"),
              o)
            : null)
        : null
    );
  }
  function le(t, e) {
    var n;
    return t.matchString('!')
      ? ((n = t.remaining().indexOf(e.close)),
        -1 !== n ? ((t.pos += n + e.close.length), { t: ec }) : void 0)
      : null;
  }
  function fe(t, e) {
    var n, i, r;
    if (((n = t.pos), (i = Ol(t)), !i)) return null;
    for (r = 0; r < e.length; r += 1)
      if (t.remaining().substr(0, e[r].length) === e[r]) return i;
    return ((t.pos = n), sl(t));
  }
  function de(t, e) {
    var n, i, r, s;
    n = t.pos;
    try {
      i = Il(t, [e.close]);
    } catch (o) {
      s = o;
    }
    if (!i) {
      if ('!' === t.str.charAt(n)) return ((t.pos = n), null);
      if (s) throw s;
    }
    if (
      !t.matchString(e.close) &&
      (t.error("Expected closing delimiter '" + e.close + "' after reference"),
      !i)
    ) {
      if ('!' === t.nextChar()) return null;
      t.error('Expected expression or legal reference');
    }
    return ((r = { t: Hh }), Tl(i, r), r);
  }
  function pe(t, e) {
    var n, i, r;
    return t.matchPattern(Ml)
      ? ((n = t.pos),
        (i = t.matchPattern(/^[a-zA-Z_$][a-zA-Z_$0-9\-]*/)),
        t.allowWhitespace(),
        t.matchString(e.close) || t.error('expected legal partial name'),
        (r = { t: oc }),
        i && (r.n = i),
        r)
      : null;
  }
  function me(t, e) {
    var n, i, r, s;
    return (
      (n = t.pos),
      t.matchString(e.open)
        ? (t.allowWhitespace(),
          t.matchString('/')
            ? (t.allowWhitespace(),
              (i = t.remaining()),
              (r = i.indexOf(e.close)),
              -1 !== r
                ? ((s = { t: Jh, r: i.substr(0, r).split(' ')[0] }),
                  (t.pos += r),
                  t.matchString(e.close) ||
                    t.error("Expected closing delimiter '" + e.close + "'"),
                  s)
                : ((t.pos = n), null))
            : ((t.pos = n), null))
        : null
    );
  }
  function ve(t, e) {
    var n = t.pos;
    return t.matchString(e.open)
      ? t.matchPattern(zl)
        ? (t.matchString(e.close) ||
            t.error("Expected closing delimiter '" + e.close + "'"),
          { t: Tc })
        : ((t.pos = n), null)
      : null;
  }
  function ge(t, e) {
    var n,
      i = t.pos;
    return t.matchString(e.open)
      ? t.matchPattern(ql)
        ? ((n = Ol(t)),
          t.matchString(e.close) ||
            t.error("Expected closing delimiter '" + e.close + "'"),
          { t: Fc, x: n })
        : ((t.pos = i), null)
      : null;
  }
  function ye(t, e) {
    var n, i, r, s, o, a, u, h, c, l, f, d;
    if (((n = t.pos), t.matchString('^'))) r = { t: Gh, f: [], n: Sc };
    else {
      if (!t.matchString('#')) return null;
      ((r = { t: Gh, f: [] }),
        t.matchString('partial') &&
          ((t.pos = n - t.standardDelimiters[0].length),
          t.error(
            'Partial definitions can only be at the top level of the template, or immediately inside components'
          )),
        (u = t.matchPattern(Kl)) && ((d = u), (r.n = $l[u])));
    }
    if (
      (t.allowWhitespace(),
      (i = Ol(t)),
      i || t.error('Expected expression'),
      (f = t.matchPattern(Zl)))
    ) {
      var p = void 0;
      r.i = (p = t.matchPattern(Hl)) ? f + ',' + p : f;
    }
    (t.allowWhitespace(),
      t.matchString(e.close) ||
        t.error("Expected closing delimiter '" + e.close + "'"),
      (t.sectionDepth += 1),
      (o = r.f),
      (c = []));
    do
      if ((s = Ul(t, e)))
        (d && s.r !== d && t.error('Expected ' + e.open + '/' + d + e.close),
          (t.sectionDepth -= 1),
          (l = !0));
      else if ((s = Bl(t, e)))
        (r.n === Sc && t.error('{{else}} not allowed in {{#unless}}'),
          a && t.error('illegal {{elseif...}} after {{else}}'),
          h || (h = be(i, r.n)),
          h.f.push({ t: Gh, n: Ac, x: Pl(xe(c.concat(s.x))), f: (o = []) }),
          c.push(we(s.x)));
      else if ((s = Wl(t, e)))
        (r.n === Sc && t.error('{{else}} not allowed in {{#unless}}'),
          a &&
            t.error(
              'there can only be one {{else}} block, at the end of a section'
            ),
          (a = !0),
          h
            ? h.f.push({ t: Gh, n: Ac, x: Pl(xe(c)), f: (o = []) })
            : ((h = be(i, r.n)), (o = h.f)));
      else {
        if (((s = t.read(td)), !s)) break;
        o.push(s);
      }
    while (!l);
    return (
      h && (r.n === Oc && (r.n = Pc), (r.l = h)),
      Tl(i, r),
      r.f.length || delete r.f,
      r
    );
  }
  function be(t, e) {
    var n;
    return (
      e === Oc
        ? ((n = { t: Gh, n: Ac, f: [] }), Tl(we(t), n))
        : ((n = { t: Gh, n: Sc, f: [] }), Tl(t, n)),
      n
    );
  }
  function we(t) {
    return t.t === wc && '!' === t.s ? t.o : { t: wc, s: '!', o: ke(t) };
  }
  function xe(t) {
    return 1 === t.length
      ? t[0]
      : { t: Ec, s: '&&', o: [ke(t[0]), ke(xe(t.slice(1)))] };
  }
  function ke(t) {
    return { t: xc, x: t };
  }
  function Ee(t) {
    var e, n, i, r, s;
    return (
      (e = t.pos),
      t.matchString(Yl)
        ? ((i = t.remaining()),
          (r = i.indexOf(Jl)),
          -1 === r &&
            t.error("Illegal HTML - expected closing comment sequence ('-->')"),
          (n = i.substr(0, r)),
          (t.pos += r + 3),
          (s = { t: ec, c: n }),
          t.includeLinePositions && (s.p = t.getLinePos(e)),
          s)
        : null
    );
  }
  function _e(t) {
    return t.replace(kl, function (t, e) {
      var n;
      return (
        (n =
          '#' !== e[0]
            ? wl[e]
            : 'x' === e[1]
              ? parseInt(e.substring(2), 16)
              : parseInt(e.substring(1), 10)),
        n ? String.fromCharCode(Ae(n)) : t
      );
    });
  }
  function Ae(t) {
    return t
      ? 10 === t
        ? 32
        : 128 > t
          ? t
          : 159 >= t
            ? xl[t - 128]
            : 55296 > t
              ? t
              : 57343 >= t
                ? 65533
                : 65535 >= t
                  ? t
                  : 65533
      : 65533;
  }
  function Se(t) {
    return t.replace(Al, '&amp;').replace(El, '&lt;').replace(_l, '&gt;');
  }
  function Ce(t) {
    return 'string' == typeof t;
  }
  function Oe(t) {
    return t.t === ec || t.t === nc;
  }
  function Pe(t) {
    return (t.t === Gh || t.t === Yh) && t.f;
  }
  function Te(t, e, n, i, r) {
    var o, a, u, h, c, l, f, d;
    for (hf(t), o = t.length; o--; )
      ((a = t[o]),
        a.exclude ? t.splice(o, 1) : e && a.t === ec && t.splice(o, 1));
    for (cf(t, i ? pf : null, r ? mf : null), o = t.length; o--; ) {
      if (((a = t[o]), a.f)) {
        var p = a.t === Xh && df.test(a.e);
        ((c = n || p),
          !n && p && cf(a.f, vf, gf),
          c ||
            ((u = t[o - 1]),
            (h = t[o + 1]),
            (!u || ('string' == typeof u && mf.test(u))) && (l = !0),
            (!h || ('string' == typeof h && pf.test(h))) && (f = !0)),
          Te(a.f, e, c, l, f));
      }
      if (
        (a.l && (Te(a.l.f, e, n, l, f), t.splice(o + 1, 0, a.l), delete a.l),
        a.a)
      )
        for (d in a.a)
          a.a.hasOwnProperty(d) &&
            'string' != typeof a.a[d] &&
            Te(a.a[d], e, n, l, f);
      if ((a.m && Te(a.m, e, n, l, f), a.v))
        for (d in a.v)
          a.v.hasOwnProperty(d) &&
            (s(a.v[d].n) && Te(a.v[d].n, e, n, l, f),
            s(a.v[d].d) && Te(a.v[d].d, e, n, l, f));
    }
    for (o = t.length; o--; )
      'string' == typeof t[o] &&
        ('string' == typeof t[o + 1] &&
          ((t[o] = t[o] + t[o + 1]), t.splice(o + 1, 1)),
        n || (t[o] = t[o].replace(ff, ' ')),
        '' === t[o] && t.splice(o, 1));
  }
  function Fe(t) {
    var e, n;
    return (
      (e = t.pos),
      t.matchString('</')
        ? (n = t.matchPattern(bf))
          ? t.inside && n !== t.inside
            ? ((t.pos = e), null)
            : { t: rc, e: n }
          : ((t.pos -= 2), void t.error('Illegal closing tag'))
        : null
    );
  }
  function Re(t) {
    var e, n, i;
    return (
      t.allowWhitespace(),
      (n = t.matchPattern(kf))
        ? ((e = { name: n }), (i = je(t)), null != i && (e.value = i), e)
        : null
    );
  }
  function je(t) {
    var e, n, i, r;
    return (
      (e = t.pos),
      /[=\/>\s]/.test(t.nextChar()) ||
        t.error('Expected `=`, `/`, `>` or whitespace'),
      t.allowWhitespace(),
      t.matchString('=')
        ? (t.allowWhitespace(),
          (n = t.pos),
          (i = t.sectionDepth),
          (r = Ie(t, "'") || Ie(t, '"') || De(t)),
          null === r && t.error('Expected valid attribute value'),
          t.sectionDepth !== i &&
            ((t.pos = n),
            t.error(
              'An attribute value must contain as many opening section tags as closing section tags'
            )),
          r.length
            ? 1 === r.length && 'string' == typeof r[0]
              ? _e(r[0])
              : r
            : '')
        : ((t.pos = e), null)
    );
  }
  function Ne(t) {
    var e, n, i, r, s;
    return (
      (e = t.pos),
      (n = t.matchPattern(Ef))
        ? ((i = n),
          (r = t.tags.map(function (t) {
            return t.open;
          })),
          -1 !== (s = wf(i, r)) &&
            ((n = n.substr(0, s)), (t.pos = e + n.length)),
          n)
        : null
    );
  }
  function De(t) {
    var e, n;
    for (t.inAttribute = !0, e = [], n = Lc(t) || Ne(t); null !== n; )
      (e.push(n), (n = Lc(t) || Ne(t)));
    return e.length ? ((t.inAttribute = !1), e) : null;
  }
  function Ie(t, e) {
    var n, i, r;
    if (((n = t.pos), !t.matchString(e))) return null;
    for (t.inAttribute = e, i = [], r = Lc(t) || Le(t, e); null !== r; )
      (i.push(r), (r = Lc(t) || Le(t, e)));
    return t.matchString(e) ? ((t.inAttribute = !1), i) : ((t.pos = n), null);
  }
  function Le(t, e) {
    var n, i, r, s;
    return (
      (n = t.pos),
      (r = t.remaining()),
      (s = t.tags.map(function (t) {
        return t.open;
      })),
      s.push(e),
      (i = wf(r, s)),
      -1 === i && t.error('Quoted attribute value must have a closing quote'),
      i ? ((t.pos += i), r.substr(0, i)) : null
    );
  }
  function Ve(t) {
    var e, n, i;
    return (
      t.allowWhitespace(),
      (e = Yc(t))
        ? ((i = { key: e }),
          t.allowWhitespace(),
          t.matchString(':')
            ? (t.allowWhitespace(),
              (n = t.read()) ? ((i.value = n.v), i) : null)
            : null)
        : null
    );
  }
  function Me(t, e) {
    var n, i, r, s, o, a, u, h, c;
    if ('string' == typeof t) {
      if ((i = Cf.exec(t))) {
        var l = t.lastIndexOf(')');
        return (
          Of.test(t) ||
            e.error(
              "Invalid input after method call expression '" +
                t.slice(l + 1) +
                "'"
            ),
          (n = { m: i[1] }),
          (s = '[' + t.slice(n.m.length + 1, l) + ']'),
          (r = new _f(s)),
          (n.a = Pl(r.result[0])),
          n
        );
      }
      if (-1 === t.indexOf(':')) return t.trim();
      t = [t];
    }
    if (((n = {}), (u = []), (h = []), t)) {
      for (; t.length; )
        if (((o = t.shift()), 'string' == typeof o)) {
          if (((a = o.indexOf(':')), -1 !== a)) {
            (a && u.push(o.substr(0, a)),
              o.length > a + 1 && (h[0] = o.substring(a + 1)));
            break;
          }
          u.push(o);
        } else u.push(o);
      h = h.concat(t);
    }
    return (
      u.length
        ? h.length || 'string' != typeof u
          ? ((n = { n: 1 === u.length && 'string' == typeof u[0] ? u[0] : u }),
            1 === h.length && 'string' == typeof h[0]
              ? ((c = Af('[' + h[0] + ']')), (n.a = c ? c.value : h[0].trim()))
              : (n.d = h))
          : (n = u)
        : (n = ''),
      n
    );
  }
  function Ue(t) {
    var e, n, i, r, s, o, a, u, h, c, l, f, d, p, m, v;
    if (((e = t.pos), t.inside || t.inAttribute)) return null;
    if (!t.matchString('<')) return null;
    if ('/' === t.nextChar()) return null;
    if (
      ((n = {}),
      t.includeLinePositions && (n.p = t.getLinePos(e)),
      t.matchString('!'))
    )
      return (
        (n.t = uc),
        t.matchPattern(/^doctype/i) || t.error('Expected DOCTYPE declaration'),
        (n.a = t.matchPattern(/^(.+?)>/)),
        n
      );
    if (((n.t = Xh), (n.e = t.matchPattern(Tf)), !n.e)) return null;
    for (
      Ff.test(t.nextChar()) || t.error('Illegal tag name'),
        s = function (e, i) {
          var r = i.n || i;
          (Nf.test(r) &&
            ((t.pos -= r.length),
            t.error(
              'Cannot use reserved event names (change, reset, teardown, update, construct, config, init, render, unrender, detach, insert)'
            )),
            (n.v[e] = i));
        },
        t.allowWhitespace();
      (o = Lc(t) || xf(t));

    )
      (o.name
        ? (i = Df[o.name])
          ? (n[i] = Sf(o.value, t))
          : (r = jf.exec(o.name))
            ? (n.v || (n.v = {}), (a = Sf(o.value, t)), s(r[1], a))
            : (t.sanitizeEventAttributes && Rf.test(o.name)) ||
              (n.a || (n.a = {}),
              (n.a[o.name] = o.value || ('' === o.value ? '' : 0)))
        : (n.m || (n.m = []), n.m.push(o)),
        t.allowWhitespace());
    if (
      (t.allowWhitespace(), t.matchString('/') && (u = !0), !t.matchString('>'))
    )
      return null;
    var g = n.e.toLowerCase(),
      y = t.preserveWhitespace;
    if (!u && !bl.test(n.e)) {
      (t.elementStack.push(g),
        ('script' === g || 'style' === g) && (t.inside = g),
        (h = []),
        (c = wa(null)));
      do
        if (((p = t.pos), (m = t.remaining()), We(g, m)))
          if ((v = yf(t))) {
            d = !0;
            var b = v.e.toLowerCase();
            if (b !== g && ((t.pos = p), !~t.elementStack.indexOf(b))) {
              var w = 'Unexpected closing tag';
              (bl.test(b) &&
                (w +=
                  ' (<' +
                  b +
                  '> is a void element - it cannot contain children)'),
                t.error(w));
            }
          } else
            (f = Ul(t, {
              open: t.standardDelimiters[0],
              close: t.standardDelimiters[1],
            }))
              ? ((d = !0), (t.pos = p))
              : (f = t.read(ed))
                ? (c[f.n] &&
                    ((t.pos = p), t.error('Duplicate partial definition')),
                  lf(f.f, t.stripComments, y, !y, !y),
                  (c[f.n] = f.f),
                  (l = !0))
                : (f = t.read(td))
                  ? h.push(f)
                  : (d = !0);
        else d = !0;
      while (!d);
      (h.length && (n.f = h), l && (n.p = c), t.elementStack.pop());
    }
    return (
      (t.inside = null),
      t.sanitizeElements && -1 !== t.sanitizeElements.indexOf(g) ? If : n
    );
  }
  function We(t, e) {
    var n, i;
    return (
      (n = /^<([a-zA-Z][a-zA-Z0-9]*)/.exec(e)),
      (i = Pf[t]),
      n && i ? !~i.indexOf(n[1].toLowerCase()) : !0
    );
  }
  function ze(t) {
    var e, n, i, r;
    return (
      (n = t.remaining()),
      (r = t.inside ? '</' + t.inside : '<'),
      t.inside && !t.interpolate[t.inside]
        ? (e = n.indexOf(r))
        : ((i = t.tags.map(function (t) {
            return t.open;
          })),
          (i = i.concat(
            t.tags.map(function (t) {
              return '\\' + t.open;
            })
          )),
          t.inAttribute === !0
            ? i.push('"', "'", '=', '<', '>', '`')
            : i.push(t.inAttribute ? t.inAttribute : r),
          (e = wf(n, i))),
      e
        ? (-1 === e && (e = n.length),
          (t.pos += e),
          t.inside ? n.substr(0, e) : _e(n.substr(0, e)))
        : null
    );
  }
  function Be(t) {
    return t.replace(Wf, '\\$&');
  }
  function qe(t) {
    var e = t.pos,
      n = t.standardDelimiters[0],
      i = t.standardDelimiters[1],
      r = void 0,
      s = void 0;
    if (!t.matchPattern(Bf) || !t.matchString(n)) return ((t.pos = e), null);
    var o = t.matchPattern(qf);
    if (
      (v(
        'Inline partial comments are deprecated.\nUse this...\n  {{#partial ' +
          o +
          '}} ... {{/partial}}\n\n...instead of this:\n  <!-- {{>' +
          o +
          '}} --> ... <!-- {{/' +
          o +
          "}} -->'"
      ),
      !t.matchString(i) || !t.matchPattern($f))
    )
      return ((t.pos = e), null);
    r = [];
    var a = new RegExp(
      '^<!--\\s*' + Uf(n) + '\\s*\\/\\s*' + o + '\\s*' + Uf(i) + '\\s*-->'
    );
    do
      t.matchPattern(a)
        ? (s = !0)
        : ((Lf = t.read(td)),
          Lf ||
            t.error(
              "expected closing comment ('<!-- " + n + '/' + o + i + " -->')"
            ),
          r.push(Lf));
    while (!s);
    return { t: ac, f: r, n: o };
  }
  function $e(t) {
    var e, n, i, r, s;
    e = t.pos;
    var o = t.standardDelimiters;
    if (!t.matchString(o[0])) return null;
    if (!t.matchPattern(Zf)) return ((t.pos = e), null);
    ((n = t.matchPattern(/^[a-zA-Z_$][a-zA-Z_$0-9\-]*/)),
      n || t.error('expected legal partial name'),
      t.matchString(o[1]) ||
        t.error("Expected closing delimiter '" + o[1] + "'"),
      (i = []));
    do
      (r = Ul(t, {
        open: t.standardDelimiters[0],
        close: t.standardDelimiters[1],
      }))
        ? ('partial' === !r.r &&
            t.error('Expected ' + o[0] + '/partial' + o[1]),
          (s = !0))
        : ((r = t.read(td)),
          r || t.error('Expected ' + o[0] + '/partial' + o[1]),
          i.push(r));
    while (!s);
    return { t: ac, n: n, f: i };
  }
  function Qe(t) {
    for (
      var e = [], n = wa(null), i = !1, r = t.preserveWhitespace;
      t.pos < t.str.length;

    ) {
      var s = t.pos,
        o = void 0,
        a = void 0;
      (a = t.read(ed))
        ? (n[a.n] && ((t.pos = s), t.error('Duplicated partial definition')),
          lf(a.f, t.stripComments, r, !r, !r),
          (n[a.n] = a.f),
          (i = !0))
        : (o = t.read(td))
          ? e.push(o)
          : t.error('Unexpected template content');
    }
    var u = { v: oa, t: e };
    return (i && (u.p = n), u);
  }
  function Ze(t, e) {
    return new Xf(t, e || {}).result;
  }
  function He(t) {
    var e = wa(od);
    return (
      (e.parse = function (e, n) {
        return Ke(e, n || t);
      }),
      e
    );
  }
  function Ke(t, e) {
    if (!Kf)
      throw new Error(
        'Missing Ractive.parse - cannot parse template. Either preparse or use the version that includes the parser'
      );
    return Kf(t, e || this.options);
  }
  function Ge(t, e) {
    var n;
    if (!Xo) {
      if (e && e.noThrow) return;
      throw new Error(
        'Cannot retrieve template #' +
          t +
          ' as Ractive is not running in a browser.'
      );
    }
    if ((Ye(t) && (t = t.substring(1)), !(n = document.getElementById(t)))) {
      if (e && e.noThrow) return;
      throw new Error('Could not find template element with id #' + t);
    }
    if ('SCRIPT' !== n.tagName.toUpperCase()) {
      if (e && e.noThrow) return;
      throw new Error(
        'Template element with id #' + t + ', must be a <script> element'
      );
    }
    return 'textContent' in n ? n.textContent : n.innerHTML;
  }
  function Ye(t) {
    return t && '#' === t[0];
  }
  function Je(t) {
    return !('string' == typeof t);
  }
  function Xe(t) {
    return (
      t.defaults && (t = t.defaults),
      sd.reduce(function (e, n) {
        return ((e[n] = t[n]), e);
      }, {})
    );
  }
  function tn(t) {
    var e,
      n = t._config.template;
    if (n && n.fn)
      return (
        (e = en(t, n.fn)),
        e !== n.result ? ((n.result = e), (e = rn(e, t))) : void 0
      );
  }
  function en(t, e) {
    var n = nn(ad.getParseOptions(t));
    return e.call(t, n);
  }
  function nn(t) {
    var e = wa(ad);
    return (
      (e.parse = function (e, n) {
        return ad.parse(e, n || t);
      }),
      e
    );
  }
  function rn(t, e) {
    if ('string' == typeof t)
      ('#' === t[0] && (t = ad.fromId(t)), (t = Kf(t, ad.getParseOptions(e))));
    else {
      if (void 0 == t) throw new Error('The template cannot be ' + t + '.');
      if ('number' != typeof t.v)
        throw new Error(
          "The template parser was passed a non-string template, but the template doesn't have a version.  Make sure you're passing in the template you think you are."
        );
      if (t.v !== oa)
        throw new Error(
          'Mismatched template version (expected ' +
            oa +
            ', got ' +
            t.v +
            ') Please ensure you are using the latest version of Ractive.js in your build process as well as in your app'
        );
    }
    return t;
  }
  function sn(t, e, n) {
    if (e) for (var i in e) (n || !t.hasOwnProperty(i)) && (t[i] = e[i]);
  }
  function on(t, e, n) {
    if (!/_super/.test(n)) return n;
    var i = function () {
      var t,
        r = an(i._parent, e),
        s = '_super' in this,
        o = this._super;
      return (
        (this._super = r),
        (t = n.apply(this, arguments)),
        s ? (this._super = o) : delete this._super,
        t
      );
    };
    return ((i._parent = t), (i._method = n), i);
  }
  function an(t, e) {
    var n, i;
    return (
      e in t
        ? ((n = t[e]),
          (i =
            'function' == typeof n
              ? n
              : function () {
                  return n;
                }))
        : (i = Fa),
      i
    );
  }
  function un(t, e, n) {
    return (
      'options.' +
      t +
      ' has been deprecated in favour of options.' +
      e +
      '.' +
      (n
        ? ' You cannot specify both options, please use options.' + e + '.'
        : '')
    );
  }
  function hn(t, e, n) {
    if (e in t) {
      if (n in t) throw new Error(un(e, n, !0));
      (m(un(e, n)), (t[n] = t[e]));
    }
  }
  function cn(t) {
    (hn(t, 'beforeInit', 'onconstruct'),
      hn(t, 'init', 'onrender'),
      hn(t, 'complete', 'oncomplete'),
      hn(t, 'eventDefinitions', 'events'),
      s(t.adaptors) && hn(t, 'adaptors', 'adapt'));
  }
  function ln(t, e, n, i) {
    yd(i);
    for (var r in i)
      if (md.hasOwnProperty(r)) {
        var s = i[r];
        'el' !== r && 'function' == typeof s
          ? m(
              '' +
                r +
                ' is a Ractive option that does not expect a function and will be ignored',
              'init' === t ? n : null
            )
          : (n[r] = s);
      }
    (vd.forEach(function (r) {
      r[t](e, n, i);
    }),
      Th[t](e, n, i),
      hd[t](e, n, i),
      Mh[t](e, n, i),
      fn(e.prototype, n, i));
  }
  function fn(t, e, n) {
    for (var i in n)
      if (!pd[i] && n.hasOwnProperty(i)) {
        var r = n[i];
        ('function' == typeof r && (r = gd(t, i, r)), (e[i] = r));
      }
  }
  function dn(t) {
    var e = {};
    return (
      t.forEach(function (t) {
        return (e[t] = !0);
      }),
      e
    );
  }
  function pn() {
    ((this.dirtyValue = this.dirtyArgs = !0),
      this.bound &&
        'function' == typeof this.owner.bubble &&
        this.owner.bubble());
  }
  function mn() {
    var t;
    return 1 === this.items.length
      ? this.items[0].detach()
      : ((t = document.createDocumentFragment()),
        this.items.forEach(function (e) {
          var n = e.detach();
          n && t.appendChild(n);
        }),
        t);
  }
  function vn(t) {
    var e, n, i, r;
    if (this.items) {
      for (n = this.items.length, e = 0; n > e; e += 1)
        if (((i = this.items[e]), i.find && (r = i.find(t)))) return r;
      return null;
    }
  }
  function gn(t, e) {
    var n, i, r;
    if (this.items)
      for (i = this.items.length, n = 0; i > n; n += 1)
        ((r = this.items[n]), r.findAll && r.findAll(t, e));
    return e;
  }
  function yn(t, e) {
    var n, i, r;
    if (this.items)
      for (i = this.items.length, n = 0; i > n; n += 1)
        ((r = this.items[n]), r.findAllComponents && r.findAllComponents(t, e));
    return e;
  }
  function bn(t) {
    var e, n, i, r;
    if (this.items) {
      for (e = this.items.length, n = 0; e > n; n += 1)
        if (((i = this.items[n]), i.findComponent && (r = i.findComponent(t))))
          return r;
      return null;
    }
  }
  function wn(t) {
    var e,
      n = t.index;
    return (e = this.items[n + 1]
      ? this.items[n + 1].firstNode()
      : this.owner === this.root
        ? this.owner.component
          ? this.owner.component.findNextNode()
          : null
        : this.owner.findNextNode(this));
  }
  function xn() {
    return this.items && this.items[0] ? this.items[0].firstNode() : null;
  }
  function kn(t, e, n, i) {
    return (
      (i = i || 0),
      t
        .map(function (t) {
          var r, s, o;
          return t.text
            ? t.text
            : t.fragments
              ? t.fragments
                  .map(function (t) {
                    return kn(t.items, e, n, i);
                  })
                  .join('')
              : ((r = n + '-' + i++),
                (o =
                  t.keypath && (s = t.root.viewmodel.wrapped[t.keypath.str])
                    ? s.value
                    : t.getValue()),
                (e[r] = o),
                '${' + r + '}');
        })
        .join('')
    );
  }
  function En() {
    var t, e, n, i;
    return (
      this.dirtyArgs &&
        ((e = Od(this.items, (t = {}), this.root._guid)),
        (n = Af('[' + e + ']', t)),
        (i = n ? n.value : [this.toString()]),
        (this.argsList = i),
        (this.dirtyArgs = !1)),
      this.argsList
    );
  }
  function _n() {
    var t = this;
    do if (t.pElement) return t.pElement.node;
    while ((t = t.parent));
    return this.root.detached || this.root.el;
  }
  function An() {
    var t, e, n, i;
    return (
      this.dirtyValue &&
        ((e = Od(this.items, (t = {}), this.root._guid)),
        (n = Af(e, t)),
        (i = n ? n.value : this.toString()),
        (this.value = i),
        (this.dirtyValue = !1)),
      this.value
    );
  }
  function Sn() {
    (this.registered && this.root.viewmodel.unregister(this.keypath, this),
      this.resolver && this.resolver.unbind());
  }
  function Cn() {
    return this.value;
  }
  function On(t, e) {
    for (var n, i = 0; i < e.prop.length; i++)
      if (void 0 !== (n = t[e.prop[i]])) return n;
  }
  function Pn(t, e) {
    var n,
      i,
      r,
      s,
      o,
      a = {},
      u = !1;
    for (e || (a.refs = n = {}); t; ) {
      if ((o = t.owner) && (i = o.indexRefs)) {
        if (e && (r = o.getIndexRef(e)))
          return ((a.ref = { fragment: t, ref: r }), a);
        if (!e)
          for (s in i)
            ((r = i[s]),
              n[r.n] || ((u = !0), (n[r.n] = { fragment: t, ref: r })));
      }
      !t.parent &&
      t.owner &&
      t.owner.component &&
      t.owner.component.parentFragment &&
      !t.owner.component.instance.isolated
        ? ((a.componentBoundary = !0), (t = t.owner.component.parentFragment))
        : (t = t.parent);
    }
    return u ? a : void 0;
  }
  function Tn(t, e, n) {
    var i;
    return '@' === e.charAt(0)
      ? new Wd(t, e, n)
      : (i = qd(t.parentFragment, e))
        ? new Bd(t, i, n)
        : new Vd(t, e, n);
  }
  function Fn(t, e) {
    var n, i;
    if (Hd[t]) return Hd[t];
    for (i = []; e--; ) i[e] = '_' + e;
    return (
      (n = new Function(i.join(','), 'return(' + t + ')')),
      (Hd[t] = n),
      n
    );
  }
  function Rn(t) {
    return t.call();
  }
  function jn(t, e) {
    return t.replace(/_([0-9]+)/g, function (t, n) {
      var i, r;
      return +n >= e.length
        ? '_' + n
        : ((i = e[n]),
          void 0 === i
            ? 'undefined'
            : i.isSpecial
              ? ((r = i.value), 'number' == typeof r ? r : '"' + r + '"')
              : i.str);
    });
  }
  function Nn(t) {
    return _('${' + t.replace(/[\.\[\]]/g, '-').replace(/\*/, '#MUL#') + '}');
  }
  function Dn(t) {
    return void 0 !== t && '@' !== t[0];
  }
  function In(t, e) {
    var n, i, r;
    if (t.__ractive_nowrap) return t;
    if (((i = '__ractive_' + e._guid), (n = t[i]))) return n;
    if (/this/.test(t.toString())) {
      xa(t, i, { value: Kd.call(t, e), configurable: !0 });
      for (r in t) t.hasOwnProperty(r) && (t[i][r] = t[r]);
      return (e._boundFunctions.push({ fn: t, prop: i }), t[i]);
    }
    return (xa(t, '__ractive_nowrap', { value: t }), t.__ractive_nowrap);
  }
  function Ln(t) {
    return t.value;
  }
  function Vn(t) {
    return void 0 != t;
  }
  function Mn(t) {
    t.forceResolution();
  }
  function Un(t, e) {
    function n(e) {
      t.resolve(e);
    }
    function i(e) {
      var n = t.keypath;
      e != n &&
        (t.resolve(e),
        void 0 !== n &&
          t.fragments &&
          t.fragments.forEach(function (t) {
            t.rebind(n, e);
          }));
    }
    var r, s, o;
    ((s = e.parentFragment),
      (o = e.template),
      (t.root = s.root),
      (t.parentFragment = s),
      (t.pElement = s.pElement),
      (t.template = e.template),
      (t.index = e.index || 0),
      (t.isStatic = e.template.s),
      (t.type = e.template.t),
      (t.registered = !1),
      (r = o.r) && (t.resolver = Qd(t, r, n)),
      e.template.x && (t.resolver = new Gd(t, s, e.template.x, i)),
      e.template.rx && (t.resolver = new tp(t, e.template.rx, i)),
      t.template.n !== Sc || t.hasOwnProperty('value') || t.setValue(void 0));
  }
  function Wn(t) {
    var e, n, i;
    return t && t.isSpecial
      ? ((this.keypath = t), void this.setValue(t.value))
      : (this.registered &&
          (this.root.viewmodel.unregister(this.keypath, this),
          (this.registered = !1),
          (e = !0)),
        (this.keypath = t),
        void 0 != t &&
          ((n = this.root.viewmodel.get(t)),
          this.root.viewmodel.register(t, this),
          (this.registered = !0)),
        this.setValue(n),
        void (e && (i = this.twowayBinding) && i.rebound()));
  }
  function zn(t, e) {
    (this.fragments &&
      this.fragments.forEach(function (n) {
        return n.rebind(t, e);
      }),
      this.resolver && this.resolver.rebind(t, e));
  }
  function Bn() {
    this.parentFragment.bubble();
  }
  function qn() {
    var t;
    return 1 === this.fragments.length
      ? this.fragments[0].detach()
      : ((t = document.createDocumentFragment()),
        this.fragments.forEach(function (e) {
          t.appendChild(e.detach());
        }),
        t);
  }
  function $n(t) {
    var e, n, i;
    for (n = this.fragments.length, e = 0; n > e; e += 1)
      if ((i = this.fragments[e].find(t))) return i;
    return null;
  }
  function Qn(t, e) {
    var n, i;
    for (i = this.fragments.length, n = 0; i > n; n += 1)
      this.fragments[n].findAll(t, e);
  }
  function Zn(t, e) {
    var n, i;
    for (i = this.fragments.length, n = 0; i > n; n += 1)
      this.fragments[n].findAllComponents(t, e);
  }
  function Hn(t) {
    var e, n, i;
    for (n = this.fragments.length, e = 0; n > e; e += 1)
      if ((i = this.fragments[e].findComponent(t))) return i;
    return null;
  }
  function Kn(t) {
    return this.fragments[t.index + 1]
      ? this.fragments[t.index + 1].firstNode()
      : this.parentFragment.findNextNode(this);
  }
  function Gn() {
    var t, e, n;
    if ((t = this.fragments.length))
      for (e = 0; t > e; e += 1)
        if ((n = this.fragments[e].firstNode())) return n;
    return this.parentFragment.findNextNode(this);
  }
  function Yn(t) {
    var e,
      n,
      i,
      r,
      s,
      o,
      a,
      u = this;
    if (!this.shuffling && !this.unbound && this.currentSubtype === Cc) {
      if (
        ((this.shuffling = !0),
        mu.scheduleTask(function () {
          return (u.shuffling = !1);
        }),
        (e = this.parentFragment),
        (s = []),
        t.forEach(function (t, e) {
          var i, r, o, a, h;
          return t === e
            ? void (s[t] = u.fragments[e])
            : ((i = u.fragments[e]),
              void 0 === n && (n = e),
              -1 === t
                ? (u.fragmentsToUnrender.push(i), void i.unbind())
                : ((r = t - e),
                  (o = u.keypath.join(e)),
                  (a = u.keypath.join(t)),
                  (i.index = t),
                  (h = i.registeredIndexRefs) && h.forEach(Jn),
                  i.rebind(o, a),
                  void (s[t] = i)));
        }),
        (r = this.root.viewmodel.get(this.keypath).length),
        void 0 === n)
      ) {
        if (this.length === r) return;
        n = this.length;
      }
      for (
        this.length = this.fragments.length = r,
          this.rendered && mu.addView(this),
          o = { template: this.template.f, root: this.root, owner: this },
          i = n;
        r > i;
        i += 1
      )
        ((a = s[i]),
          a || this.fragmentsToCreate.push(i),
          (this.fragments[i] = a));
    }
  }
  function Jn(t) {
    t.rebind('', '');
  }
  function Xn() {
    var t = this;
    return (
      (this.docFrag = document.createDocumentFragment()),
      this.fragments.forEach(function (e) {
        return t.docFrag.appendChild(e.render());
      }),
      (this.renderedFragments = this.fragments.slice()),
      (this.fragmentsToRender = []),
      (this.rendered = !0),
      this.docFrag
    );
  }
  function ti(t) {
    var e,
      n,
      i = this;
    this.updating ||
      ((this.updating = !0),
      this.keypath &&
        (e = this.root.viewmodel.wrapped[this.keypath.str]) &&
        (t = e.get()),
      this.fragmentsToCreate.length
        ? ((n = {
            template: this.template.f || [],
            root: this.root,
            pElement: this.pElement,
            owner: this,
          }),
          this.fragmentsToCreate.forEach(function (t) {
            var e;
            ((n.context = i.keypath.join(t)),
              (n.index = t),
              (e = new yb(n)),
              i.fragmentsToRender.push((i.fragments[t] = e)));
          }),
          (this.fragmentsToCreate.length = 0))
        : ni(this, t) && (this.bubble(), this.rendered && mu.addView(this)),
      (this.value = t),
      (this.updating = !1));
  }
  function ei(t, e, n) {
    if (e === Cc && t.indexRefs && t.indexRefs[0]) {
      var i = t.indexRefs[0];
      (((n && 'i' === i.t) || (!n && 'k' === i.t)) &&
        (n ||
          ((t.length = 0),
          (t.fragmentsToUnrender = t.fragments.slice(0)),
          t.fragmentsToUnrender.forEach(function (t) {
            return t.unbind();
          }))),
        (i.t = n ? 'k' : 'i'));
    }
    t.currentSubtype = e;
  }
  function ni(t, e) {
    var n = {
      template: t.template.f || [],
      root: t.root,
      pElement: t.parentFragment.pElement,
      owner: t,
    };
    if (((t.hasContext = !0), t.subtype))
      switch (t.subtype) {
        case Ac:
          return ((t.hasContext = !1), ai(t, e, !1, n));
        case Sc:
          return ((t.hasContext = !1), ai(t, e, !0, n));
        case Oc:
          return oi(t, n);
        case Pc:
          return si(t, e, n);
        case Cc:
          if (h(e)) return (ei(t, t.subtype, !0), ri(t, e, n));
      }
    return (
      (t.ordered = !!o(e)),
      t.ordered
        ? (ei(t, Cc, !1), ii(t, e, n))
        : h(e) || 'function' == typeof e
          ? t.template.i
            ? (ei(t, Cc, !0), ri(t, e, n))
            : (ei(t, Oc, !1), oi(t, n))
          : (ei(t, Ac, !1), (t.hasContext = !1), ai(t, e, !1, n))
    );
  }
  function ii(t, e, n) {
    var i, r, s;
    if (((r = e.length), r === t.length)) return !1;
    if (r < t.length)
      ((t.fragmentsToUnrender = t.fragments.splice(r, t.length - r)),
        t.fragmentsToUnrender.forEach(Z));
    else if (r > t.length)
      for (i = t.length; r > i; i += 1)
        ((n.context = t.keypath.join(i)),
          (n.index = i),
          (s = new yb(n)),
          t.fragmentsToRender.push((t.fragments[i] = s)));
    return ((t.length = r), !0);
  }
  function ri(t, e, n) {
    var i, r, s, o, a, u;
    for (s = t.hasKey || (t.hasKey = {}), r = t.fragments.length; r--; )
      ((o = t.fragments[r]),
        o.key in e ||
          ((a = !0),
          o.unbind(),
          t.fragmentsToUnrender.push(o),
          t.fragments.splice(r, 1),
          (s[o.key] = !1)));
    for (r = t.fragments.length; r--; )
      ((o = t.fragments[r]),
        o.index !== r &&
          ((o.index = r), (u = o.registeredIndexRefs) && u.forEach(ci)));
    r = t.fragments.length;
    for (i in e)
      s[i] ||
        ((a = !0),
        (n.context = t.keypath.join(i)),
        (n.key = i),
        (n.index = r++),
        (o = new yb(n)),
        t.fragmentsToRender.push(o),
        t.fragments.push(o),
        (s[i] = !0));
    return ((t.length = t.fragments.length), a);
  }
  function si(t, e, n) {
    return e ? oi(t, n) : ui(t);
  }
  function oi(t, e) {
    var n;
    return t.length
      ? void 0
      : ((e.context = t.keypath),
        (e.index = 0),
        (n = new yb(e)),
        t.fragmentsToRender.push((t.fragments[0] = n)),
        (t.length = 1),
        !0);
  }
  function ai(t, e, n, i) {
    var r, s, a, u, c;
    if (((s = o(e) && 0 === e.length), (a = !1), !o(e) && h(e))) {
      a = !0;
      for (c in e) {
        a = !1;
        break;
      }
    }
    return (
      (r = n ? s || a || !e : e && !s && !a),
      r
        ? t.length
          ? t.length > 1
            ? ((t.fragmentsToUnrender = t.fragments.splice(1)),
              t.fragmentsToUnrender.forEach(Z),
              !0)
            : void 0
          : ((i.index = 0),
            (u = new yb(i)),
            t.fragmentsToRender.push((t.fragments[0] = u)),
            (t.length = 1),
            !0)
        : ui(t)
    );
  }
  function ui(t) {
    return t.length
      ? ((t.fragmentsToUnrender = t.fragments
          .splice(0, t.fragments.length)
          .filter(hi)),
        t.fragmentsToUnrender.forEach(Z),
        (t.length = t.fragmentsToRender.length = 0),
        !0)
      : void 0;
  }
  function hi(t) {
    return t.rendered;
  }
  function ci(t) {
    t.rebind('', '');
  }
  function li(t) {
    var e, n, i;
    for (e = '', n = 0, i = this.length, n = 0; i > n; n += 1)
      e += this.fragments[n].toString(t);
    return e;
  }
  function fi() {
    var t = this;
    (this.fragments.forEach(Z),
      this.fragmentsToRender.forEach(function (e) {
        return I(t.fragments, e);
      }),
      (this.fragmentsToRender = []),
      Dd.call(this),
      (this.length = 0),
      (this.unbound = !0));
  }
  function di(t) {
    (this.fragments.forEach(t ? pi : mi),
      (this.renderedFragments = []),
      (this.rendered = !1));
  }
  function pi(t) {
    t.unrender(!0);
  }
  function mi(t) {
    t.unrender(!1);
  }
  function vi() {
    var t, e, n, i, r, s, o;
    for (n = this.renderedFragments; (t = this.fragmentsToUnrender.pop()); )
      (t.unrender(!0), n.splice(n.indexOf(t), 1));
    for (; (t = this.fragmentsToRender.shift()); ) t.render();
    for (
      this.rendered && (r = this.parentFragment.getNode()),
        o = this.fragments.length,
        s = 0;
      o > s;
      s += 1
    )
      ((t = this.fragments[s]),
        (e = n.indexOf(t, s)),
        e !== s
          ? (this.docFrag.appendChild(t.detach()),
            -1 !== e && n.splice(e, 1),
            n.splice(s, 0, t))
          : this.docFrag.childNodes.length &&
            ((i = t.firstNode()), r.insertBefore(this.docFrag, i)));
    (this.rendered &&
      this.docFrag.childNodes.length &&
      ((i = this.parentFragment.findNextNode(this)),
      r.insertBefore(this.docFrag, i)),
      (this.renderedFragments = this.fragments.slice()));
  }
  function gi() {
    var t, e;
    if (this.docFrag) {
      for (t = this.nodes.length, e = 0; t > e; e += 1)
        this.docFrag.appendChild(this.nodes[e]);
      return this.docFrag;
    }
  }
  function yi(t) {
    var e, n, i, r;
    for (n = this.nodes.length, e = 0; n > e; e += 1)
      if (((i = this.nodes[e]), 1 === i.nodeType)) {
        if (fa(i, t)) return i;
        if ((r = i.querySelector(t))) return r;
      }
    return null;
  }
  function bi(t, e) {
    var n, i, r, s, o, a;
    for (i = this.nodes.length, n = 0; i > n; n += 1)
      if (
        ((r = this.nodes[n]),
        1 === r.nodeType &&
          (fa(r, t) && e.push(r), (s = r.querySelectorAll(t))))
      )
        for (o = s.length, a = 0; o > a; a += 1) e.push(s[a]);
  }
  function wi() {
    return this.rendered && this.nodes[0]
      ? this.nodes[0]
      : this.parentFragment.findNextNode(this);
  }
  function xi(t) {
    return Fp[t] || (Fp[t] = la(t));
  }
  function ki(t) {
    var e, n, i;
    t &&
      'select' === t.name &&
      t.binding &&
      ((e = L(t.node.options).filter(Ei)),
      t.getAttribute('multiple')
        ? (i = e.map(function (t) {
            return t.value;
          }))
        : (n = e[0]) && (i = n.value),
      void 0 !== i && t.binding.setValue(i),
      t.bubble());
  }
  function Ei(t) {
    return t.selected;
  }
  function _i() {
    if (this.rendered)
      throw new Error('Attempted to render an item that was already rendered');
    return (
      (this.docFrag = document.createDocumentFragment()),
      (this.nodes = Rp(
        this.value,
        this.parentFragment.getNode(),
        this.docFrag
      )),
      jp(this.pElement),
      (this.rendered = !0),
      this.docFrag
    );
  }
  function Ai(t) {
    var e;
    ((e = this.root.viewmodel.wrapped[this.keypath.str]) && (t = e.get()),
      t !== this.value &&
        ((this.value = t),
        this.parentFragment.bubble(),
        this.rendered && mu.addView(this)));
  }
  function Si() {
    return void 0 != this.value ? _e('' + this.value) : '';
  }
  function Ci(t) {
    this.rendered && t && (this.nodes.forEach(e), (this.rendered = !1));
  }
  function Oi() {
    var t, e;
    if (this.rendered) {
      for (; this.nodes && this.nodes.length; )
        ((t = this.nodes.pop()), t.parentNode.removeChild(t));
      ((e = this.parentFragment.getNode()),
        (this.nodes = Rp(this.value, e, this.docFrag)),
        e.insertBefore(this.docFrag, this.parentFragment.findNextNode(this)),
        jp(this.pElement));
    }
  }
  function Pi() {
    var t,
      e = this.node;
    return e ? ((t = e.parentNode) && t.removeChild(e), e) : void 0;
  }
  function Ti() {
    return null;
  }
  function Fi() {
    return this.node;
  }
  function Ri(t) {
    return this.attributes && this.attributes[t]
      ? this.attributes[t].value
      : void 0;
  }
  function ji() {
    var t =
      this.useProperty || !this.rendered
        ? this.fragment.getValue()
        : this.fragment.toString();
    a(t, this.value) ||
      ('id' === this.name && this.value && delete this.root.nodes[this.value],
      (this.value = t),
      'value' === this.name && this.node && (this.node._ractive.value = t),
      this.rendered && mu.addView(this));
  }
  function Ni(t) {
    var e = t.fragment.items;
    if (1 === e.length) return e[0].type === Hh ? e[0] : void 0;
  }
  function Di(t) {
    return (
      (this.type = ic),
      (this.element = t.element),
      (this.root = t.root),
      sm(this, t.name),
      (this.isBoolean = yl.test(this.name)),
      t.value && 'string' != typeof t.value
        ? ((this.parentFragment = this.element.parentFragment),
          (this.fragment = new yb({
            template: t.value,
            root: this.root,
            owner: this,
          })),
          (this.value = this.fragment.getValue()),
          (this.interpolator = om(this)),
          (this.isBindable =
            !!this.interpolator && !this.interpolator.isStatic),
          void (this.ready = !0))
        : void (this.value = this.isBoolean ? !0 : t.value || '')
    );
  }
  function Ii(t, e) {
    this.fragment && this.fragment.rebind(t, e);
  }
  function Li(t) {
    var e;
    ((this.node = t),
      (t.namespaceURI && t.namespaceURI !== ia.html) ||
        ((e = cm[this.name] || this.name),
        void 0 !== t[e] && (this.propertyName = e),
        (this.isBoolean || this.isTwoway) && (this.useProperty = !0),
        'value' === e && (t._ractive.value = this.value)),
      (this.rendered = !0),
      this.update());
  }
  function Vi() {
    var t = this,
      e = t.name,
      n = t.namespacePrefix,
      i = t.value,
      r = t.interpolator,
      s = t.fragment;
    if (
      ('value' !== e ||
        ('select' !== this.element.name && 'textarea' !== this.element.name)) &&
      ('value' !== e || void 0 === this.element.getAttribute('contenteditable'))
    ) {
      if ('name' === e && 'input' === this.element.name && r)
        return 'name={{' + (r.keypath.str || r.ref) + '}}';
      if (this.isBoolean) return i ? e : '';
      if (s) {
        if (1 === s.items.length && null == s.items[0].value) return '';
        i = s.toString();
      }
      return (n && (e = n + ':' + e), i ? e + '="' + Mi(i) + '"' : e);
    }
  }
  function Mi(t) {
    return t
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }
  function Ui() {
    (this.fragment && this.fragment.unbind(),
      'id' === this.name && delete this.root.nodes[this.value]);
  }
  function Wi() {
    var t,
      e,
      n,
      i,
      r = this.value;
    if (!this.locked)
      for (
        this.node._ractive.value = r, t = this.node.options, i = t.length;
        i--;

      )
        if (
          ((e = t[i]), (n = e._ractive ? e._ractive.value : e.value), n == r)
        ) {
          e.selected = !0;
          break;
        }
  }
  function zi() {
    var t,
      e,
      n,
      i,
      r = this.value;
    for (s(r) || (r = [r]), t = this.node.options, e = t.length; e--; )
      ((n = t[e]),
        (i = n._ractive ? n._ractive.value : n.value),
        (n.selected = R(r, i)));
  }
  function Bi() {
    var t = this,
      e = t.node,
      n = t.value;
    e.checked = n == e._ractive.value;
  }
  function qi() {
    var t,
      e,
      n,
      i,
      r = this.node;
    if (
      ((t = r.checked),
      (r.value = this.element.getAttribute('value')),
      (r.checked =
        this.element.getAttribute('value') ===
        this.element.getAttribute('name')),
      t &&
        !r.checked &&
        this.element.binding &&
        ((n = this.element.binding.siblings), (i = n.length)))
    ) {
      for (; i--; ) {
        if (((e = n[i]), !e.element.node)) return;
        if (e.element.node.checked)
          return (mu.addRactive(e.root), e.handleChange());
      }
      this.root.viewmodel.set(e.keypath, void 0);
    }
  }
  function $i() {
    var t,
      e,
      n = this,
      i = n.element,
      r = n.node,
      o = n.value,
      a = i.binding;
    if (((t = i.getAttribute('value')), s(o))) {
      for (e = o.length; e--; )
        if (t == o[e]) return void (a.isChecked = r.checked = !0);
      a.isChecked = r.checked = !1;
    } else a.isChecked = r.checked = o == t;
  }
  function Qi() {
    this.node.className = n(this.value);
  }
  function Zi() {
    var t = this,
      e = t.node,
      n = t.value;
    ((this.root.nodes[n] = e), (e.id = n));
  }
  function Hi() {
    var t, e;
    ((t = this.node),
      (e = this.value),
      void 0 === e && (e = ''),
      t.style.setAttribute('cssText', e));
  }
  function Ki() {
    var t = this.value;
    (void 0 === t && (t = ''), this.locked || (this.node.innerHTML = t));
  }
  function Gi() {
    var t = this,
      e = t.node,
      n = t.value;
    ((e._ractive.value = n), this.locked || (e.value = void 0 == n ? '' : n));
  }
  function Yi() {
    this.locked || (this.node[this.propertyName] = this.value);
  }
  function Ji() {
    var t = this,
      e = t.node,
      n = t.namespace,
      i = t.name,
      r = t.value,
      s = t.fragment;
    n
      ? e.setAttributeNS(n, i, (s || r).toString())
      : this.isBoolean
        ? r
          ? e.setAttribute(i, '')
          : e.removeAttribute(i)
        : null == r
          ? e.removeAttribute(i)
          : e.setAttribute(i, (s || r).toString());
  }
  function Xi() {
    var t,
      e,
      n = this,
      i = n.name,
      r = n.element,
      s = n.node;
    ('id' === i
      ? (e = bm)
      : 'value' === i
        ? 'select' === r.name && 'value' === i
          ? (e = r.getAttribute('multiple') ? pm : dm)
          : 'textarea' === r.name
            ? (e = km)
            : null != r.getAttribute('contenteditable')
              ? (e = xm)
              : 'input' === r.name &&
                ((t = r.getAttribute('type')),
                (e =
                  'file' === t
                    ? Fa
                    : 'radio' === t && r.binding && 'name' === r.binding.name
                      ? vm
                      : km))
        : this.isTwoway && 'name' === i
          ? 'radio' === s.type
            ? (e = mm)
            : 'checkbox' === s.type && (e = gm)
          : 'style' === i && s.style.setAttribute
            ? (e = wm)
            : 'class' !== i || (s.namespaceURI && s.namespaceURI !== ia.html)
              ? this.useProperty && (e = Em)
              : (e = ym),
      e || (e = _m),
      (this.update = e),
      this.update());
  }
  function tr(t, e) {
    var n = e ? 'svg' : 'div';
    return (
      (Cm.innerHTML = '<' + n + ' ' + t + '></' + n + '>'),
      L(Cm.childNodes[0].attributes)
    );
  }
  function er(t, e) {
    for (var n = t.length; n--; ) if (t[n].name === e.name) return !1;
    return !0;
  }
  function nr(t) {
    for (; (t = t.parent); ) if ('form' === t.name) return t;
  }
  function ir() {
    this._ractive.binding.handleChange();
  }
  function rr() {
    var t;
    (Im.call(this),
      (t = this._ractive.root.viewmodel.get(this._ractive.binding.keypath)),
      (this.value = void 0 == t ? '' : t));
  }
  function sr() {
    var t = this._ractive.binding,
      e = this;
    (t._timeout && clearTimeout(t._timeout),
      (t._timeout = setTimeout(function () {
        (t.rendered && Im.call(e), (t._timeout = void 0));
      }, t.element.lazy)));
  }
  function or(t, e, n) {
    var i = t + e + n;
    return Wm[i] || (Wm[i] = []);
  }
  function ar(t) {
    return t.isChecked;
  }
  function ur(t) {
    return t.element.getAttribute('value');
  }
  function hr(t) {
    var e,
      n,
      i,
      r,
      s,
      o = t.attributes;
    return (
      t.binding && (t.binding.teardown(), (t.binding = null)),
      (t.getAttribute('contenteditable') ||
        (o.contenteditable && cr(o.contenteditable))) &&
      cr(o.value)
        ? (n = Mm)
        : 'input' === t.name
          ? ((e = t.getAttribute('type')),
            'radio' === e || 'checkbox' === e
              ? ((i = cr(o.name)),
                (r = cr(o.checked)),
                i &&
                  r &&
                  m(
                    'A radio input can have two-way binding on its name attribute, or its checked attribute - not both',
                    { ractive: t.root }
                  ),
                i
                  ? (n = 'radio' === e ? $m : Zm)
                  : r && (n = 'radio' === e ? Bm : Km))
              : 'file' === e && cr(o.value)
                ? (n = ev)
                : cr(o.value) &&
                  (n = 'number' === e || 'range' === e ? nv : Lm))
          : 'select' === t.name && cr(o.value)
            ? (n = t.getAttribute('multiple') ? Xm : Ym)
            : 'textarea' === t.name && cr(o.value) && (n = Lm),
      n && (s = new n(t)) && s.keypath ? s : void 0
    );
  }
  function cr(t) {
    return t && t.isBindable;
  }
  function lr() {
    var t = this.getAction();
    t && !this.hasListener
      ? this.listen()
      : !t && this.hasListener && this.unrender();
  }
  function fr(t) {
    Wu(this.root, this.getAction(), { event: t });
  }
  function dr() {
    return this.action.toString().trim();
  }
  function pr(t, e, n) {
    var i,
      r,
      s,
      o = this;
    ((this.element = t),
      (this.root = t.root),
      (this.parentFragment = t.parentFragment),
      (this.name = e),
      -1 !== e.indexOf('*') &&
        (l(
          'Only component proxy-events may contain "*" wildcards, <%s on-%s="..."/> is not valid',
          t.name,
          e
        ),
        (this.invalid = !0)),
      n.m
        ? ((r = n.a.r),
          (this.method = n.m),
          (this.keypaths = []),
          (this.fn = Zd(n.a.s, r.length)),
          (this.parentFragment = t.parentFragment),
          (s = this.root),
          (this.refResolvers = []),
          r.forEach(function (t, e) {
            var n = void 0;
            (n = uv.exec(t))
              ? (o.keypaths[e] = {
                  eventObject: !0,
                  refinements: n[1] ? n[1].split('.') : [],
                })
              : o.refResolvers.push(
                  Qd(o, t, function (t) {
                    return o.resolve(e, t);
                  })
                );
          }),
          (this.fire = mr))
        : ((i = n.n || n),
          'string' != typeof i &&
            (i = new yb({ template: i, root: this.root, owner: this })),
          (this.action = i),
          n.d
            ? ((this.dynamicParams = new yb({
                template: n.d,
                root: this.root,
                owner: this.element,
              })),
              (this.fire = gr))
            : n.a && ((this.params = n.a), (this.fire = vr))));
  }
  function mr(t) {
    var e, n, i;
    if (((e = this.root), 'function' != typeof e[this.method]))
      throw new Error(
        'Attempted to call a non-existent method ("' + this.method + '")'
      );
    ((n = this.keypaths.map(function (n) {
      var i, r, s;
      if (void 0 === n) return void 0;
      if (n.eventObject) {
        if (((i = t), (r = n.refinements.length)))
          for (s = 0; r > s; s += 1) i = i[n.refinements[s]];
      } else i = e.viewmodel.get(n);
      return i;
    })),
      Uu.enqueue(e, t),
      (i = this.fn.apply(null, n)),
      e[this.method].apply(e, i),
      Uu.dequeue(e));
  }
  function vr(t) {
    Wu(this.root, this.getAction(), { event: t, args: this.params });
  }
  function gr(t) {
    var e = this.dynamicParams.getArgsList();
    ('string' == typeof e && (e = e.substr(1, e.length - 2)),
      Wu(this.root, this.getAction(), { event: t, args: e }));
  }
  function yr(t) {
    var e,
      n,
      i,
      r = {};
    ((e = this._ractive),
      (n = e.events[t.type]),
      (i = qd(n.element.parentFragment)) && (r = qd.resolve(i)),
      n.fire({
        node: this,
        original: t,
        index: r,
        keypath: e.keypath.str,
        context: e.root.viewmodel.get(e.keypath),
      }));
  }
  function br() {
    var t,
      e = this.name;
    if (!this.invalid) {
      if ((t = g('events', this.root, e))) this.custom = t(this.node, wr(e));
      else {
        if (!('on' + e in this.node || (window && 'on' + e in window) || ta))
          return void (fv[e] || v(Da(e, 'event'), { node: this.node }));
        this.node.addEventListener(e, hv, !1);
      }
      this.hasListener = !0;
    }
  }
  function wr(t) {
    return (
      lv[t] ||
        (lv[t] = function (e) {
          var n = e.node._ractive;
          ((e.index = n.index),
            (e.keypath = n.keypath.str),
            (e.context = n.root.viewmodel.get(n.keypath)),
            n.events[t].fire(e));
        }),
      lv[t]
    );
  }
  function xr(t, e) {
    function n(n) {
      n && n.rebind(t, e);
    }
    var i;
    return this.method
      ? ((i = this.element.parentFragment), void this.refResolvers.forEach(n))
      : ('string' != typeof this.action && n(this.action),
        void (this.dynamicParams && n(this.dynamicParams)));
  }
  function kr() {
    ((this.node = this.element.node),
      (this.node._ractive.events[this.name] = this),
      (this.method || this.getAction()) && this.listen());
  }
  function Er(t, e) {
    this.keypaths[t] = e;
  }
  function _r() {
    return this.method
      ? void this.refResolvers.forEach(Z)
      : ('string' != typeof this.action && this.action.unbind(),
        void (this.dynamicParams && this.dynamicParams.unbind()));
  }
  function Ar() {
    (this.custom
      ? this.custom.teardown()
      : this.node.removeEventListener(this.name, hv, !1),
      (this.hasListener = !1));
  }
  function Sr() {
    var t = this;
    (this.dirty ||
      ((this.dirty = !0),
      mu.scheduleTask(function () {
        (Cr(t), (t.dirty = !1));
      })),
      this.parentFragment.bubble());
  }
  function Cr(t) {
    var e, n, i, r, s;
    ((e = t.node),
      e &&
        ((r = L(e.options)),
        (n = t.getAttribute('value')),
        (i = t.getAttribute('multiple')),
        void 0 !== n
          ? (r.forEach(function (t) {
              var e, r;
              ((e = t._ractive ? t._ractive.value : t.value),
                (r = i ? Or(n, e) : n == e),
                r && (s = !0),
                (t.selected = r));
            }),
            s ||
              (r[0] && (r[0].selected = !0),
              t.binding && t.binding.forceUpdate()))
          : t.binding && t.binding.forceUpdate()));
  }
  function Or(t, e) {
    for (var n = t.length; n--; ) if (t[n] == e) return !0;
  }
  function Pr(t, e) {
    ((t.select = Fr(t.parent)),
      t.select &&
        (t.select.options.push(t),
        e.a || (e.a = {}),
        void 0 !== e.a.value ||
          e.a.hasOwnProperty('disabled') ||
          (e.a.value = e.f),
        'selected' in e.a &&
          void 0 !== t.select.getAttribute('value') &&
          delete e.a.selected));
  }
  function Tr(t) {
    t.select && I(t.select.options, t);
  }
  function Fr(t) {
    if (t)
      do if ('select' === t.name) return t;
      while ((t = t.parent));
  }
  function Rr(t) {
    var e, n, i, r, s, o, a;
    ((this.type = Xh),
      (e = this.parentFragment = t.parentFragment),
      (n = this.template = t.template),
      (this.parent = t.pElement || e.pElement),
      (this.root = i = e.root),
      (this.index = t.index),
      (this.key = t.key),
      (this.name = rm(n.e)),
      'option' === this.name && Pr(this, n),
      'select' === this.name && ((this.options = []), (this.bubble = Sr)),
      'form' === this.name && (this.formBindings = []),
      (a = nm(this, n)),
      (this.attributes = Pm(this, n.a)),
      (this.conditionalAttributes = Rm(this, n.m)),
      n.f &&
        (this.fragment = new yb({
          template: n.f,
          root: i,
          owner: this,
          pElement: this,
          cssIds: null,
        })),
      (o = i.twoway),
      a.twoway === !1 ? (o = !1) : a.twoway === !0 && (o = !0),
      (this.twoway = o),
      (this.lazy = a.lazy),
      o &&
        (r = iv(this, n.a)) &&
        ((this.binding = r),
        (s =
          this.root._twowayBindings[r.keypath.str] ||
          (this.root._twowayBindings[r.keypath.str] = [])),
        s.push(r)),
      n.v && (this.eventHandlers = wv(this, n.v)),
      n.o && (this.decorator = new Av(this, n.o)),
      (this.intro = n.t0 || n.t1),
      (this.outro = n.t0 || n.t2));
  }
  function jr(t, e) {
    function n(n) {
      n.rebind(t, e);
    }
    var i, r, s, o;
    if (
      (this.attributes && this.attributes.forEach(n),
      this.conditionalAttributes && this.conditionalAttributes.forEach(n),
      this.eventHandlers && this.eventHandlers.forEach(n),
      this.decorator && n(this.decorator),
      this.fragment && n(this.fragment),
      (s = this.liveQueries))
    )
      for (o = this.root, i = s.length; i--; ) s[i]._makeDirty();
    this.node && (r = this.node._ractive) && k(r, 'keypath', t, e);
  }
  function Nr(t) {
    var e;
    (t.attributes.width || t.attributes.height) &&
      t.node.addEventListener(
        'load',
        (e = function () {
          var n = t.getAttribute('width'),
            i = t.getAttribute('height');
          (void 0 !== n && t.node.setAttribute('width', n),
            void 0 !== i && t.node.setAttribute('height', i),
            t.node.removeEventListener('load', e, !1));
        }),
        !1
      );
  }
  function Dr(t) {
    t.node.addEventListener('reset', Lr, !1);
  }
  function Ir(t) {
    t.node.removeEventListener('reset', Lr, !1);
  }
  function Lr() {
    var t = this._ractive.proxy;
    (mu.start(), t.formBindings.forEach(Vr), mu.end());
  }
  function Vr(t) {
    t.root.viewmodel.set(t.keypath, t.resetValue);
  }
  function Mr(t, e, n) {
    var i, r, s;
    ((this.element = t),
      (this.root = i = t.root),
      (this.isIntro = n),
      (r = e.n || e),
      ('string' == typeof r ||
        ((s = new yb({ template: r, root: i, owner: t })),
        (r = s.toString()),
        s.unbind(),
        '' !== r)) &&
        ((this.name = r),
        e.a
          ? (this.params = e.a)
          : e.d &&
            ((s = new yb({ template: e.d, root: i, owner: t })),
            (this.params = s.getArgsList()),
            s.unbind()),
        (this._fn = g('transitions', i, r)),
        this._fn || v(Da(r, 'transition'), { ractive: this.root })));
  }
  function Ur(t) {
    return t;
  }
  function Wr() {
    eg.hidden = document[Yv];
  }
  function zr() {
    eg.hidden = !0;
  }
  function Br() {
    eg.hidden = !1;
  }
  function qr() {
    var t,
      e,
      n,
      i = this;
    return (
      (t = this.node = this.element.node),
      (e = t.getAttribute('style')),
      (this.complete = function (r) {
        n ||
          (!r && i.isIntro && $r(t, e),
          (t._ractive.transition = null),
          i._manager.remove(i),
          (n = !0));
      }),
      this._fn
        ? void this._fn.apply(this.root, [this].concat(this.params))
        : void this.complete()
    );
  }
  function $r(t, e) {
    e
      ? t.setAttribute('style', e)
      : (t.getAttribute('style'), t.removeAttribute('style'));
  }
  function Qr() {
    var t,
      e,
      n,
      i = this,
      r = this.root;
    return (
      (t = Zr(this)),
      (e = this.node = la(this.name, t)),
      this.parentFragment.cssIds &&
        this.node.setAttribute(
          'data-ractive-css',
          this.parentFragment.cssIds
            .map(function (t) {
              return '{' + t + '}';
            })
            .join(' ')
        ),
      xa(this.node, '_ractive', {
        value: {
          proxy: this,
          keypath: au(this.parentFragment),
          events: wa(null),
          root: r,
        },
      }),
      this.attributes.forEach(function (t) {
        return t.render(e);
      }),
      this.conditionalAttributes.forEach(function (t) {
        return t.render(e);
      }),
      this.fragment &&
        ('script' === this.name
          ? ((this.bubble = fg),
            (this.node.text = this.fragment.toString(!1)),
            (this.fragment.unrender = Fa))
          : 'style' === this.name
            ? ((this.bubble = lg), this.bubble(), (this.fragment.unrender = Fa))
            : this.binding && this.getAttribute('contenteditable')
              ? (this.fragment.unrender = Fa)
              : this.node.appendChild(this.fragment.render())),
      this.binding &&
        (this.binding.render(), (this.node._ractive.binding = this.binding)),
      this.eventHandlers &&
        this.eventHandlers.forEach(function (t) {
          return t.render();
        }),
      'option' === this.name && Hr(this),
      'img' === this.name
        ? Nr(this)
        : 'form' === this.name
          ? Dr(this)
          : 'input' === this.name || 'textarea' === this.name
            ? (this.node.defaultValue = this.node.value)
            : 'option' === this.name &&
              (this.node.defaultSelected = this.node.selected),
      this.decorator &&
        this.decorator.fn &&
        mu.scheduleTask(function () {
          i.decorator.torndown || i.decorator.init();
        }, !0),
      r.transitionsEnabled &&
        this.intro &&
        ((n = new dg(this, this.intro, !0)),
        mu.registerTransition(n),
        mu.scheduleTask(function () {
          return n.start();
        }, !0),
        (this.transition = n)),
      this.node.autofocus &&
        mu.scheduleTask(function () {
          return i.node.focus();
        }, !0),
      Kr(this),
      this.node
    );
  }
  function Zr(t) {
    var e, n, i;
    return (e = (n = t.getAttribute('xmlns'))
      ? n
      : 'svg' === t.name
        ? ia.svg
        : (i = t.parent)
          ? 'foreignObject' === i.name
            ? ia.html
            : i.node.namespaceURI
          : t.root.el.namespaceURI);
  }
  function Hr(t) {
    var e, n, i;
    if (t.select && ((n = t.select.getAttribute('value')), void 0 !== n))
      if (((e = t.getAttribute('value')), t.select.node.multiple && s(n))) {
        for (i = n.length; i--; )
          if (e == n[i]) {
            t.node.selected = !0;
            break;
          }
      } else t.node.selected = e == n;
  }
  function Kr(t) {
    var e, n, i, r, s;
    e = t.root;
    do
      for (n = e._liveQueries, i = n.length; i--; )
        ((r = n[i]),
          (s = n['_' + r]),
          s._test(t) && (t.liveQueries || (t.liveQueries = [])).push(s));
    while ((e = e.parent));
  }
  function Gr(t) {
    var e, n, i;
    if (((e = t.getAttribute('value')), void 0 === e || !t.select)) return !1;
    if (((n = t.select.getAttribute('value')), n == e)) return !0;
    if (t.select.getAttribute('multiple') && s(n))
      for (i = n.length; i--; ) if (n[i] == e) return !0;
  }
  function Yr(t) {
    var e, n, i, r;
    return (
      (e = t.attributes),
      (n = e.type),
      (i = e.value),
      (r = e.name),
      n &&
      'radio' === n.value &&
      i &&
      r.interpolator &&
      i.value === r.interpolator.value
        ? !0
        : void 0
    );
  }
  function Jr(t) {
    var e = t.toString();
    return e ? ' ' + e : '';
  }
  function Xr() {
    (this.fragment && this.fragment.unbind(),
      this.binding && this.binding.unbind(),
      this.eventHandlers && this.eventHandlers.forEach(Z),
      'option' === this.name && Tr(this),
      this.attributes.forEach(Z),
      this.conditionalAttributes.forEach(Z));
  }
  function ts(t) {
    var e, n, i;
    ((i = this.transition) && i.complete(),
      'option' === this.name ? this.detach() : t && mu.detachWhenReady(this),
      this.fragment && this.fragment.unrender(!1),
      (e = this.binding) &&
        (this.binding.unrender(),
        (this.node._ractive.binding = null),
        (n = this.root._twowayBindings[e.keypath.str]),
        n.splice(n.indexOf(e), 1)),
      this.eventHandlers && this.eventHandlers.forEach(H),
      this.decorator && mu.registerDecorator(this.decorator),
      this.root.transitionsEnabled &&
        this.outro &&
        ((i = new dg(this, this.outro, !1)),
        mu.registerTransition(i),
        mu.scheduleTask(function () {
          return i.start();
        })),
      this.liveQueries && es(this),
      'form' === this.name && Ir(this));
  }
  function es(t) {
    var e, n, i;
    for (i = t.liveQueries.length; i--; )
      ((e = t.liveQueries[i]), (n = e.selector), e._remove(t.node));
  }
  function ns(t, e) {
    var n = xg.exec(e)[0];
    return null === t || n.length < t.length ? n : t;
  }
  function is(t, e, n) {
    var i;
    if ((i = rs(t, e, n || {}))) return i;
    if ((i = ad.fromId(e, { noThrow: !0 }))) {
      i = kg(i);
      var r = ad.parse(i, ad.getParseOptions(t));
      return (t.partials[e] = r.t);
    }
  }
  function rs(t, e, n) {
    var i = void 0,
      r = as(e, n.owner);
    if (r) return r;
    var s = y('partials', t, e);
    if (s) {
      if (
        ((r = s.partials[e]),
        'function' == typeof r &&
          ((i = r.bind(s)),
          (i.isOwner = s.partials.hasOwnProperty(e)),
          (r = i.call(t, ad))),
        !r && '' !== r)
      )
        return void m(Na, e, 'partial', 'partial', { ractive: t });
      if (!ad.isParsed(r)) {
        var o = ad.parse(r, ad.getParseOptions(s));
        o.p &&
          m('Partials ({{>%s}}) cannot contain nested inline partials', e, {
            ractive: t,
          });
        var a = i ? s : ss(s, e);
        a.partials[e] = r = o.t;
      }
      return (i && (r._fn = i), r.v ? r.t : r);
    }
  }
  function ss(t, e) {
    return t.partials.hasOwnProperty(e) ? t : os(t.constructor, e);
  }
  function os(t, e) {
    return t ? (t.partials.hasOwnProperty(e) ? t : os(t._Parent, e)) : void 0;
  }
  function as(t, e) {
    if (e) {
      if (e.template && e.template.p && e.template.p[t]) return e.template.p[t];
      if (e.parentFragment && e.parentFragment.owner)
        return as(t, e.parentFragment.owner);
    }
  }
  function us(t, e) {
    var n,
      i = y('components', t, e);
    if (i && ((n = i.components[e]), !n._Parent)) {
      var r = n.bind(i);
      if (((r.isOwner = i.components.hasOwnProperty(e)), (n = r()), !n))
        return void m(Na, e, 'component', 'component', { ractive: t });
      ('string' == typeof n && (n = us(t, n)),
        (n._fn = r),
        (i.components[e] = n));
    }
    return n;
  }
  function hs() {
    var t = this.instance.fragment.detach();
    return (jg.fire(this.instance), t);
  }
  function cs(t) {
    return this.instance.fragment.find(t);
  }
  function ls(t, e) {
    return this.instance.fragment.findAll(t, e);
  }
  function fs(t, e) {
    (e._test(this, !0),
      this.instance.fragment && this.instance.fragment.findAllComponents(t, e));
  }
  function ds(t) {
    return t && t !== this.name
      ? this.instance.fragment
        ? this.instance.fragment.findComponent(t)
        : null
      : this.instance;
  }
  function ps() {
    return this.parentFragment.findNextNode(this);
  }
  function ms() {
    return this.rendered ? this.instance.fragment.firstNode() : null;
  }
  function vs(t, e, n) {
    function i(t) {
      var n, i;
      ((t.value = e),
        t.updating ||
          ((i = t.ractive),
          (n = t.keypath),
          (t.updating = !0),
          mu.start(i),
          i.viewmodel.mark(n),
          mu.end(),
          (t.updating = !1)));
    }
    var r, s, o, a, u, h;
    if (((r = t.obj), (s = t.prop), n && !n.configurable)) {
      if ('length' === s) return;
      throw new Error(
        'Cannot use magic mode with property "' +
          s +
          '" - object is not configurable'
      );
    }
    (n && ((o = n.get), (a = n.set)),
      (u =
        o ||
        function () {
          return e;
        }),
      (h = function (t) {
        (a && a(t), (e = o ? o() : t), h._ractiveWrappers.forEach(i));
      }),
      (h._ractiveWrappers = [t]),
      Object.defineProperty(r, s, {
        get: u,
        set: h,
        enumerable: !0,
        configurable: !0,
      }));
  }
  function gs(t, e) {
    var n, i, r, s;
    if (this.adaptors)
      for (n = this.adaptors.length, i = 0; n > i; i += 1)
        if (((r = this.adaptors[i]), r.filter(e, t, this.ractive)))
          return (
            (s = this.wrapped[t] = r.wrap(this.ractive, e, t, bs(t))),
            void (s.value = e)
          );
  }
  function ys(t, e) {
    var n,
      i = {};
    if (!e) return t;
    e += '.';
    for (n in t) t.hasOwnProperty(n) && (i[e + n] = t[n]);
    return i;
  }
  function bs(t) {
    var e;
    return (
      iy[t] ||
        ((e = t ? t + '.' : ''),
        (iy[t] = function (n, i) {
          var r;
          return 'string' == typeof n
            ? ((r = {}), (r[e + n] = i), r)
            : 'object' == typeof n
              ? e
                ? ys(n, t)
                : n
              : void 0;
        })),
      iy[t]
    );
  }
  function ws(t) {
    var e,
      n,
      i = [Za];
    for (e = t.length; e--; )
      for (n = t[e].parent; n && !n.isRoot; )
        (-1 === t.indexOf(n) && F(i, n), (n = n.parent));
    return i;
  }
  function xs(t, e, n) {
    var i;
    (Es(t, e),
      n ||
        ((i = e.wildcardMatches()),
        i.forEach(function (n) {
          ks(t, n, e);
        })));
  }
  function ks(t, e, n) {
    var i, r, s;
    ((e = e.str || e),
      (i = t.depsMap.patternObservers),
      (r = i && i[e]),
      r &&
        r.forEach(function (e) {
          ((s = n.join(e.lastKey)), Es(t, s), ks(t, e, s));
        }));
  }
  function Es(t, e) {
    t.patternObservers.forEach(function (t) {
      t.regex.test(e.str) && t.update(e);
    });
  }
  function _s() {
    function t(t) {
      var i = t.key;
      t.viewmodel === o
        ? (o.clearCache(i.str), t.invalidate(), n.push(i), e(i))
        : t.viewmodel.mark(i);
    }
    function e(n) {
      var i, r;
      o.noCascade.hasOwnProperty(n.str) ||
        ((r = o.deps.computed[n.str]) && r.forEach(t),
        (i = o.depsMap.computed[n.str]) && i.forEach(e));
    }
    var n,
      i,
      r,
      s = this,
      o = this,
      a = {};
    return (
      (n = this.changes),
      n.length
        ? (n.slice().forEach(e),
          (i = ry(n)),
          i.forEach(function (e) {
            var i;
            -1 === n.indexOf(e) && (i = o.deps.computed[e.str]) && i.forEach(t);
          }),
          (this.changes = []),
          this.patternObservers.length &&
            (i.forEach(function (t) {
              return sy(s, t, !0);
            }),
            n.forEach(function (t) {
              return sy(s, t);
            })),
          this.deps.observers &&
            (i.forEach(function (t) {
              return As(s, null, t, 'observers');
            }),
            Cs(this, n, 'observers')),
          this.deps['default'] &&
            ((r = []),
            i.forEach(function (t) {
              return As(s, r, t, 'default');
            }),
            r.length && Ss(this, r, n),
            Cs(this, n, 'default')),
          n.forEach(function (t) {
            a[t.str] = s.get(t);
          }),
          (this.implicitChanges = {}),
          (this.noCascade = {}),
          a)
        : void 0
    );
  }
  function As(t, e, n, i) {
    var r, s;
    (r = Os(t, n, i)) &&
      ((s = t.get(n)),
      r.forEach(function (t) {
        e && t.refineValue ? e.push(t) : t.setValue(s);
      }));
  }
  function Ss(t, e, n) {
    e.forEach(function (e) {
      for (var i = !1, r = 0, s = n.length, o = []; s > r; ) {
        var a = n[r];
        if (a === e.keypath) {
          i = !0;
          break;
        }
        (a.slice(0, e.keypath.length) === e.keypath && o.push(a), r++);
      }
      (i && e.setValue(t.get(e.keypath)), o.length && e.refineValue(o));
    });
  }
  function Cs(t, e, n) {
    function i(t) {
      (t.forEach(r), t.forEach(s));
    }
    function r(e) {
      var i = Os(t, e, n);
      i && a.push({ keypath: e, deps: i });
    }
    function s(e) {
      var r;
      (r = t.depsMap[n][e.str]) && i(r);
    }
    function o(e) {
      var n = t.get(e.keypath);
      e.deps.forEach(function (t) {
        return t.setValue(n);
      });
    }
    var a = [];
    (i(e), a.forEach(o));
  }
  function Os(t, e, n) {
    var i = t.deps[n];
    return i ? i[e.str] : null;
  }
  function Ps() {
    this.captureGroups.push([]);
  }
  function Ts(t, e) {
    var n, i;
    if (
      (e ||
        ((i = this.wrapped[t]) &&
          i.teardown() !== !1 &&
          (this.wrapped[t] = null)),
      (this.cache[t] = void 0),
      (n = this.cacheMap[t]))
    )
      for (; n.length; ) this.clearCache(n.pop());
  }
  function Fs(t, e) {
    var n = e.firstKey;
    return !(n in t.data || n in t.computations || n in t.mappings);
  }
  function Rs(t, e) {
    var n = new fy(t, e);
    return (this.ready && n.init(this), (this.computations[t.str] = n));
  }
  function js(t, e) {
    var n,
      i,
      r,
      s,
      o,
      a = this.cache,
      u = t.str;
    if (
      ((e = e || vy),
      e.capture && (s = D(this.captureGroups)) && (~s.indexOf(t) || s.push(t)),
      Oa.call(this.mappings, t.firstKey))
    )
      return this.mappings[t.firstKey].get(t, e);
    if (t.isSpecial) return t.value;
    if (
      (void 0 === a[u]
        ? ((i = this.computations[u]) && !i.bypass
            ? ((n = i.get()), this.adapt(u, n))
            : (r = this.wrapped[u])
              ? (n = r.value)
              : t.isRoot
                ? (this.adapt('', this.data), (n = this.data))
                : (n = Ns(this, t)),
          (a[u] = n))
        : (n = a[u]),
      !e.noUnwrap && (r = this.wrapped[u]) && (n = r.get()),
      t.isRoot && e.fullRootGet)
    )
      for (o in this.mappings) n[o] = this.mappings[o].getValue();
    return n === py ? void 0 : n;
  }
  function Ns(t, e) {
    var n, i, r, s;
    return (
      (n = t.get(e.parent)),
      (s = t.wrapped[e.parent.str]) && (n = s.get()),
      null !== n && void 0 !== n
        ? ((i = t.cacheMap[e.parent.str])
            ? -1 === i.indexOf(e.str) && i.push(e.str)
            : (t.cacheMap[e.parent.str] = [e.str]),
          'object' != typeof n || e.lastKey in n
            ? ((r = n[e.lastKey]),
              t.adapt(e.str, r, !1),
              (t.cache[e.str] = r),
              r)
            : (t.cache[e.str] = py))
        : void 0
    );
  }
  function Ds() {
    var t;
    for (t in this.computations) this.computations[t].init(this);
  }
  function Is(t, e) {
    var n = (this.mappings[t.str] = new by(t, e));
    return (n.initViewmodel(this), n);
  }
  function Ls(t, e) {
    var n,
      i = t.str;
    (e &&
      (e.implicit && (this.implicitChanges[i] = !0),
      e.noCascade && (this.noCascade[i] = !0)),
      (n = this.computations[i]) && n.invalidate(),
      -1 === this.changes.indexOf(t) && this.changes.push(t));
    var r = e ? e.keepExistingWrapper : !1;
    (this.clearCache(i, r), this.ready && this.onchange());
  }
  function Vs(t, e, n, i) {
    var r, s, o, a;
    if ((this.mark(t), i && i.compare)) {
      o = Us(i.compare);
      try {
        ((r = e.map(o)), (s = n.map(o)));
      } catch (u) {
        (m(
          'merge(): "%s" comparison failed. Falling back to identity checking',
          t
        ),
          (r = e),
          (s = n));
      }
    } else ((r = e), (s = n));
    ((a = xy(r, s)), this.smartUpdate(t, n, a, e.length !== n.length));
  }
  function Ms(t) {
    return JSON.stringify(t);
  }
  function Us(t) {
    if (t === !0) return Ms;
    if ('string' == typeof t)
      return (
        Ey[t] ||
          (Ey[t] = function (e) {
            return e[t];
          }),
        Ey[t]
      );
    if ('function' == typeof t) return t;
    throw new Error(
      'The `compare` option must be a function, or a string representing an identifying field (or `true` to use JSON.stringify)'
    );
  }
  function Ws(t, e) {
    var n,
      i,
      r,
      s = void 0 === arguments[2] ? 'default' : arguments[2];
    e.isStatic ||
      ((n = this.mappings[t.firstKey])
        ? n.register(t, e, s)
        : ((i = this.deps[s] || (this.deps[s] = {})),
          (r = i[t.str] || (i[t.str] = [])),
          r.push(e),
          this.depsMap[s] || (this.depsMap[s] = {}),
          t.isRoot || zs(this, t, s)));
  }
  function zs(t, e, n) {
    for (var i, r, s; !e.isRoot; )
      ((i = t.depsMap[n]),
        (r = i[e.parent.str] || (i[e.parent.str] = [])),
        (s = e.str),
        void 0 === r['_' + s] && ((r['_' + s] = 0), r.push(e)),
        (r['_' + s] += 1),
        (e = e.parent));
  }
  function Bs() {
    return this.captureGroups.pop();
  }
  function qs(t) {
    ((this.data = t), this.clearCache(''));
  }
  function $s(t, e) {
    var n,
      i,
      r,
      s,
      o = void 0 === arguments[2] ? {} : arguments[2];
    if (!o.noMapping && (n = this.mappings[t.firstKey])) return n.set(t, e);
    if ((i = this.computations[t.str])) {
      if (i.setting) return;
      (i.set(e), (e = i.get()));
    }
    a(this.cache[t.str], e) ||
      ((r = this.wrapped[t.str]),
      r && r.reset && ((s = r.reset(e) !== !1), s && (e = r.get())),
      i || s || Qs(this, t, e),
      o.silent ? this.clearCache(t.str) : this.mark(t));
  }
  function Qs(t, e, n) {
    var i, r, s, o;
    ((s = function () {
      i.set ? i.set(e.lastKey, n) : ((r = i.get()), o());
    }),
      (o = function () {
        (r || ((r = Yg(e.lastKey)), t.set(e.parent, r, { silent: !0 })),
          (r[e.lastKey] = n));
      }),
      (i = t.wrapped[e.parent.str]),
      i
        ? s()
        : ((r = t.get(e.parent)), (i = t.wrapped[e.parent.str]) ? s() : o()));
  }
  function Zs(t, e, n) {
    var i,
      r,
      s,
      o = this;
    if (
      ((r = n.length),
      n.forEach(function (e, n) {
        -1 === e && o.mark(t.join(n), Ty);
      }),
      this.set(t, e, { silent: !0 }),
      (i = this.deps['default'][t.str]) &&
        i.filter(Hs).forEach(function (t) {
          return t.shuffle(n, e);
        }),
      r !== e.length)
    ) {
      for (
        this.mark(t.join('length'), Py), s = n.touchedFrom;
        s < e.length;
        s += 1
      )
        this.mark(t.join(s));
      for (s = e.length; r > s; s += 1) this.mark(t.join(s), Ty);
    }
  }
  function Hs(t) {
    return 'function' == typeof t.shuffle;
  }
  function Ks() {
    var t,
      e = this;
    for (
      Object.keys(this.cache).forEach(function (t) {
        return e.clearCache(t);
      });
      (t = this.unresolvedImplicitDependencies.pop());

    )
      t.teardown();
  }
  function Gs(t, e) {
    var n,
      i,
      r,
      s = void 0 === arguments[2] ? 'default' : arguments[2];
    if (!e.isStatic) {
      if ((n = this.mappings[t.firstKey])) return n.unregister(t, e, s);
      if (((i = this.deps[s][t.str]), (r = i.indexOf(e)), -1 === r))
        throw new Error(
          'Attempted to remove a dependant that was no longer registered! This should not happen. If you are seeing this bug in development please raise an issue at https://github.com/RactiveJS/Ractive/issues - thanks'
        );
      (i.splice(r, 1), t.isRoot || Ys(this, t, s));
    }
  }
  function Ys(t, e, n) {
    for (var i, r; !e.isRoot; )
      ((i = t.depsMap[n]),
        (r = i[e.parent.str]),
        (r['_' + e.str] -= 1),
        r['_' + e.str] || (I(r, e), (r['_' + e.str] = void 0)),
        (e = e.parent));
  }
  function Js(t) {
    ((this.hook = new nu(t)), (this.inProcess = {}), (this.queue = {}));
  }
  function Xs(t, e) {
    return t[e._guid] || (t[e._guid] = []);
  }
  function to(t, e) {
    var n = Xs(t.queue, e);
    for (t.hook.fire(e); n.length; ) to(t, n.shift());
    delete t.queue[e._guid];
  }
  function eo(t, e) {
    var n,
      i = {};
    for (n in e) i[n] = no(t, n, e[n]);
    return i;
  }
  function no(t, e, n) {
    var i, r;
    return (
      'function' == typeof n && (i = ro(n, t)),
      'string' == typeof n && (i = io(t, n)),
      'object' == typeof n &&
        ('string' == typeof n.get
          ? (i = io(t, n.get))
          : 'function' == typeof n.get
            ? (i = ro(n.get, t))
            : l('`%s` computation must have a `get()` method', e),
        'function' == typeof n.set && (r = ro(n.set, t))),
      { getter: i, setter: r }
    );
  }
  function io(t, e) {
    var n, i, r;
    return (
      (n =
        'return (' +
        e.replace(Ly, function (t, e) {
          return ((i = !0), '__ractive.get("' + e + '")');
        }) +
        ');'),
      i && (n = 'var __ractive = this; ' + n),
      (r = new Function(n)),
      i ? r.bind(t) : r
    );
  }
  function ro(t, e) {
    return /this/.test(t.toString()) ? t.bind(e) : t;
  }
  function so(e) {
    var n,
      r,
      s = void 0 === arguments[1] ? {} : arguments[1],
      o = void 0 === arguments[2] ? {} : arguments[2];
    if (
      (Qb.DEBUG && Ca(),
      uo(e, o),
      xa(e, 'data', { get: ho }),
      Vy.fire(e, s),
      zy.forEach(function (t) {
        e[t] = i(wa(e.constructor[t] || null), s[t]);
      }),
      (r = new Ny({
        adapt: oo(e, e.adapt, s),
        data: Wh.init(e.constructor, e, s),
        computed: Iy(e, i(wa(e.constructor.prototype.computed), s.computed)),
        mappings: o.mappings,
        ractive: e,
        onchange: function () {
          return mu.addRactive(e);
        },
      })),
      (e.viewmodel = r),
      r.init(),
      bd.init(e.constructor, e, s),
      My.fire(e),
      Uy.begin(e),
      e.template)
    ) {
      var a = void 0;
      ((o.cssIds || e.cssId) &&
        ((a = o.cssIds ? o.cssIds.slice() : []), e.cssId && a.push(e.cssId)),
        (e.fragment = new yb({
          template: e.template,
          root: e,
          owner: e,
          cssIds: a,
        })));
    }
    if ((Uy.end(e), (n = t(e.el)))) {
      var u = e.render(n, e.append);
      Qb.DEBUG_PROMISES &&
        u['catch'](function (t) {
          throw (
            v(
              'Promise debugging is enabled, to help solve errors that happen asynchronously. Some browsers will log unhandled promise rejections, in which case you can safely disable promise debugging:\n  Ractive.DEBUG_PROMISES = false;'
            ),
            m('An error happened during rendering', { ractive: e }),
            t.stack && f(t.stack),
            t
          );
        });
    }
  }
  function oo(t, e, n) {
    function i(e) {
      return (
        'string' == typeof e &&
          ((e = g('adaptors', t, e)), e || l(Da(e, 'adaptor'))),
        e
      );
    }
    var r, s, o;
    if (
      ((e = e.map(i)),
      (r = N(n.adapt).map(i)),
      (r = ao(e, r)),
      (s = 'magic' in n ? n.magic : t.magic),
      (o = 'modifyArrays' in n ? n.modifyArrays : t.modifyArrays),
      s)
    ) {
      if (!na)
        throw new Error(
          'Getters and setters (magic mode) are not supported in this browser'
        );
      (o && r.push(ey), r.push(ty));
    }
    return (o && r.push(Kg), r);
  }
  function ao(t, e) {
    for (var n = t.slice(), i = e.length; i--; )
      ~n.indexOf(e[i]) || n.push(e[i]);
    return n;
  }
  function uo(t, e) {
    ((t._guid = 'r-' + Wy++),
      (t._subs = wa(null)),
      (t._config = {}),
      (t._twowayBindings = wa(null)),
      (t._animations = []),
      (t.nodes = {}),
      (t._liveQueries = []),
      (t._liveComponentQueries = []),
      (t._boundFunctions = []),
      (t._observers = []),
      e.component
        ? ((t.parent = e.parent),
          (t.container = e.container || null),
          (t.root = t.parent.root),
          (t.component = e.component),
          (e.component.instance = t),
          (t._inlinePartials = e.inlinePartials))
        : ((t.root = t), (t.parent = t.container = null)));
  }
  function ho() {
    throw new Error(
      'Using `ractive.data` is no longer supported - you must use the `ractive.get()` API instead'
    );
  }
  function co(t, e, n) {
    ((this.parentFragment = t.parentFragment),
      (this.callback = n),
      (this.fragment = new yb({ template: e, root: t.root, owner: this })),
      this.update());
  }
  function lo(t, e, n) {
    var i;
    return (
      e.r
        ? (i = Qd(t, e.r, n))
        : e.x
          ? (i = new Gd(t, t.parentFragment, e.x, n))
          : e.rx && (i = new tp(t, e.rx, n)),
      i
    );
  }
  function fo(t) {
    return 1 === t.length && t[0].t === Hh;
  }
  function po(t, e) {
    var n;
    for (n in e) e.hasOwnProperty(n) && mo(t.instance, t.root, n, e[n]);
  }
  function mo(t, e, n, i) {
    ('string' != typeof i &&
      l(
        'Components currently only support simple events - you cannot include arguments. Sorry!'
      ),
      t.on(n, function () {
        var t, n;
        return (
          arguments.length &&
            arguments[0] &&
            arguments[0].node &&
            (t = Array.prototype.shift.call(arguments)),
          (n = Array.prototype.slice.call(arguments)),
          Wu(e, i, { event: t, args: n }),
          !1
        );
      }));
  }
  function vo(t, e) {
    var n, i;
    if (!e) throw new Error('Component "' + this.name + '" not found');
    ((n = this.parentFragment = t.parentFragment),
      (i = n.root),
      (this.root = i),
      (this.type = sc),
      (this.name = t.template.e),
      (this.index = t.index),
      (this.indexRefBindings = {}),
      (this.yielders = {}),
      (this.resolvers = []),
      $y(this, e, t.template.a, t.template.f, t.template.p),
      Qy(this, t.template.v),
      (t.template.t0 || t.template.t1 || t.template.t2 || t.template.o) &&
        m(
          'The "intro", "outro" and "decorator" directives have no effect on components',
          { ractive: this.instance }
        ),
      Zy(this));
  }
  function go(t, e) {
    function n(n) {
      n.rebind(t, e);
    }
    var i;
    this.resolvers.forEach(n);
    for (var r in this.yielders) this.yielders[r][0] && n(this.yielders[r][0]);
    (i = this.root._liveComponentQueries['_' + this.name]) && i._makeDirty();
  }
  function yo() {
    var t = this.instance;
    return (
      t.render(this.parentFragment.getNode()),
      (this.rendered = !0),
      t.fragment.detach()
    );
  }
  function bo() {
    return this.instance.fragment.toString();
  }
  function wo() {
    var t = this.instance;
    (this.resolvers.forEach(Z),
      xo(this),
      t._observers.forEach(K),
      t.fragment.unbind(),
      t.viewmodel.teardown(),
      t.fragment.rendered &&
        t.el.__ractive_instances__ &&
        I(t.el.__ractive_instances__, t),
      Xy.fire(t));
  }
  function xo(t) {
    var e, n;
    e = t.root;
    do (n = e._liveComponentQueries['_' + t.name]) && n._remove(t);
    while ((e = e.parent));
  }
  function ko(t) {
    ((this.shouldDestroy = t), this.instance.unrender());
  }
  function Eo(t) {
    var e = this;
    ((this.owner = t.owner),
      (this.parent = this.owner.parentFragment),
      (this.root = t.root),
      (this.pElement = t.pElement),
      (this.context = t.context),
      (this.index = t.index),
      (this.key = t.key),
      (this.registeredIndexRefs = []),
      (this.cssIds =
        'cssIds' in t ? t.cssIds : this.parent ? this.parent.cssIds : null),
      (this.items = t.template.map(function (n, i) {
        return _o({
          parentFragment: e,
          pElement: t.pElement,
          template: n,
          index: i,
        });
      })),
      (this.value = this.argsList = null),
      (this.dirtyArgs = this.dirtyValue = !0),
      (this.bound = !0));
  }
  function _o(t) {
    if ('string' == typeof t.template) return new Nd(t);
    switch (t.template.t) {
      case oc:
        return new ob(t);
      case Hh:
        return new op(t);
      case Gh:
        return new Sp(t);
      case Kh:
        return new qp(t);
      case Xh:
        var e = void 0;
        return (e = Fg(t.parentFragment.root, t.template.e))
          ? new nb(t, e)
          : new bg(t);
      case tc:
        return new Tg(t);
      case ec:
        return new rb(t);
      case uc:
        return new ub(t);
      default:
        throw new Error(
          'Something very strange happened. Please file an issue at https://github.com/ractivejs/ractive/issues. Thanks!'
        );
    }
  }
  function Ao(t, e) {
    ((!this.owner || this.owner.hasContext) && k(this, 'context', t, e),
      this.items.forEach(function (n) {
        n.rebind && n.rebind(t, e);
      }));
  }
  function So() {
    var t;
    return (
      1 === this.items.length
        ? (t = this.items[0].render())
        : ((t = document.createDocumentFragment()),
          this.items.forEach(function (e) {
            t.appendChild(e.render());
          })),
      (this.rendered = !0),
      t
    );
  }
  function Co(t) {
    return this.items ? this.items.map(t ? Po : Oo).join('') : '';
  }
  function Oo(t) {
    return t.toString();
  }
  function Po(t) {
    return t.toString(!0);
  }
  function To() {
    this.bound && (this.items.forEach(Fo), (this.bound = !1));
  }
  function Fo(t) {
    t.unbind && t.unbind();
  }
  function Ro(t) {
    if (!this.rendered)
      throw new Error('Attempted to unrender a fragment that was not rendered');
    (this.items.forEach(function (e) {
      return e.unrender(t);
    }),
      (this.rendered = !1));
  }
  function jo(t) {
    var e, n, i, r, s;
    if (((t = t || {}), 'object' != typeof t))
      throw new Error(
        'The reset method takes either no arguments, or an object containing new data'
      );
    for (
      (n = this.viewmodel.wrapped['']) && n.reset
        ? n.reset(t) === !1 && this.viewmodel.reset(t)
        : this.viewmodel.reset(t),
        i = bd.reset(this),
        r = i.length;
      r--;

    )
      if (wb.indexOf(i[r]) > -1) {
        s = !0;
        break;
      }
    if (s) {
      var o = void 0;
      (this.viewmodel.mark(Za),
        (o = this.component) && (o.shouldDestroy = !0),
        this.unrender(),
        o && (o.shouldDestroy = !1),
        this.fragment.template !== this.template &&
          (this.fragment.unbind(),
          (this.fragment = new yb({
            template: this.template,
            root: this,
            owner: this,
          }))),
        (e = this.render(this.el, this.anchor)));
    } else ((e = mu.start(this, !0)), this.viewmodel.mark(Za), mu.end());
    return (xb.fire(this, t), e);
  }
  function No(t) {
    var e, n;
    (hd.init(null, this, { template: t }),
      (e = this.transitionsEnabled),
      (this.transitionsEnabled = !1),
      (n = this.component) && (n.shouldDestroy = !0),
      this.unrender(),
      n && (n.shouldDestroy = !1),
      this.fragment.unbind(),
      (this.fragment = new yb({
        template: this.template,
        root: this,
        owner: this,
      })),
      this.render(this.el, this.anchor),
      (this.transitionsEnabled = e));
  }
  function Do(t, e) {
    var n, i;
    if (((i = mu.start(this, !0)), h(t))) {
      n = t;
      for (t in n) n.hasOwnProperty(t) && ((e = n[t]), Io(this, t, e));
    } else Io(this, t, e);
    return (mu.end(), i);
  }
  function Io(t, e, n) {
    ((e = _(C(e))),
      e.isPattern
        ? A(t, e).forEach(function (e) {
            t.viewmodel.set(e, n);
          })
        : t.viewmodel.set(e, n));
  }
  function Lo(t, e) {
    return Ha(this, t, void 0 === e ? -1 : -e);
  }
  function Vo() {
    var t;
    return (
      this.fragment.unbind(),
      this.viewmodel.teardown(),
      this._observers.forEach(K),
      this.fragment.rendered &&
        this.el.__ractive_instances__ &&
        I(this.el.__ractive_instances__, this),
      (this.shouldDestroy = !0),
      (t = this.fragment.rendered ? this.unrender() : ou.resolve()),
      Fb.fire(this),
      this._boundFunctions.forEach(Mo),
      t
    );
  }
  function Mo(t) {
    delete t.fn[t.prop];
  }
  function Uo(t) {
    var e = this;
    if ('string' != typeof t) throw new TypeError(ja);
    var n = void 0;
    return /\*/.test(t)
      ? ((n = {}),
        A(this, _(C(t))).forEach(function (t) {
          n[t.str] = !e.viewmodel.get(t);
        }),
        this.set(n))
      : this.set(t, !this.get(t));
  }
  function Wo() {
    return this.fragment.toString(!0);
  }
  function zo() {
    var t, e;
    if (!this.fragment.rendered)
      return (
        m(
          'ractive.unrender() was called on a Ractive instance that was not rendered'
        ),
        ou.resolve()
      );
    for (
      t = mu.start(this, !0),
        e =
          !this.component || this.component.shouldDestroy || this.shouldDestroy;
      this._animations[0];

    )
      this._animations[0].stop();
    return (
      this.fragment.unrender(e),
      I(this.el.__ractive_instances__, this),
      Db.fire(this),
      mu.end(),
      t
    );
  }
  function Bo(t) {
    var e;
    return (
      (t = _(t) || Za),
      (e = mu.start(this, !0)),
      this.viewmodel.mark(t),
      mu.end(),
      Vb.fire(this, t),
      e
    );
  }
  function qo(t, e) {
    var n, i, r;
    if ('string' != typeof t || e) {
      r = [];
      for (i in this._twowayBindings)
        (!t || _(i).equalsOrStartsWith(t)) &&
          r.push.apply(r, this._twowayBindings[i]);
    } else r = this._twowayBindings[t];
    return ((n = $o(this, r)), this.set(n));
  }
  function $o(t, e) {
    var n = {},
      i = [];
    return (
      e.forEach(function (t) {
        var e, r;
        if (!t.radioName || t.element.node.checked) {
          if (t.checkboxName)
            return void (
              i[t.keypath.str] ||
              t.changed() ||
              (i.push(t.keypath), (i[t.keypath.str] = t))
            );
          ((e = t.attribute.value),
            (r = t.getValue()),
            j(e, r) || a(e, r) || (n[t.keypath.str] = r));
        }
      }),
      i.length &&
        i.forEach(function (t) {
          var e, r, s;
          ((e = i[t.str]),
            (r = e.attribute.value),
            (s = e.getValue()),
            j(r, s) || (n[t.str] = s));
        }),
      n
    );
  }
  function Qo(t, e) {
    return 'function' == typeof e && /_super/.test(t);
  }
  function Zo(t) {
    for (var e = {}; t; )
      (Ho(t, e), Go(t, e), (t = t._Parent !== Qb ? t._Parent : !1));
    return e;
  }
  function Ho(t, e) {
    vd.forEach(function (n) {
      Ko(n.useDefaults ? t.prototype : t, e, n.name);
    });
  }
  function Ko(t, e, n) {
    var i,
      r = Object.keys(t[n]);
    r.length &&
      ((i = e[n]) || (i = e[n] = {}),
      r
        .filter(function (t) {
          return !(t in i);
        })
        .forEach(function (e) {
          return (i[e] = t[n][e]);
        }));
  }
  function Go(t, e) {
    Object.keys(t.prototype).forEach(function (n) {
      if ('computed' !== n) {
        var i = t.prototype[n];
        if (n in e) {
          if (
            'function' == typeof e[n] &&
            'function' == typeof i &&
            e[n]._method
          ) {
            var r = void 0,
              s = i._method;
            (s && (i = i._method),
              (r = Wb(e[n]._method, i)),
              s && (r._method = r),
              (e[n] = r));
          }
        } else e[n] = i._method ? i._method : i;
      }
    });
  }
  function Yo() {
    for (var t = arguments.length, e = Array(t), n = 0; t > n; n++)
      e[n] = arguments[n];
    return e.length ? e.reduce(Jo, this) : Jo(this);
  }
  function Jo(t) {
    var e,
      n,
      r = void 0 === arguments[1] ? {} : arguments[1];
    return (
      r.prototype instanceof Qb && (r = zb(r)),
      (e = function (t) {
        return this instanceof e ? void By(this, t) : new e(t);
      }),
      (n = wa(t.prototype)),
      (n.constructor = e),
      ka(e, {
        defaults: { value: n },
        extend: { value: Yo, writable: !0, configurable: !0 },
        _Parent: { value: t },
      }),
      bd.extend(t, n, r),
      Wh.extend(t, n, r),
      r.computed && (n.computed = i(wa(t.prototype.computed), r.computed)),
      (e.prototype = n),
      e
    );
  }
  var Xo,
    ta,
    ea,
    na,
    ia,
    ra,
    sa,
    oa = 3,
    aa = {
      el: void 0,
      append: !1,
      template: { v: oa, t: [] },
      preserveWhitespace: !1,
      sanitize: !1,
      stripComments: !0,
      delimiters: ['{{', '}}'],
      tripleDelimiters: ['{{{', '}}}'],
      interpolate: !1,
      data: {},
      computed: {},
      magic: !1,
      modifyArrays: !0,
      adapt: [],
      isolated: !1,
      twoway: !0,
      lazy: !1,
      noIntro: !1,
      transitionsEnabled: !0,
      complete: void 0,
      css: null,
      noCssTransform: !1,
    },
    ua = aa,
    ha = {
      linear: function (t) {
        return t;
      },
      easeIn: function (t) {
        return Math.pow(t, 3);
      },
      easeOut: function (t) {
        return Math.pow(t - 1, 3) + 1;
      },
      easeInOut: function (t) {
        return (t /= 0.5) < 1
          ? 0.5 * Math.pow(t, 3)
          : 0.5 * (Math.pow(t - 2, 3) + 2);
      },
    };
  ((Xo = 'object' == typeof document),
    (ta = 'undefined' != typeof navigator && /jsDom/.test(navigator.appName)),
    (ea =
      'undefined' != typeof console &&
      'function' == typeof console.warn &&
      'function' == typeof console.warn.apply));
  try {
    (Object.defineProperty({}, 'test', { value: 0 }), (na = !0));
  } catch (ca) {
    na = !1;
  }
  ((ia = {
    html: 'http://www.w3.org/1999/xhtml',
    mathml: 'http://www.w3.org/1998/Math/MathML',
    svg: 'http://www.w3.org/2000/svg',
    xlink: 'http://www.w3.org/1999/xlink',
    xml: 'http://www.w3.org/XML/1998/namespace',
    xmlns: 'http://www.w3.org/2000/xmlns/',
  }),
    (ra =
      'undefined' == typeof document
        ? !1
        : document &&
          document.implementation.hasFeature(
            'http://www.w3.org/TR/SVG11/feature#BasicStructure',
            '1.1'
          )),
    (sa = ['o', 'ms', 'moz', 'webkit']));
  var la, fa, da, pa, ma, va, ga, ya, ba;
  if (
    ((la = ra
      ? function (t, e) {
          return e && e !== ia.html
            ? document.createElementNS(e, t)
            : document.createElement(t);
        }
      : function (t, e) {
          if (e && e !== ia.html)
            throw "This browser does not support namespaces other than http://www.w3.org/1999/xhtml. The most likely cause of this error is that you're trying to render SVG in an older browser. See http://docs.ractivejs.org/latest/svg-and-older-browsers for more information";
          return document.createElement(t);
        }),
    Xo)
  ) {
    for (
      da = la('div'),
        pa = ['matches', 'matchesSelector'],
        ba = function (t) {
          return function (e, n) {
            return e[t](n);
          };
        },
        ga = pa.length;
      ga-- && !fa;

    )
      if (((ma = pa[ga]), da[ma])) fa = ba(ma);
      else
        for (ya = sa.length; ya--; )
          if (
            ((va = sa[ga] + ma.substr(0, 1).toUpperCase() + ma.substring(1)),
            da[va])
          ) {
            fa = ba(va);
            break;
          }
    fa ||
      (fa = function (t, e) {
        var n, i, r;
        for (
          i = t.parentNode,
            i ||
              ((da.innerHTML = ''),
              (i = da),
              (t = t.cloneNode()),
              da.appendChild(t)),
            n = i.querySelectorAll(e),
            r = n.length;
          r--;

        )
          if (n[r] === t) return !0;
        return !1;
      });
  } else fa = null;
  var wa,
    xa,
    ka,
    Ea = null;
  try {
    (Object.defineProperty({}, 'test', { value: 0 }),
      Xo &&
        Object.defineProperty(document.createElement('div'), 'test', {
          value: 0,
        }),
      (xa = Object.defineProperty));
  } catch (_a) {
    xa = function (t, e, n) {
      t[e] = n.value;
    };
  }
  try {
    try {
      Object.defineProperties({}, { test: { value: 0 } });
    } catch (_a) {
      throw _a;
    }
    (Xo && Object.defineProperties(la('div'), { test: { value: 0 } }),
      (ka = Object.defineProperties));
  } catch (_a) {
    ka = function (t, e) {
      var n;
      for (n in e) e.hasOwnProperty(n) && xa(t, n, e[n]);
    };
  }
  try {
    (Object.create(null), (wa = Object.create));
  } catch (_a) {
    wa = (function () {
      var t = function () {};
      return function (e, n) {
        var i;
        return null === e
          ? {}
          : ((t.prototype = e),
            (i = new t()),
            n && Object.defineProperties(i, n),
            i);
      };
    })();
  }
  var Aa,
    Sa,
    Ca,
    Oa = Object.prototype.hasOwnProperty,
    Pa = Object.prototype.toString,
    Ta = /^\[object (?:Array|FileList)\]$/,
    Fa = function () {},
    Ra = {};
  ea
    ? !(function () {
        var t = [
            '%cRactive.js %c0.7.3 %cin debug mode, %cmore...',
            'color: rgb(114, 157, 52); font-weight: normal;',
            'color: rgb(85, 85, 85); font-weight: normal;',
            'color: rgb(85, 85, 85); font-weight: normal;',
            'color: rgb(82, 140, 224); font-weight: normal; text-decoration: underline;',
          ],
          e =
            "You're running Ractive 0.7.3 in debug mode - messages will be printed to the console to help you fix problems and optimise your application.\n\nTo disable debug mode, add this line at the start of your app:\n  Ractive.DEBUG = false;\n\nTo disable debug mode when your app is minified, add this snippet:\n  Ractive.DEBUG = /unminified/.test(function(){/*unminified*/});\n\nGet help and support:\n  http://docs.ractivejs.org\n  http://stackoverflow.com/questions/tagged/ractivejs\n  http://groups.google.com/forum/#!forum/ractive-js\n  http://twitter.com/ractivejs\n\nFound a bug? Raise an issue:\n  https://github.com/ractivejs/ractive/issues\n\n";
        ((Ca = function () {
          var n = !!console.groupCollapsed;
          (console[n ? 'groupCollapsed' : 'log'].apply(console, t),
            console.log(e),
            n && console.groupEnd(t),
            (Ca = Fa));
        }),
          (Sa = function (t, e) {
            if ((Ca(), 'object' == typeof e[e.length - 1])) {
              var n = e.pop(),
                i = n ? n.ractive : null;
              if (i) {
                var r = void 0;
                i.component &&
                  (r = i.component.name) &&
                  (t = '<' + r + '> ' + t);
                var s = void 0;
                (s =
                  n.node ||
                  (i.fragment && i.fragment.rendered && i.find('*'))) &&
                  e.push(s);
              }
            }
            console.warn.apply(
              console,
              [
                '%cRactive.js: %c' + t,
                'color: rgb(114, 157, 52);',
                'color: rgb(85, 85, 85);',
              ].concat(e)
            );
          }),
          (Aa = function () {
            console.log.apply(console, arguments);
          }));
      })()
    : (Sa = Aa = Ca = Fa);
  var ja = 'Bad arguments',
    Na = 'A function was specified for "%s" %s, but no %s was returned',
    Da = function (t, e) {
      return (
        'Missing "' +
        t +
        '" ' +
        e +
        ' plugin. You may need to download a plugin via http://docs.ractivejs.org/latest/plugins#' +
        e +
        's'
      );
    },
    Ia = function (t, e, n, i) {
      if (t === e) return b(e);
      if (i) {
        var r = g('interpolators', n, i);
        if (r) return r(t, e) || b(e);
        l(Da(i, 'interpolator'));
      }
      return Ma.number(t, e) || Ma.array(t, e) || Ma.object(t, e) || b(e);
    },
    La = Ia,
    Va = {
      number: function (t, e) {
        var n;
        return u(t) && u(e)
          ? ((t = +t),
            (e = +e),
            (n = e - t),
            n
              ? function (e) {
                  return t + e * n;
                }
              : function () {
                  return t;
                })
          : null;
      },
      array: function (t, e) {
        var n, i, r, o;
        if (!s(t) || !s(e)) return null;
        for (n = [], i = [], o = r = Math.min(t.length, e.length); o--; )
          i[o] = La(t[o], e[o]);
        for (o = r; o < t.length; o += 1) n[o] = t[o];
        for (o = r; o < e.length; o += 1) n[o] = e[o];
        return function (t) {
          for (var e = r; e--; ) n[e] = i[e](t);
          return n;
        };
      },
      object: function (t, e) {
        var n, i, r, s, o;
        if (!h(t) || !h(e)) return null;
        ((n = []), (s = {}), (r = {}));
        for (o in t)
          Oa.call(t, o) &&
            (Oa.call(e, o)
              ? (n.push(o), (r[o] = La(t[o], e[o])))
              : (s[o] = t[o]));
        for (o in e) Oa.call(e, o) && !Oa.call(t, o) && (s[o] = e[o]);
        return (
          (i = n.length),
          function (t) {
            for (var e, o = i; o--; ) ((e = n[o]), (s[e] = r[e](t)));
            return s;
          }
        );
      },
    },
    Ma = Va,
    Ua = w,
    Wa = {},
    za = /\[\s*(\*|[0-9]|[1-9][0-9]+)\s*\]/g,
    Ba = /\*/,
    qa = {},
    $a = function (t) {
      var e = t.split('.');
      ((this.str = t),
        '@' === t[0] && ((this.isSpecial = !0), (this.value = E(t))),
        (this.firstKey = e[0]),
        (this.lastKey = e.pop()),
        (this.isPattern = Ba.test(t)),
        (this.parent = '' === t ? null : _(e.join('.'))),
        (this.isRoot = !t));
    };
  $a.prototype = {
    equalsOrStartsWith: function (t) {
      return t === this || this.startsWith(t);
    },
    join: function (t) {
      return _(this.isRoot ? String(t) : this.str + '.' + t);
    },
    replace: function (t, e) {
      return this === t
        ? e
        : this.startsWith(t)
          ? null === e
            ? e
            : _(this.str.replace(t.str + '.', e.str + '.'))
          : void 0;
    },
    startsWith: function (t) {
      return t ? t && this.str.substr(0, t.str.length + 1) === t.str + '.' : !1;
    },
    toString: function () {
      throw new Error('Bad coercion');
    },
    valueOf: function () {
      throw new Error('Bad coercion');
    },
    wildcardMatches: function () {
      return this._wildcardMatches || (this._wildcardMatches = Ua(this.str));
    },
  };
  var Qa,
    Za = _(''),
    Ha = O,
    Ka = 'Cannot add to a non-numeric value',
    Ga = P;
  'undefined' == typeof window
    ? (Qa = null)
    : (!(function (t, e, n) {
        var i, r;
        if (!n.requestAnimationFrame) {
          for (i = 0; i < t.length && !n.requestAnimationFrame; ++i)
            n.requestAnimationFrame = n[t[i] + 'RequestAnimationFrame'];
          n.requestAnimationFrame ||
            ((r = n.setTimeout),
            (n.requestAnimationFrame = function (t) {
              var n, i, s;
              return (
                (n = Date.now()),
                (i = Math.max(0, 16 - (n - e))),
                (s = r(function () {
                  t(n + i);
                }, i)),
                (e = n + i),
                s
              );
            }));
        }
      })(sa, 0, window),
      (Qa = window.requestAnimationFrame));
  var Ya,
    Ja = Qa;
  Ya =
    'undefined' != typeof window &&
    window.performance &&
    'function' == typeof window.performance.now
      ? function () {
          return window.performance.now();
        }
      : function () {
          return Date.now();
        };
  var Xa = Ya,
    tu = {
      construct: { deprecated: 'beforeInit', replacement: 'onconstruct' },
      render: {
        deprecated: 'init',
        message:
          'The "init" method has been deprecated and will likely be removed in a future release. You can either use the "oninit" method which will fire only once prior to, and regardless of, any eventual ractive instance being rendered, or if you need to access the rendered DOM, use "onrender" instead. See http://docs.ractivejs.org/latest/migrating for more information.',
      },
      complete: { deprecated: 'complete', replacement: 'oncomplete' },
    };
  T.prototype.fire = function (t, e) {
    function n(n) {
      return t[n] ? (e ? t[n](e) : t[n](), !0) : void 0;
    }
    (n(this.method),
      !t[this.method] &&
        this.deprecate &&
        n(this.deprecate.deprecated) &&
        (this.deprecate.message
          ? m(this.deprecate.message)
          : m(
              'The method "%s" has been deprecated in favor of "%s" and will likely be removed in a future release. See http://docs.ractivejs.org/latest/migrating for more information.',
              this.deprecate.deprecated,
              this.deprecate.replacement
            )),
      e ? t.fire(this.event, e) : t.fire(this.event));
  };
  var eu,
    nu = T,
    iu = {},
    ru = {},
    su = {};
  'function' == typeof Promise
    ? (eu = Promise)
    : ((eu = function (t) {
        var e,
          n,
          i,
          r,
          s,
          o,
          a = [],
          u = [],
          h = iu;
        ((i = function (t) {
          return function (i) {
            h === iu && ((e = i), (h = t), (n = M(h === ru ? a : u, e)), V(n));
          };
        }),
          (r = i(ru)),
          (s = i(su)));
        try {
          t(r, s);
        } catch (c) {
          s(c);
        }
        return (
          (o = {
            then: function (t, e) {
              var i = new eu(function (r, s) {
                var o = function (t, e, n) {
                  e.push(
                    'function' == typeof t
                      ? function (e) {
                          var n;
                          try {
                            ((n = t(e)), U(i, n, r, s));
                          } catch (o) {
                            s(o);
                          }
                        }
                      : n
                  );
                };
                (o(t, a, r), o(e, u, s), h !== iu && V(n));
              });
              return i;
            },
          }),
          (o['catch'] = function (t) {
            return this.then(null, t);
          }),
          o
        );
      }),
      (eu.all = function (t) {
        return new eu(function (e, n) {
          var i,
            r,
            s,
            o = [];
          if (!t.length) return void e(o);
          for (
            s = function (t, r) {
              t && 'function' == typeof t.then
                ? t.then(function (t) {
                    ((o[r] = t), --i || e(o));
                  }, n)
                : ((o[r] = t), --i || e(o));
            },
              i = r = t.length;
            r--;

          )
            s(t[r], r);
        });
      }),
      (eu.resolve = function (t) {
        return new eu(function (e) {
          e(t);
        });
      }),
      (eu.reject = function (t) {
        return new eu(function (e, n) {
          n(t);
        });
      }));
  var ou = eu,
    au = function (t) {
      do if (void 0 !== t.context) return t.context;
      while ((t = t.parent));
      return Za;
    },
    uu = W,
    hu = function (t, e) {
      ((this.callback = t),
        (this.parent = e),
        (this.intros = []),
        (this.outros = []),
        (this.children = []),
        (this.totalChildren = this.outroChildren = 0),
        (this.detachQueue = []),
        (this.decoratorQueue = []),
        (this.outrosComplete = !1),
        e && e.addChild(this));
    };
  hu.prototype = {
    addChild: function (t) {
      (this.children.push(t),
        (this.totalChildren += 1),
        (this.outroChildren += 1));
    },
    decrementOutros: function () {
      ((this.outroChildren -= 1), J(this));
    },
    decrementTotal: function () {
      ((this.totalChildren -= 1), J(this));
    },
    add: function (t) {
      var e = t.isIntro ? this.intros : this.outros;
      e.push(t);
    },
    addDecorator: function (t) {
      this.decoratorQueue.push(t);
    },
    remove: function (t) {
      var e = t.isIntro ? this.intros : this.outros;
      (I(e, t), J(this));
    },
    init: function () {
      ((this.ready = !0), J(this));
    },
    detachNodes: function () {
      (this.decoratorQueue.forEach(Q),
        this.detachQueue.forEach(G),
        this.children.forEach(Y));
    },
  };
  var cu,
    lu,
    fu = hu,
    du = [],
    pu = new nu('change');
  lu = {
    start: function (t, e) {
      var n, i;
      return (
        e &&
          (n = new ou(function (t) {
            return (i = t);
          })),
        (cu = {
          previousBatch: cu,
          transitionManager: new fu(i, cu && cu.transitionManager),
          views: [],
          tasks: [],
          ractives: [],
          instance: t,
        }),
        t && cu.ractives.push(t),
        n
      );
    },
    end: function () {
      (X(),
        cu.transitionManager.init(),
        !cu.previousBatch &&
          cu.instance &&
          (cu.instance.viewmodel.changes = []),
        (cu = cu.previousBatch));
    },
    addRactive: function (t) {
      cu && F(cu.ractives, t);
    },
    registerTransition: function (t) {
      ((t._manager = cu.transitionManager), cu.transitionManager.add(t));
    },
    registerDecorator: function (t) {
      cu.transitionManager.addDecorator(t);
    },
    addView: function (t) {
      cu.views.push(t);
    },
    addUnresolved: function (t) {
      du.push(t);
    },
    removeUnresolved: function (t) {
      I(du, t);
    },
    detachWhenReady: function (t) {
      cu.transitionManager.detachQueue.push(t);
    },
    scheduleTask: function (t, e) {
      var n;
      if (cu) {
        for (n = cu; e && n.previousBatch; ) n = n.previousBatch;
        n.tasks.push(t);
      } else t();
    },
  };
  var mu = lu,
    vu = [],
    gu = {
      tick: function () {
        var t, e, n;
        for (n = Xa(), mu.start(), t = 0; t < vu.length; t += 1)
          ((e = vu[t]), e.tick(n) || vu.splice(t--, 1));
        (mu.end(), vu.length ? Ja(gu.tick) : (gu.running = !1));
      },
      add: function (t) {
        (vu.push(t), gu.running || ((gu.running = !0), Ja(gu.tick)));
      },
      abort: function (t, e) {
        for (var n, i = vu.length; i--; )
          ((n = vu[i]), n.root === e && n.keypath === t && n.stop());
      },
    },
    yu = gu,
    bu = function (t) {
      var e;
      this.startTime = Date.now();
      for (e in t) t.hasOwnProperty(e) && (this[e] = t[e]);
      ((this.interpolator = La(
        this.from,
        this.to,
        this.root,
        this.interpolator
      )),
        (this.running = !0),
        this.tick());
    };
  bu.prototype = {
    tick: function () {
      var t, e, n, i, r, s;
      return (
        (s = this.keypath),
        this.running
          ? ((i = Date.now()),
            (t = i - this.startTime),
            t >= this.duration
              ? (null !== s &&
                  (mu.start(this.root),
                  this.root.viewmodel.set(s, this.to),
                  mu.end()),
                this.step && this.step(1, this.to),
                this.complete(this.to),
                (r = this.root._animations.indexOf(this)),
                -1 === r && m('Animation was not found'),
                this.root._animations.splice(r, 1),
                (this.running = !1),
                !1)
              : ((e = this.easing
                  ? this.easing(t / this.duration)
                  : t / this.duration),
                null !== s &&
                  ((n = this.interpolator(e)),
                  mu.start(this.root),
                  this.root.viewmodel.set(s, n),
                  mu.end()),
                this.step && this.step(e, n),
                !0))
          : !1
      );
    },
    stop: function () {
      var t;
      ((this.running = !1),
        (t = this.root._animations.indexOf(this)),
        -1 === t && m('Animation was not found'),
        this.root._animations.splice(t, 1));
    },
  };
  var wu = bu,
    xu = nt,
    ku = { stop: Fa },
    Eu = rt,
    _u = new nu('detach'),
    Au = st,
    Su = ot,
    Cu = function () {
      var t, e, n;
      ((t =
        this._root[
          this._isComponentQuery ? 'liveComponentQueries' : 'liveQueries'
        ]),
        (e = this.selector),
        (n = t.indexOf(e)),
        -1 !== n && (t.splice(n, 1), (t[e] = null)));
    },
    Ou = function (t, e) {
      var n, i, r, s, o, a, u, h, c, l;
      for (
        n = ut(t.component || t._ractive.proxy),
          i = ut(e.component || e._ractive.proxy),
          r = D(n),
          s = D(i);
        r && r === s;

      )
        (n.pop(), i.pop(), (o = r), (r = D(n)), (s = D(i)));
      if (
        ((r = r.component || r),
        (s = s.component || s),
        (c = r.parentFragment),
        (l = s.parentFragment),
        c === l)
      )
        return (
          (a = c.items.indexOf(r)),
          (u = l.items.indexOf(s)),
          a - u || n.length - i.length
        );
      if ((h = o.fragments))
        return (
          (a = h.indexOf(c)),
          (u = h.indexOf(l)),
          a - u || n.length - i.length
        );
      throw new Error(
        'An unexpected condition was met while comparing the position of two components. Please file an issue at https://github.com/RactiveJS/Ractive/issues - thanks!'
      );
    },
    Pu = function (t, e) {
      var n;
      return t.compareDocumentPosition
        ? ((n = t.compareDocumentPosition(e)), 2 & n ? 1 : -1)
        : Ou(t, e);
    },
    Tu = function () {
      (this.sort(this._isComponentQuery ? Ou : Pu), (this._dirty = !1));
    },
    Fu = function () {
      var t = this;
      this._dirty ||
        ((this._dirty = !0),
        mu.scheduleTask(function () {
          t._sort();
        }));
    },
    Ru = function (t) {
      var e = this.indexOf(this._isComponentQuery ? t.instance : t);
      -1 !== e && this.splice(e, 1);
    },
    ju = ht,
    Nu = ct,
    Du = lt,
    Iu = ft,
    Lu = dt,
    Vu = pt,
    Mu = {
      enqueue: function (t, e) {
        (t.event &&
          ((t._eventQueue = t._eventQueue || []), t._eventQueue.push(t.event)),
          (t.event = e));
      },
      dequeue: function (t) {
        t._eventQueue && t._eventQueue.length
          ? (t.event = t._eventQueue.pop())
          : delete t.event;
      },
    },
    Uu = Mu,
    Wu = mt,
    zu = yt,
    Bu = bt,
    qu = { capture: !0, noUnwrap: !0, fullRootGet: !0 },
    $u = wt,
    Qu = new nu('insert'),
    Zu = kt,
    Hu = function (t, e, n, i) {
      ((this.root = t),
        (this.keypath = e),
        (this.callback = n),
        (this.defer = i.defer),
        (this.context = i && i.context ? i.context : t));
    };
  Hu.prototype = {
    init: function (t) {
      ((this.value = this.root.get(this.keypath.str)),
        t !== !1 ? this.update() : (this.oldValue = this.value));
    },
    setValue: function (t) {
      var e = this;
      a(t, this.value) ||
        ((this.value = t),
        this.defer && this.ready
          ? mu.scheduleTask(function () {
              return e.update();
            })
          : this.update());
    },
    update: function () {
      this.updating ||
        ((this.updating = !0),
        this.callback.call(
          this.context,
          this.value,
          this.oldValue,
          this.keypath.str
        ),
        (this.oldValue = this.value),
        (this.updating = !1));
    },
  };
  var Ku,
    Gu = Hu,
    Yu = Et,
    Ju = Array.prototype.slice;
  ((Ku = function (t, e, n, i) {
    ((this.root = t),
      (this.callback = n),
      (this.defer = i.defer),
      (this.keypath = e),
      (this.regex = new RegExp(
        '^' + e.str.replace(/\./g, '\\.').replace(/\*/g, '([^\\.]+)') + '$'
      )),
      (this.values = {}),
      this.defer && (this.proxies = []),
      (this.context = i && i.context ? i.context : t));
  }),
    (Ku.prototype = {
      init: function (t) {
        var e, n;
        if (((e = Yu(this.root, this.keypath)), t !== !1))
          for (n in e) e.hasOwnProperty(n) && this.update(_(n));
        else this.values = e;
      },
      update: function (t) {
        var e,
          n = this;
        if (t.isPattern) {
          e = Yu(this.root, t);
          for (t in e) e.hasOwnProperty(t) && this.update(_(t));
        } else if (!this.root.viewmodel.implicitChanges[t.str])
          return this.defer && this.ready
            ? void mu.scheduleTask(function () {
                return n.getProxy(t).update();
              })
            : void this.reallyUpdate(t);
      },
      reallyUpdate: function (t) {
        var e, n, i, r;
        return (
          (e = t.str),
          (n = this.root.viewmodel.get(t)),
          this.updating
            ? void (this.values[e] = n)
            : ((this.updating = !0),
              (a(n, this.values[e]) && this.ready) ||
                ((i = Ju.call(this.regex.exec(e), 1)),
                (r = [n, this.values[e], e].concat(i)),
                (this.values[e] = n),
                this.callback.apply(this.context, r)),
              void (this.updating = !1))
        );
      },
      getProxy: function (t) {
        var e = this;
        return (
          this.proxies[t.str] ||
            (this.proxies[t.str] = {
              update: function () {
                return e.reallyUpdate(t);
              },
            }),
          this.proxies[t.str]
        );
      },
    }));
  var Xu,
    th,
    eh,
    nh,
    ih,
    rh,
    sh = Ku,
    oh = _t,
    ah = {},
    uh = At,
    hh = St,
    ch = function (t) {
      return t.trim();
    },
    lh = function (t) {
      return '' !== t;
    },
    fh = Ct,
    dh = Ot,
    ph = Pt,
    mh = Tt,
    vh = Array.prototype,
    gh = function (t) {
      return function (e) {
        for (
          var n = arguments.length, i = Array(n > 1 ? n - 1 : 0), r = 1;
          n > r;
          r++
        )
          i[r - 1] = arguments[r];
        var o,
          a,
          u,
          h,
          c = [];
        if (((e = _(C(e))), (o = this.viewmodel.get(e)), (a = o.length), !s(o)))
          throw new Error(
            'Called ractive.' +
              t +
              "('" +
              e.str +
              "'), but '" +
              e.str +
              "' does not refer to an array"
          );
        return (
          (c = mh(o, t, i)),
          (h = vh[t].apply(o, i)),
          (u = mu.start(this, !0).then(function () {
            return h;
          })),
          c ? this.viewmodel.smartUpdate(e, o, c) : this.viewmodel.mark(e),
          mu.end(),
          u
        );
      };
    },
    yh = gh('pop'),
    bh = gh('push'),
    wh = '/* Ractive.js component styles */\n',
    xh = [],
    kh = !1;
  Xo
    ? ((eh = document.createElement('style')),
      (eh.type = 'text/css'),
      (nh = document.getElementsByTagName('head')[0]),
      (rh = !1),
      (ih = eh.styleSheet),
      (th = function () {
        var t =
          wh +
          xh
            .map(function (t) {
              return '\n/* {' + t.id + '} */\n' + t.styles;
            })
            .join('\n');
        (ih ? (ih.cssText = t) : (eh.innerHTML = t),
          rh || (nh.appendChild(eh), (rh = !0)));
      }),
      (Xu = {
        add: function (t) {
          (xh.push(t), (kh = !0));
        },
        apply: function () {
          kh && (th(), (kh = !1));
        },
      }))
    : (Xu = { add: Fa, apply: Fa });
  var Eh,
    _h,
    Ah = Xu,
    Sh = Rt,
    Ch = new nu('render'),
    Oh = new nu('complete'),
    Ph = {
      extend: function (t, e, n) {
        e.adapt = Nt(e.adapt, N(n.adapt));
      },
      init: function () {},
    },
    Th = Ph,
    Fh = Dt,
    Rh = /(?:^|\})?\s*([^\{\}]+)\s*\{/g,
    jh = /\/\*.*?\*\//g,
    Nh =
      /((?:(?:\[[^\]+]\])|(?:[^\s\+\>\~:]))+)((?::[^\s\+\>\~\(]+(?:\([^\)]+\))?)?\s*[\s\+\>\~]?)\s*/g,
    Dh = /^@media/,
    Ih = /\[data-ractive-css~="\{[a-z0-9-]+\}"]/g,
    Lh = 1,
    Vh = {
      name: 'css',
      extend: function (t, e, n) {
        if (n.css) {
          var i = Lh++,
            r = n.noCssTransform ? n.css : Fh(n.css, i);
          ((e.cssId = i), Ah.add({ id: i, styles: r }));
        }
      },
      init: function () {},
    },
    Mh = Vh,
    Uh = {
      name: 'data',
      extend: function (t, e, n) {
        var i = void 0,
          r = void 0;
        if (n.data && h(n.data))
          for (i in n.data)
            ((r = n.data[i]),
              r &&
                'object' == typeof r &&
                (h(r) || s(r)) &&
                m(
                  'Passing a `data` option with object and array properties to Ractive.extend() is discouraged, as mutating them is likely to cause bugs. Consider using a data function instead:\n\n  // this...\n  data: function () {\n    return {\n      myObject: {}\n    };\n  })\n\n  // instead of this:\n  data: {\n    myObject: {}\n  }'
                ));
        e.data = Mt(e.data, n.data);
      },
      init: function (t, e, n) {
        var i = Mt(t.prototype.data, n.data);
        return ('function' == typeof i && (i = i.call(e)), i || {});
      },
      reset: function (t) {
        var e = this.init(t.constructor, t, t.viewmodel);
        return (t.viewmodel.reset(e), !0);
      },
    },
    Wh = Uh,
    zh = /^\s+/;
  ((_h = function (t) {
    ((this.name = 'ParseError'), (this.message = t));
    try {
      throw new Error(t);
    } catch (e) {
      this.stack = e.stack;
    }
  }),
    (_h.prototype = Error.prototype),
    (Eh = function (t, e) {
      var n,
        i,
        r = 0;
      for (
        this.str = t,
          this.options = e || {},
          this.pos = 0,
          this.lines = this.str.split('\n'),
          this.lineEnds = this.lines.map(function (t) {
            var e = r + t.length + 1;
            return ((r = e), e);
          }, 0),
          this.init && this.init(t, e),
          n = [];
        this.pos < this.str.length && (i = this.read());

      )
        n.push(i);
      ((this.leftover = this.remaining()),
        (this.result = this.postProcess ? this.postProcess(n, e) : n));
    }),
    (Eh.prototype = {
      read: function (t) {
        var e, n, i, r;
        for (
          t || (t = this.converters), e = this.pos, i = t.length, n = 0;
          i > n;
          n += 1
        )
          if (((this.pos = e), (r = t[n](this)))) return r;
        return null;
      },
      getLinePos: function (t) {
        for (var e, n = 0, i = 0; t >= this.lineEnds[n]; )
          ((i = this.lineEnds[n]), (n += 1));
        return ((e = t - i), [n + 1, e + 1, t]);
      },
      error: function (t) {
        var e = this.getLinePos(this.pos),
          n = e[0],
          i = e[1],
          r = this.lines[e[0] - 1],
          s = 0,
          o =
            r.replace(/\t/g, function (t, n) {
              return (n < e[1] && (s += 1), '  ');
            }) +
            '\n' +
            new Array(e[1] + s).join(' ') +
            '^----',
          a = new _h('' + t + ' at line ' + n + ' character ' + i + ':\n' + o);
        throw ((a.line = e[0]), (a.character = e[1]), (a.shortMessage = t), a);
      },
      matchString: function (t) {
        return this.str.substr(this.pos, t.length) === t
          ? ((this.pos += t.length), t)
          : void 0;
      },
      matchPattern: function (t) {
        var e;
        return (e = t.exec(this.remaining()))
          ? ((this.pos += e[0].length), e[1] || e[0])
          : void 0;
      },
      allowWhitespace: function () {
        this.matchPattern(zh);
      },
      remaining: function () {
        return this.str.substring(this.pos);
      },
      nextChar: function () {
        return this.str.charAt(this.pos);
      },
    }),
    (Eh.extend = function (t) {
      var e,
        n,
        i = this;
      ((e = function (t, e) {
        Eh.call(this, t, e);
      }),
        (e.prototype = wa(i.prototype)));
      for (n in t) Oa.call(t, n) && (e.prototype[n] = t[n]);
      return ((e.extend = Eh.extend), e);
    }));
  var Bh,
    qh,
    $h,
    Qh = Eh,
    Zh = 1,
    Hh = 2,
    Kh = 3,
    Gh = 4,
    Yh = 5,
    Jh = 6,
    Xh = 7,
    tc = 8,
    ec = 9,
    nc = 10,
    ic = 13,
    rc = 14,
    sc = 15,
    oc = 16,
    ac = 17,
    uc = 18,
    hc = 20,
    cc = 21,
    lc = 22,
    fc = 23,
    dc = 24,
    pc = 25,
    mc = 26,
    vc = 27,
    gc = 30,
    yc = 31,
    bc = 32,
    wc = 33,
    xc = 34,
    kc = 35,
    Ec = 36,
    _c = 40,
    Ac = 50,
    Sc = 51,
    Cc = 52,
    Oc = 53,
    Pc = 54,
    Tc = 60,
    Fc = 61,
    Rc = zt,
    jc = /^[^\s=]+/,
    Nc = /^\s+/,
    Dc = Bt,
    Ic =
      /^(\/(?:[^\n\r\u2028\u2029\/\\[]|\\.|\[(?:[^\n\r\u2028\u2029\]\\]|\\.)*])+\/(?:([gimuy])(?![a-z]*\2))*(?![a-zA-Z_$0-9]))/,
    Lc = qt,
    Vc = { t: nc, exclude: !0 },
    Mc = 'Expected a JavaScript expression',
    Uc = 'Expected closing paren',
    Wc = Qt,
    zc =
      /^(?:[+-]?)0*(?:(?:(?:[1-9]\d*)?\.\d+)|(?:(?:0|[1-9]\d*)\.)|(?:0|[1-9]\d*))(?:[eE][+-]?\d+)?/,
    Bc = Zt;
  ((Bh = /^(?=.)[^"'\\]+?(?:(?!.)|(?=["'\\]))/),
    (qh =
      /^\\(?:['"\\bfnrt]|0(?![0-9])|x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|(?=.)[^ux0-9])/),
    ($h = /^\\(?:\r\n|[\u000A\u000D\u2028\u2029])/));
  var qc,
    $c,
    Qc = function (t) {
      return function (e) {
        var n, i, r, s;
        for (n = e.pos, i = '"', r = !1; !r; )
          ((s = e.matchPattern(Bh) || e.matchPattern(qh) || e.matchString(t)),
            s
              ? (i += '"' === s ? '\\"' : "\\'" === s ? "'" : s)
              : ((s = e.matchPattern($h)),
                s
                  ? (i +=
                      '\\u' + ('000' + s.charCodeAt(1).toString(16)).slice(-4))
                  : (r = !0)));
        return ((i += '"'), JSON.parse(i));
      };
    },
    Zc = Qc('"'),
    Hc = Qc("'"),
    Kc = function (t) {
      var e, n;
      return (
        (e = t.pos),
        t.matchString('"')
          ? ((n = Hc(t)),
            t.matchString('"') ? { t: cc, v: n } : ((t.pos = e), null))
          : t.matchString("'")
            ? ((n = Zc(t)),
              t.matchString("'") ? { t: cc, v: n } : ((t.pos = e), null))
            : null
      );
    },
    Gc = /^[a-zA-Z_$][a-zA-Z_$0-9]*/,
    Yc = Ht,
    Jc = /^[a-zA-Z_$][a-zA-Z_$0-9]*$/,
    Xc = Kt,
    tl = Gt,
    el = function (t) {
      var e, n;
      return (
        (e = t.pos),
        t.allowWhitespace(),
        t.matchString('{')
          ? ((n = tl(t)),
            t.allowWhitespace(),
            t.matchString('}') ? { t: fc, m: n } : ((t.pos = e), null))
          : ((t.pos = e), null)
      );
    },
    nl = Yt,
    il = function (t) {
      var e, n;
      return (
        (e = t.pos),
        t.allowWhitespace(),
        t.matchString('[')
          ? ((n = nl(t)),
            t.matchString(']') ? { t: lc, m: n } : ((t.pos = e), null))
          : ((t.pos = e), null)
      );
    },
    rl = Jt,
    sl = Xt,
    ol = /^(?:~\/|(?:\.\.\/)+|\.\/(?:\.\.\/)*|\.)/;
  ((qc =
    /^(?:Array|console|Date|RegExp|decodeURIComponent|decodeURI|encodeURIComponent|encodeURI|isFinite|isNaN|parseFloat|parseInt|JSON|Math|NaN|undefined|null)\b/),
    ($c =
      /^(?:break|case|catch|continue|debugger|default|delete|do|else|finally|for|function|if|in|instanceof|new|return|switch|throw|try|typeof|var|void|while|with)$/));
  var al,
    ul,
    hl = /^[a-zA-Z$_0-9]+(?:(?:\.[a-zA-Z$_0-9]+)|(?:\[[0-9]+\]))*/,
    cl = /^[a-zA-Z_$][-a-zA-Z_$0-9]*/,
    ll = te,
    fl = function (t) {
      return rl(t) || sl(t) || ll(t);
    },
    dl = ee,
    pl = function (t) {
      var e, n, i, r;
      if (((n = fl(t)), !n)) return null;
      for (; n; )
        if (((e = t.pos), (i = dl(t)))) n = { t: bc, x: n, r: i };
        else {
          if (!t.matchString('(')) break;
          (t.allowWhitespace(),
            (r = nl(t)),
            t.allowWhitespace(),
            t.matchString(')') || t.error(Uc),
            (n = { t: _c, x: n }),
            r && (n.o = r));
        }
      return n;
    };
  ((ul = function (t, e) {
    return function (n) {
      var i;
      return (i = e(n))
        ? i
        : n.matchString(t)
          ? (n.allowWhitespace(),
            (i = Ol(n)),
            i || n.error(Mc),
            { s: t, o: i, t: wc })
          : null;
    };
  }),
    (function () {
      var t, e, n, i, r;
      for (
        i = '! ~ + - typeof'.split(' '), r = pl, t = 0, e = i.length;
        e > t;
        t += 1
      )
        ((n = ul(i[t], r)), (r = n));
      al = r;
    })());
  var ml,
    vl,
    gl = al;
  ((vl = function (t, e) {
    return function (n) {
      var i, r, s;
      if (((r = e(n)), !r)) return null;
      for (;;) {
        if (((i = n.pos), n.allowWhitespace(), !n.matchString(t)))
          return ((n.pos = i), r);
        if ('in' === t && /[a-zA-Z_$0-9]/.test(n.remaining().charAt(0)))
          return ((n.pos = i), r);
        if ((n.allowWhitespace(), (s = e(n)), !s)) return ((n.pos = i), r);
        r = { t: Ec, s: t, o: [r, s] };
      }
    };
  }),
    (function () {
      var t, e, n, i, r;
      for (
        i =
          '* / % + - << >> >>> < <= > >= in instanceof == != === !== & ^ | && ||'.split(
            ' '
          ),
          r = gl,
          t = 0,
          e = i.length;
        e > t;
        t += 1
      )
        ((n = vl(i[t], r)), (r = n));
      ml = r;
    })());
  var yl,
    bl,
    wl,
    xl,
    kl,
    El,
    _l,
    Al,
    Sl = ml,
    Cl = ne,
    Ol = ie,
    Pl = re,
    Tl = oe,
    Fl = /^[0-9][1-9]*$/,
    Rl = ue,
    jl = he,
    Nl = ce,
    Dl = le,
    Il = fe,
    Ll = de,
    Vl = pe,
    Ml = /^yield\s*/,
    Ul = me,
    Wl = ve,
    zl = /^\s*else\s*/,
    Bl = ge,
    ql = /^\s*elseif\s+/,
    $l = { each: Cc, if: Ac, 'if-with': Pc, with: Oc, unless: Sc },
    Ql = ye,
    Zl = /^\s*:\s*([a-zA-Z_$][a-zA-Z_$0-9]*)/,
    Hl = /^\s*,\s*([a-zA-Z_$][a-zA-Z_$0-9]*)/,
    Kl = new RegExp('^(' + Object.keys($l).join('|') + ')\\b'),
    Gl = Ee,
    Yl = '<!--',
    Jl = '-->';
  ((yl =
    /^(allowFullscreen|async|autofocus|autoplay|checked|compact|controls|declare|default|defaultChecked|defaultMuted|defaultSelected|defer|disabled|enabled|formNoValidate|hidden|indeterminate|inert|isMap|itemScope|loop|multiple|muted|noHref|noResize|noShade|noValidate|noWrap|open|pauseOnExit|readOnly|required|reversed|scoped|seamless|selected|sortable|translate|trueSpeed|typeMustMatch|visible)$/i),
    (bl =
      /^(?:area|base|br|col|command|doctype|embed|hr|img|input|keygen|link|meta|param|source|track|wbr)$/i),
    (wl = {
      quot: 34,
      amp: 38,
      apos: 39,
      lt: 60,
      gt: 62,
      nbsp: 160,
      iexcl: 161,
      cent: 162,
      pound: 163,
      curren: 164,
      yen: 165,
      brvbar: 166,
      sect: 167,
      uml: 168,
      copy: 169,
      ordf: 170,
      laquo: 171,
      not: 172,
      shy: 173,
      reg: 174,
      macr: 175,
      deg: 176,
      plusmn: 177,
      sup2: 178,
      sup3: 179,
      acute: 180,
      micro: 181,
      para: 182,
      middot: 183,
      cedil: 184,
      sup1: 185,
      ordm: 186,
      raquo: 187,
      frac14: 188,
      frac12: 189,
      frac34: 190,
      iquest: 191,
      Agrave: 192,
      Aacute: 193,
      Acirc: 194,
      Atilde: 195,
      Auml: 196,
      Aring: 197,
      AElig: 198,
      Ccedil: 199,
      Egrave: 200,
      Eacute: 201,
      Ecirc: 202,
      Euml: 203,
      Igrave: 204,
      Iacute: 205,
      Icirc: 206,
      Iuml: 207,
      ETH: 208,
      Ntilde: 209,
      Ograve: 210,
      Oacute: 211,
      Ocirc: 212,
      Otilde: 213,
      Ouml: 214,
      times: 215,
      Oslash: 216,
      Ugrave: 217,
      Uacute: 218,
      Ucirc: 219,
      Uuml: 220,
      Yacute: 221,
      THORN: 222,
      szlig: 223,
      agrave: 224,
      aacute: 225,
      acirc: 226,
      atilde: 227,
      auml: 228,
      aring: 229,
      aelig: 230,
      ccedil: 231,
      egrave: 232,
      eacute: 233,
      ecirc: 234,
      euml: 235,
      igrave: 236,
      iacute: 237,
      icirc: 238,
      iuml: 239,
      eth: 240,
      ntilde: 241,
      ograve: 242,
      oacute: 243,
      ocirc: 244,
      otilde: 245,
      ouml: 246,
      divide: 247,
      oslash: 248,
      ugrave: 249,
      uacute: 250,
      ucirc: 251,
      uuml: 252,
      yacute: 253,
      thorn: 254,
      yuml: 255,
      OElig: 338,
      oelig: 339,
      Scaron: 352,
      scaron: 353,
      Yuml: 376,
      fnof: 402,
      circ: 710,
      tilde: 732,
      Alpha: 913,
      Beta: 914,
      Gamma: 915,
      Delta: 916,
      Epsilon: 917,
      Zeta: 918,
      Eta: 919,
      Theta: 920,
      Iota: 921,
      Kappa: 922,
      Lambda: 923,
      Mu: 924,
      Nu: 925,
      Xi: 926,
      Omicron: 927,
      Pi: 928,
      Rho: 929,
      Sigma: 931,
      Tau: 932,
      Upsilon: 933,
      Phi: 934,
      Chi: 935,
      Psi: 936,
      Omega: 937,
      alpha: 945,
      beta: 946,
      gamma: 947,
      delta: 948,
      epsilon: 949,
      zeta: 950,
      eta: 951,
      theta: 952,
      iota: 953,
      kappa: 954,
      lambda: 955,
      mu: 956,
      nu: 957,
      xi: 958,
      omicron: 959,
      pi: 960,
      rho: 961,
      sigmaf: 962,
      sigma: 963,
      tau: 964,
      upsilon: 965,
      phi: 966,
      chi: 967,
      psi: 968,
      omega: 969,
      thetasym: 977,
      upsih: 978,
      piv: 982,
      ensp: 8194,
      emsp: 8195,
      thinsp: 8201,
      zwnj: 8204,
      zwj: 8205,
      lrm: 8206,
      rlm: 8207,
      ndash: 8211,
      mdash: 8212,
      lsquo: 8216,
      rsquo: 8217,
      sbquo: 8218,
      ldquo: 8220,
      rdquo: 8221,
      bdquo: 8222,
      dagger: 8224,
      Dagger: 8225,
      bull: 8226,
      hellip: 8230,
      permil: 8240,
      prime: 8242,
      Prime: 8243,
      lsaquo: 8249,
      rsaquo: 8250,
      oline: 8254,
      frasl: 8260,
      euro: 8364,
      image: 8465,
      weierp: 8472,
      real: 8476,
      trade: 8482,
      alefsym: 8501,
      larr: 8592,
      uarr: 8593,
      rarr: 8594,
      darr: 8595,
      harr: 8596,
      crarr: 8629,
      lArr: 8656,
      uArr: 8657,
      rArr: 8658,
      dArr: 8659,
      hArr: 8660,
      forall: 8704,
      part: 8706,
      exist: 8707,
      empty: 8709,
      nabla: 8711,
      isin: 8712,
      notin: 8713,
      ni: 8715,
      prod: 8719,
      sum: 8721,
      minus: 8722,
      lowast: 8727,
      radic: 8730,
      prop: 8733,
      infin: 8734,
      ang: 8736,
      and: 8743,
      or: 8744,
      cap: 8745,
      cup: 8746,
      int: 8747,
      there4: 8756,
      sim: 8764,
      cong: 8773,
      asymp: 8776,
      ne: 8800,
      equiv: 8801,
      le: 8804,
      ge: 8805,
      sub: 8834,
      sup: 8835,
      nsub: 8836,
      sube: 8838,
      supe: 8839,
      oplus: 8853,
      otimes: 8855,
      perp: 8869,
      sdot: 8901,
      lceil: 8968,
      rceil: 8969,
      lfloor: 8970,
      rfloor: 8971,
      lang: 9001,
      rang: 9002,
      loz: 9674,
      spades: 9824,
      clubs: 9827,
      hearts: 9829,
      diams: 9830,
    }),
    (xl = [
      8364, 129, 8218, 402, 8222, 8230, 8224, 8225, 710, 8240, 352, 8249, 338,
      141, 381, 143, 144, 8216, 8217, 8220, 8221, 8226, 8211, 8212, 732, 8482,
      353, 8250, 339, 157, 382, 376,
    ]),
    (kl = new RegExp(
      '&(#?(?:x[\\w\\d]+|\\d+|' + Object.keys(wl).join('|') + '));?',
      'g'
    )),
    (El = /</g),
    (_l = />/g),
    (Al = /&/g));
  var Xl,
    tf,
    ef,
    nf,
    rf,
    sf,
    of,
    af = /^\s*\r?\n/,
    uf = /\r?\n\s*$/,
    hf = function (t) {
      var e, n, i, r, s;
      for (e = 1; e < t.length; e += 1)
        ((n = t[e]),
          (i = t[e - 1]),
          (r = t[e - 2]),
          Ce(n) &&
            Oe(i) &&
            Ce(r) &&
            uf.test(r) &&
            af.test(n) &&
            ((t[e - 2] = r.replace(uf, '\n')), (t[e] = n.replace(af, ''))),
          Pe(n) &&
            Ce(i) &&
            uf.test(i) &&
            Ce(n.f[0]) &&
            af.test(n.f[0]) &&
            ((t[e - 1] = i.replace(uf, '\n')),
            (n.f[0] = n.f[0].replace(af, ''))),
          Ce(n) &&
            Pe(i) &&
            ((s = D(i.f)),
            Ce(s) &&
              uf.test(s) &&
              af.test(n) &&
              ((i.f[i.f.length - 1] = s.replace(uf, '\n')),
              (t[e] = n.replace(af, '')))));
      return t;
    },
    cf = function (t, e, n) {
      var i;
      (e &&
        ((i = t[0]),
        'string' == typeof i &&
          ((i = i.replace(e, '')), i ? (t[0] = i) : t.shift())),
        n &&
          ((i = D(t)),
          'string' == typeof i &&
            ((i = i.replace(n, '')), i ? (t[t.length - 1] = i) : t.pop())));
    },
    lf = Te,
    ff = /[ \t\f\r\n]+/g,
    df = /^(?:pre|script|style|textarea)$/i,
    pf = /^[ \t\f\r\n]+/,
    mf = /[ \t\f\r\n]+$/,
    vf = /^(?:\r\n|\r|\n)/,
    gf = /(?:\r\n|\r|\n)$/,
    yf = Fe,
    bf = /^([a-zA-Z]{1,}:?[a-zA-Z0-9\-]*)\s*\>/,
    wf = function (t, e) {
      var n, i, r;
      for (n = e.length; n--; ) {
        if (((i = t.indexOf(e[n])), !i)) return 0;
        -1 !== i && (!r || r > i) && (r = i);
      }
      return r || -1;
    },
    xf = Re,
    kf = /^[^\s"'>\/=]+/,
    Ef = /^[^\s"'=<>`]+/;
  ((tf = { true: !0, false: !1, undefined: void 0, null: null }),
    (ef = new RegExp('^(?:' + Object.keys(tf).join('|') + ')')),
    (nf =
      /^(?:[+-]?)(?:(?:(?:0|[1-9]\d*)?\.\d+)|(?:(?:0|[1-9]\d*)\.)|(?:0|[1-9]\d*))(?:[eE][+-]?\d+)?/),
    (rf = /\$\{([^\}]+)\}/g),
    (sf = /^\$\{([^\}]+)\}/),
    (of = /^\s*$/),
    (Xl = Qh.extend({
      init: function (t, e) {
        ((this.values = e.values), this.allowWhitespace());
      },
      postProcess: function (t) {
        return 1 === t.length && of.test(this.leftover)
          ? { value: t[0].v }
          : null;
      },
      converters: [
        function (t) {
          var e;
          return t.values
            ? ((e = t.matchPattern(sf)),
              e && t.values.hasOwnProperty(e) ? { v: t.values[e] } : void 0)
            : null;
        },
        function (t) {
          var e;
          return (e = t.matchPattern(ef)) ? { v: tf[e] } : void 0;
        },
        function (t) {
          var e;
          return (e = t.matchPattern(nf)) ? { v: +e } : void 0;
        },
        function (t) {
          var e,
            n = Kc(t);
          return n && (e = t.values)
            ? {
                v: n.v.replace(rf, function (t, n) {
                  return n in e ? e[n] : n;
                }),
              }
            : n;
        },
        function (t) {
          var e, n;
          if (!t.matchString('{')) return null;
          if (((e = {}), t.allowWhitespace(), t.matchString('}')))
            return { v: e };
          for (; (n = Ve(t)); ) {
            if (((e[n.key] = n.value), t.allowWhitespace(), t.matchString('}')))
              return { v: e };
            if (!t.matchString(',')) return null;
          }
          return null;
        },
        function (t) {
          var e, n;
          if (!t.matchString('[')) return null;
          if (((e = []), t.allowWhitespace(), t.matchString(']')))
            return { v: e };
          for (; (n = t.read()); ) {
            if ((e.push(n.v), t.allowWhitespace(), t.matchString(']')))
              return { v: e };
            if (!t.matchString(',')) return null;
            t.allowWhitespace();
          }
          return null;
        },
      ],
    })));
  var _f,
    Af = function (t, e) {
      var n = new Xl(t, { values: e });
      return n.result;
    },
    Sf = Me,
    Cf = /^([a-zA-Z_$][a-zA-Z_$0-9]*)\(/,
    Of = /\)\s*$/;
  _f = Qh.extend({ converters: [Ol] });
  var Pf,
    Tf = /^[a-zA-Z]{1,}:?[a-zA-Z0-9\-]*/,
    Ff = /^[\s\n\/>]/,
    Rf = /^on/,
    jf = /^on-([a-zA-Z\\*\\.$_][a-zA-Z\\*\\.$_0-9\-]+)$/,
    Nf =
      /^(?:change|reset|teardown|update|construct|config|init|render|unrender|detach|insert)$/,
    Df = { 'intro-outro': 't0', intro: 't1', outro: 't2', decorator: 'o' },
    If = { exclude: !0 };
  Pf = {
    li: ['li'],
    dt: ['dt', 'dd'],
    dd: ['dt', 'dd'],
    p: 'address article aside blockquote div dl fieldset footer form h1 h2 h3 h4 h5 h6 header hgroup hr main menu nav ol p pre section table ul'.split(
      ' '
    ),
    rt: ['rt', 'rp'],
    rp: ['rt', 'rp'],
    optgroup: ['optgroup'],
    option: ['option', 'optgroup'],
    thead: ['tbody', 'tfoot'],
    tbody: ['tbody', 'tfoot'],
    tfoot: ['tbody'],
    tr: ['tr', 'tbody'],
    td: ['td', 'th', 'tr'],
    th: ['td', 'th', 'tr'],
  };
  var Lf,
    Vf = Ue,
    Mf = ze,
    Uf = Be,
    Wf = /[-\/\\^$*+?.()|[\]{}]/g,
    zf = qe,
    Bf = /^<!--\s*/,
    qf = /s*>\s*([a-zA-Z_$][-a-zA-Z_$0-9]*)\s*/,
    $f = /\s*-->/,
    Qf = $e,
    Zf = /^#\s*partial\s+/,
    Hf = Qe,
    Kf = Ze,
    Gf = [Nl, jl, Ql, Vl, Ll, Dl],
    Yf = [Rl],
    Jf = [jl, Ql, Ll],
    Xf = void 0,
    td = [Lc, Gl, Vf, Mf],
    ed = [zf, Qf];
  Xf = Qh.extend({
    init: function (t, e) {
      var n = e.tripleDelimiters || ['{{{', '}}}'],
        i = e.staticDelimiters || ['[[', ']]'],
        r = e.staticTripleDelimiters || ['[[[', ']]]'];
      ((this.standardDelimiters = e.delimiters || ['{{', '}}']),
        (this.tags = [
          {
            isStatic: !1,
            isTriple: !1,
            open: this.standardDelimiters[0],
            close: this.standardDelimiters[1],
            readers: Gf,
          },
          { isStatic: !1, isTriple: !0, open: n[0], close: n[1], readers: Yf },
          { isStatic: !0, isTriple: !1, open: i[0], close: i[1], readers: Jf },
          { isStatic: !0, isTriple: !0, open: r[0], close: r[1], readers: Yf },
        ]),
        this.sortMustacheTags(),
        (this.sectionDepth = 0),
        (this.elementStack = []),
        (this.interpolate = {
          script: !e.interpolate || e.interpolate.script !== !1,
          style: !e.interpolate || e.interpolate.style !== !1,
        }),
        e.sanitize === !0 &&
          (e.sanitize = {
            elements:
              'applet base basefont body frame frameset head html isindex link meta noframes noscript object param script style title'.split(
                ' '
              ),
            eventAttributes: !0,
          }),
        (this.stripComments = e.stripComments !== !1),
        (this.preserveWhitespace = e.preserveWhitespace),
        (this.sanitizeElements = e.sanitize && e.sanitize.elements),
        (this.sanitizeEventAttributes =
          e.sanitize && e.sanitize.eventAttributes),
        (this.includeLinePositions = e.includeLinePositions));
    },
    postProcess: function (t) {
      return t.length
        ? (this.sectionDepth > 0 && this.error('A section was left open'),
          lf(
            t[0].t,
            this.stripComments,
            this.preserveWhitespace,
            !this.preserveWhitespace,
            !this.preserveWhitespace
          ),
          t[0])
        : { t: [], v: oa };
    },
    converters: [Hf],
    sortMustacheTags: function () {
      this.tags.sort(function (t, e) {
        return e.open.length - t.open.length;
      });
    },
  });
  var nd,
    id,
    rd,
    sd = [
      'preserveWhitespace',
      'sanitize',
      'stripComments',
      'delimiters',
      'tripleDelimiters',
      'interpolate',
    ],
    od = {
      fromId: Ge,
      isHashedId: Ye,
      isParsed: Je,
      getParseOptions: Xe,
      createHelper: He,
      parse: Ke,
    },
    ad = od,
    ud = {
      name: 'template',
      extend: function (t, e, n) {
        var i;
        'template' in n &&
          ((i = n.template),
          (e.template = 'function' == typeof i ? i : rn(i, e)));
      },
      init: function (t, e, n) {
        var i, r;
        ((i = 'template' in n ? n.template : t.prototype.template),
          'function' == typeof i &&
            ((r = i),
            (i = en(e, r)),
            (e._config.template = { fn: r, result: i })),
          (i = rn(i, e)),
          (e.template = i.t),
          i.p && sn(e.partials, i.p));
      },
      reset: function (t) {
        var e,
          n = tn(t);
        return n
          ? ((e = rn(n, t)), (t.template = e.t), sn(t.partials, e.p, !0), !0)
          : void 0;
      },
    },
    hd = ud;
  ((nd = [
    'adaptors',
    'components',
    'computed',
    'decorators',
    'easing',
    'events',
    'interpolators',
    'partials',
    'transitions',
  ]),
    (id = function (t, e) {
      ((this.name = t), (this.useDefaults = e));
    }),
    (id.prototype = {
      constructor: id,
      extend: function (t, e, n) {
        this.configure(
          this.useDefaults ? t.defaults : t,
          this.useDefaults ? e : e.constructor,
          n
        );
      },
      init: function () {},
      configure: function (t, e, n) {
        var i,
          r = this.name,
          s = n[r];
        i = wa(t[r]);
        for (var o in s) i[o] = s[o];
        e[r] = i;
      },
      reset: function (t) {
        var e = t[this.name],
          n = !1;
        return (
          Object.keys(e).forEach(function (t) {
            var i = e[t];
            i._fn && (i._fn.isOwner ? (e[t] = i._fn) : delete e[t], (n = !0));
          }),
          n
        );
      },
    }),
    (rd = nd.map(function (t) {
      return new id(t, 'computed' === t);
    })));
  var cd,
    ld,
    fd,
    dd,
    pd,
    md,
    vd = rd,
    gd = on,
    yd = cn;
  ((dd = { adapt: Th, css: Mh, data: Wh, template: hd }),
    (fd = Object.keys(ua)),
    (md = dn(
      fd.filter(function (t) {
        return !dd[t];
      })
    )),
    (pd = dn(
      fd.concat(
        vd.map(function (t) {
          return t.name;
        })
      )
    )),
    (ld = [].concat(
      fd.filter(function (t) {
        return !vd[t] && !dd[t];
      }),
      vd,
      dd.data,
      dd.template,
      dd.css
    )),
    (cd = {
      extend: function (t, e, n) {
        return ln('extend', t, e, n);
      },
      init: function (t, e, n) {
        return ln('init', t, e, n);
      },
      reset: function (t) {
        return ld
          .filter(function (e) {
            return e.reset && e.reset(t);
          })
          .map(function (t) {
            return t.name;
          });
      },
      order: ld,
    }));
  var bd = cd,
    wd = pn,
    xd = mn,
    kd = vn,
    Ed = gn,
    _d = yn,
    Ad = bn,
    Sd = wn,
    Cd = xn,
    Od = kn,
    Pd = En,
    Td = _n,
    Fd = An,
    Rd = function () {
      return e(this.node);
    },
    jd = function (t) {
      ((this.type = Zh), (this.text = t.template));
    };
  jd.prototype = {
    detach: Rd,
    firstNode: function () {
      return this.node;
    },
    render: function () {
      return (
        this.node || (this.node = document.createTextNode(this.text)),
        this.node
      );
    },
    toString: function (t) {
      return t ? Se(this.text) : this.text;
    },
    unrender: function (t) {
      return t ? this.detach() : void 0;
    },
  };
  var Nd = jd,
    Dd = Sn,
    Id = Cn,
    Ld = function (t, e, n) {
      var i;
      ((this.ref = e),
        (this.resolved = !1),
        (this.root = t.root),
        (this.parentFragment = t.parentFragment),
        (this.callback = n),
        (i = uu(t.root, e, t.parentFragment)),
        void 0 != i ? this.resolve(i) : mu.addUnresolved(this));
    };
  Ld.prototype = {
    resolve: function (t) {
      (this.keypath && !t && mu.addUnresolved(this),
        (this.resolved = !0),
        (this.keypath = t),
        this.callback(t));
    },
    forceResolution: function () {
      this.resolve(_(this.ref));
    },
    rebind: function (t, e) {
      var n;
      void 0 != this.keypath &&
        ((n = this.keypath.replace(t, e)), void 0 !== n && this.resolve(n));
    },
    unbind: function () {
      this.resolved || mu.removeUnresolved(this);
    },
  };
  var Vd = Ld,
    Md = function (t, e, n) {
      ((this.parentFragment = t.parentFragment),
        (this.ref = e),
        (this.callback = n),
        this.rebind());
    },
    Ud = {
      '@keypath': { prefix: 'c', prop: ['context'] },
      '@index': { prefix: 'i', prop: ['index'] },
      '@key': { prefix: 'k', prop: ['key', 'index'] },
    };
  Md.prototype = {
    rebind: function () {
      var t,
        e = this.ref,
        n = this.parentFragment,
        i = Ud[e];
      if (!i)
        throw new Error(
          'Unknown special reference "' +
            e +
            '" - valid references are @index, @key and @keypath'
        );
      if (this.cached)
        return this.callback(_('@' + i.prefix + On(this.cached, i)));
      if (-1 !== i.prop.indexOf('index') || -1 !== i.prop.indexOf('key'))
        for (; n; ) {
          if (n.owner.currentSubtype === Cc && void 0 !== (t = On(n, i)))
            return (
              (this.cached = n),
              n.registerIndexRef(this),
              this.callback(_('@' + i.prefix + t))
            );
          n =
            !n.parent &&
            n.owner &&
            n.owner.component &&
            n.owner.component.parentFragment &&
            !n.owner.component.instance.isolated
              ? n.owner.component.parentFragment
              : n.parent;
        }
      else
        for (; n; ) {
          if (void 0 !== (t = On(n, i)))
            return this.callback(_('@' + i.prefix + t.str));
          n = n.parent;
        }
    },
    unbind: function () {
      this.cached && this.cached.unregisterIndexRef(this);
    },
  };
  var Wd = Md,
    zd = function (t, e, n) {
      ((this.parentFragment = t.parentFragment),
        (this.ref = e),
        (this.callback = n),
        e.ref.fragment.registerIndexRef(this),
        this.rebind());
    };
  zd.prototype = {
    rebind: function () {
      var t,
        e = this.ref.ref;
      ((t = 'k' === e.ref.t ? 'k' + e.fragment.key : 'i' + e.fragment.index),
        void 0 !== t && this.callback(_('@' + t)));
    },
    unbind: function () {
      this.ref.ref.fragment.unregisterIndexRef(this);
    },
  };
  var Bd = zd,
    qd = Pn;
  Pn.resolve = function (t) {
    var e,
      n,
      i = {};
    for (e in t.refs)
      ((n = t.refs[e]),
        (i[n.ref.n] = 'k' === n.ref.t ? n.fragment.key : n.fragment.index));
    return i;
  };
  var $d,
    Qd = Tn,
    Zd = Fn,
    Hd = {},
    Kd = Function.prototype.bind;
  (($d = function (t, e, n, i) {
    var r,
      s = this;
    ((r = t.root),
      (this.root = r),
      (this.parentFragment = e),
      (this.callback = i),
      (this.owner = t),
      (this.str = n.s),
      (this.keypaths = []),
      (this.pending = n.r.length),
      (this.refResolvers = n.r.map(function (t, e) {
        return Qd(s, t, function (t) {
          s.resolve(e, t);
        });
      })),
      (this.ready = !0),
      this.bubble());
  }),
    ($d.prototype = {
      bubble: function () {
        this.ready &&
          ((this.uniqueString = jn(this.str, this.keypaths)),
          (this.keypath = Nn(this.uniqueString)),
          this.createEvaluator(),
          this.callback(this.keypath));
      },
      unbind: function () {
        for (var t; (t = this.refResolvers.pop()); ) t.unbind();
      },
      resolve: function (t, e) {
        ((this.keypaths[t] = e), this.bubble());
      },
      createEvaluator: function () {
        var t,
          e,
          n,
          i,
          r,
          s = this;
        ((i = this.keypath),
          (t = this.root.viewmodel.computations[i.str]),
          t
            ? this.root.viewmodel.mark(i)
            : ((r = Zd(this.str, this.refResolvers.length)),
              (e = this.keypaths.map(function (t) {
                var e;
                return 'undefined' === t
                  ? function () {
                      return void 0;
                    }
                  : t.isSpecial
                    ? ((e = t.value),
                      function () {
                        return e;
                      })
                    : function () {
                        var e = s.root.viewmodel.get(t, {
                          noUnwrap: !0,
                          fullRootGet: !0,
                        });
                        return (
                          'function' == typeof e && (e = In(e, s.root)),
                          e
                        );
                      };
              })),
              (n = {
                deps: this.keypaths.filter(Dn),
                getter: function () {
                  var t = e.map(Rn);
                  return r.apply(null, t);
                },
              }),
              (t = this.root.viewmodel.compute(i, n))));
      },
      rebind: function (t, e) {
        this.refResolvers.forEach(function (n) {
          return n.rebind(t, e);
        });
      },
    }));
  var Gd = $d,
    Yd = function (t, e, n) {
      var i = this;
      ((this.resolver = e),
        (this.root = e.root),
        (this.parentFragment = n),
        (this.viewmodel = e.root.viewmodel),
        'string' == typeof t
          ? (this.value = t)
          : t.t === gc
            ? (this.refResolver = Qd(this, t.n, function (t) {
                i.resolve(t);
              }))
            : new Gd(e, n, t, function (t) {
                i.resolve(t);
              }));
    };
  Yd.prototype = {
    resolve: function (t) {
      (this.keypath && this.viewmodel.unregister(this.keypath, this),
        (this.keypath = t),
        (this.value = this.viewmodel.get(t)),
        this.bind(),
        this.resolver.bubble());
    },
    bind: function () {
      this.viewmodel.register(this.keypath, this);
    },
    rebind: function (t, e) {
      this.refResolver && this.refResolver.rebind(t, e);
    },
    setValue: function (t) {
      ((this.value = t), this.resolver.bubble());
    },
    unbind: function () {
      (this.keypath && this.viewmodel.unregister(this.keypath, this),
        this.refResolver && this.refResolver.unbind());
    },
    forceResolution: function () {
      this.refResolver && this.refResolver.forceResolution();
    },
  };
  var Jd = Yd,
    Xd = function (t, e, n) {
      var i,
        r,
        s,
        o,
        a = this;
      ((this.parentFragment = o = t.parentFragment),
        (this.root = i = t.root),
        (this.mustache = t),
        (this.ref = r = e.r),
        (this.callback = n),
        (this.unresolved = []),
        (s = uu(i, r, o))
          ? (this.base = s)
          : (this.baseResolver = new Vd(this, r, function (t) {
              ((a.base = t), (a.baseResolver = null), a.bubble());
            })),
        (this.members = e.m.map(function (t) {
          return new Jd(t, a, o);
        })),
        (this.ready = !0),
        this.bubble());
    };
  Xd.prototype = {
    getKeypath: function () {
      var t = this.members.map(Ln);
      return !t.every(Vn) || this.baseResolver
        ? null
        : this.base.join(t.join('.'));
    },
    bubble: function () {
      this.ready && !this.baseResolver && this.callback(this.getKeypath());
    },
    unbind: function () {
      this.members.forEach(Z);
    },
    rebind: function (t, e) {
      var n;
      if (this.base) {
        var i = this.base.replace(t, e);
        i && i !== this.base && ((this.base = i), (n = !0));
      }
      (this.members.forEach(function (i) {
        i.rebind(t, e) && (n = !0);
      }),
        n && this.bubble());
    },
    forceResolution: function () {
      (this.baseResolver &&
        ((this.base = _(this.ref)),
        this.baseResolver.unbind(),
        (this.baseResolver = null)),
        this.members.forEach(Mn),
        this.bubble());
    },
  };
  var tp = Xd,
    ep = Un,
    np = Wn,
    ip = zn,
    rp = { getValue: Id, init: ep, resolve: np, rebind: ip },
    sp = function (t) {
      ((this.type = Hh), rp.init(this, t));
    };
  sp.prototype = {
    update: function () {
      this.node.data = void 0 == this.value ? '' : this.value;
    },
    resolve: rp.resolve,
    rebind: rp.rebind,
    detach: Rd,
    unbind: Dd,
    render: function () {
      return (
        this.node || (this.node = document.createTextNode(n(this.value))),
        this.node
      );
    },
    unrender: function (t) {
      t && e(this.node);
    },
    getValue: rp.getValue,
    setValue: function (t) {
      var e;
      (this.keypath &&
        (e = this.root.viewmodel.wrapped[this.keypath.str]) &&
        (t = e.get()),
        a(t, this.value) ||
          ((this.value = t),
          this.parentFragment.bubble(),
          this.node && mu.addView(this)));
    },
    firstNode: function () {
      return this.node;
    },
    toString: function (t) {
      var e = '' + n(this.value);
      return t ? Se(e) : e;
    },
  };
  var op = sp,
    ap = Bn,
    up = qn,
    hp = $n,
    cp = Qn,
    lp = Zn,
    fp = Hn,
    dp = Kn,
    pp = Gn,
    mp = Yn,
    vp = function (t, e) {
      rp.rebind.call(this, t, e);
    },
    gp = Xn,
    yp = ti,
    bp = li,
    wp = fi,
    xp = di,
    kp = vi,
    Ep = function (t) {
      ((this.type = Gh),
        (this.subtype = this.currentSubtype = t.template.n),
        (this.inverted = this.subtype === Sc),
        (this.pElement = t.pElement),
        (this.fragments = []),
        (this.fragmentsToCreate = []),
        (this.fragmentsToRender = []),
        (this.fragmentsToUnrender = []),
        t.template.i &&
          (this.indexRefs = t.template.i.split(',').map(function (t, e) {
            return { n: t, t: 0 === e ? 'k' : 'i' };
          })),
        (this.renderedFragments = []),
        (this.length = 0),
        rp.init(this, t));
    };
  Ep.prototype = {
    bubble: ap,
    detach: up,
    find: hp,
    findAll: cp,
    findAllComponents: lp,
    findComponent: fp,
    findNextNode: dp,
    firstNode: pp,
    getIndexRef: function (t) {
      if (this.indexRefs)
        for (var e = this.indexRefs.length; e--; ) {
          var n = this.indexRefs[e];
          if (n.n === t) return n;
        }
    },
    getValue: rp.getValue,
    shuffle: mp,
    rebind: vp,
    render: gp,
    resolve: rp.resolve,
    setValue: yp,
    toString: bp,
    unbind: wp,
    unrender: xp,
    update: kp,
  };
  var _p,
    Ap,
    Sp = Ep,
    Cp = gi,
    Op = yi,
    Pp = bi,
    Tp = wi,
    Fp = {};
  try {
    la('table').innerHTML = 'foo';
  } catch (_a) {
    ((_p = !0),
      (Ap = {
        TABLE: ['<table class="x">', '</table>'],
        THEAD: ['<table><thead class="x">', '</thead></table>'],
        TBODY: ['<table><tbody class="x">', '</tbody></table>'],
        TR: ['<table><tr class="x">', '</tr></table>'],
        SELECT: ['<select class="x">', '</select>'],
      }));
  }
  var Rp = function (t, e, n) {
      var i,
        r,
        s,
        o,
        a,
        u = [];
      if (null != t && '' !== t) {
        for (
          _p && (r = Ap[e.tagName])
            ? ((i = xi('DIV')),
              (i.innerHTML = r[0] + t + r[1]),
              (i = i.querySelector('.x')),
              'SELECT' === i.tagName && (s = i.options[i.selectedIndex]))
            : e.namespaceURI === ia.svg
              ? ((i = xi('DIV')),
                (i.innerHTML = '<svg class="x">' + t + '</svg>'),
                (i = i.querySelector('.x')))
              : ((i = xi(e.tagName)),
                (i.innerHTML = t),
                'SELECT' === i.tagName && (s = i.options[i.selectedIndex]));
          (o = i.firstChild);

        )
          (u.push(o), n.appendChild(o));
        if ('SELECT' === e.tagName)
          for (a = u.length; a--; ) u[a] !== s && (u[a].selected = !1);
      }
      return u;
    },
    jp = ki,
    Np = _i,
    Dp = Ai,
    Ip = Si,
    Lp = Ci,
    Vp = Oi,
    Mp = function (t) {
      ((this.type = Kh), rp.init(this, t));
    };
  Mp.prototype = {
    detach: Cp,
    find: Op,
    findAll: Pp,
    firstNode: Tp,
    getValue: rp.getValue,
    rebind: rp.rebind,
    render: Np,
    resolve: rp.resolve,
    setValue: Dp,
    toString: Ip,
    unbind: Dd,
    unrender: Lp,
    update: Vp,
  };
  var Up,
    Wp,
    zp,
    Bp,
    qp = Mp,
    $p = function () {
      this.parentFragment.bubble();
    },
    Qp = Pi,
    Zp = function (t) {
      return this.node
        ? fa(this.node, t)
          ? this.node
          : this.fragment && this.fragment.find
            ? this.fragment.find(t)
            : void 0
        : null;
    },
    Hp = function (t, e) {
      (e._test(this, !0) &&
        e.live &&
        (this.liveQueries || (this.liveQueries = [])).push(e),
        this.fragment && this.fragment.findAll(t, e));
    },
    Kp = function (t, e) {
      this.fragment && this.fragment.findAllComponents(t, e);
    },
    Gp = function (t) {
      return this.fragment ? this.fragment.findComponent(t) : void 0;
    },
    Yp = Ti,
    Jp = Fi,
    Xp = Ri,
    tm = /^true|on|yes|1$/i,
    em = /^[0-9]+$/,
    nm = function (t, e) {
      var n, i, r;
      return (
        (r = e.a || {}),
        (i = {}),
        (n = r.twoway),
        void 0 !== n && (i.twoway = 0 === n || tm.test(n)),
        (n = r.lazy),
        void 0 !== n &&
          (i.lazy =
            0 !== n && em.test(n) ? parseInt(n) : 0 === n || tm.test(n)),
        i
      );
    },
    im = ji;
  ((Up =
    'altGlyph altGlyphDef altGlyphItem animateColor animateMotion animateTransform clipPath feBlend feColorMatrix feComponentTransfer feComposite feConvolveMatrix feDiffuseLighting feDisplacementMap feDistantLight feFlood feFuncA feFuncB feFuncG feFuncR feGaussianBlur feImage feMerge feMergeNode feMorphology feOffset fePointLight feSpecularLighting feSpotLight feTile feTurbulence foreignObject glyphRef linearGradient radialGradient textPath vkern'.split(
      ' '
    )),
    (Wp =
      'attributeName attributeType baseFrequency baseProfile calcMode clipPathUnits contentScriptType contentStyleType diffuseConstant edgeMode externalResourcesRequired filterRes filterUnits glyphRef gradientTransform gradientUnits kernelMatrix kernelUnitLength keyPoints keySplines keyTimes lengthAdjust limitingConeAngle markerHeight markerUnits markerWidth maskContentUnits maskUnits numOctaves pathLength patternContentUnits patternTransform patternUnits pointsAtX pointsAtY pointsAtZ preserveAlpha preserveAspectRatio primitiveUnits refX refY repeatCount repeatDur requiredExtensions requiredFeatures specularConstant specularExponent spreadMethod startOffset stdDeviation stitchTiles surfaceScale systemLanguage tableValues targetX targetY textLength viewBox viewTarget xChannelSelector yChannelSelector zoomAndPan'.split(
        ' '
      )),
    (zp = function (t) {
      for (var e = {}, n = t.length; n--; ) e[t[n].toLowerCase()] = t[n];
      return e;
    }),
    (Bp = zp(Up.concat(Wp))));
  var rm = function (t) {
      var e = t.toLowerCase();
      return Bp[e] || e;
    },
    sm = function (t, e) {
      var n, i;
      if (
        ((n = e.indexOf(':')),
        -1 === n || ((i = e.substr(0, n)), 'xmlns' === i))
      )
        t.name = t.element.namespace !== ia.html ? rm(e) : e;
      else if (
        ((e = e.substring(n + 1)),
        (t.name = rm(e)),
        (t.namespace = ia[i.toLowerCase()]),
        (t.namespacePrefix = i),
        !t.namespace)
      )
        throw 'Unknown namespace ("' + i + '")';
    },
    om = Ni,
    am = Di,
    um = Ii,
    hm = Li,
    cm = {
      'accept-charset': 'acceptCharset',
      accesskey: 'accessKey',
      bgcolor: 'bgColor',
      class: 'className',
      codebase: 'codeBase',
      colspan: 'colSpan',
      contenteditable: 'contentEditable',
      datetime: 'dateTime',
      dirname: 'dirName',
      for: 'htmlFor',
      'http-equiv': 'httpEquiv',
      ismap: 'isMap',
      maxlength: 'maxLength',
      novalidate: 'noValidate',
      pubdate: 'pubDate',
      readonly: 'readOnly',
      rowspan: 'rowSpan',
      tabindex: 'tabIndex',
      usemap: 'useMap',
    },
    lm = Vi,
    fm = Ui,
    dm = Wi,
    pm = zi,
    mm = Bi,
    vm = qi,
    gm = $i,
    ym = Qi,
    bm = Zi,
    wm = Hi,
    xm = Ki,
    km = Gi,
    Em = Yi,
    _m = Ji,
    Am = Xi,
    Sm = function (t) {
      this.init(t);
    };
  Sm.prototype = {
    bubble: im,
    init: am,
    rebind: um,
    render: hm,
    toString: lm,
    unbind: fm,
    update: Am,
  };
  var Cm,
    Om = Sm,
    Pm = function (t, e) {
      var n,
        i,
        r = [];
      for (n in e)
        'twoway' !== n &&
          'lazy' !== n &&
          e.hasOwnProperty(n) &&
          ((i = new Om({ element: t, name: n, value: e[n], root: t.root })),
          (r[n] = i),
          'value' !== n && r.push(i));
      return ((i = r.value) && r.push(i), r);
    };
  'undefined' != typeof document && (Cm = la('div'));
  var Tm = function (t, e) {
    ((this.element = t),
      (this.root = t.root),
      (this.parentFragment = t.parentFragment),
      (this.attributes = []),
      (this.fragment = new yb({ root: t.root, owner: this, template: [e] })));
  };
  Tm.prototype = {
    bubble: function () {
      (this.node && this.update(), this.element.bubble());
    },
    rebind: function (t, e) {
      this.fragment.rebind(t, e);
    },
    render: function (t) {
      ((this.node = t),
        (this.isSvg = t.namespaceURI === ia.svg),
        this.update());
    },
    unbind: function () {
      this.fragment.unbind();
    },
    update: function () {
      var t,
        e,
        n = this;
      ((t = this.fragment.toString()),
        (e = tr(t, this.isSvg)),
        this.attributes
          .filter(function (t) {
            return er(e, t);
          })
          .forEach(function (t) {
            n.node.removeAttribute(t.name);
          }),
        e.forEach(function (t) {
          n.node.setAttribute(t.name, t.value);
        }),
        (this.attributes = e));
    },
    toString: function () {
      return this.fragment.toString();
    },
  };
  var Fm = Tm,
    Rm = function (t, e) {
      return e
        ? e.map(function (e) {
            return new Fm(t, e);
          })
        : [];
    },
    jm = function (t) {
      var e, n, i, r;
      if (
        ((this.element = t),
        (this.root = t.root),
        (this.attribute = t.attributes[this.name || 'value']),
        (e = this.attribute.interpolator),
        (e.twowayBinding = this),
        (n = e.keypath))
      ) {
        if ('}' === n.str.slice(-1))
          return (
            v(
              'Two-way binding does not work with expressions (`%s` on <%s>)',
              e.resolver.uniqueString,
              t.name,
              { ractive: this.root }
            ),
            !1
          );
        if (n.isSpecial)
          return (
            v('Two-way binding does not work with %s', e.resolver.ref, {
              ractive: this.root,
            }),
            !1
          );
      } else {
        var s = e.template.r
          ? "'" + e.template.r + "' reference"
          : 'expression';
        (m(
          'The %s being used for two-way binding is ambiguous, and may cause unexpected results. Consider initialising your data to eliminate the ambiguity',
          s,
          { ractive: this.root }
        ),
          e.resolver.forceResolution(),
          (n = e.keypath));
      }
      ((this.attribute.isTwoway = !0),
        (this.keypath = n),
        (i = this.root.viewmodel.get(n)),
        void 0 === i &&
          this.getInitialValue &&
          ((i = this.getInitialValue()),
          void 0 !== i && this.root.viewmodel.set(n, i)),
        (r = nr(t)) && ((this.resetValue = i), r.formBindings.push(this)));
    };
  ((jm.prototype = {
    handleChange: function () {
      var t = this;
      (mu.start(this.root),
        (this.attribute.locked = !0),
        this.root.viewmodel.set(this.keypath, this.getValue()),
        mu.scheduleTask(function () {
          return (t.attribute.locked = !1);
        }),
        mu.end());
    },
    rebound: function () {
      var t, e, n;
      ((e = this.keypath),
        (n = this.attribute.interpolator.keypath),
        e !== n &&
          (I(this.root._twowayBindings[e.str], this),
          (this.keypath = n),
          (t =
            this.root._twowayBindings[n.str] ||
            (this.root._twowayBindings[n.str] = [])),
          t.push(this)));
    },
    unbind: function () {},
  }),
    (jm.extend = function (t) {
      var e,
        n = this;
      return (
        (e = function (t) {
          (jm.call(this, t), this.init && this.init());
        }),
        (e.prototype = wa(n.prototype)),
        i(e.prototype, t),
        (e.extend = jm.extend),
        e
      );
    }));
  var Nm,
    Dm = jm,
    Im = ir;
  Nm = Dm.extend({
    getInitialValue: function () {
      return '';
    },
    getValue: function () {
      return this.element.node.value;
    },
    render: function () {
      var t,
        e = this.element.node,
        n = !1;
      ((this.rendered = !0),
        (t = this.root.lazy),
        this.element.lazy === !0
          ? (t = !0)
          : this.element.lazy === !1
            ? (t = !1)
            : u(this.element.lazy)
              ? ((t = !1), (n = +this.element.lazy))
              : u(t || '') && ((n = +t), (t = !1), (this.element.lazy = n)),
        (this.handler = n ? sr : Im),
        e.addEventListener('change', Im, !1),
        t ||
          (e.addEventListener('input', this.handler, !1),
          e.attachEvent && e.addEventListener('keyup', this.handler, !1)),
        e.addEventListener('blur', rr, !1));
    },
    unrender: function () {
      var t = this.element.node;
      ((this.rendered = !1),
        t.removeEventListener('change', Im, !1),
        t.removeEventListener('input', this.handler, !1),
        t.removeEventListener('keyup', this.handler, !1),
        t.removeEventListener('blur', rr, !1));
    },
  });
  var Lm = Nm,
    Vm = Lm.extend({
      getInitialValue: function () {
        return this.element.fragment ? this.element.fragment.toString() : '';
      },
      getValue: function () {
        return this.element.node.innerHTML;
      },
    }),
    Mm = Vm,
    Um = or,
    Wm = {},
    zm = Dm.extend({
      name: 'checked',
      init: function () {
        ((this.siblings = Um(
          this.root._guid,
          'radio',
          this.element.getAttribute('name')
        )),
          this.siblings.push(this));
      },
      render: function () {
        var t = this.element.node;
        (t.addEventListener('change', Im, !1),
          t.attachEvent && t.addEventListener('click', Im, !1));
      },
      unrender: function () {
        var t = this.element.node;
        (t.removeEventListener('change', Im, !1),
          t.removeEventListener('click', Im, !1));
      },
      handleChange: function () {
        (mu.start(this.root),
          this.siblings.forEach(function (t) {
            t.root.viewmodel.set(t.keypath, t.getValue());
          }),
          mu.end());
      },
      getValue: function () {
        return this.element.node.checked;
      },
      unbind: function () {
        I(this.siblings, this);
      },
    }),
    Bm = zm,
    qm = Dm.extend({
      name: 'name',
      init: function () {
        ((this.siblings = Um(this.root._guid, 'radioname', this.keypath.str)),
          this.siblings.push(this),
          (this.radioName = !0));
      },
      getInitialValue: function () {
        return this.element.getAttribute('checked')
          ? this.element.getAttribute('value')
          : void 0;
      },
      render: function () {
        var t = this.element.node;
        ((t.name = '{{' + this.keypath.str + '}}'),
          (t.checked =
            this.root.viewmodel.get(this.keypath) ==
            this.element.getAttribute('value')),
          t.addEventListener('change', Im, !1),
          t.attachEvent && t.addEventListener('click', Im, !1));
      },
      unrender: function () {
        var t = this.element.node;
        (t.removeEventListener('change', Im, !1),
          t.removeEventListener('click', Im, !1));
      },
      getValue: function () {
        var t = this.element.node;
        return t._ractive ? t._ractive.value : t.value;
      },
      handleChange: function () {
        this.element.node.checked && Dm.prototype.handleChange.call(this);
      },
      rebound: function (t, e) {
        var n;
        (Dm.prototype.rebound.call(this, t, e),
          (n = this.element.node) && (n.name = '{{' + this.keypath.str + '}}'));
      },
      unbind: function () {
        I(this.siblings, this);
      },
    }),
    $m = qm,
    Qm = Dm.extend({
      name: 'name',
      getInitialValue: function () {
        return ((this.noInitialValue = !0), []);
      },
      init: function () {
        var t, e;
        ((this.checkboxName = !0),
          (this.siblings = Um(this.root._guid, 'checkboxes', this.keypath.str)),
          this.siblings.push(this),
          this.noInitialValue && (this.siblings.noInitialValue = !0),
          this.siblings.noInitialValue &&
            this.element.getAttribute('checked') &&
            ((t = this.root.viewmodel.get(this.keypath)),
            (e = this.element.getAttribute('value')),
            t.push(e)));
      },
      unbind: function () {
        I(this.siblings, this);
      },
      render: function () {
        var t,
          e,
          n = this.element.node;
        ((t = this.root.viewmodel.get(this.keypath)),
          (e = this.element.getAttribute('value')),
          (this.isChecked = s(t) ? R(t, e) : t == e),
          (n.name = '{{' + this.keypath.str + '}}'),
          (n.checked = this.isChecked),
          n.addEventListener('change', Im, !1),
          n.attachEvent && n.addEventListener('click', Im, !1));
      },
      unrender: function () {
        var t = this.element.node;
        (t.removeEventListener('change', Im, !1),
          t.removeEventListener('click', Im, !1));
      },
      changed: function () {
        var t = !!this.isChecked;
        return (
          (this.isChecked = this.element.node.checked),
          this.isChecked === t
        );
      },
      handleChange: function () {
        ((this.isChecked = this.element.node.checked),
          Dm.prototype.handleChange.call(this));
      },
      getValue: function () {
        return this.siblings.filter(ar).map(ur);
      },
    }),
    Zm = Qm,
    Hm = Dm.extend({
      name: 'checked',
      render: function () {
        var t = this.element.node;
        (t.addEventListener('change', Im, !1),
          t.attachEvent && t.addEventListener('click', Im, !1));
      },
      unrender: function () {
        var t = this.element.node;
        (t.removeEventListener('change', Im, !1),
          t.removeEventListener('click', Im, !1));
      },
      getValue: function () {
        return this.element.node.checked;
      },
    }),
    Km = Hm,
    Gm = Dm.extend({
      getInitialValue: function () {
        var t,
          e,
          n,
          i,
          r = this.element.options;
        if (
          void 0 === this.element.getAttribute('value') &&
          ((e = t = r.length), t)
        ) {
          for (; e--; )
            if (r[e].getAttribute('selected')) {
              ((n = r[e].getAttribute('value')), (i = !0));
              break;
            }
          if (!i)
            for (; ++e < t; )
              if (!r[e].getAttribute('disabled')) {
                n = r[e].getAttribute('value');
                break;
              }
          return (void 0 !== n && (this.element.attributes.value.value = n), n);
        }
      },
      render: function () {
        this.element.node.addEventListener('change', Im, !1);
      },
      unrender: function () {
        this.element.node.removeEventListener('change', Im, !1);
      },
      setValue: function (t) {
        this.root.viewmodel.set(this.keypath, t);
      },
      getValue: function () {
        var t, e, n, i, r;
        for (t = this.element.node.options, n = t.length, e = 0; n > e; e += 1)
          if (((i = t[e]), t[e].selected))
            return (r = i._ractive ? i._ractive.value : i.value);
      },
      forceUpdate: function () {
        var t = this,
          e = this.getValue();
        void 0 !== e &&
          ((this.attribute.locked = !0),
          mu.scheduleTask(function () {
            return (t.attribute.locked = !1);
          }),
          this.root.viewmodel.set(this.keypath, e));
      },
    }),
    Ym = Gm,
    Jm = Ym.extend({
      getInitialValue: function () {
        return this.element.options
          .filter(function (t) {
            return t.getAttribute('selected');
          })
          .map(function (t) {
            return t.getAttribute('value');
          });
      },
      render: function () {
        var t;
        (this.element.node.addEventListener('change', Im, !1),
          (t = this.root.viewmodel.get(this.keypath)),
          void 0 === t && this.handleChange());
      },
      unrender: function () {
        this.element.node.removeEventListener('change', Im, !1);
      },
      setValue: function () {
        throw new Error('TODO not implemented yet');
      },
      getValue: function () {
        var t, e, n, i, r, s;
        for (
          t = [], e = this.element.node.options, i = e.length, n = 0;
          i > n;
          n += 1
        )
          ((r = e[n]),
            r.selected &&
              ((s = r._ractive ? r._ractive.value : r.value), t.push(s)));
        return t;
      },
      handleChange: function () {
        var t, e, n;
        return (
          (t = this.attribute),
          (e = t.value),
          (n = this.getValue()),
          (void 0 !== e && j(n, e)) || Ym.prototype.handleChange.call(this),
          this
        );
      },
      forceUpdate: function () {
        var t = this,
          e = this.getValue();
        void 0 !== e &&
          ((this.attribute.locked = !0),
          mu.scheduleTask(function () {
            return (t.attribute.locked = !1);
          }),
          this.root.viewmodel.set(this.keypath, e));
      },
      updateModel: function () {
        (void 0 !== this.attribute.value && this.attribute.value.length) ||
          this.root.viewmodel.set(this.keypath, this.initialValue);
      },
    }),
    Xm = Jm,
    tv = Dm.extend({
      render: function () {
        this.element.node.addEventListener('change', Im, !1);
      },
      unrender: function () {
        this.element.node.removeEventListener('change', Im, !1);
      },
      getValue: function () {
        return this.element.node.files;
      },
    }),
    ev = tv,
    nv = Lm.extend({
      getInitialValue: function () {
        return void 0;
      },
      getValue: function () {
        var t = parseFloat(this.element.node.value);
        return isNaN(t) ? void 0 : t;
      },
    }),
    iv = hr,
    rv = lr,
    sv = fr,
    ov = dr,
    av = pr,
    uv = /^event(?:\.(.+))?/,
    hv = yr,
    cv = br,
    lv = {},
    fv = {
      touchstart: !0,
      touchmove: !0,
      touchend: !0,
      touchcancel: !0,
      touchleave: !0,
    },
    dv = xr,
    pv = kr,
    mv = Er,
    vv = _r,
    gv = Ar,
    yv = function (t, e, n) {
      this.init(t, e, n);
    };
  yv.prototype = {
    bubble: rv,
    fire: sv,
    getAction: ov,
    init: av,
    listen: cv,
    rebind: dv,
    render: pv,
    resolve: mv,
    unbind: vv,
    unrender: gv,
  };
  var bv = yv,
    wv = function (t, e) {
      var n,
        i,
        r,
        s,
        o = [];
      for (i in e)
        if (e.hasOwnProperty(i))
          for (r = i.split('-'), n = r.length; n--; )
            ((s = new bv(t, r[n], e[i])), o.push(s));
      return o;
    },
    xv = function (t, e) {
      var n,
        i,
        r,
        s = this;
      ((this.element = t),
        (this.root = n = t.root),
        (i = e.n || e),
        ('string' == typeof i ||
          ((r = new yb({ template: i, root: n, owner: t })),
          (i = r.toString()),
          r.unbind(),
          '' !== i)) &&
          (e.a
            ? (this.params = e.a)
            : e.d &&
              ((this.fragment = new yb({ template: e.d, root: n, owner: t })),
              (this.params = this.fragment.getArgsList()),
              (this.fragment.bubble = function () {
                ((this.dirtyArgs = this.dirtyValue = !0),
                  (s.params = this.getArgsList()),
                  s.ready && s.update());
              })),
          (this.fn = g('decorators', n, i)),
          this.fn || l(Da(i, 'decorator'))));
    };
  xv.prototype = {
    init: function () {
      var t, e, n;
      if (
        ((t = this.element.node),
        this.params
          ? ((n = [t].concat(this.params)), (e = this.fn.apply(this.root, n)))
          : (e = this.fn.call(this.root, t)),
        !e || !e.teardown)
      )
        throw new Error(
          'Decorator definition must return an object with a teardown method'
        );
      ((this.actual = e), (this.ready = !0));
    },
    update: function () {
      this.actual.update
        ? this.actual.update.apply(this.root, this.params)
        : (this.actual.teardown(!0), this.init());
    },
    rebind: function (t, e) {
      this.fragment && this.fragment.rebind(t, e);
    },
    teardown: function (t) {
      ((this.torndown = !0),
        this.ready && this.actual.teardown(),
        !t && this.fragment && this.fragment.unbind());
    },
  };
  var kv,
    Ev,
    _v,
    Av = xv,
    Sv = Rr,
    Cv = jr,
    Ov = Mr,
    Pv = function (t) {
      return t.replace(/-([a-zA-Z])/g, function (t, e) {
        return e.toUpperCase();
      });
    };
  Xo
    ? ((Ev = {}),
      (_v = la('div').style),
      (kv = function (t) {
        var e, n, i;
        if (((t = Pv(t)), !Ev[t]))
          if (void 0 !== _v[t]) Ev[t] = t;
          else
            for (
              i = t.charAt(0).toUpperCase() + t.substring(1), e = sa.length;
              e--;

            )
              if (((n = sa[e]), void 0 !== _v[n + i])) {
                Ev[t] = n + i;
                break;
              }
        return Ev[t];
      }))
    : (kv = null);
  var Tv,
    Fv,
    Rv = kv;
  Xo
    ? ((Fv = window.getComputedStyle || Ea.getComputedStyle),
      (Tv = function (t) {
        var e, n, i, r, o;
        if (((e = Fv(this.node)), 'string' == typeof t))
          return ((o = e[Rv(t)]), '0px' === o && (o = 0), o);
        if (!s(t))
          throw new Error(
            'Transition$getStyle must be passed a string, or an array of strings representing CSS properties'
          );
        for (n = {}, i = t.length; i--; )
          ((r = t[i]), (o = e[Rv(r)]), '0px' === o && (o = 0), (n[r] = o));
        return n;
      }))
    : (Tv = null);
  var jv = Tv,
    Nv = function (t, e) {
      var n;
      if ('string' == typeof t) this.node.style[Rv(t)] = e;
      else for (n in t) t.hasOwnProperty(n) && (this.node.style[Rv(n)] = t[n]);
      return this;
    },
    Dv = function (t) {
      var e;
      ((this.duration = t.duration),
        (this.step = t.step),
        (this.complete = t.complete),
        'string' == typeof t.easing
          ? ((e = t.root.easing[t.easing]),
            e || (v(Da(t.easing, 'easing')), (e = Ur)))
          : (e = 'function' == typeof t.easing ? t.easing : Ur),
        (this.easing = e),
        (this.start = Xa()),
        (this.end = this.start + this.duration),
        (this.running = !0),
        yu.add(this));
    };
  Dv.prototype = {
    tick: function (t) {
      var e, n;
      return this.running
        ? t > this.end
          ? (this.step && this.step(1), this.complete && this.complete(1), !1)
          : ((e = t - this.start),
            (n = this.easing(e / this.duration)),
            this.step && this.step(n),
            !0)
        : !1;
    },
    stop: function () {
      (this.abort && this.abort(), (this.running = !1));
    },
  };
  var Iv,
    Lv,
    Vv,
    Mv,
    Uv,
    Wv,
    zv,
    Bv,
    qv = Dv,
    $v = new RegExp('^-(?:' + sa.join('|') + ')-'),
    Qv = function (t) {
      return t.replace($v, '');
    },
    Zv = new RegExp('^(?:' + sa.join('|') + ')([A-Z])'),
    Hv = function (t) {
      var e;
      return t
        ? (Zv.test(t) && (t = '-' + t),
          (e = t.replace(/[A-Z]/g, function (t) {
            return '-' + t.toLowerCase();
          })))
        : '';
    },
    Kv = {},
    Gv = {};
  Xo
    ? ((Lv = la('div').style),
      (function () {
        void 0 !== Lv.transition
          ? ((Vv = 'transition'), (Mv = 'transitionend'), (Uv = !0))
          : void 0 !== Lv.webkitTransition
            ? ((Vv = 'webkitTransition'),
              (Mv = 'webkitTransitionEnd'),
              (Uv = !0))
            : (Uv = !1);
      })(),
      Vv &&
        ((Wv = Vv + 'Duration'),
        (zv = Vv + 'Property'),
        (Bv = Vv + 'TimingFunction')),
      (Iv = function (t, e, n, i, r) {
        setTimeout(function () {
          var s, o, a, u, h;
          ((u = function () {
            o && a && (t.root.fire(t.name + ':end', t.node, t.isIntro), r());
          }),
            (s = (t.node.namespaceURI || '') + t.node.tagName),
            (t.node.style[zv] = i.map(Rv).map(Hv).join(',')),
            (t.node.style[Bv] = Hv(n.easing || 'linear')),
            (t.node.style[Wv] = n.duration / 1e3 + 's'),
            (h = function (e) {
              var n;
              ((n = i.indexOf(Pv(Qv(e.propertyName)))),
                -1 !== n && i.splice(n, 1),
                i.length ||
                  (t.node.removeEventListener(Mv, h, !1), (a = !0), u()));
            }),
            t.node.addEventListener(Mv, h, !1),
            setTimeout(function () {
              for (var r, c, l, f, d, p = i.length, v = []; p--; )
                ((f = i[p]),
                  (r = s + f),
                  Uv &&
                    !Gv[r] &&
                    ((t.node.style[Rv(f)] = e[f]),
                    Kv[r] ||
                      ((c = t.getStyle(f)),
                      (Kv[r] = t.getStyle(f) != e[f]),
                      (Gv[r] = !Kv[r]),
                      Gv[r] && (t.node.style[Rv(f)] = c))),
                  (!Uv || Gv[r]) &&
                    (void 0 === c && (c = t.getStyle(f)),
                    (l = i.indexOf(f)),
                    -1 === l
                      ? m(
                          'Something very strange happened with transitions. Please raise an issue at https://github.com/ractivejs/ractive/issues - thanks!',
                          { node: t.node }
                        )
                      : i.splice(l, 1),
                    (d = /[^\d]*$/.exec(e[f])[0]),
                    v.push({
                      name: Rv(f),
                      interpolator: La(parseFloat(c), parseFloat(e[f])),
                      suffix: d,
                    })));
              (v.length
                ? new qv({
                    root: t.root,
                    duration: n.duration,
                    easing: Pv(n.easing || ''),
                    step: function (e) {
                      var n, i;
                      for (i = v.length; i--; )
                        ((n = v[i]),
                          (t.node.style[n.name] =
                            n.interpolator(e) + n.suffix));
                    },
                    complete: function () {
                      ((o = !0), u());
                    },
                  })
                : (o = !0),
                i.length ||
                  (t.node.removeEventListener(Mv, h, !1), (a = !0), u()));
            }, 0));
        }, n.delay || 0);
      }))
    : (Iv = null);
  var Yv,
    Jv,
    Xv,
    tg,
    eg,
    ng = Iv;
  if ('undefined' != typeof document) {
    if (((Yv = 'hidden'), (eg = {}), Yv in document)) Xv = '';
    else
      for (tg = sa.length; tg--; )
        ((Jv = sa[tg]), (Yv = Jv + 'Hidden'), Yv in document && (Xv = Jv));
    void 0 !== Xv
      ? (document.addEventListener(Xv + 'visibilitychange', Wr), Wr())
      : ('onfocusout' in document
          ? (document.addEventListener('focusout', zr),
            document.addEventListener('focusin', Br))
          : (window.addEventListener('pagehide', zr),
            window.addEventListener('blur', zr),
            window.addEventListener('pageshow', Br),
            window.addEventListener('focus', Br)),
        (eg.hidden = !1));
  }
  var ig,
    rg,
    sg,
    og = eg;
  Xo
    ? ((rg = window.getComputedStyle || Ea.getComputedStyle),
      (ig = function (t, e, n) {
        var i,
          r = this;
        if (4 === arguments.length)
          throw new Error(
            't.animateStyle() returns a promise - use .then() instead of passing a callback'
          );
        if (og.hidden) return (this.setStyle(t, e), sg || (sg = ou.resolve()));
        ('string' == typeof t ? ((i = {}), (i[t] = e)) : ((i = t), (n = e)),
          n ||
            (v(
              'The "%s" transition does not supply an options object to `t.animateStyle()`. This will break in a future version of Ractive. For more info see https://github.com/RactiveJS/Ractive/issues/340',
              this.name
            ),
            (n = this)));
        var s = new ou(function (t) {
          var e, s, o, a, u, h, c;
          if (!n.duration) return (r.setStyle(i), void t());
          for (
            e = Object.keys(i), s = [], o = rg(r.node), u = {}, h = e.length;
            h--;

          )
            ((c = e[h]),
              (a = o[Rv(c)]),
              '0px' === a && (a = 0),
              a != i[c] && (s.push(c), (r.node.style[Rv(c)] = a)));
          return s.length ? void ng(r, i, n, s, t) : void t();
        });
        return s;
      }))
    : (ig = null);
  var ag = ig,
    ug = function (t, e) {
      return (
        'number' == typeof t
          ? (t = { duration: t })
          : 'string' == typeof t
            ? (t =
                'slow' === t
                  ? { duration: 600 }
                  : 'fast' === t
                    ? { duration: 200 }
                    : { duration: 400 })
            : t || (t = {}),
        r({}, t, e)
      );
    },
    hg = qr,
    cg = function (t, e, n) {
      this.init(t, e, n);
    };
  cg.prototype = {
    init: Ov,
    start: hg,
    getStyle: jv,
    setStyle: Nv,
    animateStyle: ag,
    processParams: ug,
  };
  var lg,
    fg,
    dg = cg,
    pg = Qr;
  ((lg = function () {
    var t = this.node,
      e = this.fragment.toString(!1);
    if (
      (window && window.appearsToBeIELessEqual8 && (t.type = 'text/css'),
      t.styleSheet)
    )
      t.styleSheet.cssText = e;
    else {
      for (; t.hasChildNodes(); ) t.removeChild(t.firstChild);
      t.appendChild(document.createTextNode(e));
    }
  }),
    (fg = function () {
      ((this.node.type && 'text/javascript' !== this.node.type) ||
        m(
          'Script tag was updated. This does not cause the code to be re-evaluated!',
          { ractive: this.root }
        ),
        (this.node.text = this.fragment.toString(!1)));
    }));
  var mg = function () {
      var t, e;
      return this.template.y
        ? '<!DOCTYPE' + this.template.dd + '>'
        : ((t = '<' + this.template.e),
          (t +=
            this.attributes.map(Jr).join('') +
            this.conditionalAttributes.map(Jr).join('')),
          'option' === this.name && Gr(this) && (t += ' selected'),
          'input' === this.name && Yr(this) && (t += ' checked'),
          (t += '>'),
          'textarea' === this.name && void 0 !== this.getAttribute('value')
            ? (t += Se(this.getAttribute('value')))
            : void 0 !== this.getAttribute('contenteditable') &&
              (t += this.getAttribute('value') || ''),
          this.fragment &&
            ((e = 'script' !== this.name && 'style' !== this.name),
            (t += this.fragment.toString(e))),
          bl.test(this.template.e) || (t += '</' + this.template.e + '>'),
          t);
    },
    vg = Xr,
    gg = ts,
    yg = function (t) {
      this.init(t);
    };
  yg.prototype = {
    bubble: $p,
    detach: Qp,
    find: Zp,
    findAll: Hp,
    findAllComponents: Kp,
    findComponent: Gp,
    findNextNode: Yp,
    firstNode: Jp,
    getAttribute: Xp,
    init: Sv,
    rebind: Cv,
    render: pg,
    toString: mg,
    unbind: vg,
    unrender: gg,
  };
  var bg = yg,
    wg = /^\s*$/,
    xg = /^\s*/,
    kg = function (t) {
      var e, n, i, r;
      return (
        (e = t.split('\n')),
        (n = e[0]),
        void 0 !== n && wg.test(n) && e.shift(),
        (i = D(e)),
        void 0 !== i && wg.test(i) && e.pop(),
        (r = e.reduce(ns, null)),
        r &&
          (t = e
            .map(function (t) {
              return t.replace(r, '');
            })
            .join('\n')),
        t
      );
    },
    Eg = is,
    _g = function (t, e) {
      var n;
      return e
        ? (n = t
            .split('\n')
            .map(function (t, n) {
              return n ? e + t : t;
            })
            .join('\n'))
        : t;
    },
    Ag = 'Could not find template for partial "%s"',
    Sg = function (t) {
      var e, n;
      ((e = this.parentFragment = t.parentFragment),
        (this.root = e.root),
        (this.type = tc),
        (this.index = t.index),
        (this.name = t.template.r),
        (this.rendered = !1),
        (this.fragment =
          this.fragmentToRender =
          this.fragmentToUnrender =
            null),
        rp.init(this, t),
        this.keypath ||
          ((n = Eg(this.root, this.name, e))
            ? (Dd.call(this), (this.isNamed = !0), this.setTemplate(n))
            : v(Ag, this.name)));
    };
  Sg.prototype = {
    bubble: function () {
      this.parentFragment.bubble();
    },
    detach: function () {
      return this.fragment.detach();
    },
    find: function (t) {
      return this.fragment.find(t);
    },
    findAll: function (t, e) {
      return this.fragment.findAll(t, e);
    },
    findComponent: function (t) {
      return this.fragment.findComponent(t);
    },
    findAllComponents: function (t, e) {
      return this.fragment.findAllComponents(t, e);
    },
    firstNode: function () {
      return this.fragment.firstNode();
    },
    findNextNode: function () {
      return this.parentFragment.findNextNode(this);
    },
    getPartialName: function () {
      return this.isNamed && this.name
        ? this.name
        : void 0 === this.value
          ? this.name
          : this.value;
    },
    getValue: function () {
      return this.fragment.getValue();
    },
    rebind: function (t, e) {
      (this.isNamed || ip.call(this, t, e),
        this.fragment && this.fragment.rebind(t, e));
    },
    render: function () {
      return (
        (this.docFrag = document.createDocumentFragment()),
        this.update(),
        (this.rendered = !0),
        this.docFrag
      );
    },
    resolve: rp.resolve,
    setValue: function (t) {
      var e;
      (void 0 === t || t !== this.value) &&
        (void 0 !== t && (e = Eg(this.root, '' + t, this.parentFragment)),
        !e &&
          this.name &&
          (e = Eg(this.root, this.name, this.parentFragment)) &&
          (Dd.call(this), (this.isNamed = !0)),
        e || v(Ag, this.name, { ractive: this.root }),
        (this.value = t),
        this.setTemplate(e || []),
        this.bubble(),
        this.rendered && mu.addView(this));
    },
    setTemplate: function (t) {
      (this.fragment &&
        (this.fragment.unbind(),
        this.rendered && (this.fragmentToUnrender = this.fragment)),
        (this.fragment = new yb({
          template: t,
          root: this.root,
          owner: this,
          pElement: this.parentFragment.pElement,
        })),
        (this.fragmentToRender = this.fragment));
    },
    toString: function (t) {
      var e, n, i, r;
      return (
        (e = this.fragment.toString(t)),
        (n = this.parentFragment.items[this.index - 1]),
        n && n.type === Zh
          ? ((i = n.text.split('\n').pop()),
            (r = /^\s+$/.exec(i)) ? _g(e, r[0]) : e)
          : e
      );
    },
    unbind: function () {
      (this.isNamed || Dd.call(this), this.fragment && this.fragment.unbind());
    },
    unrender: function (t) {
      this.rendered &&
        (this.fragment && this.fragment.unrender(t), (this.rendered = !1));
    },
    update: function () {
      var t, e;
      (this.fragmentToUnrender &&
        (this.fragmentToUnrender.unrender(!0),
        (this.fragmentToUnrender = null)),
        this.fragmentToRender &&
          (this.docFrag.appendChild(this.fragmentToRender.render()),
          (this.fragmentToRender = null)),
        this.rendered &&
          ((t = this.parentFragment.getNode()),
          (e = this.parentFragment.findNextNode(this)),
          t.insertBefore(this.docFrag, e)));
    },
  };
  var Cg,
    Og,
    Pg,
    Tg = Sg,
    Fg = us,
    Rg = hs,
    jg = new nu('detach'),
    Ng = cs,
    Dg = ls,
    Ig = fs,
    Lg = ds,
    Vg = ps,
    Mg = ms,
    Ug = function (t, e, n, i) {
      var r = t.root,
        s = t.keypath;
      i ? r.viewmodel.smartUpdate(s, e, i) : r.viewmodel.mark(s);
    },
    Wg = [],
    zg = ['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'];
  (zg.forEach(function (t) {
    var e = function () {
      for (var e = arguments.length, n = Array(e), i = 0; e > i; i++)
        n[i] = arguments[i];
      var r, s, o, a;
      for (
        r = mh(this, t, n),
          s = Array.prototype[t].apply(this, arguments),
          mu.start(),
          this._ractive.setting = !0,
          a = this._ractive.wrappers.length;
        a--;

      )
        ((o = this._ractive.wrappers[a]),
          mu.addRactive(o.root),
          Ug(o, this, t, r));
      return (mu.end(), (this._ractive.setting = !1), s);
    };
    xa(Wg, t, { value: e });
  }),
    (Cg = {}),
    Cg.__proto__
      ? ((Og = function (t) {
          t.__proto__ = Wg;
        }),
        (Pg = function (t) {
          t.__proto__ = Array.prototype;
        }))
      : ((Og = function (t) {
          var e, n;
          for (e = zg.length; e--; )
            ((n = zg[e]), xa(t, n, { value: Wg[n], configurable: !0 }));
        }),
        (Pg = function (t) {
          var e;
          for (e = zg.length; e--; ) delete t[zg[e]];
        })),
    (Og.unpatch = Pg));
  var Bg,
    qg,
    $g,
    Qg = Og;
  ((Bg = {
    filter: function (t) {
      return s(t) && (!t._ractive || !t._ractive.setting);
    },
    wrap: function (t, e, n) {
      return new qg(t, e, n);
    },
  }),
    (qg = function (t, e, n) {
      ((this.root = t),
        (this.value = e),
        (this.keypath = _(n)),
        e._ractive ||
          (xa(e, '_ractive', {
            value: { wrappers: [], instances: [], setting: !1 },
            configurable: !0,
          }),
          Qg(e)),
        e._ractive.instances[t._guid] ||
          ((e._ractive.instances[t._guid] = 0), e._ractive.instances.push(t)),
        (e._ractive.instances[t._guid] += 1),
        e._ractive.wrappers.push(this));
    }),
    (qg.prototype = {
      get: function () {
        return this.value;
      },
      teardown: function () {
        var t, e, n, i, r;
        if (
          ((t = this.value),
          (e = t._ractive),
          (n = e.wrappers),
          (i = e.instances),
          e.setting)
        )
          return !1;
        if (((r = n.indexOf(this)), -1 === r)) throw new Error($g);
        if ((n.splice(r, 1), n.length)) {
          if (((i[this.root._guid] -= 1), !i[this.root._guid])) {
            if (((r = i.indexOf(this.root)), -1 === r)) throw new Error($g);
            i.splice(r, 1);
          }
        } else (delete t._ractive, Qg.unpatch(this.value));
      },
    }),
    ($g = 'Something went wrong in a rather interesting way'));
  var Zg,
    Hg,
    Kg = Bg,
    Gg = /^\s*[0-9]+\s*$/,
    Yg = function (t) {
      return Gg.test(t) ? [] : {};
    };
  try {
    (Object.defineProperty({}, 'test', { value: 0 }),
      (Zg = {
        filter: function (t, e, n) {
          var i, r;
          return e
            ? ((e = _(e)),
              (i = n.viewmodel.wrapped[e.parent.str]) && !i.magic
                ? !1
                : ((r = n.viewmodel.get(e.parent)),
                  s(r) && /^[0-9]+$/.test(e.lastKey)
                    ? !1
                    : r && ('object' == typeof r || 'function' == typeof r)))
            : !1;
        },
        wrap: function (t, e, n) {
          return new Hg(t, e, n);
        },
      }),
      (Hg = function (t, e, n) {
        var i, r, s;
        return (
          (n = _(n)),
          (this.magic = !0),
          (this.ractive = t),
          (this.keypath = n),
          (this.value = e),
          (this.prop = n.lastKey),
          (i = n.parent),
          (this.obj = i.isRoot ? t.viewmodel.data : t.viewmodel.get(i)),
          (r = this.originalDescriptor =
            Object.getOwnPropertyDescriptor(this.obj, this.prop)),
          r && r.set && (s = r.set._ractiveWrappers)
            ? void (-1 === s.indexOf(this) && s.push(this))
            : void vs(this, e, r)
        );
      }),
      (Hg.prototype = {
        get: function () {
          return this.value;
        },
        reset: function (t) {
          return this.updating
            ? void 0
            : ((this.updating = !0),
              (this.obj[this.prop] = t),
              mu.addRactive(this.ractive),
              this.ractive.viewmodel.mark(this.keypath, {
                keepExistingWrapper: !0,
              }),
              (this.updating = !1),
              !0);
        },
        set: function (t, e) {
          this.updating ||
            (this.obj[this.prop] ||
              ((this.updating = !0),
              (this.obj[this.prop] = Yg(t)),
              (this.updating = !1)),
            (this.obj[this.prop][t] = e));
        },
        teardown: function () {
          var t, e, n, i, r;
          return this.updating
            ? !1
            : ((t = Object.getOwnPropertyDescriptor(this.obj, this.prop)),
              (e = t && t.set),
              void (
                e &&
                ((i = e._ractiveWrappers),
                (r = i.indexOf(this)),
                -1 !== r && i.splice(r, 1),
                i.length ||
                  ((n = this.obj[this.prop]),
                  Object.defineProperty(
                    this.obj,
                    this.prop,
                    this.originalDescriptor || {
                      writable: !0,
                      enumerable: !0,
                      configurable: !0,
                    }
                  ),
                  (this.obj[this.prop] = n)))
              ));
        },
      }));
  } catch (_a) {
    Zg = !1;
  }
  var Jg,
    Xg,
    ty = Zg;
  ty &&
    ((Jg = {
      filter: function (t, e, n) {
        return ty.filter(t, e, n) && Kg.filter(t);
      },
      wrap: function (t, e, n) {
        return new Xg(t, e, n);
      },
    }),
    (Xg = function (t, e, n) {
      ((this.value = e),
        (this.magic = !0),
        (this.magicWrapper = ty.wrap(t, e, n)),
        (this.arrayWrapper = Kg.wrap(t, e, n)));
    }),
    (Xg.prototype = {
      get: function () {
        return this.value;
      },
      teardown: function () {
        (this.arrayWrapper.teardown(), this.magicWrapper.teardown());
      },
      reset: function (t) {
        return this.magicWrapper.reset(t);
      },
    }));
  var ey = Jg,
    ny = gs,
    iy = {},
    ry = ws,
    sy = xs,
    oy = _s,
    ay = Ps,
    uy = Ts,
    hy = function (t, e) {
      ((this.computation = t),
        (this.viewmodel = t.viewmodel),
        (this.ref = e),
        (this.root = this.viewmodel.ractive),
        (this.parentFragment =
          this.root.component && this.root.component.parentFragment));
    };
  hy.prototype = {
    resolve: function (t) {
      (this.computation.softDeps.push(t),
        (this.computation.unresolvedDeps[t.str] = null),
        this.viewmodel.register(t, this.computation, 'computed'));
    },
  };
  var cy = hy,
    ly = function (t, e) {
      ((this.key = t),
        (this.getter = e.getter),
        (this.setter = e.setter),
        (this.hardDeps = e.deps || []),
        (this.softDeps = []),
        (this.unresolvedDeps = {}),
        (this.depValues = {}),
        (this._dirty = this._firstRun = !0));
    };
  ly.prototype = {
    constructor: ly,
    init: function (t) {
      var e,
        n = this;
      ((this.viewmodel = t),
        (this.bypass = !0),
        (e = t.get(this.key)),
        t.clearCache(this.key.str),
        (this.bypass = !1),
        this.setter && void 0 !== e && this.set(e),
        this.hardDeps &&
          this.hardDeps.forEach(function (e) {
            return t.register(e, n, 'computed');
          }));
    },
    invalidate: function () {
      this._dirty = !0;
    },
    get: function () {
      var t,
        e,
        n = this,
        i = !1;
      if (this.getting) {
        var r =
          'The ' +
          this.key.str +
          " computation indirectly called itself. This probably indicates a bug in the computation. It is commonly caused by `array.sort(...)` - if that's the case, clone the array first with `array.slice().sort(...)`";
        return (p(r), this.value);
      }
      if (((this.getting = !0), this._dirty)) {
        if (
          (this._firstRun || (!this.hardDeps.length && !this.softDeps.length)
            ? (i = !0)
            : [this.hardDeps, this.softDeps].forEach(function (t) {
                var e, r, s;
                if (!i)
                  for (s = t.length; s--; )
                    if (
                      ((e = t[s]),
                      (r = n.viewmodel.get(e)),
                      !a(r, n.depValues[e.str]))
                    )
                      return ((n.depValues[e.str] = r), void (i = !0));
              }),
          i)
        ) {
          this.viewmodel.capture();
          try {
            this.value = this.getter();
          } catch (s) {
            (m('Failed to compute "%s"', this.key.str),
              f(s.stack || s),
              (this.value = void 0));
          }
          ((t = this.viewmodel.release()),
            (e = this.updateDependencies(t)),
            e &&
              [this.hardDeps, this.softDeps].forEach(function (t) {
                t.forEach(function (t) {
                  n.depValues[t.str] = n.viewmodel.get(t);
                });
              }));
        }
        this._dirty = !1;
      }
      return ((this.getting = this._firstRun = !1), this.value);
    },
    set: function (t) {
      if (this.setting) return void (this.value = t);
      if (!this.setter)
        throw new Error(
          'Computed properties without setters are read-only. (This may change in a future version of Ractive!)'
        );
      this.setter(t);
    },
    updateDependencies: function (t) {
      var e, n, i, r, s;
      for (n = this.softDeps, e = n.length; e--; )
        ((i = n[e]),
          -1 === t.indexOf(i) &&
            ((r = !0), this.viewmodel.unregister(i, this, 'computed')));
      for (e = t.length; e--; )
        ((i = t[e]),
          -1 !== n.indexOf(i) ||
            (this.hardDeps && -1 !== this.hardDeps.indexOf(i)) ||
            ((r = !0),
            Fs(this.viewmodel, i) && !this.unresolvedDeps[i.str]
              ? ((s = new cy(this, i.str)),
                t.splice(e, 1),
                (this.unresolvedDeps[i.str] = s),
                mu.addUnresolved(s))
              : this.viewmodel.register(i, this, 'computed')));
      return (r && (this.softDeps = t.slice()), r);
    },
  };
  var fy = ly,
    dy = Rs,
    py = { FAILED_LOOKUP: !0 },
    my = js,
    vy = {},
    gy = Ds,
    yy = Is,
    by = function (t, e) {
      ((this.localKey = t),
        (this.keypath = e.keypath),
        (this.origin = e.origin),
        (this.deps = []),
        (this.unresolved = []),
        (this.resolved = !1));
    };
  by.prototype = {
    forceResolution: function () {
      ((this.keypath = this.localKey), this.setup());
    },
    get: function (t, e) {
      return this.resolved ? this.origin.get(this.map(t), e) : void 0;
    },
    getValue: function () {
      return this.keypath ? this.origin.get(this.keypath) : void 0;
    },
    initViewmodel: function (t) {
      ((this.local = t), this.setup());
    },
    map: function (t) {
      return void 0 === typeof this.keypath
        ? this.localKey
        : t.replace(this.localKey, this.keypath);
    },
    register: function (t, e, n) {
      (this.deps.push({ keypath: t, dep: e, group: n }),
        this.resolved && this.origin.register(this.map(t), e, n));
    },
    resolve: function (t) {
      (void 0 !== this.keypath && this.unbind(!0),
        (this.keypath = t),
        this.setup());
    },
    set: function (t, e) {
      (this.resolved || this.forceResolution(),
        this.origin.set(this.map(t), e));
    },
    setup: function () {
      var t = this;
      void 0 !== this.keypath &&
        ((this.resolved = !0),
        this.deps.length &&
          (this.deps.forEach(function (e) {
            var n = t.map(e.keypath);
            if ((t.origin.register(n, e.dep, e.group), e.dep.setValue))
              e.dep.setValue(t.origin.get(n));
            else {
              if (!e.dep.invalidate)
                throw new Error(
                  'An unexpected error occurred. Please raise an issue at https://github.com/ractivejs/ractive/issues - thanks!'
                );
              e.dep.invalidate();
            }
          }),
          this.origin.mark(this.keypath)));
    },
    setValue: function (t) {
      if (!this.keypath)
        throw new Error(
          'Mapping does not have keypath, cannot set value. Please raise an issue at https://github.com/ractivejs/ractive/issues - thanks!'
        );
      this.origin.set(this.keypath, t);
    },
    unbind: function (t) {
      var e = this;
      (t || delete this.local.mappings[this.localKey],
        this.resolved &&
          (this.deps.forEach(function (t) {
            e.origin.unregister(e.map(t.keypath), t.dep, t.group);
          }),
          this.tracker && this.origin.unregister(this.keypath, this.tracker)));
    },
    unregister: function (t, e, n) {
      var i, r;
      if (this.resolved) {
        for (i = this.deps, r = i.length; r--; )
          if (i[r].dep === e) {
            i.splice(r, 1);
            break;
          }
        this.origin.unregister(this.map(t), e, n);
      }
    },
  };
  var wy = Ls,
    xy = function (t, e) {
      var n, i, r, s;
      return (
        (n = {}),
        (i = 0),
        (r = t.map(function (t, r) {
          var o, a, u;
          ((a = i), (u = e.length));
          do {
            if (((o = e.indexOf(t, a)), -1 === o)) return ((s = !0), -1);
            a = o + 1;
          } while (n[o] && u > a);
          return (o === i && (i += 1), o !== r && (s = !0), (n[o] = !0), o);
        }))
      );
    },
    ky = Vs,
    Ey = {},
    _y = Ws,
    Ay = Bs,
    Sy = qs,
    Cy = $s,
    Oy = Zs,
    Py = { implicit: !0 },
    Ty = { noCascade: !0 },
    Fy = Ks,
    Ry = Gs,
    jy = function (t) {
      var e,
        n,
        i = t.adapt,
        r = t.data,
        s = t.ractive,
        o = t.computed,
        a = t.mappings;
      ((this.ractive = s),
        (this.adaptors = i),
        (this.onchange = t.onchange),
        (this.cache = {}),
        (this.cacheMap = wa(null)),
        (this.deps = { computed: wa(null), default: wa(null) }),
        (this.depsMap = { computed: wa(null), default: wa(null) }),
        (this.patternObservers = []),
        (this.specials = wa(null)),
        (this.wrapped = wa(null)),
        (this.computations = wa(null)),
        (this.captureGroups = []),
        (this.unresolvedImplicitDependencies = []),
        (this.changes = []),
        (this.implicitChanges = {}),
        (this.noCascade = {}),
        (this.data = r),
        (this.mappings = wa(null)));
      for (e in a) this.map(_(e), a[e]);
      if (r)
        for (e in r)
          (n = this.mappings[e]) && void 0 === n.getValue() && n.setValue(r[e]);
      for (e in o)
        (a && e in a && l("Cannot map to a computed property ('%s')", e),
          this.compute(_(e), o[e]));
      this.ready = !0;
    };
  jy.prototype = {
    adapt: ny,
    applyChanges: oy,
    capture: ay,
    clearCache: uy,
    compute: dy,
    get: my,
    init: gy,
    map: yy,
    mark: wy,
    merge: ky,
    register: _y,
    release: Ay,
    reset: Sy,
    set: Cy,
    smartUpdate: Oy,
    teardown: Fy,
    unregister: Ry,
  };
  var Ny = jy;
  Js.prototype = {
    constructor: Js,
    begin: function (t) {
      this.inProcess[t._guid] = !0;
    },
    end: function (t) {
      var e = t.parent;
      (e && this.inProcess[e._guid] ? Xs(this.queue, e).push(t) : to(this, t),
        delete this.inProcess[t._guid]);
    },
  };
  var Dy = Js,
    Iy = eo,
    Ly = /\$\{([^\}]+)\}/g,
    Vy = new nu('construct'),
    My = new nu('config'),
    Uy = new Dy('init'),
    Wy = 0,
    zy = [
      'adaptors',
      'components',
      'decorators',
      'easing',
      'events',
      'interpolators',
      'partials',
      'transitions',
    ],
    By = so,
    qy = co;
  co.prototype = {
    bubble: function () {
      this.dirty || ((this.dirty = !0), mu.addView(this));
    },
    update: function () {
      (this.callback(this.fragment.getValue()), (this.dirty = !1));
    },
    rebind: function (t, e) {
      this.fragment.rebind(t, e);
    },
    unbind: function () {
      this.fragment.unbind();
    },
  };
  var $y = function (t, e, n, r, o) {
      var a,
        u,
        h,
        c,
        l,
        f,
        d = {},
        p = {},
        v = {},
        g = [];
      for (
        u = t.parentFragment,
          h = t.root,
          o = o || {},
          i(d, o),
          o.content = r || [],
          d[''] = o.content,
          e.defaults.el &&
            m(
              'The <%s/> component has a default `el` property; it has been disregarded',
              t.name
            ),
          c = u;
        c;

      ) {
        if (c.owner.type === oc) {
          l = c.owner.container;
          break;
        }
        c = c.parent;
      }
      return (
        n &&
          Object.keys(n).forEach(function (e) {
            var i,
              r,
              o = n[e];
            if ('string' == typeof o) ((i = Af(o)), (p[e] = i ? i.value : o));
            else if (0 === o) p[e] = !0;
            else {
              if (!s(o)) throw new Error('erm wut');
              (fo(o)
                ? ((v[e] = { origin: t.root.viewmodel, keypath: void 0 }),
                  (r = lo(t, o[0], function (t) {
                    t.isSpecial
                      ? f
                        ? a.set(e, t.value)
                        : ((p[e] = t.value), delete v[e])
                      : f
                        ? a.viewmodel.mappings[e].resolve(t)
                        : (v[e].keypath = t);
                  })))
                : (r = new qy(t, o, function (t) {
                    f ? a.set(e, t) : (p[e] = t);
                  })),
                g.push(r));
            }
          }),
        (a = wa(e.prototype)),
        By(
          a,
          {
            el: null,
            append: !0,
            data: p,
            partials: o,
            magic: h.magic || e.defaults.magic,
            modifyArrays: h.modifyArrays,
            adapt: h.adapt,
          },
          {
            parent: h,
            component: t,
            container: l,
            mappings: v,
            inlinePartials: d,
            cssIds: u.cssIds,
          }
        ),
        (f = !0),
        (t.resolvers = g),
        a
      );
    },
    Qy = po,
    Zy = function (t) {
      var e, n;
      for (e = t.root; e; )
        ((n = e._liveComponentQueries['_' + t.name]) && n.push(t.instance),
          (e = e.parent));
    },
    Hy = vo,
    Ky = go,
    Gy = yo,
    Yy = bo,
    Jy = wo,
    Xy = new nu('teardown'),
    tb = ko,
    eb = function (t, e) {
      this.init(t, e);
    };
  eb.prototype = {
    detach: Rg,
    find: Ng,
    findAll: Dg,
    findAllComponents: Ig,
    findComponent: Lg,
    findNextNode: Vg,
    firstNode: Mg,
    init: Hy,
    rebind: Ky,
    render: Gy,
    toString: Yy,
    unbind: Jy,
    unrender: tb,
  };
  var nb = eb,
    ib = function (t) {
      ((this.type = ec), (this.value = t.template.c));
    };
  ib.prototype = {
    detach: Rd,
    firstNode: function () {
      return this.node;
    },
    render: function () {
      return (
        this.node || (this.node = document.createComment(this.value)),
        this.node
      );
    },
    toString: function () {
      return '<!--' + this.value + '-->';
    },
    unrender: function (t) {
      t && this.node.parentNode.removeChild(this.node);
    },
  };
  var rb = ib,
    sb = function (t) {
      var e, n;
      ((this.type = oc),
        (this.container = e = t.parentFragment.root),
        (this.component = n = e.component),
        (this.container = e),
        (this.containerFragment = t.parentFragment),
        (this.parentFragment = n.parentFragment));
      var i = (this.name = t.template.n || ''),
        r = e._inlinePartials[i];
      (r ||
        (m('Could not find template for partial "' + i + '"', {
          ractive: t.root,
        }),
        (r = [])),
        (this.fragment = new yb({
          owner: this,
          root: e.parent,
          template: r,
          pElement: this.containerFragment.pElement,
        })),
        s(n.yielders[i]) ? n.yielders[i].push(this) : (n.yielders[i] = [this]),
        mu.scheduleTask(function () {
          if (n.yielders[i].length > 1)
            throw new Error(
              'A component template can only have one {{yield' +
                (i ? ' ' + i : '') +
                '}} declaration at a time'
            );
        }));
    };
  sb.prototype = {
    detach: function () {
      return this.fragment.detach();
    },
    find: function (t) {
      return this.fragment.find(t);
    },
    findAll: function (t, e) {
      return this.fragment.findAll(t, e);
    },
    findComponent: function (t) {
      return this.fragment.findComponent(t);
    },
    findAllComponents: function (t, e) {
      return this.fragment.findAllComponents(t, e);
    },
    findNextNode: function () {
      return this.containerFragment.findNextNode(this);
    },
    firstNode: function () {
      return this.fragment.firstNode();
    },
    getValue: function (t) {
      return this.fragment.getValue(t);
    },
    render: function () {
      return this.fragment.render();
    },
    unbind: function () {
      this.fragment.unbind();
    },
    unrender: function (t) {
      (this.fragment.unrender(t), I(this.component.yielders[this.name], this));
    },
    rebind: function (t, e) {
      this.fragment.rebind(t, e);
    },
    toString: function () {
      return this.fragment.toString();
    },
  };
  var ob = sb,
    ab = function (t) {
      this.declaration = t.template.a;
    };
  ab.prototype = {
    init: Fa,
    render: Fa,
    unrender: Fa,
    teardown: Fa,
    toString: function () {
      return '<!DOCTYPE' + this.declaration + '>';
    },
  };
  var ub = ab,
    hb = Eo,
    cb = Ao,
    lb = So,
    fb = Co,
    db = To,
    pb = Ro,
    mb = function (t) {
      this.init(t);
    };
  mb.prototype = {
    bubble: wd,
    detach: xd,
    find: kd,
    findAll: Ed,
    findAllComponents: _d,
    findComponent: Ad,
    findNextNode: Sd,
    firstNode: Cd,
    getArgsList: Pd,
    getNode: Td,
    getValue: Fd,
    init: hb,
    rebind: cb,
    registerIndexRef: function (t) {
      var e = this.registeredIndexRefs;
      -1 === e.indexOf(t) && e.push(t);
    },
    render: lb,
    toString: fb,
    unbind: db,
    unregisterIndexRef: function (t) {
      var e = this.registeredIndexRefs;
      e.splice(e.indexOf(t), 1);
    },
    unrender: pb,
  };
  var vb,
    gb,
    yb = mb,
    bb = jo,
    wb = ['template', 'partials', 'components', 'decorators', 'events'],
    xb = new nu('reset'),
    kb = function (t, e) {
      function n(e, i, r) {
        (r && r.partials[t]) ||
          e.forEach(function (e) {
            (e.type === tc && e.getPartialName() === t && i.push(e),
              e.fragment && n(e.fragment.items, i, r),
              s(e.fragments)
                ? n(e.fragments, i, r)
                : s(e.items)
                  ? n(e.items, i, r)
                  : e.type === sc &&
                    e.instance &&
                    n(e.instance.fragment.items, i, e.instance),
              e.type === Xh &&
                (s(e.attributes) && n(e.attributes, i, r),
                s(e.conditionalAttributes) &&
                  n(e.conditionalAttributes, i, r)));
          });
      }
      var i,
        r = [];
      return (
        n(this.fragment.items, r),
        (this.partials[t] = e),
        (i = mu.start(this, !0)),
        r.forEach(function (e) {
          ((e.value = void 0), e.setValue(t));
        }),
        mu.end(),
        i
      );
    },
    Eb = No,
    _b = gh('reverse'),
    Ab = Do,
    Sb = gh('shift'),
    Cb = gh('sort'),
    Ob = gh('splice'),
    Pb = Lo,
    Tb = Vo,
    Fb = new nu('teardown'),
    Rb = Uo,
    jb = Wo,
    Nb = zo,
    Db = new nu('unrender'),
    Ib = gh('unshift'),
    Lb = Bo,
    Vb = new nu('update'),
    Mb = qo,
    Ub = {
      add: Ga,
      animate: xu,
      detach: Eu,
      find: Au,
      findAll: Nu,
      findAllComponents: Du,
      findComponent: Iu,
      findContainer: Lu,
      findParent: Vu,
      fire: zu,
      get: Bu,
      insert: $u,
      merge: Zu,
      observe: uh,
      observeOnce: hh,
      off: fh,
      on: dh,
      once: ph,
      pop: yh,
      push: bh,
      render: Sh,
      reset: bb,
      resetPartial: kb,
      resetTemplate: Eb,
      reverse: _b,
      set: Ab,
      shift: Sb,
      sort: Cb,
      splice: Ob,
      subtract: Pb,
      teardown: Tb,
      toggle: Rb,
      toHTML: jb,
      toHtml: jb,
      unrender: Nb,
      unshift: Ib,
      update: Lb,
      updateModel: Mb,
    },
    Wb = function (t, e, n) {
      return n || Qo(t, e)
        ? function () {
            var n,
              i = '_super' in this,
              r = this._super;
            return (
              (this._super = e),
              (n = t.apply(this, arguments)),
              i && (this._super = r),
              n
            );
          }
        : t;
    },
    zb = Zo,
    Bb = Yo,
    qb = function (t) {
      var e,
        n,
        i = {};
      return t && (e = t._ractive)
        ? ((i.ractive = e.root),
          (i.keypath = e.keypath.str),
          (i.index = {}),
          (n = qd(e.proxy.parentFragment)) && (i.index = qd.resolve(n)),
          i)
        : i;
    };
  ((vb = function (t) {
    return this instanceof vb ? void By(this, t) : new vb(t);
  }),
    (gb = {
      DEBUG: { writable: !0, value: !0 },
      DEBUG_PROMISES: { writable: !0, value: !0 },
      extend: { value: Bb },
      getNodeInfo: { value: qb },
      parse: { value: Kf },
      Promise: { value: ou },
      svg: { value: ra },
      magic: { value: na },
      VERSION: { value: '0.7.3' },
      adaptors: { writable: !0, value: {} },
      components: { writable: !0, value: {} },
      decorators: { writable: !0, value: {} },
      easing: { writable: !0, value: ha },
      events: { writable: !0, value: {} },
      interpolators: { writable: !0, value: Ma },
      partials: { writable: !0, value: {} },
      transitions: { writable: !0, value: {} },
    }),
    ka(vb, gb),
    (vb.prototype = i(Ub, ua)),
    (vb.prototype.constructor = vb),
    (vb.defaults = vb.prototype));
  var $b = 'function';
  if (
    typeof Date.now !== $b ||
    typeof String.prototype.trim !== $b ||
    typeof Object.keys !== $b ||
    typeof Array.prototype.indexOf !== $b ||
    typeof Array.prototype.forEach !== $b ||
    typeof Array.prototype.map !== $b ||
    typeof Array.prototype.filter !== $b ||
    ('undefined' != typeof window && typeof window.addEventListener !== $b)
  )
    throw new Error(
      "It looks like you're attempting to use Ractive.js in an older browser. You'll need to use one of the 'legacy builds' in order to continue - see http://docs.ractivejs.org/latest/legacy-builds for more information."
    );
  var Qb = vb;
  return Qb;
});
//# sourceMappingURL=ractive.min.js.map
