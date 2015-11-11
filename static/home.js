$(document).ready(function () {

    var imageIndex = -1;
    var active = true;

    setInterval(changeImage, 5000);


    function changeImage() {
        if (!active)
            return;
        imageIndex += 1;
        var $images = $('.img-slider');
        if (imageIndex > $images.length - 1)
            imageIndex = 0;
        var image = $images.get(imageIndex);
        var url = $(image).attr("src");
        var title = $(image).attr("data-title");
        var text = $(image).attr("data-text");
        var link = $(image).attr("data-link");

        $images.removeClass("active");
        $(image).addClass("active");


        var $panel = $('.slider-image');

        if (!$(image).position())
            return;

        var scrollSize = $panel.scrollLeft() + $(image).position().left - 100;
        $panel.animate({scrollLeft: scrollSize}, 500);

        $("#slide-image, #slide-title, #slide-text")
            .fadeOut(400, function () {
                $("#slide-image").attr('src', url);
                $("#slide-title").html(title);
                $("#slide-text").html(text);
                $(".slider-text").attr("href", link);
            })
            .fadeIn(400);
    }

    changeImage();


    $('.img-slider').click(function () {
        var myIndex = $(this).index();
        imageIndex = myIndex - 1;
        active = true;
        changeImage();
    });

    $('.slider').mouseenter(function () {
        active = false;
    }).mouseleave(function () {
        active = true;
    });

    $('.card-container').mouseenter(function () {
        $(this).addClass('active');
    }).mouseleave(function () {
        $(this).removeClass('active');
    });

    $('.tab-link').click(function () {
        $('.tab-link').removeClass("active");
        $(this).addClass("active");

        var tabId = $(this).attr('data-tab');

        $(".tab").hide();

        $("#" + tabId).fadeIn(300);
    });

    var flag = false;
    $('.right-arrow').click(function () {
        if (flag)return;

        flag = true;
        var $panel = $('.slider-image');

        $panel.animate({scrollLeft: $panel.scrollLeft() + 100}, 500, function () {
            flag = false;
        });

    });

    $('.left-arrow').click(function () {
        if (flag)return;

        flag = true;
        var $panel = $('.slider-image');

        $panel.animate({scrollLeft: $panel.scrollLeft() - 100}, 500, function () {
            flag = false;
        });

    });


    // EXPERIENCE FILTER

    $('.exp-left-header').click(function () {

        var uni = $('.uni-filter').val();
        var service = $('.service-filter').val();
        var year = $('.year-filter').val();
        var tag = $('#tag-id').val();

        if (uni || service || year || tag) {
            $('.exp-choose').submit();
        }

    });


    $("#tag-search").on("keyup", function () {
        var word = $(this).val().trim();

        if (word.length > 1)

            $.ajax({
                type: 'GET',
                url: tag_url,
                data: {
                    'q': word
                },
                success: function (msg) {
                    var res = eval(msg);

                    $("ul#tag-res").empty();

                    for (var k in res) {
                        if (res.hasOwnProperty(k)) {
                            $('<li />', {'html': res[k], 'data-value': k}).appendTo('ul#tag-res')
                        }
                    }

                    $("ul#tag-res").fadeIn();

                }
            });
        else
            $("ul#tag-res").empty();


    });

    $(document).on('click', "ul#tag-res li", function () {
        $('#tag-id').val($(this).attr('data-value'));
        $("#tag-search").val($(this).html().trim());
    });

    $("#tag-search").focusin(function () {
    }).focusout(function () {
        $("ul#tag-res").fadeOut();
    });


});
