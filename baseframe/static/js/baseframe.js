// This is a global function. Isn't there a better way to do this?

function activate_widgets() {
  // Activate select2.js and CodeMirror for non-mobile browsers
  if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
    $('select:not(.notselect)').select2({allowClear: true});

    var cm_markdown_config = { mode: 'gfm',
      lineNumbers: false,
      theme: "default",
      lineWrapping: true,
      autoCloseBrackets: true,
      viewportMargin: Infinity,
      extraKeys: {
        "Enter": "newlineAndIndentContinueMarkdownList",
        "Tab": false,
        "Shift-Tab": false,
        "Home": "goLineLeft",
        "End": "goLineRight",
        "Cmd-Left": "goLineLeft",
        "Cmd-Right": "goLineRight"
      }
    };

    var cm_css_config = { mode: 'css',
      lineNumbers: false,
      theme: "default",
      lineWrapping: true,
      autoCloseBrackets: true,
      matchBrackets: true,
      viewportMargin: Infinity,
      extraKeys: {
        "Tab": false,
        "Shift-Tab": false,
        "Home": "goLineLeft",
        "End": "goLineRight",
        "Cmd-Left": "goLineLeft",
        "Cmd-Right": "goLineRight"
      }
    };

    // Activate codemirror on all textareas with class='markdown'
    $('textarea.markdown').each(function(){
      var editor = CodeMirror.fromTextArea(this, cm_markdown_config);
      var delay;
      editor.on('change', function(instance){
        clearTimeout(delay);
        delay = setTimeout(function() {
          editor.save();
        }, 300);
      });
    });

    // Activate codemirror on all textareas with class='stylesheet'
    $('textarea.stylesheet').each(function() {
      var editor = CodeMirror.fromTextArea(this, cm_css_config);
      var delay;
      editor.on('change', function(instance){
        clearTimeout(delay);
        delay = setTimeout(function() {
          editor.save();
        }, 300);
      });
    });
  }
  $('input.datetime-time').timepicker({ 'scrollDefaultNow': true });
}

function radioHighlight(radioName, highlightClass) {
  var selector = "input[name='" + radioName + "']";
  $(selector + ":checked").parent().addClass(highlightClass);
  var handler = function() {
      $(selector).parent().removeClass(highlightClass);
      $(selector + ":checked").parent().addClass(highlightClass);
  };
  $(selector).change(handler);
  $(selector).click(handler);
}

function activate_lastuser_autocomplete(selector, autocomplete_endpoint, getuser_endpoint) {
  $(selector).select2({
    placeholder: "Search for a user",
    multiple: true,
    minimumInputLength: 2,
    ajax: {
      url: autocomplete_endpoint,
      dataType: "jsonp",
      data: function(term, page) {
        return {
          q: term
        };
      },
      results: function(data, page) {
        var rdata = [];
        if (data.status == 'ok') {
          for (var i=0; i < data.users.length; i++) {
            rdata.push({
              id: data.users[i].buid, text: data.users[i].label
            });
          }
        }
        return {more: false, results: rdata};
      }
    },
    initSelection: function(element, callback) {
      var val = $(element).val();
      if (val !== '') {
        var qs = '?userid=' + val.replace(/,/g, '&userid=');
        $.ajax(getuser_endpoint + qs, {
          accepts: "application/json",
          dataType: "jsonp"
        }).done(function(data) {
          $(element).val('');  // Clear it in preparation for incoming data
          var rdata = [];
          if (data.status == 'ok') {
            for (var i=0; i < data.results.length; i++) {
              rdata.push({
                id: data.results[i].buid, text: data.results[i].label
              });
            }
          }
          callback(rdata);
        });
      }
    }
  });
}

function activate_geoname_autocomplete(selector, autocomplete_endpoint, getname_endpoint) {
  $(selector).select2({
    placeholder: "Search for a location",
    multiple: true,
    minimumInputLength: 2,
    ajax: {
      url: autocomplete_endpoint,
      dataType: "jsonp",
      data: function(term, page) {
        return {
          q: term
        };
      },
      results: function(data, page) {
        var rdata = [];
        if (data.status == 'ok') {
          for (var i=0; i < data.result.length; i++) {
            rdata.push({
              id: data.result[i].geonameid, text: data.result[i].ascii_title
            });
          }
        }
        return {more: false, results: rdata};
      }
    },
    initSelection: function(element, callback) {
      var val = $(element).val();
      if (val !== '') {
        var qs = '?name=' + val.replace(/,/g, '&name=');
        $.ajax(getname_endpoint + qs, {
          accepts: "application/json",
          dataType: "jsonp"
        }).done(function(data) {
          $(element).val('');  // Clear it in preparation for incoming data
          var rdata = [];
          if (data.status == 'ok') {
            for (var i=0; i < data.result.length; i++) {
              rdata.push({
                id: data.result[i].geonameid, text: data.result[i].ascii_title
              });
            }
          }
          callback(rdata);
        });
      }
    }
  });
}

