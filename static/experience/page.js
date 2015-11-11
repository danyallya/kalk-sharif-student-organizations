$(document).ready(function () {


    $('.send-image').click(function () {
        $('#send-image-file').click();
    });

    $('#send-image-file').change(function () {
        var fileName = $(this).val();
        if (fileName) {
            $('#send-image-form').submit();
        }
    });


    $('#experience-extra-images').Thumbelina({
        $bwdBut: $('#experience-extra-images .left'),    // Selector to left button.
        $fwdBut: $('#experience-extra-images .right')    // Selector to right button.
    });

    $("a.fancy-image").fancybox({
        prevMethod: 'changeIn',
        nextMethod: 'changeOut'
    });


    $('#show-all-images').click(function () {
        var dialog = $("#dialog-gallery").dialog({
            autoOpen: false,
            height: 'auto',
            width: 'auto',
            modal: true,
            close: function () {
            }
        });
        dialog.dialog("open");
    });


});