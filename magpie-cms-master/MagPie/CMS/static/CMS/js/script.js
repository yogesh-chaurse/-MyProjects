$(document).ready(function(){
	sectionHeight();
	activeMenu();
	menuDropdown();
	flashMessage();
	sectionShowHide();
	customCheckbox();
});

/* Calculate the section height */
function sectionHeight(){
	var headerHeight = $('.magpieHeader').outerHeight();
    var windowHeight = $(window).height();
$('.commonWrap').css('min-height', windowHeight - headerHeight);
}
$(window).resize(function(){
	sectionHeight();
});

/* Function menu active state */
function activeMenu(){
		$('.navbar-nav li a').click(function(){
				$('.navbar-nav li a').removeClass('active');
				$(this).addClass('active');
		});
}

/* Function Navigation animation */
function menuDropdown(){
	$('.magpieHeader .dropdownToggle').click(function(){
		$('.dropdown').animate({
			left: '0'
		},500);
		$('.menuOpecWrap').show('fast');
	});

	$('.dropdownClose').click(function(){
		$('.dropdown').animate({
			left: '-290'
		},500);
		$('.menuOpecWrap').hide('fast');

	});
	$('.menuOpecWrap').click(function(){
		$('.dropdown').animate({
			left: '-290'
		},500);
		$(this).hide('fast');

	});
 }

 /* function Checkbox */
 function customCheckbox(){
	$('input[type="radio"]:checked').parent().addClass('checked')

	$('input[type="radio"]').change(function () {
	 $('input[type="radio"]').parent().removeClass("checked");
		if($('input[type="radio"]').is(":checked")) {
			$(this).parent().addClass("checked");
		} else {
			$('input[type="radio"]').parent().removeClass("checked");
		}
	});
	}

 /* FUnction Menu slide */

 function sectionShowHide() {
  $(".screens").hide();
$(".screens#webAppScreen").show();
    $(".appOptions li a").on('click',function(){
        $(".appOptions li a").removeClass('active');
        $(this).addClass('active');
        var $hrefID = $(this).attr('data-href');
        $(".screens").slideUp();
        $($hrefID).slideDown();
    })

}

/* Flash Message */

function flashMessage(){
	$('.messages').delay(3000).fadeOut('slow');
}


