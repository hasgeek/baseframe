// This is a global function. Isn't there a better way to do this?

function activate_widgets() {
  var cm_markdown_config = {
    mode: 'gfm',
    lineNumbers: false,
    theme: 'default',
    lineWrapping: true,
    autoCloseBrackets: true,
    viewportMargin: Infinity,
    extraKeys: {
      Enter: 'newlineAndIndentContinueMarkdownList',
      Tab: false,
      'Shift-Tab': false,
      Home: 'goLineLeft',
      End: 'goLineRight',
      'Cmd-Left': 'goLineLeft',
      'Cmd-Right': 'goLineRight',
    },
  };

  var cm_css_config = {
    mode: 'css',
    lineNumbers: false,
    theme: 'default',
    lineWrapping: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    viewportMargin: Infinity,
    extraKeys: {
      Tab: false,
      'Shift-Tab': false,
      Home: 'goLineLeft',
      End: 'goLineRight',
      'Cmd-Left': 'goLineLeft',
      'Cmd-Right': 'goLineRight',
    },
  };

  var cm_json_config = {
    mode: { name: 'javascript', json: true },
    lineNumbers: true,
    theme: 'default',
    lineWrapping: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    viewportMargin: Infinity,
    indentSize: 2,
    tabSize: 2,
    foldGutter: true,
    gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
    extraKeys: {
      Tab: false,
      'Shift-Tab': false,
      Home: 'goLineLeft',
      End: 'goLineRight',
      'Cmd-Left': 'goLineLeft',
      'Cmd-Right': 'goLineRight',
      F11: function (cm) {
        cm.setOption('fullScreen', !cm.getOption('fullScreen'));
      },
      'Shift-F11': function (cm) {
        cm.setOption('fullScreen', !cm.getOption('fullScreen'));
      },
      Esc: function (cm) {
        if (cm.getOption('fullScreen')) cm.setOption('fullScreen', false);
      },
      'Shift-Esc': function (cm) {
        if (cm.getOption('fullScreen')) cm.setOption('fullScreen', false);
      },
    },
  };
  // Activate codemirror on all textareas with class='markdown'
  $('textarea.markdown').each(function () {
    var editor = CodeMirror.fromTextArea(this, cm_markdown_config);
    var delay;
    editor.on('change', function (instance) {
      clearTimeout(delay);
      delay = setTimeout(function () {
        editor.save();
      }, 300);
    });
  });

  // Activate codemirror on all textareas with class='stylesheet'
  $('textarea.stylesheet').each(function () {
    var editor = CodeMirror.fromTextArea(this, cm_css_config);
    var delay;
    editor.on('change', function (instance) {
      clearTimeout(delay);
      delay = setTimeout(function () {
        editor.save();
      }, 300);
    });
  });

  // Activate codemirror on all textareas with class='json'
  $('textarea.json').each(function () {
    var editor = CodeMirror.fromTextArea(this, cm_json_config);
    var delay;
    editor.on('change', function (instance) {
      clearTimeout(delay);
      delay = setTimeout(function () {
        editor.save();
      }, 300);
    });
  });
}

function radioHighlight(radioName, highlightClass) {
  var selector = "input[name='" + radioName + "']";
  $(selector + ':checked')
    .parent()
    .addClass(highlightClass);
  var handler = function () {
    $(selector).parent().removeClass(highlightClass);
    $(selector + ':checked')
      .parent()
      .addClass(highlightClass);
  };
  $(selector).change(handler);
  $(selector).click(handler);
}

