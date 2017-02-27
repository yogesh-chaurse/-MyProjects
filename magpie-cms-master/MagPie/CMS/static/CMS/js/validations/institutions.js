$(document).ready(function(){
    $('#institutionForm').validate({
        onKeyup:true,
        onChange:true,
        onBlur:true,
        onSubmit:true,
        eachValidField:function () {
            $(this).closest('.inpData').removeClass('has-error').addClass('has-success');
        },
        eachInvalidField:function () {
            $(this).closest('.inpData').removeClass('has-success').addClass('has-error');
        },
        eachField:function() {
            userText = $(this).val().replace(/^\s+/, '').replace(/\s+$/, '');
            if (userText === '') {
                $(this).val('');
            }
        },
        description:{
            name_en:{
                required:'<div class="error">Please enter institution name in English</div>',
                pattern:'<div class="error">Please enter valid institution name</div>'
            },
            allow_reorder_cards:{
                required:'<div class="error">Please select at least one</div>',
            },
            contact_no:{
                required:'<div class="error">Please enter contact number</div>',
                pattern:'<div class="error">Please enter valid contact number</div>'
            },
            region:{
                required:'<div class="error">Please enter region / country</div>',
                pattern:'<div class="error">Please enter valid region / country</div>'
            },
            email:{
                pattern:'<div class="error">Please enter valid contact email</div>'
            },
        }
    });
});