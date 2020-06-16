window.onscroll = function() {
	var winScrolled = window.scrollY/window.innerHeight;
	console.log("Window scrolled:", winScrolled);
	if(winScrolled >= .5)
		$('#uplink').attr("class", "vis");
	else
		$('#uplink').attr("class", "invis");
}

function waveScrollTo(offset, time) {
        $('body,html').animate({scrollTop:offset}, time);return false;

        event.preventDefault();
        return false;
    }