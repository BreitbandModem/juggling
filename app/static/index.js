$(document).ready(function() {
    $('#calibrate_form').on('submit', function(event) {
        $.ajax({
            data :
                {
                    brightness : $('#brightness').val()
                },
                type : 'POST',
                url : '/'
        });
        event.preventDefault();
    });
});