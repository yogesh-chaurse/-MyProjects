$('#login').validate({
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
            email:{
                required:'<div class="error">'+ gettext('Enter email Id')+ '</div>',
                pattern:'<div class="error">' + gettext('Enter valid email id') + '</div>'
            },
            password:{
                required:'<div class="error">'+ gettext('Enter password')+ '</div>',
            },

        }
});