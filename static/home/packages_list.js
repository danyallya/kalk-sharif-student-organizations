$(document).ready(function () {


    $('.rate-h').each(function () {
        var rate = $(this).attr("data-rate");

        var width = 0;
        if (rate == 0) {

        } else if (rate == 5) {
            width = 106;
        } else {
            width = 12 + (rate * 16);
        }

        $(this).width(width);

    });


    var last_index = 0;
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() > $(document).height() - 200) {

            var last_id = $('.item').last().index();

            if (last_id > last_index) {
                last_index = last_id;
                $.ajax({

                    type: 'GET',
                    url: page_url,

                    data: {
                        'last_index': last_index
                    },
                    success: function (msg) {
                        var res = msg;
                        $('.item-list').append(res);
                    }
                });
            }

        }
    });
});