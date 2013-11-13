(function($) {
    var OTHER_CHOICE = '__other__'; //See
    $(function(){
        var wrappers = $('.choice_with_other_wrapper');
        wrappers.each(function(){
            var select = $('select', this);
            var text_input = $('input', this);
            select.change(function(){
                if(select.val() == OTHER_CHOICE){
                    ;
                }else{
                    text_input.val(select.val());
                }
            });
            text_input.keyup(function(){
                var match = false;
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
            });
            select.change();
        })
    })
})(django.jQuery);
