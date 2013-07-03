// Activate chosen.js only if not on a mobile browser
// This is a global function. Isn't there a better way to do this?
function activate_chosen(selector) {
  if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
    // $(selector).chosen({allow_single_deselect: true});
    $(selector).select2({allowClear: true});
  }
}

function activate_codemirror(textarea, config){
  if (typeof(config) == 'undefined'){
    config =  { mode: 'markdown',
                lineNumbers: true,
                theme: "default",
                extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList" }
         };
    }
    var editor = CodeMirror.fromTextArea(textarea, config);
}

$(function() {
  // Activate chosen on all 'select' tags.
  activate_chosen('select:not(.notselect)');

  // Activate codemirror on all textareas with class='codemirror'
  $('textarea.codemirror').each(function() {
    activate_codemirror(this);
  });

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
