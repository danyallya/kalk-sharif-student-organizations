$(document).ready(function () {

    //ENTER SEARCH
    $('.enter-search').keyup(function (event) {
        if (event.keyCode == 13) {
            $(this).parents('form').first().submit();
        }
    });


});