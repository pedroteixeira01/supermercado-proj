document.addEventListener("DOMContentLoaded", () => {
	loadComponent("header-placeholder", "components/header.html");
	loadComponent("footer-placeholder", "components/footer.html");
	setupCartPopup();

	const contactForm = document.getElementById("contactForm");
	if (contactForm) {
		contactForm.addEventListener("submit", handleFormSubmit);
	}
});

// ====== COMPONENTES ======

async function loadComponent(elementId, componentPath) {
	try {
		const response = await fetch(componentPath);
		if (!response.ok) throw new Error("Falha ao carregar componente");
		const html = await response.text();
		document.getElementById(elementId).innerHTML = html;

		if (elementId === "header-placeholder") {
			setupMobileMenu();
			highlightCurrentPage();
			checkAuthState();
		}
	} catch (error) {
		console.error("Erro:", error);
	}
}

function checkAuthState() {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");
	const authLink = document.getElementById("auth-link");
	const cartBtn = document.getElementById("cart-btn");
	const adminContainer = document.getElementById("admin-link-container");

	if (authLink) {
		if (token) {
			authLink.textContent = "Sair";
			authLink.href = "#";
			authLink.addEventListener("click", (e) => {
				e.preventDefault();
				localStorage.removeItem("token");
				localStorage.removeItem("cart");
				localStorage.removeItem("role");
				window.location.reload();
			});
			if (cartBtn) {
				cartBtn.style.display = "flex";
				updateCartUI();
			}
			if (adminContainer && role === "admin") {
				adminContainer.style.display = "";
			}
		} else {
			authLink.textContent = "Login";
			authLink.href = "login.html";
			if (cartBtn) cartBtn.style.display = "none";
		}
	}

	if (cartBtn) {
		cartBtn.addEventListener("click", () => openCartPopup());
	}
}

function setupMobileMenu() {
	const btn = document.querySelector(".mobile-menu-btn");
	const nav = document.querySelector(".nav-links");
	if (btn && nav) {
		btn.addEventListener("click", () => {
			nav.classList.toggle("active");
		});
	}
}

function highlightCurrentPage() {
	const links = document.querySelectorAll(".nav-links a");
	const currentPath = window.location.pathname;

	links.forEach((link) => {
		if (currentPath.includes(link.getAttribute("href"))) {
			link.style.color = "var(--primary-color)";
		}
	});
}

function handleFormSubmit(e) {
	e.preventDefault();
	const msg = document.getElementById("form-msg");
	msg.style.display = "block";
	e.target.reset();
	setTimeout(() => {
		msg.style.display = "none";
	}, 3000);
}

// ====== CARRINHO ======

let cart = JSON.parse(localStorage.getItem("cart") || "[]");

function saveCart() {
	localStorage.setItem("cart", JSON.stringify(cart));
}

