window.addEventListener("load", function() {
    (function($) {
        var OTHER_CHOICE = '__other__'; //See
        $(function(){
            $('body').delegate('.choice_with_other_wrapper select', 'change', function(e){
                var select = $(this)
                var text_input = $(this).parent().find('input')
                if(select.val() == OTHER_CHOICE){
                    ;
                }else{
                    text_input.val(select.val());
                }
            });
            var text_input = $('input', this);
            $('body').delegate('.choice_with_other_wrapper input', 'keyup', function(e){
                var match = false;
                var text_input = $(this)
                var select = $(this).parent().find('select')
                $(select).find('option').each(function(){
                    if($(this).attr('value') == text_input.val()){
                        match = true;
                    }
                })
                if(!match){
                    select.val(OTHER_CHOICE);
                }else{
                    select.val(text_input.val());
                }
            })

            $('.choice_with_other_wrapper').each(function(){
                $('select', this).change();
            })

        })
    })(django.jQuery);
});
