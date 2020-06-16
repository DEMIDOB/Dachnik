window.onscroll = function() {
	
}

function waveScrollTo(offset, time) {
        $('body,html').animate({scrollTop:offset}, time);return false;

        event.preventDefault();
        return false;
    }