(function($) {
    var OTHER_CHOICE = '__other__'; //See
    $(function(){
        var wrappers = $('.choice_with_other_wrapper');
        wrappers.each(function(){
            var select = $('select', this);
            var text_input = $('input', this);
            select.change(function(){
                text_input.val(select.val());
//                if(!(select.val() == OTHER_CHOICE)){
//                    text_input.show();
//                }else{
//                    text_input.show();
//                }
            });
            text_input.keyup(function(){
                select.val(text_input.val());
            });
            select.change();
        })
    })
})(django.jQuery);