$(function() {
  // Activate Chrome/Windows font hack
  if ((navigator.userAgent.toLowerCase().indexOf('chrome') > -1) && (navigator.userAgent.toLowerCase().indexOf('windows') > -1)) {
    document.body.style.webkitTextStroke = '0.2px';
  }

  // activate all widgets
  activate_widgets();

  var matchtab = function() {
    var url = document.location.toString(), tabmatch = null;
    if (url.match('#/')) {
      tabmatch = $('.nav-tabs.nav-tabs-auto a[href="#'+url.split('#/')[1]+'"]');
    } else if (url.match('#')) {
      tabmatch = $('.nav-tabs.nav-tabs-auto a[href="#'+url.split('#')[1]+'"]');
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

$(function() {
  // Code notice
  console.log("Hello, curious geek. Our source is at https://github.com/hasgeek. Why not contribute a patch?");
});

// Single Global Baseframe Object that serves as a namespace
window.Baseframe = {
};

window.Baseframe.Config = {
  defaultLatitude: "12.961443",
  defaultLongitude: "77.64435000000003"
};

window.Baseframe.Forms = {
  preventSubmitOnEnter: function(id){
    $('#' + id).on("keyup keypress", function(e) {
      var code = e.keyCode || e.which; 
      if (code === 13) {               
        e.preventDefault();
        return false;
      }
    });
  },
  lastuserAutocomplete: function(options) {
    var assembleUsers = function(users) {
      return users.map(function(user){
        return {id: user.buid, text: user.label};
      });
    };

    $("#" + options.id).select2({
      placeholder: "Search for a user",
      multiple: options.multiple,
      minimumInputLength: 2,
      ajax: {
        url: options.autocomplete_endpoint,
        dataType: "jsonp",
        data: function(term, page) {
          return {
            q: term
          };
        },
        results: function(data, page) {
          var users = [];
          if (data.status == 'ok') {
            users = assembleUsers(data.users);
          }
          return {more: false, results: users};
        }
      },
      initSelection: function(element, callback) {
        var val = $(element).val();
        if (val !== '') {
          $.ajax(options.getuser_endpoint + '?userid=' + val.replace(/,/g, '&userid='), {
            accepts: "application/json",
            dataType: "jsonp"
          }).done(function(data) {
            $(element).val('');  // Clear it in preparation for incoming data
            var results = [];
            if (data.status == 'ok') {
              results = assembleUsers(data.results);
            }
            callback(results);
          });
        }
      }
    });
  }
};

window.Baseframe.MapMarker = function(field){
  this.field = field;
  this.activate();
  return this;
};

window.Baseframe.MapMarker.prototype.activate = function(){
  var self = this;
  Baseframe.Forms.preventSubmitOnEnter(this.field.location_id);

  // locationpicker.jquery.js
  $("#" + this.field.map_id).locationpicker({
    location: self.getDefaultLocation(),
    radius: 0,
    inputBinding: {
      latitudeInput: $("#" + this.field.latitude_id),
      longitudeInput: $("#" + this.field.longitude_id),
      locationNameInput: $("#" + this.field.location_id)
    },
    enableAutocomplete: true,
    onchanged: function(currentLocation, radius, isMarkerDropped) {
    },
    onlocationnotfound: function(locationName) {
    },
    oninitialized: function (component) {
    }
  });
};

window.Baseframe.MapMarker.prototype.getDefaultLocation = function() {
  var latitude, longitude;
  if ($("#" + this.field.latitude_id).val() === '' && $("#" + this.field.longitude_id).val() === '') {
    latitude = Baseframe.Config.defaultLatitude;
    longitude = Baseframe.Config.defaultLongitude;
  } else {
    latitude = $("#" + this.field.latitude_id).val();
    longitude = $("#" + this.field.longitude_id).val();
  }
  return {latitude: latitude, longitude: longitude};
};