function getCartTotal() {
	return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function getCartItemCount() {
	return cart.reduce((sum, item) => sum + item.quantity, 0);
}

function updateCartUI() {
	const countEl = document.getElementById("cart-count");
	if (countEl) {
		countEl.textContent = getCartItemCount();
	}
}

function addToCart(product) {
	if (!localStorage.getItem("token")) {
		alert("Faça login para adicionar produtos ao carrinho.");
		window.location.href = "login.html";
		return;
	}
	const existing = cart.find((i) => i.id === product.id);
	if (existing) {
		existing.quantity++;
	} else {
		cart.push({ id: product.id, name: product.name, price: product.price, quantity: 1 });
	}
	saveCart();
	updateCartUI();
	showCartToast(`"${product.name}" adicionado ao carrinho!`);
}

function removeFromCart(productId) {
	cart = cart.filter((i) => i.id !== productId);
	saveCart();
	updateCartUI();
	renderCartItems();
}

function changeQuantity(productId, delta) {
	const item = cart.find((i) => i.id === productId);
	if (!item) return;
	item.quantity += delta;
	if (item.quantity <= 0) {
		removeFromCart(productId);
		return;
	}
	saveCart();
	updateCartUI();
	renderCartItems();
}

function showCartToast(message) {
	const toast = document.getElementById("cart-toast");
	if (toast) {
		toast.textContent = message;
		toast.style.display = "block";
		setTimeout(() => (toast.style.display = "none"), 2500);
	}
}

function setupCartPopup() {
	const overlay = document.createElement("div");
	overlay.id = "cart-overlay";
	overlay.className = "cart-overlay";
	overlay.innerHTML = `
        <div class="cart-popup">
            <div class="cart-popup-header">
                <h2>Meu Carrinho</h2>
                <button id="cart-close" class="cart-close" aria-label="Fechar carrinho">✕</button>
            </div>
            <div class="cart-popup-items" id="cart-popup-items"></div>
            <div class="cart-popup-footer">
                <div class="cart-total-row">
                    <span>Total:</span>
                    <strong id="cart-total-amount">R$ 0,00</strong>
                </div>
                <button class="btn-checkout" id="checkout-btn">Prosseguir Compra</button>
            </div>
        </div>
    `;
	document.body.appendChild(overlay);

	const toast = document.createElement("div");
	toast.id = "cart-toast";
	toast.className = "cart-toast";
	document.body.appendChild(toast);

	document.getElementById("cart-close").addEventListener("click", closeCartPopup);
	overlay.addEventListener("click", (e) => {
		if (e.target === overlay) closeCartPopup();
	});
	document.getElementById("checkout-btn").addEventListener("click", () => {
		closeCartPopup();
		window.location.href = "checkout.html";
	});
}

function openCartPopup() {
	renderCartItems();
	document.getElementById("cart-overlay").classList.add("open");
	document.body.style.overflow = "hidden";
}

function closeCartPopup() {
	document.getElementById("cart-overlay").classList.remove("open");
	document.body.style.overflow = "";
}

function renderCartItems() {
	const itemsEl = document.getElementById("cart-popup-items");
	const totalEl = document.getElementById("cart-total-amount");

	if (cart.length === 0) {
		itemsEl.innerHTML = '<p class="cart-empty">Seu carrinho está vazio.</p>';
		totalEl.textContent = "R$ 0,00";
		return;
	}

	itemsEl.innerHTML = cart
		.map(
			(item) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">R$ ${(item.price * item.quantity).toFixed(2).replace(".", ",")}</div>
            </div>
            <div class="cart-item-controls">
                <button class="qty-btn" onclick="changeQuantity(${item.id}, -1)">−</button>
                <span>${item.quantity}</span>
                <button class="qty-btn" onclick="changeQuantity(${item.id}, 1)">+</button>
                <button class="qty-btn remove-btn" onclick="removeFromCart(${item.id})" aria-label="Remover">✕</button>
            </div>
        </div>
    `
		)
		.join("");

	totalEl.textContent = `R$ ${getCartTotal().toFixed(2).replace(".", ",")}`;
}

// ====== PRODUTOS ======

async function fetchProducts() {
	const productList = document.getElementById("product-list");
	const loading = document.getElementById("loading");

	try {
		const response = await fetch(`${API_BASE}/products/`);
		if (!response.ok) throw new Error("Erro ao buscar produtos da API");

		const products = await response.json();
		loading.style.display = "none";

		if (products.length === 0) {
			productList.innerHTML = "<p>Nenhum produto encontrado.</p>";
			return;
		}

		products.forEach((product) => {
			const card = document.createElement("div");
			card.className = "product-card";

			const imgSrc =
				product.image_url &&
				product.image_url !== "images/maca.jpg" &&
				product.image_url !== "images/alface.jpg" &&
				product.image_url !== "images/picanha.jpg" &&
				product.image_url !== "images/pao.jpg" &&
				product.image_url !== "images/refrigerante.jpg" &&
				product.image_url !== "images/suco.jpg"
					? product.image_url
					: "images/logo.svg";

			card.innerHTML = `
                <img src="${imgSrc}" alt="${product.name}" class="product-img">
                <div class="product-category">${product.category || "Sem Categoria"}</div>
                <h3>${product.name}</h3>
                <p class="product-price">R$ ${product.price.toFixed(2).replace(".", ",")}</p>
                <p>${product.description}</p>
                <button class="btn-add-cart">Adicionar ao Carrinho</button>
            `;

			card.querySelector(".btn-add-cart").addEventListener("click", () => {
				addToCart({ id: product.id, name: product.name, price: product.price });
			});

			productList.appendChild(card);
		});
	} catch (error) {
		console.error("Erro na API:", error);
		loading.innerText =
			"Erro ao carregar os produtos. Verifique se a API está rodando.";
	}
}
