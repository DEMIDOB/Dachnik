

function addToCart(article) {
	amount = document.getElementById('count1').innerHTML;
	makeRequest("/cart/add/?article=" + article + "&amount=" + amount);
}