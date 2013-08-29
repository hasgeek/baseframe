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

// $(function(){
// 	var windowHeight = $(window).height();
// 		$('.navbar-collapse').css('max-height',( windowHeight - 50));
// });

$(function(){
	$('.navbar-collapse').css('max-height',(window.innerHeight));
// Listen for orientation changes
window.addEventListener("orientationchange", function() {
	if( window.orientation == 0){
		$('.navbar-collapse').css('max-height',(window.innerHeight));
		// alert("width="+$('.navbar-collapse').css('width')+
		// 	" , height="+$('.navbar-collapse').css('max-height')+
		// 	" , win-width="+(window.innerWidth)+
		// 	" , win-height="+(window.innerHeight));

	} else if( window.orientation == 90){
		$('.navbar-collapse').css('max-height',(window.innerHeight));			
		//$('.navbar-collapse').css('max-height',(window.innerHeight));
		// alert("width="+$('.navbar-collapse').css('width')+
		// 	" , height="+$('.navbar-collapse').css('max-height')+
		// 	" , win-width="+(window.innerWidth)+
		// 	" , win-height="+(window.innerHeight));
	}
	// Announce the new orientation number
	//alert(window.orientation+" ,"+window.innerWidth+", "+$('#page-header').height());
	//$('.navbar-collapse').css({'max-height':(window.innerWidth - 150), 'width': '100%'});
	//alert(getElementById('navbar-collapse').style.maxHeight);
}, false);
});
