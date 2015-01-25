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
});

$(function(){
	// two pane sidebar collapse
	$('#hamburger-icon').click(function() {
		$('#left').toggleClass('in');
		$('#right').toggleClass('in');
		$('#left').toggleClass('out');
		$('#right').toggleClass('out');
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
	// close the sidebar when networkbar dropdowns are clicked
	if (Modernizr.mq('only screen and (max-width: 768px)')) {
		$('#hg-panel .nav.pull-right > li > a').click(function() {
			if ($('#left').hasClass('out')) {
				$('#left').toggleClass('in');
				$('#right').toggleClass('in');
				$('#left').toggleClass('out');
				$('#right').toggleClass('out');
			}
		});
	}
});

$(function(){
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