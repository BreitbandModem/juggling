$(document).ready(function() {
    $('#inputSelection').on('change', function(event) {
        alert( this.value );
        $.ajax({
            data :
                {
		            inputSelection : this.value
                },
                type : 'POST',
                url : '/'
        });
        event.preventDefault();
    });

    $('#brightness').on('change', function(event) {
        $.ajax({
            data :
                {
		            brightness : this.value
                },
                type : 'POST',
                url : '/'
        });
        event.preventDefault();
    });
});
