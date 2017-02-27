$(document).ready(function(){
    $('#id_date_time').datetimepicker({
        pick12HourFormat: true,
        endDate: new Date(),
        autoclose: true
    });

    $('#id_date_time').datetimepicker().on('changeDate', function(){
        $(this).blur();
    });

     var checkedAtLeastOne = false;
     $('#submitBtn').click(function(){
        $('input[type="checkbox"]').each(function() {
            if ($(this).is(":checked")) {
                checkedAtLeastOne = true;
            }
            last_checkbox = $(this)
        });
        if(!checkedAtLeastOne) {
            alert(gettext('Please select at least one card.'));
            return false;
        }
     });

      $('#lostCardsForm').validate({
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
            id_address:{
                required:'<div class="error">' + gettext('Please enter address') + '</div>',
            },
             id_contact_info:{
                required:'<div class="error">' + gettext('Please enter valid data') + '</div>',
            },
            id_zipcode:{
                required:'<div class="error">' + gettext('Please enter postcode') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid postcode') + '</div>',
            },
            email:{
                required:'<div class="error">' + gettext('Please enter email id') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid email id') + '</div>'
            },
            id_date_time:{
                required:'<div class="error">' + gettext('Please select date and time') + '</div>',
            },
            id_lost_stolen:{
                required:'<div class="error">' + gettext('Please select at least one') + '</div>',
            }
        }
    });
});