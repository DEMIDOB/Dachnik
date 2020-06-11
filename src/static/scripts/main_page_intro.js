function finalize(argument) {
	
	let inviss = document.getElementsByClassName('invis');
	for (var i = inviss.length - 1; i >= 0; i--) {
		inviss[i].classList.add('vis');
		inviss[i].classList.remove('invis');
	}

	let futureColMd7s = document.getElementsByClassName('futureColMd7');
	for (var i = futureColMd7s.length - 1; i >= 0; i--) {
		futureColMd7s[i].classList.add('col-md-7');
		futureColMd7s[i].classList.remove('futureColMd7');
	}

	let futureColMd5s = document.getElementsByClassName('futureColMd5 vis');
	for (var i = futureColMd5s.length - 1; i >= 0; i--) {
		futureColMd5s[i].classList.add('col-md-5');
		futureColMd5s[i].classList.remove('futureColMd5');
	}

	let img = document.getElementsByClassName('logo_vid')[0];
	img.src = "http://demidob.site/dch/vids/logo-w.mp4";
	console.log(img);
}

function makeNormal() {
	console.log("xui");

	let thief = document.getElementById('center_me');
	thief.classList.remove('absolute_me');
	thief.classList.add('normalizeMe');

	setTimeout(finalize, 2000);
}

window.onload = function () {
	makeNormal();
}