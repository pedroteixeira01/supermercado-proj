const API_BASE = "http://localhost:8000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
	const loginForm = document.getElementById("loginForm");
	if (!loginForm) return;

	loginForm.addEventListener("submit", async (e) => {
		e.preventDefault();
		const formData = new FormData(loginForm);

		try {
			const response = await fetch(`${API_BASE}/auth/login/access-token`, {
				method: "POST",
				body: formData,
			});

			if (response.ok) {
				const data = await response.json();
				localStorage.setItem("token", data.access_token);

				try {
					const meRes = await fetch(`${API_BASE}/auth/me`, {
						headers: { Authorization: `Bearer ${data.access_token}` },
					});
					if (meRes.ok) {
						const me = await meRes.json();
						if (me.role) localStorage.setItem("role", me.role);
					}
				} catch (_) {}

				window.location.href = "index.html";
			} else {
				const errorMsg = document.getElementById("login-error-msg");
				errorMsg.style.display = "block";
				errorMsg.style.background = "#f8d7da";
				errorMsg.style.color = "#721c24";
				setTimeout(() => {
					errorMsg.style.display = "none";
				}, 3000);
			}
		} catch (error) {
			console.error("Erro de login:", error);
		}
	});
});
