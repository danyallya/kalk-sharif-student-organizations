$(document).ready(function () {

    checkButtons();

    if (typeof $.validationEngineLanguage != 'undefined') {

        $.extend($.validationEngineLanguage.allRules, {
            "mobile": {
                "regex": /^0\d{10}$/,
                "alertText": "* شماره تلفن همراه معتبر وارد کنید"
            },
            only_english: {
                "regex": /^[0-9a-zA-Z!#\$%&'\*\+\-\/=\?\^_`{\|}~@.,]+$/,
                "alertText": "* فقط اعداد و حروف انگلیسی وارد کنید"
            },
            usernameAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
//                "alertTextOk": "این نام کاربری در دسترس است",
                "alertText": "* این نام‌کاربری تکراری است"
//                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            },
            emailAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
//                "alertTextOk": "این ایمیل در دسترس است",
                "alertText": "* این پست الکترونیک تکراری است"
//                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            },
            nameAjaxEngineCall: {
                "url": "/ajax/validationEngine/",
//                "alertTextOk": "این ایمیل در دسترس است",
                "alertText": "* این نام تکراری است"
//                "alertTextLoad": "* درحال اعتبار سنجی، لطفا صبر کنید"
            }
        });
//        $(".js-validation-from").validationEngine({
//            promptPosition: "centerLeft:0,-5",
//            scroll: true,
//            validationEventTrigger: 'blur'
//        });
    }
    $('#logo-container').click(function () {
        location.replace("/");
    });
//    $(".js-validation-from").submit(function () {
//        $('.dynamic-formset0').each(function () {
//            var has_val = false;
//            $(this).find('input[type=text], select').each(function () {
//                var value = $(this).val();
//                if (value && value != '') {
//                    has_val = true
//                }
//            });
//            if (!has_val) {
//                alert($(this).attr('class'));
//                $(this).validationEngine('detach');
//                $(this).validationEngine('hideAll');
//            }
//        });
//    });


    $(window).mouseover(function (ev) {
        var target = $(ev.target);
        var elId = target.attr('id');
        var title = target.attr('data-title');
        if (title && typeof title != "undefined") {
            $('#help-bar').html(title);
        }
    });


    // TABS JS

    $('.tab-link').click(function (e) {
        var tab_id = $(this).attr('data-tab');

        $('.tab-link').removeClass('current');
        $('.tab-content').removeClass('current');

        $(this).addClass('current');
        $("#" + tab_id).addClass('current');

        e.stopPropagation();
        e.preventDefault();
    });

    // TREE JS

    $('.tree li').each(function () {
        if ($(this).children('ul').length > 0) {
            $(this).addClass('parent');
        }
    });

    $(document).on('click', '.tree li.parent > .tree-item', function (e) {
        $(this).parent().toggleClass('active');
        $(this).parent().children('ul').slideToggle('fast');
        e.stopPropagation();
        e.preventDefault();
    });

    //$(document).on('click', '.tree li.parent > .tree-item a', function (e) {
    //    e.stopPropagation();
    //    e.preventDefault();
    //});


    $('.tree #toggleall').click(function () {

        $('.tree li').each(function () {
            $(this).toggleClass('active');
            $(this).children('ul').slideToggle('fast');
        });
    });

    // DATA TOOLTIPS
    if (typeof help != "undefined") {
        $('[id]').each(function () {
            if ($(this).attr('id') in help) {
                $(this).attr('data-title', help[$(this).attr('id')]);
            }
        });

        $('[class]').each(function () {
            var $this_element = $(this);

            $($this_element.attr('class').split(' ')).each(function () {
                if (this in help) {
                    $this_element.attr('data-title', help[this]);
                }
            });
        });
    }

    // STICKY DOC HEADERS
    if (typeof $.fn.stickySectionHeaders != 'undefined')
        reStick();

    // SELECT2 UNIVERSITY
    django_select2.s2_state_param_gen = function (term, page) {
        var proxFunc = $.proxy(django_select2.get_url_params, this);
        // no need for a custom func here.
        var results = proxFunc(term, page, 'django_select2.process_results');
        results.state = $("[id$='uni_state']").val();
        results.uni_type = $("[id$='uni_type']").val();
        return results;
    };


});

function reStick() {
    $('#sticky-list').stickySectionHeaders({
        stickyClass: 'sticky',
        headlineSelector: 'h1'
    });

}


function checkButtons() {
    $('button, input[type=submit], input[type=reset], input[type=button], .button_link').button();
}

function popitup(url, windowName) {
    var width = '600';
    var height = '500';
    var left = (screen.width / 2) - (width / 2);
    var top = (screen.height / 2) - (height / 2);

    newwindow = window.open(url, windowName, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
    if (window.focus) {
        newwindow.focus()
    }
    return false;
}


function createIfNotExist(term, data) {
    if (!data || jQuery(data).filter(function () {
            return this.text.localeCompare(term) === 0;
        }).length === 0) {
        return {
            id: term,
            text: term
        };
    }
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}


// COMMENTS PANEL HANDLE


if (typeof sendCommentUrl != "undefined") {

    $(document).on('click', '.comment-reply', function () {
        if ($(this).parent().find('.reply-form').find('.comment-form-text').size() == 0) {
            var content = $('#comment-form-content').html();
            $(this).parent().find('.reply-form').first().append(content);
            $(this).parent().find('.reply-form').fadeIn();
        } else {
            $(this).parent().find('.reply-form').fadeOut(function () {
                $(this).parent().find('.reply-form').first().html("");
            });
        }
    });

    $(document).on('click', '.comment-form-submit', function () {
        var $form_text = $(this).parent().find('.comment-form-text').first();
        var $form_name = $(this).parent().find('.comment-form-name').first();
        var $form_uni_name = $(this).parent().find('.comment-form-uni').first();
        var text = $form_text.val().trim();
        var name = "", uni_name = "";
        if ($form_name.length > 0)
            name = $form_name.val().trim();
        if ($form_uni_name.length > 0)
            uni_name = $form_uni_name.val().trim();
        var $reply_form = $(this).parent().parent().find('.reply-form');
        if (!text) {
            alert("متن پیام اجباری است.");
            return;
        }
        var parent_id = '';
        if ($(this).parents('.comment-item').size() != 0) {
            parent_id = $(this).parents('.comment-item').first().attr('data-comment-id');
        }
        $.ajax({
            type: 'POST',
            url: sendCommentUrl,
            data: {
                'id': objId,
                'parent_id': parent_id,
                'text': text,
                'name': name,
                'uni_name': uni_name
            },
            success: function (msg) {
                var res = eval(msg);
                var message = res.message;
                alertify.success(message);
                $form_text.val("");
                if (parent_id) {
                    $reply_form.fadeOut(function () {
                        $reply_form.first().html("");
                    });
                }
                if (res.res) {
                    var content = res.content;
                    if (content)
                        if (parent_id) {
                            $('#comments-ul li[data-comment-id=' + parent_id + ']').after(content);
                        } else {
                            $('#comments-ul').append(content);
                        }
                }

            }
        });
    });
}

if (typeof sendRateUrl != "undefined")
    $(document).on('change', '.rating', function () {
        var rate = $(this).val();

        $.ajax({
            type: 'POST',
            url: sendRateUrl,
            data: {
                'id': objId,
                'rate': rate
            },
            success: function (msg) {
                var res = eval(msg);
                var message = res.message;
                alertify.success(message);
            }
        });
    });
