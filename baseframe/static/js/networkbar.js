// Disable hg-submenu link href
$(function(){
    $('a.hg-submenu').click(function(e) {
        e.preventDefault();
        return false;
    });
});
