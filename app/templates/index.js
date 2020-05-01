function updateBrightnessLabel(value) {
    $('#brightnessLabel').html(value);
}

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
    });

    $('#vflip').on('change', function(event) {
        $.ajax({
            data :
                {
		            vflip : this.checked
                },
                type : 'POST',
                url : '{{ url_for('vflip') }}'
        });
    });
});
