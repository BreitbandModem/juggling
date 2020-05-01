$(document).ready(function() {
    $('#inputSelection').on('change', function(event) {
        $.ajax({
            data :
                {
		            inputSelection : this.value
                },
                type : 'POST',
                url : '{{ url_for('input_selection') }}'
        }).done(function(data){
            d = new Date();
            $('#video_feed').attr("src", "/video_feed?"+d.getTime());
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
                url : '{{ url_for('brightness') }}'
        });
        event.preventDefault();
    });
});
