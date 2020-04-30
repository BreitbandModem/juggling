$(document).ready(function() {
    $('#brightness').on('change', function(event) {
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
