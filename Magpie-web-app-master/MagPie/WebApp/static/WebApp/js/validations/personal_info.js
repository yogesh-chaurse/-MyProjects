$(document).ready(function(){
    $('#personalInfoForm').validate({
        onKeyup:true,
        onChange:true,
        onBlur:true,
        onSubmit:true,
        eachValidField : function() {
            $(this).closest('.inpData').removeClass('has-error').addClass('has-success');
        },
        eachInvalidField : function() {
            $(this).closest('.inpData').removeClass('has-success').addClass('has-error');
        },
        description :{
            first_name:{
                required:'<div class="error">' + gettext('Please enter first name') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid first name') + '</div>'
            },
            last_name:{
                required:'<div class="error">' + gettext('Please enter last name') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid last name') + '</div>'
            },
            address_line1:{
                required:'<div class="error">' + gettext('Please enter address line 1') + '</div>',
            },
            city:{
                required:'<div class="error">' + gettext('Please enter city') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid city') + '</div>'
            },
            country:{
                required:'<div class="error">' + gettext('Please enter country') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid country') + '</div>'
            },
            zipcode:{
                required:'<div class="error">' + gettext('Please enter postcode') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid postcode') + '</div>',

            },
            phone_number:{
                required:'<div class="error">' + gettext('Please enter phone number') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid phone number') + '</div>',

            },
            email:{
                required:'<div class="error">' + gettext('Please enter email id') + '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid email id') + '</div>'
            }
        }
    });
});