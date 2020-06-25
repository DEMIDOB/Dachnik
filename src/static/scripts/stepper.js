
function BtnOncl (button, countId, countMax) {
	
	let btn = button.innerHTML
	let countSpan = document.getElementById (countId)
	let countInner = countSpan.innerHTML
	let countNum = Number(countInner)
	if (btn == "+" && countNum < countMax) {
		countNum = countNum + 1
		countSpan.innerHTML = countNum

	}
	if (btn == "-" && countNum > 1) {
		countNum = countNum - 1
		countSpan.innerHTML = countNum

	}

}