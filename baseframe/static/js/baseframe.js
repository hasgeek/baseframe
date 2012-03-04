// Activate chosen.js only if not on a mobile browser
// This is a global function. Isn't there a better way to do this?
function activate_chosen(selector) {
  if (!navigator.userAgent.match(/(iPod|iPad|iPhone|Android)/)) {
    $(selector).chosen({allow_single_deselect: true});
  }
}

$(function() {
  activate_chosen('select');
});
