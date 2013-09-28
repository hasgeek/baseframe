// This is a global function. Isn't there a better way to do this?

function activate_widgets(){
    // Activate select2.js for non-mobile browsers
    if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
        $('select:not(.notselect)').select2({allowClear: true});
    }

    var cm_config = { mode: 'gfm',
        lineNumbers: false,
        theme: "default",
        lineWrapping: true,
        extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList" }
    };

    // Activate codemirror on all textareas with class='markdown'
    $('textarea.markdown').each(function(){
        var editor = CodeMirror.fromTextArea(this, cm_config);
    });
}

$(function() {
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
