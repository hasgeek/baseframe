// Disable hg-submenu link href
$(function(){
    $('a.hg-submenu').click(function(e) {
        e.preventDefault();
        return false;
    });
});


//bs3
$(function(){
	$('#navbar-toggle-1').click(function(){
		if(!$('#navbar-toggle-2').hasClass('collapse')){
			var collapse2 = function(){
				$('#navbar-toggle-2').addClass('collapsed');
				$('#navbar-collapse-2').addClass('collapse');			
				$('#navbar-collapse-2').removeClass('in');	
			}
			setTimeout(collapse2, 480);			
			$('#navbar-collapse-2').animate({height:"2px"});
		}
	});
	$('#navbar-toggle-2').click(function(){
		if(!$('#navbar-toggle-1').hasClass('collapse')){
			var collapse1 = function(){
				$('#navbar-toggle-1').addClass('collapsed');
				$('#navbar-collapse-1').addClass('collapse');			
				$('#navbar-collapse-1').removeClass('in');	
			}
			setTimeout(collapse1, 480);			
			$('#navbar-collapse-1').animate({height:"2px"});
		}
	});
});

// var IS_IPAD = navigator.userAgent.match(/iPad/i) != null;
// if (IS_IPAD){
// 	$('.dropdown').click(function(){
// 		if($(this).hasClass('open')){
// 			$(this).css('background', 'red');
// 			$('.dropdown-menu').css('visibility', 'hidden');
// 			$('.dropdown-menu').css('max-height', '0');
// 			$(this).removeClass('open');
// 		}else if(!$(this).hasClass('open')){
// 			$(this).addClass('open');
// 			$('.dropdown-menu').css('visibility', 'visible');
// 			$('.dropdown-menu').css('max-height', '40em');
// 			$(this).css('background', 'green');
// 		}
// 	});
// }

