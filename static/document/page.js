$(document).ready(function () {


    $('.comments_link').each(function () {
        var objId = $(this).parent().attr('data-id');
        var $countSpan = $(this).find('span').first();
        $(this).attr('href', showCommentUrl + "?id=" + objId);
        $(this).fancybox({
            helpers: {
                overlay: {
                    css: {
                        'background': 'rgba(194,194,194, 0.5)',
                        'overflow': 'auto'
                    }
                }
            },
            padding: 0,
            afterClose: function () {
                $.ajax({
                    type: 'GET',
                    url: countCommentUrl,
                    data: {
                        'id': objId
                    },
                    success: function (msg) {
                        var res = eval(msg);
                        var count = res.count;
                        $countSpan.html(count);
                    }
                });
            },
            height: 300,
            width: 500
        });
    });

    $('.refs_link').each(function () {
        var objId = $(this).parent().attr('data-id');
        $(this).attr('href', showReferencesUrl + "?id=" + objId);
        $(this).fancybox({
            helpers: {
                overlay: {
                    css: {
                        'background': 'rgba(194,194,194, 0.5)',
                        'overflow': 'auto'
                    }
                }
            },
            padding: 0,
            afterClose: function () {
            },
            height: 300,
            width: 300
        });
    });

    $(document).on('click', '.tree-item', function (e) {

        var $panel = $("#main-doc-content");

        // SCROLL BODY TO TOP OF CONTENT
        var $body = $('body');
        var topOfContent = $panel.offset().top;
        var bodyScroll = $body.scrollTop();
        if (bodyScroll > topOfContent + 10 || bodyScroll < topOfContent - 20)
            $body.animate({scrollTop: topOfContent - 10}, 200);


        // SCROLL CONTENT TO SELECTED ITEM
        var data_id = parseInt($(this).attr('data-id'));
        var $element = $('#level-' + data_id);
        if (typeof $element.next().position() != "undefined")
            $element = $element.next();
        //if (data_id == 0)return;
        var scrollSize = $panel.scrollTop() + $element.position().top - $element.height() - 30;
        $panel.animate({scrollTop: scrollSize}, 1500);
    });


    var currentH2Id = '';
    $('#main-doc-content').scroll(function () {

        // SCROLL BODY TO TOP OF CONTENT
        var $body = $('body');
        var topOfContent = $(this).offset().top;
        var bodyScroll = $body.scrollTop();
        if (bodyScroll > topOfContent + 10 || bodyScroll < topOfContent - 20)
            $body.animate({scrollTop: topOfContent - 10}, 200);

        // FOR OPEN AND CLOSE TREE WHEN SCROLL ON CONTENT
        var cutoff = $(this).scrollTop();
        var $mostTop = $(this).find('h2').first();
        $(this).find('h2').each(function () {
            if ($(this).offset().top > 0) {
                var objId = $mostTop.attr('data-id');
                if (currentH2Id == objId)
                    return false;
                else
                    currentH2Id = objId;
                var tagId = '#level-link-' + objId;

                $('.tree li').each(function () {
                    if ($(this).find(tagId).length == 0) {

                        $(this).removeClass('active');
                        $(this).children('ul').slideUp('fast');
                    }
                });

                $(tagId).addClass('active');
                $(tagId).children('ul').slideDown('fast');

                $(tagId).parents('li').addClass('active');
                $(tagId).parents('li').children('ul').slideDown('fast');
                return false;
            }
            $mostTop = $(this);
        });
    });

});