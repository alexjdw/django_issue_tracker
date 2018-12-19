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
});