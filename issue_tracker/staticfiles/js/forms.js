function removeuser(e) {
    console.log($(this));
    $.ajax({
            url: 'remove-user/' + $(this).attr('issueid'),
            data: 'id=' + $(this).attr('uid'),
            context: $(this).parent('td')
        })
        .done(function(response) {
            $(this).html(response);
            $('.remove-user').on('click', removeuser);
        })
        .fail(function(response) {
            console.log("Error: ");
            console.log(response);
        });
}

function clean_modal_form() {
    $('#modal-selected-users').html('');
    $('#ids').val('');
    $('.modal-target').removeClass('modal-target');
}

$(document).ready(function() {
    // Autocomplete off
    if (document.getElementsByTagName) {
        var inputElements = document.getElementsByTagName("input");
        for (i = 0; inputElements[i]; i++) {
            if (inputElements[i].className && (inputElements[i].className.indexOf("disableAutoComplete") != -1)) {
                inputElements[i].setAttribute("autocomplete", "off");
            }
        }
    }

    //Autocomplete for the search bar and new issue #category field.
    $.getJSON(
        '/api/categories?format=json',
        function(json) {
            var autocomplete_lists = {};
            autocomplete_lists['.nav-search'] = [];
            autocomplete_lists['#category'] = [];

            $.each(json, function(item) {
                autocomplete_lists['.nav-search'].push(json[item].name);
                autocomplete_lists['#category'].push(json[item].name);
            });
            Object.keys(autocomplete_lists).forEach(function(key) {
                $(key).autocomplete({
                    source: autocomplete_lists[key],
                    autoFocus: true,
                });
            });
        });

    //Autocomplete for the #notifications form
    $.getJSON(
        '/api/users/?format=json',
        function(json) {
            var autocomplete_lists = {};
            autocomplete_lists['#notifications'] = [];
            $.each(json, function(item) {
                autocomplete_lists['#notifications'].push({
                    label: json[item].first_name + ' ' + json[item].last_name + ', ' + json[item].email,
                    value: json[item].id
                });
            });
            $('#notifications').autocomplete({
                source: autocomplete_lists['#notifications'],
                autoFocus: true,
                select: function(event, ui) {
                    $('#notify-users').append(
                        '<li><span class="tag light">' + ui.item.label + '</span></li>'
                    );
                    $('input#notify-ids').val(
                        $('input#notify-ids').val() + ' ' + ui.item.value
                    );
                    $('#notifications').val('');
                    return false;
                }
            });
        });

    //Form constraints for severity
    $("#severity").on("keyup keydown", function(e) {
        if (e.originalEvent.key.match(/0|[6-9]|\D+/g) || $('#severity').val().length >= 1) {
            if (e.originalEvent.keyCode != 8 && e.originalEvent.keyCode != 46) {
                // Backspace and delete are ok I guess
                e.preventDefault();
            }
        }
        //apply filter to things like copy and pastes
        $('#severity').val(
            $('#severity').val().replace(/0|[6-9]|\D/g, '')
        );
        //enforce length = 1
        if ($('#severity').val().length > 1) {
            $('#severity').val($('#severity').val().substring(0, 1));
        }
    });

    /* Generate the preview */
    $('#shortdesc, #desc, #severity, #category').keyup(function(e) {
        $('.issue-inner').html(
            '<h4>' +
            $('#category').val() +
            '-###</h4>' +
            $('#shortdesc').val()
        );
        var sev = '?';
        var sevclass = '3';
        if ($('#severity').val().length > 0) {
            sev = $('#severity').val();
            sevclass = $('#severity').val();
        }
        $('.grid-info').html(
            '<br><span class="sev-' + sevclass + '">' +
            sev +
            '</span><p>Created By: Username<br>Created: <em>Now</em><br>Updated: <em>Now</em></p>'
        );
        $('.grid-footer').html(
            '<h4>Issue Details</h4>' + $('#desc').val()
        );
    });

    $('.show-modal').on('click', function(e) {
        // Clean up the form and set its properties.
        clean_modal_form();
        $('#modal-selected-users').attr(
            'modal-max-selections',
            $(this).attr('modal-max-selections')
        );

        // Show the pop-up form.
        $('.modal').fadeIn(200);
        $('#modal-loader').fadeIn(200);
        $('#modal-form').attr(
            'action',
            $(this).attr('modal-action')
        );
        e.preventDefault();

        $(this).parent().prev().addClass('modal-target');

        // Populate the autocomplete.
        $.getJSON(
            '/api/users?format=json',
            function(json) {
                var autocomplete_lists = {};
                autocomplete_lists['.modal-users'] = [];

                $.each(json, function(item) {
                    autocomplete_lists['.modal-users'].push({
                        label: json[item].first_name + ' ' + json[item].last_name + ', ' + json[item].email,
                        value: json[item].id
                    });
                });

                $('.modal-users').autocomplete({
                    source: autocomplete_lists['.modal-users'],
                    autoFocus: true,
                    select: function(e, ui) {
                        $('.modal-users').val('');
                        if ($('#modal-selected-users').children('li').length < $('#modal-selected-users').attr('modal-max-selections') &&
                            $('#modal-selected-users:contains("' + ui.item.label + '")').length == 0) {
                            $('#modal-selected-users').append(
                                '<li><span class="tag light">' + ui.item.label + '</span></li>'
                            );
                            $('input#ids').val(
                                $('input#ids').val() + ' ' + ui.item.value
                            );
                        }
                        return false;
                    }
                });
                $('#modal-loader').fadeOut();
            });
    });

    $('#modal-form').submit(function(e) {
        e.preventDefault();
        var data = $(this).serialize();
        // Select the TD element to pass it to the .done handler.
        var context = $(this).attr('issue-id');
        context = $('.modal-target');
        $('#modal-loader').fadeIn();
        console.log(context);
        $.ajax({
                url: $(this).attr('action'),
                data: data,
                context: context
            })
            .done(function(response) {
                $(this).html(response);
                console.log($(this));
                $('#modal-loader').fadeOut();
                $('.modal').fadeOut();
            })
            .fail(function(response) {
                console.log("Error: ");
                console.log(response);
                $('#modal-loader').fadeOut();
            });
    });

    $('.mark-complete, .drop-issue').on("submit", function(e) {
        e.preventDefault();
        var data = $(this).serialize();
        var context = $(this).children('input').first().val();
        context = $('#issue-' + context);

        $.ajax({
                data: data,
                url: $(this).attr('action'),
                context: context
            })
            .done(function(response) {
                $(this).fadeOut();
            })
            .fail(function(response) {
                console.log("Request failed.")
            });
    });

    $('.edit, td.sev-td').on('click', function(e) {
        if (e.target.nodeName == "INPUT") {
            return false;
        }
        
        var text = $(this);

        if ($(this).hasClass('sev-td')) {
            text = $(this).children('.edit').first();
            console.log(text);
        }

        if (text.is(':animated')) {
            return false;
        }

        if (text.is(':visible')) {
            text.fadeToggle(200);
            text.next().delay(200).fadeToggle(200);
        } else {
            text.delay(200).fadeToggle(200);
            text.next().fadeToggle(200);
        }

        text.parent('td').toggleClass('selected');
        return false;
    });

    $('.dropdown-toggle').on('click', function(e) {
        $(this).next().slideToggle()
        $(this).toggleClass('active');
    });

    $('.edit-show').on('keydown', function(e) {
        if (e.keyCode == 13) {
            $(this).hide();
            $(this).siblings('.loader-sm').fadeIn();
            var issueid = $(this).parents('tr').attr('issue-id');
            var data = $(this).serialize();
            var context = $(this).prev('.edit');
            console.log(context);
            $.ajax({
                    url: '/super/edit-priority/' + issueid,
                    data: data,
                    context: context
                })
                .done(function(response) {
                    $(this).css('color', '');
                    $(this).siblings('.loader-sm').fadeOut();
                    $(this).html(response);
                    $(this).delay(500).fadeIn();
                })
                .fail(function(response) {
                    $(this).siblings('.loader-sm').fadeOut(100);
                    $(this).delay(500).fadeIn();
                    $(this).delay(500).css('color', 'red');
                    console.log("response:", response);
                });
        }
    });

    $('.remove-user').on('click', removeuser);

    $(document).on('keyup', function(e) {
        if (e.keyCode == 27) {
            //escape pressed
            $('.edit-show').hide();
            $('.edit').show();
            $('.modal').hide();
        }
    });

    $('#showreg').click(function() {
        $('#login').fadeOut(200);
        $('#register').delay(200).fadeIn(200);
    });

    $('#showlogin').click(function() {
        $('#login').delay(200).fadeIn(200);
        $('#register').fadeOut(200);
    });
});