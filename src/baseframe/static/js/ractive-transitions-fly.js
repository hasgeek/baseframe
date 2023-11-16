!(function (t, e) {
  'object' == typeof exports && 'undefined' != typeof module
    ? (module.exports = e())
    : 'function' == typeof define && define.amd
      ? define(e)
      : (t.Ractive.transitions.fly = e());
})(this, function () {
  'use strict';
  function t(t) {
    return 0 === t || 'string' == typeof t ? t : t + 'px';
  }
  function e(e, o) {
    var i, r, a, s;
    (o = e.processParams(o, n)),
      (i = t(o.x)),
      (r = t(o.y)),
      (a = { transform: 'translate(' + i + ',' + r + ')', opacity: 0 }),
      e.isIntro
        ? ((s = e.getStyle(['opacity', 'transform'])), e.setStyle(a))
        : (s = a),
      e.animateStyle(s, o).then(e.complete);
  }
  var n = { duration: 400, easing: 'easeOut', opacity: 0, x: -500, y: 0 };
  return e;
});
