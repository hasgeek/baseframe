/*! jQRangeSlider 5.3.0 - 2013-07-12 - Copyright (C) Guillaume Gautreau 2012 - MIT and GPLv3 licenses.*/ (!(function (
  a
) {
  'use strict';
  a.widget('ui.rangeSliderMouseTouch', a.ui.mouse, {
    enabled: !0,
    _mouseInit: function () {
      var b = this;
      (a.ui.mouse.prototype._mouseInit.apply(this),
        (this._mouseDownEvent = !1),
        this.element.bind('touchstart.' + this.widgetName, function (a) {
          return b._touchStart(a);
        }));
    },
    _mouseDestroy: function () {
      (a(document)
        .unbind('touchmove.' + this.widgetName, this._touchMoveDelegate)
        .unbind('touchend.' + this.widgetName, this._touchEndDelegate),
        a.ui.mouse.prototype._mouseDestroy.apply(this));
    },
    enable: function () {
      this.enabled = !0;
    },
    disable: function () {
      this.enabled = !1;
    },
    destroy: function () {
      (this._mouseDestroy(),
        a.ui.mouse.prototype.destroy.apply(this),
        (this._mouseInit = null));
    },
    _touchStart: function (b) {
      if (!this.enabled) return !1;
      ((b.which = 1), b.preventDefault(), this._fillTouchEvent(b));
      var c = this,
        d = this._mouseDownEvent;
      (this._mouseDown(b),
        d !== this._mouseDownEvent &&
          ((this._touchEndDelegate = function (a) {
            c._touchEnd(a);
          }),
          (this._touchMoveDelegate = function (a) {
            c._touchMove(a);
          }),
          a(document)
            .bind('touchmove.' + this.widgetName, this._touchMoveDelegate)
            .bind('touchend.' + this.widgetName, this._touchEndDelegate)));
    },
    _mouseDown: function (b) {
      return this.enabled
        ? a.ui.mouse.prototype._mouseDown.apply(this, [b])
        : !1;
    },
    _touchEnd: function (b) {
      (this._fillTouchEvent(b),
        this._mouseUp(b),
        a(document)
          .unbind('touchmove.' + this.widgetName, this._touchMoveDelegate)
          .unbind('touchend.' + this.widgetName, this._touchEndDelegate),
        (this._mouseDownEvent = !1),
        a(document).trigger('mouseup'));
    },
    _touchMove: function (a) {
      return (a.preventDefault(), this._fillTouchEvent(a), this._mouseMove(a));
    },
    _fillTouchEvent: function (a) {
      var b;
      ((b =
        'undefined' == typeof a.targetTouches &&
        'undefined' == typeof a.changedTouches
          ? a.originalEvent.targetTouches[0] ||
            a.originalEvent.changedTouches[0]
          : a.targetTouches[0] || a.changedTouches[0]),
        (a.pageX = b.pageX),
        (a.pageY = b.pageY));
    },
  });
})(jQuery),
  (function (a) {
    'use strict';
    a.widget('ui.rangeSliderDraggable', a.ui.rangeSliderMouseTouch, {
      cache: null,
      options: { containment: null },
      _create: function () {
        (a.ui.rangeSliderMouseTouch.prototype._create.apply(this),
          setTimeout(a.proxy(this._initElementIfNotDestroyed, this), 10));
      },
      destroy: function () {
        ((this.cache = null),
          a.ui.rangeSliderMouseTouch.prototype.destroy.apply(this));
      },
      _initElementIfNotDestroyed: function () {
        this._mouseInit && this._initElement();
      },
      _initElement: function () {
        (this._mouseInit(), this._cache());
      },
      _setOption: function (b, c) {
        'containment' === b &&
          (this.options.containment =
            null === c || 0 === a(c).length ? null : a(c));
      },
      _mouseStart: function (a) {
        return (
          this._cache(),
          (this.cache.click = { left: a.pageX, top: a.pageY }),
          (this.cache.initialOffset = this.element.offset()),
          this._triggerMouseEvent('mousestart'),
          !0
        );
      },
      _mouseDrag: function (a) {
        var b = a.pageX - this.cache.click.left;
        return (
          (b = this._constraintPosition(b + this.cache.initialOffset.left)),
          this._applyPosition(b),
          this._triggerMouseEvent('sliderDrag'),
          !1
        );
      },
      _mouseStop: function () {
        this._triggerMouseEvent('stop');
      },
      _constraintPosition: function (a) {
        return (
          0 !== this.element.parent().length &&
            null !== this.cache.parent.offset &&
            ((a = Math.min(
              a,
              this.cache.parent.offset.left +
                this.cache.parent.width -
                this.cache.width.outer
            )),
            (a = Math.max(a, this.cache.parent.offset.left))),
          a
        );
      },
      _applyPosition: function (a) {
        var b = { top: this.cache.offset.top, left: a };
        (this.element.offset({ left: a }), (this.cache.offset = b));
      },
      _cacheIfNecessary: function () {
        null === this.cache && this._cache();
      },
      _cache: function () {
        ((this.cache = {}),
          this._cacheMargins(),
          this._cacheParent(),
          this._cacheDimensions(),
          (this.cache.offset = this.element.offset()));
      },
      _cacheMargins: function () {
        this.cache.margin = {
          left: this._parsePixels(this.element, 'marginLeft'),
          right: this._parsePixels(this.element, 'marginRight'),
          top: this._parsePixels(this.element, 'marginTop'),
          bottom: this._parsePixels(this.element, 'marginBottom'),
        };
      },
      _cacheParent: function () {
        if (null !== this.options.parent) {
          var a = this.element.parent();
          this.cache.parent = { offset: a.offset(), width: a.width() };
        } else this.cache.parent = null;
      },
      _cacheDimensions: function () {
        this.cache.width = {
          outer: this.element.outerWidth(),
          inner: this.element.width(),
        };
      },
      _parsePixels: function (a, b) {
        return parseInt(a.css(b), 10) || 0;
      },
      _triggerMouseEvent: function (a) {
        var b = this._prepareEventData();
        this.element.trigger(a, b);
      },
      _prepareEventData: function () {
        return { element: this.element, offset: this.cache.offset || null };
      },
    });
  })(jQuery),
  (function (a, b) {
    'use strict';
    a.widget('ui.rangeSlider', {
      options: {
        bounds: { min: 0, max: 100 },
        defaultValues: { min: 20, max: 50 },
        wheelMode: null,
        wheelSpeed: 4,
        arrows: !0,
        valueLabels: 'show',
        formatter: null,
        durationIn: 0,
        durationOut: 400,
        delayOut: 200,
        range: { min: !1, max: !1 },
        step: !1,
        scales: !1,
        enabled: !0,
      },
      _values: null,
      _valuesChanged: !1,
      bar: null,
      leftHandle: null,
      rightHandle: null,
      innerBar: null,
      container: null,
      arrows: null,
      labels: null,
      changing: { min: !1, max: !1 },
      changed: { min: !1, max: !1 },
      ruler: null,
      _create: function () {
        (this._setDefaultValues(),
          (this.labels = {
            left: null,
            right: null,
            leftDisplayed: !0,
            rightDisplayed: !0,
          }),
          (this.arrows = { left: null, right: null }),
          (this.changing = { min: !1, max: !1 }),
          (this.changed = { min: !1, max: !1 }),
          this._createElements(),
          this._bindResize(),
          setTimeout(a.proxy(this.resize, this), 1),
          setTimeout(a.proxy(this._initValues, this), 1));
      },
      _setDefaultValues: function () {
        this._values = {
          min: this.options.defaultValues.min,
          max: this.options.defaultValues.max,
        };
      },
      _bindResize: function () {
        var b = this;
        ((this._resizeProxy = function (a) {
          b.resize(a);
        }),
          a(window).resize(this._resizeProxy));
      },
      _initWidth: function () {
        (this.container.css(
          'width',
          this.element.width() -
            this.container.outerWidth(!0) +
            this.container.width()
        ),
          this.innerBar.css(
            'width',
            this.container.width() -
              this.innerBar.outerWidth(!0) +
              this.innerBar.width()
          ));
      },
      _initValues: function () {
        this.values(this._values.min, this._values.max);
      },
      _setOption: function (a, b) {
        (this._setWheelOption(a, b),
          this._setArrowsOption(a, b),
          this._setLabelsOption(a, b),
          this._setLabelsDurations(a, b),
          this._setFormatterOption(a, b),
          this._setBoundsOption(a, b),
          this._setRangeOption(a, b),
          this._setStepOption(a, b),
          this._setScalesOption(a, b),
          this._setEnabledOption(a, b));
      },
      _validProperty: function (a, b, c) {
        return null === a || 'undefined' == typeof a[b] ? c : a[b];
      },
      _setStepOption: function (a, b) {
        'step' === a &&
          ((this.options.step = b),
          this._leftHandle('option', 'step', b),
          this._rightHandle('option', 'step', b),
          this._changed(!0));
      },
      _setScalesOption: function (a, b) {
        'scales' === a &&
          (b === !1 || null === b
            ? ((this.options.scales = !1), this._destroyRuler())
            : b instanceof Array &&
              ((this.options.scales = b), this._updateRuler()));
      },
      _setRangeOption: function (a, b) {
        'range' === a &&
          (this._bar('option', 'range', b),
          (this.options.range = this._bar('option', 'range')),
          this._changed(!0));
      },
      _setBoundsOption: function (a, b) {
        'bounds' === a &&
          'undefined' != typeof b.min &&
          'undefined' != typeof b.max &&
          this.bounds(b.min, b.max);
      },
      _setWheelOption: function (a, b) {
        ('wheelMode' === a || 'wheelSpeed' === a) &&
          (this._bar('option', a, b),
          (this.options[a] = this._bar('option', a)));
      },
      _setLabelsOption: function (a, b) {
        if ('valueLabels' === a) {
          if ('hide' !== b && 'show' !== b && 'change' !== b) return;
          ((this.options.valueLabels = b),
            'hide' !== b
              ? (this._createLabels(),
                this._leftLabel('update'),
                this._rightLabel('update'))
              : this._destroyLabels());
        }
      },
      _setFormatterOption: function (a, b) {
        'formatter' === a &&
          null !== b &&
          'function' == typeof b &&
          ((this.options.formatter = b),
          'hide' !== this.options.valueLabels &&
            (this._destroyLabels(), this._createLabels()));
      },
      _setArrowsOption: function (a, b) {
        'arrows' !== a ||
          (b !== !0 && b !== !1) ||
          b === this.options.arrows ||
          (b === !0
            ? (this.element
                .removeClass('ui-rangeSlider-noArrow')
                .addClass('ui-rangeSlider-withArrows'),
              this.arrows.left.css('display', 'block'),
              this.arrows.right.css('display', 'block'),
              (this.options.arrows = !0))
            : b === !1 &&
              (this.element
                .addClass('ui-rangeSlider-noArrow')
                .removeClass('ui-rangeSlider-withArrows'),
              this.arrows.left.css('display', 'none'),
              this.arrows.right.css('display', 'none'),
              (this.options.arrows = !1)),
          this._initWidth());
      },
      _setLabelsDurations: function (a, b) {
        if ('durationIn' === a || 'durationOut' === a || 'delayOut' === a) {
          if (parseInt(b, 10) !== b) return;
          (null !== this.labels.left && this._leftLabel('option', a, b),
            null !== this.labels.right && this._rightLabel('option', a, b),
            (this.options[a] = b));
        }
      },
      _setEnabledOption: function (a, b) {
        'enabled' === a && this.toggle(b);
      },
      _createElements: function () {
        ('absolute' !== this.element.css('position') &&
          this.element.css('position', 'relative'),
          this.element.addClass('ui-rangeSlider'),
          (this.container = a("<div class='ui-rangeSlider-container' />")
            .css('position', 'absolute')
            .appendTo(this.element)),
          (this.innerBar = a("<div class='ui-rangeSlider-innerBar' />")
            .css('position', 'absolute')
            .css('top', 0)
            .css('left', 0)),
          this._createHandles(),
          this._createBar(),
          this.container.prepend(this.innerBar),
          this._createArrows(),
          'hide' !== this.options.valueLabels
            ? this._createLabels()
            : this._destroyLabels(),
          this._updateRuler(),
          this.options.enabled || this._toggle(this.options.enabled));
      },
      _createHandle: function (b) {
        return a('<div />')
          [this._handleType()](b)
          .bind('sliderDrag', a.proxy(this._changing, this))
          .bind('stop', a.proxy(this._changed, this));
      },
      _createHandles: function () {
        ((this.leftHandle = this._createHandle({
          isLeft: !0,
          bounds: this.options.bounds,
          value: this._values.min,
          step: this.options.step,
        }).appendTo(this.container)),
          (this.rightHandle = this._createHandle({
            isLeft: !1,
            bounds: this.options.bounds,
            value: this._values.max,
            step: this.options.step,
          }).appendTo(this.container)));
      },
      _createBar: function () {
        ((this.bar = a('<div />')
          .prependTo(this.container)
          .bind('sliderDrag scroll zoom', a.proxy(this._changing, this))
          .bind('stop', a.proxy(this._changed, this))),
          this._bar({
            leftHandle: this.leftHandle,
            rightHandle: this.rightHandle,
            values: { min: this._values.min, max: this._values.max },
            type: this._handleType(),
            range: this.options.range,
            wheelMode: this.options.wheelMode,
            wheelSpeed: this.options.wheelSpeed,
          }),
          (this.options.range = this._bar('option', 'range')),
          (this.options.wheelMode = this._bar('option', 'wheelMode')),
          (this.options.wheelSpeed = this._bar('option', 'wheelSpeed')));
      },
      _createArrows: function () {
        ((this.arrows.left = this._createArrow('left')),
          (this.arrows.right = this._createArrow('right')),
          this.options.arrows
            ? this.element.addClass('ui-rangeSlider-withArrows')
            : (this.arrows.left.css('display', 'none'),
              this.arrows.right.css('display', 'none'),
              this.element.addClass('ui-rangeSlider-noArrow')));
      },
      _createArrow: function (b) {
        var c,
          d = a("<div class='ui-rangeSlider-arrow' />")
            .append("<div class='ui-rangeSlider-arrow-inner' />")
            .addClass('ui-rangeSlider-' + b + 'Arrow')
            .css('position', 'absolute')
            .css(b, 0)
            .appendTo(this.element);
        return (
          (c =
            'right' === b
              ? a.proxy(this._scrollRightClick, this)
              : a.proxy(this._scrollLeftClick, this)),
          d.bind('mousedown touchstart', c),
          d
        );
      },
      _proxy: function (a, b, c) {
        var d = Array.prototype.slice.call(c);
        return a[b].apply(a, d);
      },
      _handleType: function () {
        return 'rangeSliderHandle';
      },
      _barType: function () {
        return 'rangeSliderBar';
      },
      _bar: function () {
        return this._proxy(this.bar, this._barType(), arguments);
      },
      _labelType: function () {
        return 'rangeSliderLabel';
      },
      _leftLabel: function () {
        return this._proxy(this.labels.left, this._labelType(), arguments);
      },
      _rightLabel: function () {
        return this._proxy(this.labels.right, this._labelType(), arguments);
      },
      _leftHandle: function () {
        return this._proxy(this.leftHandle, this._handleType(), arguments);
      },
      _rightHandle: function () {
        return this._proxy(this.rightHandle, this._handleType(), arguments);
      },
      _getValue: function (a, b) {
        return (
          b === this.rightHandle && (a -= b.outerWidth()),
          (a * (this.options.bounds.max - this.options.bounds.min)) /
            (this.container.innerWidth() - b.outerWidth(!0)) +
            this.options.bounds.min
        );
      },
      _trigger: function (a) {
        var b = this;
        setTimeout(function () {
          b.element.trigger(a, { label: b.element, values: b.values() });
        }, 1);
      },
      _changing: function () {
        this._updateValues() &&
          (this._trigger('valuesChanging'), (this._valuesChanged = !0));
      },
      _changed: function (a) {
        (this._updateValues() || this._valuesChanged) &&
          (this._trigger('valuesChanged'),
          a !== !0 && this._trigger('userValuesChanged'),
          (this._valuesChanged = !1));
      },
      _updateValues: function () {
        var a = this._leftHandle('value'),
          b = this._rightHandle('value'),
          c = this._min(a, b),
          d = this._max(a, b),
          e = c !== this._values.min || d !== this._values.max;
        return (
          (this._values.min = this._min(a, b)),
          (this._values.max = this._max(a, b)),
          e
        );
      },
      _min: function (a, b) {
        return Math.min(a, b);
      },
      _max: function (a, b) {
        return Math.max(a, b);
      },
      _createLabel: function (b, c) {
        var d;
        return (
          null === b
            ? ((d = this._getLabelConstructorParameters(b, c)),
              (b = a('<div />').appendTo(this.element)[this._labelType()](d)))
            : ((d = this._getLabelRefreshParameters(b, c)),
              b[this._labelType()](d)),
          b
        );
      },
      _getLabelConstructorParameters: function (a, b) {
        return {
          handle: b,
          handleType: this._handleType(),
          formatter: this._getFormatter(),
          show: this.options.valueLabels,
          durationIn: this.options.durationIn,
          durationOut: this.options.durationOut,
          delayOut: this.options.delayOut,
        };
      },
      _getLabelRefreshParameters: function () {
        return {
          formatter: this._getFormatter(),
          show: this.options.valueLabels,
          durationIn: this.options.durationIn,
          durationOut: this.options.durationOut,
          delayOut: this.options.delayOut,
        };
      },
      _getFormatter: function () {
        return this.options.formatter === !1 || null === this.options.formatter
          ? this._defaultFormatter
          : this.options.formatter;
      },
      _defaultFormatter: function (a) {
        return Math.round(a);
      },
      _destroyLabel: function (a) {
        return (
          null !== a &&
            (a[this._labelType()]('destroy'), a.remove(), (a = null)),
          a
        );
      },
      _createLabels: function () {
        ((this.labels.left = this._createLabel(
          this.labels.left,
          this.leftHandle
        )),
          (this.labels.right = this._createLabel(
            this.labels.right,
            this.rightHandle
          )),
          this._leftLabel('pair', this.labels.right));
      },
      _destroyLabels: function () {
        ((this.labels.left = this._destroyLabel(this.labels.left)),
          (this.labels.right = this._destroyLabel(this.labels.right)));
      },
      _stepRatio: function () {
        return this._leftHandle('stepRatio');
      },
      _scrollRightClick: function (a) {
        return this.options.enabled
          ? (a.preventDefault(),
            this._bar('startScroll'),
            this._bindStopScroll(),
            this._continueScrolling('scrollRight', 4 * this._stepRatio(), 1),
            void 0)
          : !1;
      },
      _continueScrolling: function (a, b, c, d) {
        if (!this.options.enabled) return !1;
        (this._bar(a, c), (d = d || 5), d--);
        var e = this,
          f = 16,
          g = Math.max(1, 4 / this._stepRatio());
        this._scrollTimeout = setTimeout(function () {
          (0 === d &&
            (b > f ? (b = Math.max(f, b / 1.5)) : (c = Math.min(g, 2 * c)),
            (d = 5)),
            e._continueScrolling(a, b, c, d));
        }, b);
      },
      _scrollLeftClick: function (a) {
        return this.options.enabled
          ? (a.preventDefault(),
            this._bar('startScroll'),
            this._bindStopScroll(),
            this._continueScrolling('scrollLeft', 4 * this._stepRatio(), 1),
            void 0)
          : !1;
      },
      _bindStopScroll: function () {
        var b = this;
        ((this._stopScrollHandle = function (a) {
          (a.preventDefault(), b._stopScroll());
        }),
          a(document).bind('mouseup touchend', this._stopScrollHandle));
      },
      _stopScroll: function () {
        (a(document).unbind('mouseup touchend', this._stopScrollHandle),
          (this._stopScrollHandle = null),
          this._bar('stopScroll'),
          clearTimeout(this._scrollTimeout));
      },
      _createRuler: function () {
        this.ruler = a("<div class='ui-rangeSlider-ruler' />").appendTo(
          this.innerBar
        );
      },
      _setRulerParameters: function () {
        this.ruler.ruler({
          min: this.options.bounds.min,
          max: this.options.bounds.max,
          scales: this.options.scales,
        });
      },
      _destroyRuler: function () {
        null !== this.ruler &&
          a.fn.ruler &&
          (this.ruler.ruler('destroy'),
          this.ruler.remove(),
          (this.ruler = null));
      },
      _updateRuler: function () {
        (this._destroyRuler(),
          this.options.scales !== !1 &&
            a.fn.ruler &&
            (this._createRuler(), this._setRulerParameters()));
      },
      values: function (a, b) {
        var c = this._bar('values', a, b);
        return (
          'undefined' != typeof a &&
            'undefined' != typeof b &&
            this._changed(!0),
          c
        );
      },
      min: function (a) {
        return (
          (this._values.min = this.values(a, this._values.max).min),
          this._values.min
        );
      },
      max: function (a) {
        return (
          (this._values.max = this.values(this._values.min, a).max),
          this._values.max
        );
      },
      bounds: function (a, b) {
        return (
          this._isValidValue(a) &&
            this._isValidValue(b) &&
            b > a &&
            (this._setBounds(a, b), this._updateRuler(), this._changed(!0)),
          this.options.bounds
        );
      },
      _isValidValue: function (a) {
        return 'undefined' != typeof a && parseFloat(a) === a;
      },
      _setBounds: function (a, b) {
        ((this.options.bounds = { min: a, max: b }),
          this._leftHandle('option', 'bounds', this.options.bounds),
          this._rightHandle('option', 'bounds', this.options.bounds),
          this._bar('option', 'bounds', this.options.bounds));
      },
      zoomIn: function (a) {
        this._bar('zoomIn', a);
      },
      zoomOut: function (a) {
        this._bar('zoomOut', a);
      },
      scrollLeft: function (a) {
        (this._bar('startScroll'),
          this._bar('scrollLeft', a),
          this._bar('stopScroll'));
      },
      scrollRight: function (a) {
        (this._bar('startScroll'),
          this._bar('scrollRight', a),
          this._bar('stopScroll'));
      },
      resize: function () {
        (this._initWidth(),
          this._leftHandle('update'),
          this._rightHandle('update'),
          this._bar('update'));
      },
      enable: function () {
        this.toggle(!0);
      },
      disable: function () {
        this.toggle(!1);
      },
      toggle: function (a) {
        (a === b && (a = !this.options.enabled),
          this.options.enabled !== a && this._toggle(a));
      },
      _toggle: function (a) {
        ((this.options.enabled = a),
          this.element.toggleClass('ui-rangeSlider-disabled', !a));
        var b = a ? 'enable' : 'disable';
        (this._bar(b),
          this._leftHandle(b),
          this._rightHandle(b),
          this._leftLabel(b),
          this._rightLabel(b));
      },
      destroy: function () {
        (this.element.removeClass(
          'ui-rangeSlider-withArrows ui-rangeSlider-noArrow ui-rangeSlider-disabled'
        ),
          this._destroyWidgets(),
          this._destroyElements(),
          this.element.removeClass('ui-rangeSlider'),
          (this.options = null),
          a(window).unbind('resize', this._resizeProxy),
          (this._resizeProxy = null),
          (this._bindResize = null),
          a.Widget.prototype.destroy.apply(this, arguments));
      },
      _destroyWidget: function (a) {
        (this['_' + a]('destroy'), this[a].remove(), (this[a] = null));
      },
      _destroyWidgets: function () {
        (this._destroyWidget('bar'),
          this._destroyWidget('leftHandle'),
          this._destroyWidget('rightHandle'),
          this._destroyRuler(),
          this._destroyLabels());
      },
      _destroyElements: function () {
        (this.container.remove(),
          (this.container = null),
          this.innerBar.remove(),
          (this.innerBar = null),
          this.arrows.left.remove(),
          this.arrows.right.remove(),
          (this.arrows = null));
      },
    });
  })(jQuery),
  (function (a) {
    'use strict';
    a.widget('ui.rangeSliderHandle', a.ui.rangeSliderDraggable, {
      currentMove: null,
      margin: 0,
      parentElement: null,
      options: {
        isLeft: !0,
        bounds: { min: 0, max: 100 },
        range: !1,
        value: 0,
        step: !1,
      },
      _value: 0,
      _left: 0,
      _create: function () {
        (a.ui.rangeSliderDraggable.prototype._create.apply(this),
          this.element
            .css('position', 'absolute')
            .css('top', 0)
            .addClass('ui-rangeSlider-handle')
            .toggleClass('ui-rangeSlider-leftHandle', this.options.isLeft)
            .toggleClass('ui-rangeSlider-rightHandle', !this.options.isLeft),
          this.element.append("<div class='ui-rangeSlider-handle-inner' />"),
          (this._value = this._constraintValue(this.options.value)));
      },
      destroy: function () {
        (this.element.empty(),
          a.ui.rangeSliderDraggable.prototype.destroy.apply(this));
      },
      _setOption: function (b, c) {
        ('isLeft' !== b || (c !== !0 && c !== !1) || c === this.options.isLeft
          ? 'step' === b && this._checkStep(c)
            ? ((this.options.step = c), this.update())
            : 'bounds' === b
              ? ((this.options.bounds = c), this.update())
              : 'range' === b &&
                this._checkRange(c) &&
                ((this.options.range = c), this.update())
          : ((this.options.isLeft = c),
            this.element
              .toggleClass('ui-rangeSlider-leftHandle', this.options.isLeft)
              .toggleClass('ui-rangeSlider-rightHandle', !this.options.isLeft),
            this._position(this._value),
            this.element.trigger('switch', this.options.isLeft)),
          a.ui.rangeSliderDraggable.prototype._setOption.apply(this, [b, c]));
      },
      _checkRange: function (a) {
        return (
          a === !1 || (!this._isValidValue(a.min) && !this._isValidValue(a.max))
        );
      },
      _isValidValue: function (a) {
        return 'undefined' != typeof a && a !== !1 && parseFloat(a) !== a;
      },
      _checkStep: function (a) {
        return a === !1 || parseFloat(a) === a;
      },
      _initElement: function () {
        (a.ui.rangeSliderDraggable.prototype._initElement.apply(this),
          0 === this.cache.parent.width || null === this.cache.parent.width
            ? setTimeout(a.proxy(this._initElementIfNotDestroyed, this), 500)
            : (this._position(this._value),
              this._triggerMouseEvent('initialize')));
      },
      _bounds: function () {
        return this.options.bounds;
      },
      _cache: function () {
        (a.ui.rangeSliderDraggable.prototype._cache.apply(this),
          this._cacheParent());
      },
      _cacheParent: function () {
        var a = this.element.parent();
        this.cache.parent = {
          element: a,
          offset: a.offset(),
          padding: { left: this._parsePixels(a, 'paddingLeft') },
          width: a.width(),
        };
      },
      _position: function (a) {
        var b = this._getPositionForValue(a);
        this._applyPosition(b);
      },
      _constraintPosition: function (a) {
        var b = this._getValueForPosition(a);
        return this._getPositionForValue(b);
      },
      _applyPosition: function (b) {
        (a.ui.rangeSliderDraggable.prototype._applyPosition.apply(this, [b]),
          (this._left = b),
          this._setValue(this._getValueForPosition(b)),
          this._triggerMouseEvent('moving'));
      },
      _prepareEventData: function () {
        var b =
          a.ui.rangeSliderDraggable.prototype._prepareEventData.apply(this);
        return ((b.value = this._value), b);
      },
      _setValue: function (a) {
        a !== this._value && (this._value = a);
      },
      _constraintValue: function (a) {
        if (
          ((a = Math.min(a, this._bounds().max)),
          (a = Math.max(a, this._bounds().min)),
          (a = this._round(a)),
          this.options.range !== !1)
        ) {
          var b = this.options.range.min || !1,
            c = this.options.range.max || !1;
          (b !== !1 && (a = Math.max(a, this._round(b))),
            c !== !1 && (a = Math.min(a, this._round(c))),
            (a = Math.min(a, this._bounds().max)),
            (a = Math.max(a, this._bounds().min)));
        }
        return a;
      },
      _round: function (a) {
        return this.options.step !== !1 && this.options.step > 0
          ? Math.round(a / this.options.step) * this.options.step
          : a;
      },
      _getPositionForValue: function (a) {
        if (
          !this.cache ||
          !this.cache.parent ||
          null === this.cache.parent.offset
        )
          return 0;
        a = this._constraintValue(a);
        var b =
            (a - this.options.bounds.min) /
            (this.options.bounds.max - this.options.bounds.min),
          c = this.cache.parent.width - this.cache.width.outer,
          d = this.cache.parent.offset.left;
        return b * c + d;
      },
      _getValueForPosition: function (a) {
        var b = this._getRawValueForPositionAndBounds(
          a,
          this.options.bounds.min,
          this.options.bounds.max
        );
        return this._constraintValue(b);
      },
      _getRawValueForPositionAndBounds: function (a, b, c) {
        var d =
            null === this.cache.parent.offset
              ? 0
              : this.cache.parent.offset.left,
          e = this.cache.parent.width - this.cache.width.outer,
          f = (a - d) / e;
        return f * (c - b) + b;
      },
      value: function (a) {
        return (
          'undefined' != typeof a &&
            (this._cache(), (a = this._constraintValue(a)), this._position(a)),
          this._value
        );
      },
      update: function () {
        this._cache();
        var a = this._constraintValue(this._value),
          b = this._getPositionForValue(a);
        a !== this._value
          ? (this._triggerMouseEvent('updating'),
            this._position(a),
            this._triggerMouseEvent('update'))
          : b !== this.cache.offset.left &&
            (this._triggerMouseEvent('updating'),
            this._position(a),
            this._triggerMouseEvent('update'));
      },
      position: function (a) {
        return (
          'undefined' != typeof a &&
            (this._cache(),
            (a = this._constraintPosition(a)),
            this._applyPosition(a)),
          this._left
        );
      },
      add: function (a, b) {
        return a + b;
      },
      substract: function (a, b) {
        return a - b;
      },
      stepsBetween: function (a, b) {
        return this.options.step === !1 ? b - a : (b - a) / this.options.step;
      },
      multiplyStep: function (a, b) {
        return a * b;
      },
      moveRight: function (a) {
        var b;
        return this.options.step === !1
          ? ((b = this._left), this.position(this._left + a), this._left - b)
          : ((b = this._value),
            this.value(this.add(b, this.multiplyStep(this.options.step, a))),
            this.stepsBetween(b, this._value));
      },
      moveLeft: function (a) {
        return -this.moveRight(-a);
      },
      stepRatio: function () {
        if (this.options.step === !1) return 1;
        var a =
          (this.options.bounds.max - this.options.bounds.min) /
          this.options.step;
        return this.cache.parent.width / a;
      },
    });
  })(jQuery),
  (function (a) {
    'use strict';
    a.widget('ui.rangeSliderBar', a.ui.rangeSliderDraggable, {
      options: {
        leftHandle: null,
        rightHandle: null,
        bounds: { min: 0, max: 100 },
        type: 'rangeSliderHandle',
        range: !1,
        drag: function () {},
        stop: function () {},
        values: { min: 0, max: 20 },
        wheelSpeed: 4,
        wheelMode: null,
      },
      _values: { min: 0, max: 20 },
      _waitingToInit: 2,
      _wheelTimeout: !1,
      _create: function () {
        (a.ui.rangeSliderDraggable.prototype._create.apply(this),
          this.element
            .css('position', 'absolute')
            .css('top', 0)
            .addClass('ui-rangeSlider-bar'),
          this.options.leftHandle
            .bind('initialize', a.proxy(this._onInitialized, this))
            .bind('mousestart', a.proxy(this._cache, this))
            .bind('stop', a.proxy(this._onHandleStop, this)),
          this.options.rightHandle
            .bind('initialize', a.proxy(this._onInitialized, this))
            .bind('mousestart', a.proxy(this._cache, this))
            .bind('stop', a.proxy(this._onHandleStop, this)),
          this._bindHandles(),
          (this._values = this.options.values),
          this._setWheelModeOption(this.options.wheelMode));
      },
      destroy: function () {
        (this.options.leftHandle.unbind('.bar'),
          this.options.rightHandle.unbind('.bar'),
          (this.options = null),
          a.ui.rangeSliderDraggable.prototype.destroy.apply(this));
      },
      _setOption: function (a, b) {
        'range' === a
          ? this._setRangeOption(b)
          : 'wheelSpeed' === a
            ? this._setWheelSpeedOption(b)
            : 'wheelMode' === a && this._setWheelModeOption(b);
      },
      _setRangeOption: function (a) {
        if (
          (('object' != typeof a || null === a) && (a = !1),
          a !== !1 || this.options.range !== !1)
        ) {
          if (a !== !1) {
            var b =
                'undefined' == typeof a.min
                  ? this.options.range.min || !1
                  : a.min,
              c =
                'undefined' == typeof a.max
                  ? this.options.range.max || !1
                  : a.max;
            this.options.range = { min: b, max: c };
          } else this.options.range = !1;
          (this._setLeftRange(), this._setRightRange());
        }
      },
      _setWheelSpeedOption: function (a) {
        'number' == typeof a && a > 0 && (this.options.wheelSpeed = a);
      },
      _setWheelModeOption: function (a) {
        (null === a || a === !1 || 'zoom' === a || 'scroll' === a) &&
          (this.options.wheelMode !== a &&
            this.element.parent().unbind('mousewheel.bar'),
          this._bindMouseWheel(a),
          (this.options.wheelMode = a));
      },
      _bindMouseWheel: function (b) {
        'zoom' === b
          ? this.element
              .parent()
              .bind('mousewheel.bar', a.proxy(this._mouseWheelZoom, this))
          : 'scroll' === b &&
            this.element
              .parent()
              .bind('mousewheel.bar', a.proxy(this._mouseWheelScroll, this));
      },
      _setLeftRange: function () {
        if (this.options.range === !1) return !1;
        var a = this._values.max,
          b = { min: !1, max: !1 };
        ((b.max =
          (this.options.range.min || !1) !== !1
            ? this._leftHandle('substract', a, this.options.range.min)
            : !1),
          (b.min =
            (this.options.range.max || !1) !== !1
              ? this._leftHandle('substract', a, this.options.range.max)
              : !1),
          this._leftHandle('option', 'range', b));
      },
      _setRightRange: function () {
        var a = this._values.min,
          b = { min: !1, max: !1 };
        ((b.min =
          (this.options.range.min || !1) !== !1
            ? this._rightHandle('add', a, this.options.range.min)
            : !1),
          (b.max =
            (this.options.range.max || !1) !== !1
              ? this._rightHandle('add', a, this.options.range.max)
              : !1),
          this._rightHandle('option', 'range', b));
      },
      _deactivateRange: function () {
        (this._leftHandle('option', 'range', !1),
          this._rightHandle('option', 'range', !1));
      },
      _reactivateRange: function () {
        this._setRangeOption(this.options.range);
      },
      _onInitialized: function () {
        (this._waitingToInit--, 0 === this._waitingToInit && this._initMe());
      },
      _initMe: function () {
        (this._cache(), this.min(this._values.min), this.max(this._values.max));
        var a = this._leftHandle('position'),
          b = this._rightHandle('position') + this.options.rightHandle.width();
        (this.element.offset({ left: a }), this.element.css('width', b - a));
      },
      _leftHandle: function () {
        return this._handleProxy(this.options.leftHandle, arguments);
      },
      _rightHandle: function () {
        return this._handleProxy(this.options.rightHandle, arguments);
      },
      _handleProxy: function (a, b) {
        var c = Array.prototype.slice.call(b);
        return a[this.options.type].apply(a, c);
      },
      _cache: function () {
        (a.ui.rangeSliderDraggable.prototype._cache.apply(this),
          this._cacheHandles());
      },
      _cacheHandles: function () {
        ((this.cache.rightHandle = {}),
          (this.cache.rightHandle.width = this.options.rightHandle.width()),
          (this.cache.rightHandle.offset = this.options.rightHandle.offset()),
          (this.cache.leftHandle = {}),
          (this.cache.leftHandle.offset = this.options.leftHandle.offset()));
      },
      _mouseStart: function (b) {
        (a.ui.rangeSliderDraggable.prototype._mouseStart.apply(this, [b]),
          this._deactivateRange());
      },
      _mouseStop: function (b) {
        (a.ui.rangeSliderDraggable.prototype._mouseStop.apply(this, [b]),
          this._cacheHandles(),
          (this._values.min = this._leftHandle('value')),
          (this._values.max = this._rightHandle('value')),
          this._reactivateRange(),
          this._leftHandle().trigger('stop'),
          this._rightHandle().trigger('stop'));
      },
      _onDragLeftHandle: function (a, b) {
        return (
          this._cacheIfNecessary(),
          this._switchedValues()
            ? (this._switchHandles(), this._onDragRightHandle(a, b), void 0)
            : ((this._values.min = b.value),
              (this.cache.offset.left = b.offset.left),
              (this.cache.leftHandle.offset = b.offset),
              this._positionBar(),
              void 0)
        );
      },
      _onDragRightHandle: function (a, b) {
        return (
          this._cacheIfNecessary(),
          this._switchedValues()
            ? (this._switchHandles(), this._onDragLeftHandle(a, b), void 0)
            : ((this._values.max = b.value),
              (this.cache.rightHandle.offset = b.offset),
              this._positionBar(),
              void 0)
        );
      },
      _positionBar: function () {
        var a =
          this.cache.rightHandle.offset.left +
          this.cache.rightHandle.width -
          this.cache.leftHandle.offset.left;
        ((this.cache.width.inner = a),
          this.element
            .css('width', a)
            .offset({ left: this.cache.leftHandle.offset.left }));
      },
      _onHandleStop: function () {
        (this._setLeftRange(), this._setRightRange());
      },
      _switchedValues: function () {
        if (this.min() > this.max()) {
          var a = this._values.min;
          return (
            (this._values.min = this._values.max),
            (this._values.max = a),
            !0
          );
        }
        return !1;
      },
      _switchHandles: function () {
        var a = this.options.leftHandle;
        ((this.options.leftHandle = this.options.rightHandle),
          (this.options.rightHandle = a),
          this._leftHandle('option', 'isLeft', !0),
          this._rightHandle('option', 'isLeft', !1),
          this._bindHandles(),
          this._cacheHandles());
      },
      _bindHandles: function () {
        (this.options.leftHandle
          .unbind('.bar')
          .bind(
            'sliderDrag.bar update.bar moving.bar',
            a.proxy(this._onDragLeftHandle, this)
          ),
          this.options.rightHandle
            .unbind('.bar')
            .bind(
              'sliderDrag.bar update.bar moving.bar',
              a.proxy(this._onDragRightHandle, this)
            ));
      },
      _constraintPosition: function (b) {
        var c,
          d = {};
        return (
          (d.left =
            a.ui.rangeSliderDraggable.prototype._constraintPosition.apply(
              this,
              [b]
            )),
          (d.left = this._leftHandle('position', d.left)),
          (c = this._rightHandle(
            'position',
            d.left + this.cache.width.outer - this.cache.rightHandle.width
          )),
          (d.width = c - d.left + this.cache.rightHandle.width),
          d
        );
      },
      _applyPosition: function (b) {
        (a.ui.rangeSliderDraggable.prototype._applyPosition.apply(this, [
          b.left,
        ]),
          this.element.width(b.width));
      },
      _mouseWheelZoom: function (b, c, d, e) {
        var f = this._values.min + (this._values.max - this._values.min) / 2,
          g = {},
          h = {};
        return (
          this.options.range === !1 || this.options.range.min === !1
            ? ((g.max = f), (h.min = f))
            : ((g.max = f - this.options.range.min / 2),
              (h.min = f + this.options.range.min / 2)),
          this.options.range !== !1 &&
            this.options.range.max !== !1 &&
            ((g.min = f - this.options.range.max / 2),
            (h.max = f + this.options.range.max / 2)),
          this._leftHandle('option', 'range', g),
          this._rightHandle('option', 'range', h),
          clearTimeout(this._wheelTimeout),
          (this._wheelTimeout = setTimeout(
            a.proxy(this._wheelStop, this),
            200
          )),
          this.zoomOut(e * this.options.wheelSpeed),
          !1
        );
      },
      _mouseWheelScroll: function (b, c, d, e) {
        return (
          this._wheelTimeout === !1
            ? this.startScroll()
            : clearTimeout(this._wheelTimeout),
          (this._wheelTimeout = setTimeout(
            a.proxy(this._wheelStop, this),
            200
          )),
          this.scrollLeft(e * this.options.wheelSpeed),
          !1
        );
      },
      _wheelStop: function () {
        (this.stopScroll(), (this._wheelTimeout = !1));
      },
      min: function (a) {
        return this._leftHandle('value', a);
      },
      max: function (a) {
        return this._rightHandle('value', a);
      },
      startScroll: function () {
        this._deactivateRange();
      },
      stopScroll: function () {
        (this._reactivateRange(),
          this._triggerMouseEvent('stop'),
          this._leftHandle().trigger('stop'),
          this._rightHandle().trigger('stop'));
      },
      scrollLeft: function (a) {
        return (
          (a = a || 1),
          0 > a
            ? this.scrollRight(-a)
            : ((a = this._leftHandle('moveLeft', a)),
              this._rightHandle('moveLeft', a),
              this.update(),
              this._triggerMouseEvent('scroll'),
              void 0)
        );
      },
      scrollRight: function (a) {
        return (
          (a = a || 1),
          0 > a
            ? this.scrollLeft(-a)
            : ((a = this._rightHandle('moveRight', a)),
              this._leftHandle('moveRight', a),
              this.update(),
              this._triggerMouseEvent('scroll'),
              void 0)
        );
      },
      zoomIn: function (a) {
        if (((a = a || 1), 0 > a)) return this.zoomOut(-a);
        var b = this._rightHandle('moveLeft', a);
        (a > b && ((b /= 2), this._rightHandle('moveRight', b)),
          this._leftHandle('moveRight', b),
          this.update(),
          this._triggerMouseEvent('zoom'));
      },
      zoomOut: function (a) {
        if (((a = a || 1), 0 > a)) return this.zoomIn(-a);
        var b = this._rightHandle('moveRight', a);
        (a > b && ((b /= 2), this._rightHandle('moveLeft', b)),
          this._leftHandle('moveLeft', b),
          this.update(),
          this._triggerMouseEvent('zoom'));
      },
      values: function (a, b) {
        if ('undefined' != typeof a && 'undefined' != typeof b) {
          var c = Math.min(a, b),
            d = Math.max(a, b);
          (this._deactivateRange(),
            this.options.leftHandle.unbind('.bar'),
            this.options.rightHandle.unbind('.bar'),
            (this._values.min = this._leftHandle('value', c)),
            (this._values.max = this._rightHandle('value', d)),
            this._bindHandles(),
            this._reactivateRange(),
            this.update());
        }
        return { min: this._values.min, max: this._values.max };
      },
      update: function () {
        ((this._values.min = this.min()),
          (this._values.max = this.max()),
          this._cache(),
          this._positionBar());
      },
    });
  })(jQuery),
  (function (a) {
    'use strict';
    function b(b, c, d, e) {
      ((this.label1 = b),
        (this.label2 = c),
        (this.type = d),
        (this.options = e),
        (this.handle1 = this.label1[this.type]('option', 'handle')),
        (this.handle2 = this.label2[this.type]('option', 'handle')),
        (this.cache = null),
        (this.left = b),
        (this.right = c),
        (this.moving = !1),
        (this.initialized = !1),
        (this.updating = !1),
        (this.Init = function () {
          (this.BindHandle(this.handle1),
            this.BindHandle(this.handle2),
            'show' === this.options.show
              ? (setTimeout(a.proxy(this.PositionLabels, this), 1),
                (this.initialized = !0))
              : setTimeout(a.proxy(this.AfterInit, this), 1e3),
            (this._resizeProxy = a.proxy(this.onWindowResize, this)),
            a(window).resize(this._resizeProxy));
        }),
        (this.Destroy = function () {
          (this._resizeProxy &&
            (a(window).unbind('resize', this._resizeProxy),
            (this._resizeProxy = null),
            this.handle1.unbind('.positionner'),
            (this.handle1 = null),
            this.handle2.unbind('.positionner'),
            (this.handle2 = null),
            (this.label1 = null),
            (this.label2 = null),
            (this.left = null),
            (this.right = null)),
            (this.cache = null));
        }),
        (this.AfterInit = function () {
          this.initialized = !0;
        }),
        (this.Cache = function () {
          'none' !== this.label1.css('display') &&
            ((this.cache = {}),
            (this.cache.label1 = {}),
            (this.cache.label2 = {}),
            (this.cache.handle1 = {}),
            (this.cache.handle2 = {}),
            (this.cache.offsetParent = {}),
            this.CacheElement(this.label1, this.cache.label1),
            this.CacheElement(this.label2, this.cache.label2),
            this.CacheElement(this.handle1, this.cache.handle1),
            this.CacheElement(this.handle2, this.cache.handle2),
            this.CacheElement(
              this.label1.offsetParent(),
              this.cache.offsetParent
            ));
        }),
        (this.CacheIfNecessary = function () {
          null === this.cache
            ? this.Cache()
            : (this.CacheWidth(this.label1, this.cache.label1),
              this.CacheWidth(this.label2, this.cache.label2),
              this.CacheHeight(this.label1, this.cache.label1),
              this.CacheHeight(this.label2, this.cache.label2),
              this.CacheWidth(
                this.label1.offsetParent(),
                this.cache.offsetParent
              ));
        }),
        (this.CacheElement = function (a, b) {
          (this.CacheWidth(a, b),
            this.CacheHeight(a, b),
            (b.offset = a.offset()),
            (b.margin = {
              left: this.ParsePixels('marginLeft', a),
              right: this.ParsePixels('marginRight', a),
            }),
            (b.border = {
              left: this.ParsePixels('borderLeftWidth', a),
              right: this.ParsePixels('borderRightWidth', a),
            }));
        }),
        (this.CacheWidth = function (a, b) {
          ((b.width = a.width()), (b.outerWidth = a.outerWidth()));
        }),
        (this.CacheHeight = function (a, b) {
          b.outerHeightMargin = a.outerHeight(!0);
        }),
        (this.ParsePixels = function (a, b) {
          return parseInt(b.css(a), 10) || 0;
        }),
        (this.BindHandle = function (b) {
          (b.bind('updating.positionner', a.proxy(this.onHandleUpdating, this)),
            b.bind('update.positionner', a.proxy(this.onHandleUpdated, this)),
            b.bind('moving.positionner', a.proxy(this.onHandleMoving, this)),
            b.bind('stop.positionner', a.proxy(this.onHandleStop, this)));
        }),
        (this.PositionLabels = function () {
          if ((this.CacheIfNecessary(), null !== this.cache)) {
            var a = this.GetRawPosition(this.cache.label1, this.cache.handle1),
              b = this.GetRawPosition(this.cache.label2, this.cache.handle2);
            (this.ConstraintPositions(a, b),
              this.PositionLabel(this.label1, a.left, this.cache.label1),
              this.PositionLabel(this.label2, b.left, this.cache.label2));
          }
        }),
        (this.PositionLabel = function (a, b, c) {
          var d,
            e,
            f,
            g =
              this.cache.offsetParent.offset.left +
              this.cache.offsetParent.border.left;
          g - b >= 0
            ? (a.css('right', ''), a.offset({ left: b }))
            : ((d = g + this.cache.offsetParent.width),
              (e = b + c.margin.left + c.outerWidth + c.margin.right),
              (f = d - e),
              a.css('left', ''),
              a.css('right', f));
        }),
        (this.ConstraintPositions = function (a, b) {
          a.center < b.center && a.outerRight > b.outerLeft
            ? ((a = this.getLeftPosition(a, b)),
              (b = this.getRightPosition(a, b)))
            : a.center > b.center &&
              b.outerRight > a.outerLeft &&
              ((b = this.getLeftPosition(b, a)),
              (a = this.getRightPosition(b, a)));
        }),
        (this.getLeftPosition = function (a, b) {
          var c = (b.center + a.center) / 2,
            d =
              c -
              a.cache.outerWidth -
              a.cache.margin.right +
              a.cache.border.left;
          return ((a.left = d), a);
        }),
        (this.getRightPosition = function (a, b) {
          var c = (b.center + a.center) / 2;
          return ((b.left = c + b.cache.margin.left + b.cache.border.left), b);
        }),
        (this.ShowIfNecessary = function () {
          'show' === this.options.show ||
            this.moving ||
            !this.initialized ||
            this.updating ||
            (this.label1.stop(!0, !0).fadeIn(this.options.durationIn || 0),
            this.label2.stop(!0, !0).fadeIn(this.options.durationIn || 0),
            (this.moving = !0));
        }),
        (this.HideIfNeeded = function () {
          this.moving === !0 &&
            (this.label1
              .stop(!0, !0)
              .delay(this.options.delayOut || 0)
              .fadeOut(this.options.durationOut || 0),
            this.label2
              .stop(!0, !0)
              .delay(this.options.delayOut || 0)
              .fadeOut(this.options.durationOut || 0),
            (this.moving = !1));
        }),
        (this.onHandleMoving = function (a, b) {
          (this.ShowIfNecessary(),
            this.CacheIfNecessary(),
            this.UpdateHandlePosition(b),
            this.PositionLabels());
        }),
        (this.onHandleUpdating = function () {
          this.updating = !0;
        }),
        (this.onHandleUpdated = function () {
          ((this.updating = !1), (this.cache = null));
        }),
        (this.onHandleStop = function () {
          this.HideIfNeeded();
        }),
        (this.onWindowResize = function () {
          this.cache = null;
        }),
        (this.UpdateHandlePosition = function (a) {
          null !== this.cache &&
            (a.element[0] === this.handle1[0]
              ? this.UpdatePosition(a, this.cache.handle1)
              : this.UpdatePosition(a, this.cache.handle2));
        }),
        (this.UpdatePosition = function (a, b) {
          b.offset = a.offset;
        }),
        (this.GetRawPosition = function (a, b) {
          var c = b.offset.left + b.outerWidth / 2,
            d = c - a.outerWidth / 2,
            e = d + a.outerWidth - a.border.left - a.border.right,
            f = d - a.margin.left - a.border.left,
            g = b.offset.top - a.outerHeightMargin;
          return {
            left: d,
            outerLeft: f,
            top: g,
            right: e,
            outerRight: f + a.outerWidth + a.margin.left + a.margin.right,
            cache: a,
            center: c,
          };
        }),
        this.Init());
    }
    a.widget('ui.rangeSliderLabel', a.ui.rangeSliderMouseTouch, {
      options: {
        handle: null,
        formatter: !1,
        handleType: 'rangeSliderHandle',
        show: 'show',
        durationIn: 0,
        durationOut: 500,
        delayOut: 500,
        isLeft: !1,
      },
      cache: null,
      _positionner: null,
      _valueContainer: null,
      _innerElement: null,
      _create: function () {
        ((this.options.isLeft = this._handle('option', 'isLeft')),
          this.element
            .addClass('ui-rangeSlider-label')
            .css('position', 'absolute')
            .css('display', 'block'),
          this._createElements(),
          this._toggleClass(),
          this.options.handle
            .bind('moving.label', a.proxy(this._onMoving, this))
            .bind('update.label', a.proxy(this._onUpdate, this))
            .bind('switch.label', a.proxy(this._onSwitch, this)),
          'show' !== this.options.show && this.element.hide(),
          this._mouseInit());
      },
      destroy: function () {
        (this.options.handle.unbind('.label'),
          (this.options.handle = null),
          (this._valueContainer = null),
          (this._innerElement = null),
          this.element.empty(),
          this._positionner &&
            (this._positionner.Destroy(), (this._positionner = null)),
          a.ui.rangeSliderMouseTouch.prototype.destroy.apply(this));
      },
      _createElements: function () {
        ((this._valueContainer = a(
          "<div class='ui-rangeSlider-label-value' />"
        ).appendTo(this.element)),
          (this._innerElement = a(
            "<div class='ui-rangeSlider-label-inner' />"
          ).appendTo(this.element)));
      },
      _handle: function () {
        var a = Array.prototype.slice.apply(arguments);
        return this.options.handle[this.options.handleType].apply(
          this.options.handle,
          a
        );
      },
      _setOption: function (a, b) {
        'show' === a
          ? this._updateShowOption(b)
          : ('durationIn' === a || 'durationOut' === a || 'delayOut' === a) &&
            this._updateDurations(a, b);
      },
      _updateShowOption: function (a) {
        ((this.options.show = a),
          'show' !== this.options.show
            ? this.element.hide()
            : (this.element.show(),
              this._display(
                this.options.handle[this.options.handleType]('value')
              ),
              this._positionner.PositionLabels()),
          (this._positionner.options.show = this.options.show));
      },
      _updateDurations: function (a, b) {
        parseInt(b, 10) === b &&
          ((this._positionner.options[a] = b), (this.options[a] = b));
      },
      _display: function (a) {
        this.options.formatter === !1
          ? this._displayText(Math.round(a))
          : this._displayText(this.options.formatter(a));
      },
      _displayText: function (a) {
        this._valueContainer.text(a);
      },
      _toggleClass: function () {
        this.element
          .toggleClass('ui-rangeSlider-leftLabel', this.options.isLeft)
          .toggleClass('ui-rangeSlider-rightLabel', !this.options.isLeft);
      },
      _mouseDown: function (a) {
        this.options.handle.trigger(a);
      },
      _mouseUp: function (a) {
        this.options.handle.trigger(a);
      },
      _mouseMove: function (a) {
        this.options.handle.trigger(a);
      },
      _onMoving: function (a, b) {
        this._display(b.value);
      },
      _onUpdate: function () {
        'show' === this.options.show && this.update();
      },
      _onSwitch: function (a, b) {
        ((this.options.isLeft = b),
          this._toggleClass(),
          this._positionner.PositionLabels());
      },
      pair: function (a) {
        null === this._positionner &&
          ((this._positionner = new b(this.element, a, this.widgetName, {
            show: this.options.show,
            durationIn: this.options.durationIn,
            durationOut: this.options.durationOut,
            delayOut: this.options.delayOut,
          })),
          a[this.widgetName]('positionner', this._positionner));
      },
      positionner: function (a) {
        return (
          'undefined' != typeof a && (this._positionner = a),
          this._positionner
        );
      },
      update: function () {
        ((this._positionner.cache = null),
          this._display(this._handle('value')),
          'show' === this.options.show && this._positionner.PositionLabels());
      },
    });
  })(jQuery));
