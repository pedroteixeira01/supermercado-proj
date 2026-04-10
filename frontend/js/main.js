document.addEventListener("DOMContentLoaded", () => {
	loadComponent("header-placeholder", "/components/header.html");
	loadComponent("footer-placeholder", "/components/footer.html");

	const contactForm = document.getElementById("contactForm");
	if (contactForm) {
		contactForm.addEventListener("submit", handleFormSubmit);
	}
});

async function loadComponent(elementId, componentPath) {
	try {
		const response = await fetch(componentPath);
		if (!response.ok) throw new Error("Falha ao carregar componente");
		const html = await response.text();
		document.getElementById(elementId).innerHTML = html;

		// Ativar menu mobile após carregar header
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
	const authLink = document.getElementById("auth-link");

	if (authLink) {
		if (token) {
			authLink.textContent = "Sair";
			authLink.href = "#";
			authLink.addEventListener("click", (e) => {
				e.preventDefault();
				localStorage.removeItem("token");
				window.location.reload();
			});
		} else {
			authLink.textContent = "Login";
			authLink.href = "login.html";
		}
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

// Consumo da API no Backend
async function fetchProducts() {
	const productList = document.getElementById("product-list");
	const loading = document.getElementById("loading");

	try {
		const response = await fetch("http://localhost:8000/api/v1/products/");
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

			// Usando logo como fallback de imagem
			const imgSrc =
				product.image_url &&
				product.image_url !== "images/maca.jpg" &&
				product.image_url !== "images/alface.jpg" &&
				product.image_url !== "images/picanha.jpg" &&
				product.image_url !== "images/pao.jpg" &&
				product.image_url !== "images/refrigerante.jpg" &&
				product.image_url !== "images/suco.jpg"
					? product.image_url
					: "/images/logo.svg";

			card.innerHTML = `
                <img src="${imgSrc}" alt="${product.name}" class="product-img">
                <div class="product-category">${product.category || "Sem Categoria"}</div>
                <h3>${product.name}</h3>
                <p class="product-price">R$ ${product.price.toFixed(2).replace(".", ",")}</p>
                <p>${product.description}</p>
            `;
			productList.appendChild(card);
		});
	} catch (error) {
		console.error("Erro na API:", error);
		loading.innerText =
			"Erro ao carregar os produtos. Verifique se a API está rodando.";
	}
}
