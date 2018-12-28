// Constants
var autocomplete_lists = new Object();

$.getJSON(
    '/api/categories?format=json',
    function(json) {
        autocomplete_lists['.nav-search'] = [];
        autocomplete_lists['#category'] = [];

        $.each(json, function(item) {
            console.log(json[item]);
            autocomplete_lists['.nav-search'].push(json[item].name);
            autocomplete_lists['#category'].push(json[item].name);
        });
        console.log(autocomplete_lists);
        Object.keys(autocomplete_lists).forEach(function(key) {
            $(key).autocomplete({
                source: autocomplete_lists[key],
                autoFocus: true,
            });
        });
    });


$.getJSON(
    '/api/users/?format=json',
    function(json) {
        console.log(json)
        json.each(function(item) {
            autocomplete_lists['.search-users'].push(
                json[item].first_name + ' ' + json[item].last_name + ' ' + json[item.email]);
        });
    });


$(document).ready(function() {
    $("#severity").on("keyup keydown", function(e) {
        if (e.originalEvent.key.match(/0|[6-9]|\D+/g) || $('#severity').val().length >= 1) {
            if (e.originalEvent.keyCode != 8 && e.originalEvent.keyCode != 46) {
                // Backspace and delete are ok I guess
                e.preventDefault();
            }
        }
        //filter pastes
        $('#severity').val(
            $('#severity').val().replace(/0|[6-9]|\D/g, '')
        );
        //enforce length = 1
        if ($('#severity').val().length > 1) {
            $('#severity').val($('#severity').val().substring(0, 1));
        }
    });

    $('#shortdesc, #desc, #severity, #category').keyup(function(e) {
        $('.issue-inner').html(
            '<h4>'
            + $('#category').val()
            + '-###</h4>'
            + $('#shortdesc').val()
            );
        var sev = '?';
        if ($('#severity').val().length > 0) {
            sev = $('#severity').val();
        }
        $('.grid-info').html(
            '<div class="sev">' 
            + sev 
            + '</div><p>Created By: Username<br>Created: <em>Now</em><br>Updated: <em>Now</em></p>'
        );
        $('grid-footer').html('<h4>Issue Details</h4>' + $('#desc').val());
    });

    $('input#notifications').keypress(function(e) {
        console.log(e);
    });
});