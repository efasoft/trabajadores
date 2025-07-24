document.addEventListener("DOMContentLoaded", function () {
  const togglePassword = document.querySelector("#togglePassword");
  const passwordInput = document.querySelector("#id_password");

  if (togglePassword && passwordInput) {
      togglePassword.addEventListener("click", function () {
          const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
          passwordInput.setAttribute("type", type);
          this.classList.toggle("fa-eye-slash");
      });
  }

  // Mostrar errores desde validaciones del backend vía Django
  const errorContainer = document.getElementById("form-errors");
  if (errorContainer) {
      const errorMessages = JSON.parse(errorContainer.dataset.errors);
      if (Object.keys(errorMessages).length > 0) {
          let msg = "";
          for (const field in errorMessages) {
              msg += `<b>${field}:</b> ${errorMessages[field].join(", ")}<br>`;
          }

          Swal.fire({
              icon: "error",
              title: "Errores en el formulario",
              html: msg,
              confirmButtonColor: "#3085d6",
              confirmButtonText: "Entendido"
          });
      }
  }
});

document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".toggle-password");
    toggles.forEach(toggle => {
        toggle.addEventListener("click", function () {
            const input = document.querySelector(this.getAttribute("toggle"));
            const type = input.getAttribute("type") === "password" ? "text" : "password";
            input.setAttribute("type", type);
            this.classList.toggle("fa-eye");
            this.classList.toggle("fa-eye-slash");
        });
    });
});

