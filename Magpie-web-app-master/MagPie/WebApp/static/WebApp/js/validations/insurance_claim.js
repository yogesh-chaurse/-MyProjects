$(document).ready(function(){
    var isRead = 0;
    $('input[type=file]').val();
    /*$('#id_claim_types').change(function(){
        isRead = 0;
        var claim_type = $(this).val();
        $('.claim_msg').remove();
        $('.file_msg').remove();
        $.ajax({
            url:"/insurance_claim_details/",
            type:'GET',
            dataType:'JSON',
            data:{id:$(this).val()},
            success: function(data){
                $('.moreInfo').before("<div><p class='claim_msg  inpField clear'>" + data['claim_description'] + "<p></div>");
                $('#id_claim_description').prop('placeholder',data['placeholder']);
                $('.file_description').html(gettext('Attach Proof of ') + claim_type);
            }
        });
    });*/

   $('#insuranceForm').validate({
        onKeyup:true,
        onChange:true,
        onBlur:true,
        onSubmit:true,
        eachValidField : function() {
            $(this).closest('.inpField').removeClass('has-error').addClass('has-success');
        },
        eachInvalidField : function() {
            $(this).closest('.inpField').removeClass('has-success').addClass('has-error');
        },
        description :{
            id_claim_types:{
                required:'<div class="error">' + gettext('Please select claim types') + '</div>',
                conditional:'<div class="error">' + gettext('Please read the conditions and exclusions for the selected insurance type.') + '</div>',
            },
            id_address_line1:{
                required:'<div class="error">' + gettext('Please enter address line 1') + '</div>',
                conditional:'<div class="error">' + gettext('Please enter address line 1') + '</div>',
            },
            id_city:{
                required:'<div class="error">' + gettext('Please enter city') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid city') + '</div>',
            },
            id_country:{
                required:'<div class="error">' + gettext('Please enter country') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid country') + '</div>'
            },
            id_zipcode:{
                required:'<div class="error">' + gettext('Please enter postcode') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid postcode') + '</div>',
            },
            email:{
                required:'<div class="error">' + gettext('Please enter email id') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid email id') + '</div>'
            },
            attach_file:{
                required:'<div class="error">' + gettext('Please attach file') + '</div>',
            }
        },
        conditional : {
            check_spaces : function(value) {
                if(value.trim()==''){
                    return false;
                }
                else {
                    return true;
                }
            },
            check_more_info_read : function(){
                if(!isRead){
                    return false;
                } else {
                    return true;
                }
            }
        }
   });

   $('#attach_file').on('change' , function(e) {
         var file_extn =['png','jpg','jpeg'];
         filename_extn = $('input[type=file]').val().split('\\').pop().split('.').splice(-1,1);
        if(!($.inArray(filename_extn[0] , file_extn )>=0))
        {
           $('#attach_file-description').append(gettext("File type should be png jpg only"));
        }
   });

   $('#moreInfo').on('click', function(){
       isRead = 1;
   });
	  $('.closeLink').click(function(){
	 	$('#id_claim_types').blur();
	 });
	$('.popup').click(function(){
		$('#id_claim_types').blur();
	});
});

function checkError(){
    var isError = 0;
    if($('div.error').length > 0){
        isError = 1;
    }
    if(isError == 0) {
        $.ajax({
            url: "/check_personal_info_changes/",
            type: "POST",
            async:true,
            data: {
                'addressLine1':$('#id_address_line1').val(),
                'addressLine2':$('#id_address_line2').val(),
                'addressLine3':$('#id_address_line3').val(),
                'city':$('#id_city').val(),
                'country':$('#id_country').val(),
                'postcode':$('#id_zipcode').val(),
                'email':$('#email').val(),
                'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()
            },
            success:function(response){
                if(response === "True"){
                    var confirmBox = confirm(gettext('We noticed the contact info you submitted is different than your contact info on file, do you want to update your contact info on file?'));
                    if(confirmBox == false) {
                        $('#savePersonalInfo').val("0");
                    } else {
                        $('#savePersonalInfo').val("1");
                    }
                }
                $('#insuranceForm').submit();
            }
        });
    }
    return true;
}