function activate_geoname_autocomplete(
  selector,
  autocomplete_endpoint,
  getname_endpoint,
  separator
) {
  $(selector).select2({
    placeholder: 'Search for a location',
    multiple: true,
    minimumInputLength: 2,
    theme: 'bootstrap',
    ajax: {
      url: autocomplete_endpoint,
      dataType: 'jsonp',
      data: function (params, page) {
        return {
          q: params.term,
        };
      },
      processResults: function (data, page) {
        var rdata = [];
        if (data.status == 'ok') {
          for (var i = 0; i < data.result.length; i++) {
            rdata.push({
              id: data.result[i].geonameid,
              text: data.result[i].picker_title,
            });
          }
        }
        return { more: false, results: rdata };
      },
    },
  });

  //Setting label for Geoname ids
  var val = $(selector).val();
  if (val) {
    val = val.map(function (id) {
      return 'name=' + id;
    });
    var qs = val.join('&');
    $.ajax(getname_endpoint + '?' + qs, {
      accepts: 'application/json',
      dataType: 'jsonp',
    }).done(function (data) {
      $(selector).empty();
      var rdata = [];
      if (data.status == 'ok') {
        for (var i = 0; i < data.result.length; i++) {
          $(selector).append(
            '<option value="' +
              data.result[i].geonameid +
              '" selected>' +
              data.result[i].picker_title +
              '</option>'
          );
          rdata.push(data.result[i].geonameid);
        }
        $(selector).val(rdata).trigger('change');
      }
    });
  }
}

$(function () {
  // activate all widgets
  activate_widgets();

  var matchtab = function () {
    var url = document.location.toString(),
      tabmatch = null;
    if (url.match('#/')) {
      tabmatch = $(
        '.nav-tabs.nav-tabs-auto a[href="#' + url.split('#/')[1] + '"]'
      );
    } else if (url.match('#')) {
      tabmatch = $(
        '.nav-tabs.nav-tabs-auto a[href="#' + url.split('#')[1] + '"]'
      );
    }
    if (tabmatch !== null && tabmatch.length !== 0) {
      $(tabmatch[0]).tab('show');
    }
  };

  // Load correct tab when fragment identifier changes
  $(window).bind('hashchange', matchtab);
  // Load correct tab when the page loads
  matchtab();
  // Change hash for tab click
  $('.nav-tabs.nav-tabs-auto a').on('shown', function (e) {
    window.location.hash = '#/' + e.target.hash.slice(1);
  });
  var url = document.location.toString();
  if (!url.match('#')) {
    // Activate the first tab if none are active
    var tabmatch = $('.nav-tabs.nav-tabs-auto a').filter(':first');
    if (tabmatch.length !== 0) {
      $(tabmatch[0]).tab('show');
    }
  }
});

$(function () {
  // Code notice
  console.log(
    'Hello, curious geek. Our source is at https://github.com/hasgeek. Why not contribute a patch?'
  );
});

// Single Global Baseframe Object that serves as a namespace
window.Baseframe = {};

window.Baseframe.Config = {
  defaultLatitude: '12.961443',
  defaultLongitude: '77.64435000000003',
};

