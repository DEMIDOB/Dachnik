

function addToCart(article) {
	amount = document.getElementById('count1').innerHTML;
	response = makeRequest("/cart/add/?article=" + article + "&amount=" + amount);
	if (response == "0") {
		document.getElementById('modalAmount').innerHTML = "Успешно добавлено в корзину " + amount + " шт.";
	} else {
		document.getElementById('modalAmount').innerHTML = "Невозможно добавить в корзину так много товаров!";
	}
}