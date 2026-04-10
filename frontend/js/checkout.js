const API_BASE = "http://localhost:8000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
	if (!localStorage.getItem("token")) {
		window.location.href = "login.html";
		return;
	}

	renderCheckout();
	document.getElementById("confirm-btn").addEventListener("click", confirmOrder);
});

function renderCheckout() {
	const checkoutCart = JSON.parse(localStorage.getItem("cart") || "[]");
	const itemsEl = document.getElementById("checkout-items");
	const totalEl = document.getElementById("checkout-total");
	const confirmBtn = document.getElementById("confirm-btn");

	if (checkoutCart.length === 0) {
		itemsEl.innerHTML =
			'<p>Seu carrinho está vazio. <a href="produtos.html">Ver produtos</a></p>';
		confirmBtn.style.display = "none";
		return;
	}

	let total = 0;
	itemsEl.innerHTML = checkoutCart
		.map((item) => {
			const subtotal = item.price * item.quantity;
			total += subtotal;
			return `
			<div class="checkout-item">
				<div class="checkout-item-info">
					<span class="checkout-item-name">${item.name}</span>
					<span class="checkout-item-qty">Qtd: ${item.quantity}</span>
				</div>
				<span class="checkout-item-subtotal">R$ ${subtotal.toFixed(2).replace(".", ",")}</span>
			</div>
		`;
		})
		.join("");

	totalEl.textContent = `R$ ${total.toFixed(2).replace(".", ",")}`;
}

async function confirmOrder() {
	const checkoutCart = JSON.parse(localStorage.getItem("cart") || "[]");
	const token = localStorage.getItem("token");
	const btn = document.getElementById("confirm-btn");

	btn.disabled = true;
	btn.textContent = "Processando...";

	try {
		const response = await fetch(`${API_BASE}/orders/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify({
				items: checkoutCart.map((item) => ({
					product_id: item.id,
					quantity: item.quantity,
				})),
			}),
		});

		if (response.ok) {
			localStorage.removeItem("cart");
			document.getElementById("checkout-view").style.display = "none";
			document.getElementById("success-view").style.display = "block";
		} else if (response.status === 401 || response.status === 403) {
			alert("Sessão expirada. Faça login novamente.");
			localStorage.removeItem("token");
			window.location.href = "login.html";
		} else {
			const err = await response.json().catch(() => ({}));
			alert(
				`Erro: ${err.detail || "Não foi possível criar o pedido. Tente novamente."}`,
			);
			btn.disabled = false;
			btn.textContent = "Confirmar Pedido";
		}
	} catch (e) {
		alert("Erro de conexão. Verifique se a API está rodando.");
		btn.disabled = false;
		btn.textContent = "Confirmar Pedido";
	}
}
