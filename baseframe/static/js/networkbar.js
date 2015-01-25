//bs3
$(document).ready(function(){
	$('.navbar-toggle').addClass('collapsed');
});

$(function(){
	$('#navbar-toggle-1').click(function(){
		if(!$('#navbar-toggle-2').hasClass('collapse')){
			var collapse2 = function(){
				$('#navbar-toggle-2').addClass('collapsed');
				$('.navbar-ex2-collapse').addClass('collapse');			
				$('.navbar-ex2-collapse').removeClass('in');	
			}
			setTimeout(collapse2, 480);			
			$('.navbar-ex2-collapse').animate({height:"2px"});
		}
	});
	$('#navbar-toggle-2').click(function(){
		if(!$('#navbar-toggle-1').hasClass('collapse')){
			var collapse1 = function(){
				$('#navbar-toggle-1').addClass('collapsed');
				$('.navbar-ex1-collapse').addClass('collapse');			
				$('.navbar-ex1-collapse').removeClass('in');	
			}
			setTimeout(collapse1, 480);			
			$('.navbar-ex1-collapse').animate({height:"2px"});
		}
	});
	if (Modernizr.touch){
		$('.navbar-toggle').click(function(){
			if(!$('.navbar-collapse').hasClass('in')){
				$('body').addClass('nav-open');
			}else{
				$('body').removeClass('nav-open');
			}	
		});	
	}
});

var toggleSidebar = function() {
	$('#left').toggleClass('in');
	$('#left').toggleClass('out');
	$('#right').toggleClass('in');
	$('#right').toggleClass('out');
}
var mobCloseSidebar = function() {
	$('#left, #right').removeClass('out').addClass('in');
}
var mobOpenSidebar = function() {
	$('#left, #right').removeClass('in').addClass('out');
}

$(function(){
	// two pane sidebar collapse
	$('#hamburger-icon').click(function() {
		toggleSidebar();
	});
	// sidebar form floating label
	$('#left .form-group input').focusout(function() {		
		var inputContent = $(this).val();
		if ( inputContent !== '' ) {
			$(this).addClass('has-content');
		} else {
			$(this).removeClass('has-content');
		}
	});
	
	if (Modernizr.mq('only screen and (max-width: 768px)')) {
		// close the sidebar when networkbar dropdowns are clicked
		$('#hg-panel .nav.pull-right > li > a').click(function() {
			if ($('#left').hasClass('out')) {
				mobCloseSidebar();
			}
		});
		// swipe toggle for sidebar
		$(function() {
			$("#right .wrapper").swipe( {
				swipeRight:function(event) {
					if (event.pageX < 150) {
						mobOpenSidebar();
					}
				},
				swipeLeft:function(event) {
					if (event.pageX > 200) {
						mobCloseSidebar();
					}
				}
			});
		});
	}
});