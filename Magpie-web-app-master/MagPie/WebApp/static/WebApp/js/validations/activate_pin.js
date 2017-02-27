$(document).ready(function(){
    $('#activatePinForm').validate({
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
            pin:{
                required:'<div class="error">' + gettext('Please enter the PIN') + '</div>',
                pattern:'<div class="error">' + gettext('Please input your 8 digit PIN') + '</div>'
            }
        }
    });
});