window.Baseframe.Forms = {
  preventSubmitOnEnter: function (id) {
    $('#' + id).on('keyup keypress', function (e) {
      var code = e.keyCode || e.which;
      if (code === 13) {
        e.preventDefault();
        return false;
      }
    });
  },
  lastuserAutocomplete: function (options) {
    var assembleUsers = function (users) {
      return users.map(function (user) {
        return { id: user.buid, text: user.label };
      });
    };

    $('#' + options.id).select2({
      placeholder: 'Search for a user',
      multiple: options.multiple,
      minimumInputLength: 2,
      theme: 'bootstrap',
      ajax: {
        url: options.autocomplete_endpoint,
        dataType: 'jsonp',
        data: function (params, page) {
          if ('client_id' in options) {
            return {
              q: params.term,
              client_id: options.client_id,
              session: options.session_id,
            };
          } else {
            return {
              q: params.term,
            };
          }
        },
        processResults: function (data, page) {
          var users = [];
          if (data.status == 'ok') {
            users = assembleUsers(data.users);
          }
          return { more: false, results: users };
        },
      },
    });
  },
  textAutocomplete: function (options) {
    $('#' + options.id).select2({
      placeholder: 'Type to select',
      multiple: options.multiple,
      minimumInputLength: 2,
      theme: 'bootstrap',
      ajax: {
        url: options.autocomplete_endpoint,
        dataType: 'json',
        data: function (params, page) {
          return {
            q: params.term,
            page: page,
          };
        },
        processResults: function (data, page) {
          return {
            more: false,
            results: data[options.key].map(function (item) {
              return { id: item, text: item };
            }),
          };
        },
      },
    });
  },
  /* Takes 'formId' and 'errors'
   'formId' is the id attribute of the form for which errors needs to be displayed
   'errors' is the WTForm validation errors expected in the following format
    {
      "title": [
        "This field is required"
      ]
      "email": [
        "Not a valid email"
      ]
    }
    For each error, a 'p' tag is created if not present and
    assigned the error value as its text content.
    The field wrapper and field are queried in the DOM
    using the unique form id. And the newly created 'p' tag
    is inserted in the DOM below the field.
  */
  showValidationErrors: function (formId, errors) {
    var form = document.getElementById(formId);
    Object.keys(errors).forEach(function (fieldName) {
      if (Array.isArray(errors[fieldName])) {
        var fieldWrapper = form.querySelector('#field-' + fieldName);
        if (fieldWrapper) {
          var errorElem = fieldWrapper.querySelector('.help-error');
          // If error P tag doesn't exist, create it
          if (!errorElem) {
            errorElem = document.createElement('p');
            errorElem.classList.add('help-error');
          }
          errorElem.innerText = errors[fieldName][0];
          var field = form.querySelector('#' + fieldName);
          // Insert the p tag below the field
          field.parentNode.appendChild(errorElem);
          // Add error class to field wrapper
          fieldWrapper.classList.add('has-error');
        }
      }
    });
  },
  /* Takes formId, url, onSuccess, onError, config
   'formId' - Form id selector to query the DOM for the form
   'url' - The url to which the post request is sent
   'onSuccess' - A callback function that is executed if the request succeeds
   'onError' - A callback function that is executed if the request fails
   'config' -  An object that can contain dataType, beforeSend function
    handleFormSubmit handles form submit, serializes the form values,
      disables the submit button to prevent double submit,
      displays the loading indicator and submits the form via ajax.
      On completing the ajax request, calls the onSuccess/onError callback function.
  */
  handleFormSubmit: function (formId, url, onSuccess, onError, config) {
    $('#' + formId)
      .find('button[type="submit"]')
      .click(function (event) {
        event.preventDefault();
        $.ajax({
          url: url,
          type: 'POST',
          data: $('#' + formId).serialize(),
          dataType: config.dataType ? config.dataType : 'json',
          beforeSend: function () {
            // Disable submit button to prevent double submit
            $('#' + formId)
              .find('button[type="submit"]')
              .prop('disabled', true);
            // Baseframe form has a loading indication which is hidden by default. Show the loading indicator
            $('#' + formId)
              .find('.loading')
              .removeClass('hidden');
            if (config.beforeSend) config.beforeSend();
          },
        })
          .done(function (remoteData) {
            onSuccess(remoteData);
          })
          .fail(function (response) {
            onError(response);
          });
      });
  },
};

window.Baseframe.MapMarker = function (field) {
  this.field = field;
  this.activate();
  return this;
};

