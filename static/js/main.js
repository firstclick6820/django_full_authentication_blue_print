$(document).ready(function() {
    $('.choice input[type=radio]').click(function() {
        $('.choice').removeClass('bg-red-600');
        $(this).parent().parent().addClass('bg-red-600');
    });
});