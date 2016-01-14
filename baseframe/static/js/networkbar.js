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
