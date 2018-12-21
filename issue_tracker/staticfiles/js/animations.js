$(document).ready(function() {
    $('.issue').on("mousedown mouseup mouseenter mouseleave", function(e) {
        // Only animate if the div has a URL.
        if ($(this).attr("url")) {
            if (e.type === "mousedown") {
                $(this).addClass("active");
                window.location = $(this).attr("url");
            }
            if (e.type === "mouseenter") {
                $(this).addClass("hover");
            }
            if (e.type ==="mouseleave") {
                $(this).removeClass("hover");
            }
        }
    });

    $('nav div.expand i').on("click", function(e) {
        console.log("clicked");
        $('.collapse').slideToggle();
    });

    $('tbody tr').on('click', function(e) {
        if (e.target.tagName == 'BUTTON' || e.target.tagName == 'a') {
            return;
        }
        $(this).toggleClass('selected');
        $(this).find('button.hide').animate({width: 'toggle', height: 'toggle', padding: 'toggle', margin: 'toggle', border: 'toggle'});
    });
});