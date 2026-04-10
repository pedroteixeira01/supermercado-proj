document.addEventListener("DOMContentLoaded", () => {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");

	if (!token || role !== "admin") {
		window.location.href = "index.html";
		return;
	}

	loadCategories();
	loadProducts();

	document
		.getElementById("add-product-form")
		.addEventListener("submit", handleAddProduct);
	document
		.getElementById("add-user-form")
		.addEventListener("submit", handleAddUser);

	document.querySelectorAll(".admin-tab").forEach((btn) => {
		btn.addEventListener("click", () => {
			document
				.querySelectorAll(".admin-tab")
				.forEach((b) => b.classList.remove("active"));
			btn.classList.add("active");

			const tab = btn.dataset.tab;
			document.getElementById("tab-produtos").style.display =
				tab === "produtos" ? "grid" : "none";
			document.getElementById("tab-usuarios").style.display =
				tab === "usuarios" ? "grid" : "none";

			if (tab === "usuarios") loadUsers();
		});
	});
});

async function loadCategories() {
	const select = document.getElementById("prod-category");
	try {
		const res = await fetch(`${API_BASE}/products/categories`);
		if (!res.ok) throw new Error();
		const categories = await res.json();
		select.innerHTML =
			'<option value="">Selecione a categoria</option>' +
			categories
				.map((c) => `<option value="${c.id}">${c.name}</option>`)
				.join("");
	} catch {
		select.innerHTML = '<option value="">Erro ao carregar categorias</option>';
	}
}

async function loadProducts() {
	const loading = document.getElementById("admin-loading");
	const table = document.getElementById("products-table");
	const tbody = document.getElementById("products-tbody");

	try {
		const res = await fetch(`${API_BASE}/products/`);
		if (!res.ok) throw new Error();
		const products = await res.json();

		loading.style.display = "none";
		table.style.display = "table";

		tbody.innerHTML =
			products.length === 0
				? '<tr><td colspan="4" style="text-align:center;color:#888;">Nenhum produto cadastrado.</td></tr>'
				: products
						.map(
							(p) => `
					<tr>
						<td>${p.id}</td>
						<td>${p.name}</td>
						<td>${p.category || "—"}</td>
						<td>R$ ${p.price.toFixed(2).replace(".", ",")}</td>
					</tr>
				`,
						)
						.join("");
	} catch {
		loading.textContent = "Erro ao carregar produtos.";
	}
}

async function handleAddProduct(e) {
	e.preventDefault();
	const token = localStorage.getItem("token");
	const submitBtn = e.target.querySelector("button[type=submit]");

	const payload = {
		name: document.getElementById("prod-name").value.trim(),
		description:
			document.getElementById("prod-description").value.trim() || null,
		price: parseFloat(document.getElementById("prod-price").value),
		category_id:
			parseInt(document.getElementById("prod-category").value) || null,
		image_url: document.getElementById("prod-image").value.trim() || null,
	};

	submitBtn.disabled = true;
	submitBtn.textContent = "Adicionando...";

	try {
		const res = await fetch(`${API_BASE}/products/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify(payload),
		});

		if (res.ok) {
			showFeedback(
				"product-feedback",
				"Produto adicionado com sucesso!",
				"success",
			);
			e.target.reset();
			loadProducts();
		} else {
			const err = await res.json().catch(() => ({}));
			showFeedback(
				"product-feedback",
				`Erro: ${err.detail || "Tente novamente."}`,
				"error",
			);
		}
	} catch {
		showFeedback("product-feedback", "Erro de conexão com a API.", "error");
	} finally {
		submitBtn.disabled = false;
		submitBtn.textContent = "Adicionar Produto";
	}
}

async function loadUsers() {
	const loading = document.getElementById("users-loading");
	const table = document.getElementById("users-table");
	const tbody = document.getElementById("users-tbody");
	const token = localStorage.getItem("token");

	loading.style.display = "block";
	table.style.display = "none";

	try {
		const res = await fetch(`${API_BASE}/users/`, {
			headers: { Authorization: `Bearer ${token}` },
		});
		if (!res.ok) throw new Error();
		const users = await res.json();

		loading.style.display = "none";
		table.style.display = "table";

		tbody.innerHTML =
			users.length === 0
				? '<tr><td colspan="4" style="text-align:center;color:#888;">Nenhum usuário encontrado.</td></tr>'
				: users
						.map(
							(u) => `
					<tr>
						<td>${u.id}</td>
						<td>${u.email}</td>
						<td><span class="role-badge role-badge--${u.role}">${u.role || "—"}</span></td>
						<td>${u.is_active ? "✓" : "✗"}</td>
					</tr>
				`,
						)
						.join("");
	} catch {
		loading.textContent = "Erro ao carregar usuários.";
	}
}

async function handleAddUser(e) {
	e.preventDefault();
	const token = localStorage.getItem("token");
	const submitBtn = e.target.querySelector("button[type=submit]");

	const payload = {
		email: document.getElementById("user-email").value.trim(),
		password: document.getElementById("user-password").value,
	};

	submitBtn.disabled = true;
	submitBtn.textContent = "Criando...";

	try {
		const res = await fetch(`${API_BASE}/users/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify(payload),
		});

		if (res.ok) {
			showFeedback("user-feedback", "Usuário criado com sucesso!", "success");
			e.target.reset();
			loadUsers();
		} else {
			const err = await res.json().catch(() => ({}));
			showFeedback(
				"user-feedback",
				`Erro: ${err.detail || "Tente novamente."}`,
				"error",
			);
		}
	} catch {
		showFeedback("user-feedback", "Erro de conexão com a API.", "error");
	} finally {
		submitBtn.disabled = false;
		submitBtn.textContent = "Criar Usuário";
	}
}

function showFeedback(id, message, type) {
	const el = document.getElementById(id);
	el.textContent = message;
	el.className = `admin-feedback admin-feedback--${type}`;
	el.style.display = "block";
	setTimeout(() => {
		el.style.display = "none";
	}, 4000);
}
