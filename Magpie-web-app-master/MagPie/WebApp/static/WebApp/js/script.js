$(document).ready(function(){
	sectionHeight();
	menuDropdown();
	flashMessage();
	getInputFileValue();
	customCheckbox();
	CustomSelect();
	popup();
});

/* Calculate the section height */
function sectionHeight(){
	var headerHeight = ($('.magpieHeader').outerHeight(true));
	var windowHeight = $(window).height();

$('.commonWrap').css('min-height', windowHeight - headerHeight);
}

/* Calculate the section height on window resize */
$(window).resize(function(){
	sectionHeight();
});

/* Function Navigation animation */
function menuDropdown(){
	$('.magpieHeader .responsiveMenu').click(function(){
		$('.menuSlide').animate({
			left: '0'
		},500);
		$('.menuOpecWrap').show('fast');
	});

	$('.linkClose').click(function(){
		$('.menuSlide').animate({
			left: '-290'
		},500);
		$('.menuOpecWrap').hide('fast');

	});
	$('.menuOpecWrap').click(function(){
		$('.menuSlide').animate({
			left: '-290'
		},500);
		$(this).hide('fast');

	});
 }

/* Select Box Function */
function CustomSelect(){
	$("select").wrap("<div class='selectWrap'></div>")
		$(".selectWrap").prepend("<div class='customSelect'></div>")

		$("select").each(function(){
				$(this).prev().html($('option:selected',this).text());
		});

		$("select").click(function(){
				$(this).prev().html($('option:selected',this).text());
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

/* Flash Message */

function flashMessage(){
	$('.messages').delay(3000).fadeOut('slow');
}

/* Popup Functionality */
function popup(){
	 $('#moreInfo').click(function(){
	 	$('.popup').fadeIn('slow');
	 });
	  $('.closeLink').click(function(){
	 	$('.popup').fadeOut('slow');
	 });
	$('.popup').click(function(){
		$(this).fadeOut('slow');
	});
	$(".popupOverlay").click(function(e){
		e.stopPropagation();
	});
}


/* Custom upload file getting value*/
function getInputFileValue(){
$("#attach_file").on("change",function(){
		var currentValue = $(this).val();
		$("#inpFile").html(currentValue);
	});
}

