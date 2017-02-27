$('#activateBundleServices').validate({
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
                required:'<div class="error">'+ gettext('Enter valid email Id')+ '</div>',
                pattern:'<div class="error">' + gettext('Please enter valid email id') + '</div>'
            },

        }
});