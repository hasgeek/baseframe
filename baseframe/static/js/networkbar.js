// Disable hg-submenu link href
$(function(){
    $('a.hg-submenu').click(function(e) {
        e.preventDefault();
        return false;
    });
});


//bs3
$(function(){
	var windowHeight = $(window).height();
	if ($('.navbar-collapse').height() >= windowHeight ){
		$('.navbar-collapse').css('max-height', windowHeight - 60);
	}else{
		$('.navbar-collapse').css('max-height', 390);
	}
});