$(document).ready(function () {

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
                        'last_index': last_index,
                        'uni': $("select#uni-select").val(),
                        's': $("select.service").val(),
                        't': $("#tag-id").val(),
                        'tn': $("#tag-search").val(),
                        'y': $("select.date").val()
                    },
                    success: function (msg) {
                        var res = msg;
                        $('.item-list').append(res);
                    }
                });
            }
        }
    });

    $('#uni-state, #uni-type').change(function () {
        var uniState = $('#uni-state').val();
        var uniType = $('#uni-type').val();

        if (uniState && uniType) {
            $.ajax({

                type: 'GET',
                url: uni_url,

                data: {
                    'last_index': last_index,
                    state: uniState,
                    type: uniType
                },

                success: function (msg) {
                    var res = eval(msg);

                    $("select#uni-select").empty();

                    $('<option />', {
                        'html': "انتخاب دانشگاه",
                        'value': "",
                    }).appendTo('select#uni-select');

                    for (var k in res) {
                        if (res.hasOwnProperty(k)) {
                            $('<option />', {'html': res[k], 'value': k}).appendTo('select#uni-select')
                        }
                    }

                }
            });
        } else {
            $("select#uni-select").empty();
            $('<option />', {
                'html': "انتخاب دانشگاه",
                'value': "",
                'disabled': 'disabled'
            }).appendTo('select#uni-select');
            $("select#uni-select").val("");
            $("select.uni option").html("انتخاب دانشگاه");
        }
    });

    $("select#uni-select").change(function () {
        $("select.uni option").html($(this).find(":selected").text());
    });

});