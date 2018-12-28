$(document).ready(function() {
    $('.issue').on("mousedown mouseenter mouseleave", function(e) {
        // Only animate if the div has a URL.
        if ($(this).attr("url")) {
            if (e.type === "mousedown") {
                $(this).addClass("active");
                window.location = $(this).attr("url");
            }
            if (e.type === "mouseenter") {
                // $(this).addClass("hover");
                $(this).width($(this).width() * 1.02);
                $(this).height($(this).height() * 1.02);
            }
            if (e.type ==="mouseleave") {
                // $(this).removeClass("hover");
                $(this).width($(this).width() / 1.02);
                $(this).height($(this).height() / 1.02);
            }
        }
    });

    $('nav div.expand i').on("click", function(e) {
        console.log("clicked");
        $('.collapse').slideToggle();
    });

    $('tbody tr').on('click', function(e) {
        if (e.target.tagName == 'TD') {
            $(this).toggleClass('selected');
            $(this).find('button.hide').animate({width: 'toggle', height: 'toggle', padding: 'toggle', margin: 'toggle', border: 'toggle'});
        }
    });

    $('.x').on('click', function(e) {
        $('.modal').fadeOut(200);
    });

    $('.show-modal').on('click', function(e) {
        $('.modal').fadeIn(200);
        e.preventDefault();
    });
});
