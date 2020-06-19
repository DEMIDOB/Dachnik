function mouseOver(divId) {
    document.getElementById(divId).classList.add("productDescHover");
}

function mouseLeave(divId) {
    document.getElementById(divId).classList.remove("productDescHover");
}

function makeRequest(url) {
	const xhr = new XMLHttpRequest();
	xhr.open("GET", url, false);
	xhr.send();
	return xhr.responseText;
}

function buyButtonPressed(requestUrl) {
	html_data = makeRequest(requestUrl);
	console.log(html_data);
	$('#detail_view_content').html(html_data);
}