(function($) {
    var OTHER_CHOICE = '__other__'; //See
    $(function(){
        var wrappers = $('.choice_with_other_wrapper');
        wrappers.each(function(){
            var select = $('select', this);
            var text_input = $('input', this);
            select.change(function(){
                if(!(select.val() == OTHER_CHOICE)){
                    text_input.hide();
                }else{
                    text_input.show();
                }
            })
            select.change();
        })
    })
})(django.jQuery);