window.Baseframe.MapMarker.prototype.activate = function () {
  var self = this;
  Baseframe.Forms.preventSubmitOnEnter(this.field.location_id);

  // locationpicker.jquery.js
  $('#' + this.field.map_id).locationpicker({
    location: self.getDefaultLocation(),
    radius: 0,
    zoom: 18,
    inputBinding: {
      latitudeInput: $('#' + this.field.latitude_id),
      longitudeInput: $('#' + this.field.longitude_id),
      locationNameInput: $('#' + this.field.location_id),
    },
    enableAutocomplete: true,
    onchanged: function (currentLocation, radius, isMarkerDropped) {
      if ($('#' + self.field.location_id).val()) {
        $('#' + self.field.map_id).removeClass('hidden');
      }
    },
    onlocationnotfound: function (locationName) {},
    oninitialized: function (component) {
      // Locationpicker sets latitude and longitude field value to 0,
      // this is to empty the fields and hide the map
      if (!$('#' + self.field.location_id).val()) {
        $('#' + self.field.latitude_id).val('');
        $('#' + self.field.longitude_id).val('');
        $('#' + self.field.map_id).addClass('hidden');
      }
    },
  });

  // On clicking clear, empty latitude, longitude, location fields and hide map
  $('#' + this.field.clear_id).on('click', function (event) {
    event.preventDefault();
    $('#' + self.field.latitude_id).val('');
    $('#' + self.field.longitude_id).val('');
    $('#' + self.field.location_id).val('');
    $('#' + self.field.map_id).addClass('hidden');
  });
};

window.Baseframe.MapMarker.prototype.getDefaultLocation = function () {
  var latitude, longitude;
  latitude = $('#' + this.field.latitude_id).val();
  longitude = $('#' + this.field.longitude_id).val();
  return { latitude: latitude, longitude: longitude };
};

window.Baseframe.Utils = {
  getInitials: function (name) {
    if (name) {
      var parts = name.split(/\s+/);
      var len = parts.length;
      if (len > 1) {
        return (
          (parts[0] ? parts[0][0] : '') +
          (parts[len - 1] ? parts[len - 1][0] : '')
        );
      } else if (parts) {
        return parts[0] ? parts[0][0] : '';
      }
    }
    return '';
  },
};

window.ParsleyConfig = {
  errorsWrapper: '<div></div>',
  errorTemplate: '<p class="help-error"></p>',
  errorClass: 'has-error',
  classHandler: function (ParsleyField) {
    return ParsleyField.$element.closest('.form-group');
  },
  errorsContainer: function (ParsleyField) {
    return ParsleyField.$element.closest('.controls');
  },
  i18n: {
    en: {},
  },
};

$(function () {
  // Override Parsley.js's default messages after the page loads.
  // Our versions don't use full stops after phrases.
  window.ParsleyConfig.i18n.en = $.extend(window.ParsleyConfig.i18n.en || {}, {
    defaultMessage: 'This value seems to be invalid',
    notblank: 'This value should not be blank',
    required: 'This value is required',
    pattern: 'This value seems to be invalid',
    min: 'This value should be greater than or equal to %s',
    max: 'This value should be lower than or equal to %s',
    range: 'This value should be between %s and %s',
    minlength: 'This value is too short. It should have %s characters or more',
    maxlength: 'This value is too long. It should have %s characters or fewer',
    length: 'This value should be between %s and %s characters long',
    mincheck: 'You must select at least %s choices',
    maxcheck: 'You must select %s choices or fewer',
    check: 'You must select between %s and %s choices',
    equalto: 'This value should be the same',
  });
  window.ParsleyConfig.i18n.en.type = $.extend(
    window.ParsleyConfig.i18n.en.type || {},
    {
      email: 'This value should be a valid email',
      url: 'This value should be a valid url',
      number: 'This value should be a valid number',
      integer: 'This value should be a valid integer',
      digits: 'This value should be digits',
      alphanum: 'This value should be alphanumeric',
    }
  );

  var csrfRefresh = function () {
    $.ajax({
      type: 'GET',
      url: '/api/baseframe/1/csrf/refresh',
      timeout: 5000,
      dataType: 'json',
      success: function (data) {
        $('meta[name="csrf-token"]').attr('content', data.csrf_token);
        $('input[name="csrf_token"]').val(data.csrf_token);
      },
    });
  };

  //Request for new CSRF token and update the page every 15 mins
  setInterval(csrfRefresh, 900000);
});
