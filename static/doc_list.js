$(document).ready(function () {

    $('.card-container:not(.active)').hover(function () {
        $(this).addClass('active');
    }, function () {
        $(this).removeClass('active');
    });


    $('.rate-h').each(function () {
        var rate = $(this).attr("data-rate");

        var width = 0;
        if (rate == 0) {

        } else if (rate == 5) {
            width = 91;
        } else {
            width = 13 + (rate * 13);
        }

        $(this).width(width);

    });

});