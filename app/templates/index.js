function updateBrightnessLabel(value) {
    $('#brightnessLabel').html(value);
}

$(document).ready(function() {

    $('#videoFeed').on('load', function() {
        videoWidth = this.width;
        console.log('Detected video width: '+ videoWidth);
        $('#cropSlider').width(videoWidth);
    });

    var cropSlider = document.getElementById('cropSlider');

    noUiSlider.create(cropSlider, {
        start: [0, 100],
        connect: true,
        range: {
            'min': 0,
            'max': 100
        }
    });
    cropSlider.noUiSlider.on('change', function(values, handle, unencoded, tap, positions, noUiSlider) {
        console.log('slider: '+values);
        $.ajax({
            data :
                {
		            cropLeft : values[0],
		            cropRight : values[1]
                },
                type : 'POST',
                url : '{{ url_for('crop') }}'
        });
    });

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
            $('#videoFeed').attr("src", "/video_feed?"+d.getTime());
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
