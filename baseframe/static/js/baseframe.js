// This is a global function. Isn't there a better way to do this?

function activate_widgets(){
    // Activate select2.js and CodeMirror for non-mobile browsers
    if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
      $('select:not(.notselect)').select2({allowClear: true});

      var cm_markdown_config = { mode: 'gfm',
          lineNumbers: false,
          theme: "default",
          lineWrapping: true,
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

      // Activate codemirror on all textareas with class='markdown'
      $('textarea.markdown').each(function(){
          var editor = CodeMirror.fromTextArea(this, cm_markdown_config);
      });
    }
}

function activate_ajax_link(form) {
  form.ajaxForm({
    target: form.attr('data-target'),
    replaceTarget: Boolean(Number(form.attr('data-replace-target'))),
    success: function(response, status, xhr, form) {
      if(xhr.status == 200) toastr.success('', $(form[0]).attr('data-success-msg'))
    },
    error: function(xhr) {
      if(xhr.status == 401) toastr.error('', xhr.responseText);
      else if(xhr.status == 500) toastr.error('', "There was an unexpected error.")
      else toastr.error('', "Server not reachable");
    }
  });
  form.find('a').click(function() {
    $(this).parent().submit();
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

  $('form.ajax_link').each(function() {
    activate_ajax_link($(this));
  });
});


$(function() {
  // Code notice
  console.log("Hello, curious geek. Our source is at https://github.com/hasgeek. Why not contribute a patch?");
});
