function updateBrightnessLabel(value) {
    $('#brightnessLabel').html(value);
}

$(document).ready(function() {

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
        }).done(function(data){
            // offset video to the right according to the position of the left slide handle
            $('#videoFeed').css('margin-left', positions[0] + 'px');
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
            // attach current date to image source to force reload instead of cache
            d = new Date();
            $('#videoFeed').attr("src", "/video_feed?"+d.getTime());

            // adapt the slider width to the new camera source image size
            $('#cropSlider').width(data.videoWidth);
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
