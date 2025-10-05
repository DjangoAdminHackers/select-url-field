(function ($) {
    'use strict';

    /* 1.  Cache the promise so we hit the server only once per page load */
    var choicesPromise = null;
    function getChoices() {
        if (!choicesPromise) {
            choicesPromise = $.getJSON('/select-url-choices/');
        }
        return choicesPromise;
    }

    /* 2.  Build <select> out of the JSON */
    function buildSelect(data, currentVal) {
        var $sel = $('<select>', { 'class': 'ajax-select-url-select' });
        $sel.append('<option value="">---------</option>')
        var got_selected = false;
        $.each(data, function (_, group) {
            var $og = $('<optgroup>', { label: group.group_name });
            $.each(group.group_choices, function (_, opt) {
                /* opt = [label, value] */
                var val = opt[1];
                var selected = (val === currentVal);
                $og.append(
                    $('<option>', {
                        text:  opt[0],
                        value: val,
                        selected: selected   // keep existing value
                    })
                );
                if(selected){
                    got_selected = true;
                }
            });
            $sel.append($og);
        });
        if(got_selected){
            $sel.append('<option value="__other__"></option>')
        }else{
            $sel.append('<option value="__other__" selected=""></option>')
        }
        return $sel;
    }

    /* 3.  Upgrade one text input */
    function upgradeInput($input) {
        if ($input.hasClass('upgraded')) { return; }   // run once
        $input.addClass('upgraded');
        $input.attr({"size": "80"});
        var currentVal = $input.val();
        getChoices().done(function (data) {
            var $select = buildSelect(data, currentVal);

            /* copy the base part of the name/id from the text input */
            var baseName = $input.attr('name');
            var baseId   = $input.attr('id');

            $select.attr({
                name: baseName + '_0',
                id:   baseId   + '_0',
            });

            /* insert select right before the text box */
            $input.before($select);
        });
    }

    /* 4.  Auto-initialise */
    $(function () {
        $('input.ajax-select-url').each(function () {
            upgradeInput($(this));
        });
    });

    /* 5.  Django-admin dynamic inlines */
    $(document).on('formset:added', function (ev, row) {
        row.find('input.ajax-select-url').each(function () {
            upgradeInput($(this));
        });
    });
})(jQuery);