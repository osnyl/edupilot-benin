(() => {
  const tabs = Array.from(document.querySelectorAll("[data-mode]"));
  const panels = {
    login: document.getElementById("login-panel"),
    register: document.getElementById("register-panel"),
  };
  const schoolInput = document.getElementById("school-name");
  const schoolHeading = document.getElementById("welcome-school-name");
  const roleInputs = Array.from(document.querySelectorAll('input[name="school-role"]'));
  const loginAction = document.getElementById("login-action");
  const registerAction = document.getElementById("register-action");
  const loginStatus = document.getElementById("login-status");
  const registerStatus = document.getElementById("register-status");

  function setMode(mode) {
    for (const tab of tabs) {
      const selected = tab.dataset.mode === mode;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    }
    for (const [panelMode, panel] of Object.entries(panels)) {
      panel.hidden = panelMode !== mode;
    }
  }

  for (const tab of tabs) {
    tab.addEventListener("click", () => setMode(tab.dataset.mode));
    tab.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      const nextMode = tab.dataset.mode === "login" ? "register" : "login";
      setMode(nextMode);
      document.querySelector(`[data-mode="${nextMode}"]`).focus();
    });
  }

  function selectedRole() {
    return roleInputs.find((input) => input.checked)?.value || "";
  }

  function updateRoleActions() {
    const enabled = Boolean(selectedRole());
    loginAction.disabled = !enabled;
    registerAction.disabled = !enabled;
    loginStatus.textContent = "";
    registerStatus.textContent = "";
  }

  for (const input of roleInputs) {
    input.addEventListener("change", updateRoleActions);
  }

  schoolInput.addEventListener("input", () => {
    schoolHeading.textContent = schoolInput.value.trim() || "votre établissement";
  });

  loginAction.addEventListener("click", () => {
    const role = selectedRole();
    if (!role) return;
    loginStatus.textContent = `Espace ${role} : cette connexion est une maquette. Aucune identité n’a été vérifiée et aucun compte n’a été ouvert.`;
  });

  registerAction.addEventListener("click", () => {
    const role = selectedRole();
    if (!role) return;
    registerStatus.textContent = `Création de compte pour le profil ${role} : non disponible dans cette démo. Aucun compte ni aucune donnée n’ont été créés ou envoyés.`;
  });

  const requestedMode = new URLSearchParams(window.location.search).get("mode");
  setMode(requestedMode === "register" ? "register" : "login");
})();
