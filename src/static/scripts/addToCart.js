

function addToCart(article) {
	amount = document.getElementById('count1').innerHTML;
	document.getElementById('modalAmount').innerHTML = amount;
	makeRequest("/cart/add/?article=" + article + "&amount=" + amount);
}