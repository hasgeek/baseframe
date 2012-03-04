// Activate chosen.js only if not on a mobile browser
// This is a global function. Isn't there a better way to do this?
function activate_chosen(selector) {
  if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
    $(selector).chosen({allow_single_deselect: true});
  }
}

$(function() {
  activate_chosen('select');

  // Load correct tab when fragment identifier changes
  $(window).bind('hashchange', function() {
    var url = document.location.toString();
    if (url.match('#')) {
      $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show') ;
    }
  });
  // Load correct tab when the page loads
  var url = document.location.toString();
  if (url.match('#')) {
    $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show') ;
  }
  // Change hash for tab click
  $('.nav-tabs a').on('shown', function (e) {
    window.location.hash = e.target.hash;
  });
});
