 // Mostrar/ocultar contraseña
document.addEventListener("DOMContentLoaded", function () {
    const toggleIcons = document.querySelectorAll('.toggle-password');
  
    toggleIcons.forEach(icon => {
      icon.addEventListener('click', function () {
        const input = document.getElementById(this.dataset.target);
        if (input.type === "password") {
          input.type = "text";
          this.classList.remove("fa-eye");
          this.classList.add("fa-eye-slash");
        } else {
          input.type = "password";
          this.classList.remove("fa-eye-slash");
          this.classList.add("fa-eye");
        }
      });
    });
  });
  
  // Validación con SweetAlert (para futuros usos)
  function mostrarAlertaError(mensaje) {
    Swal.fire({
      icon: 'error',
      title: 'Error de validación',
      text: mensaje,
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Entendido'
    });
  }
  
  // Confirmar eliminación (si se usa eliminación fuerte)
  function confirmarEliminacion(url) {
    Swal.fire({
      title: '¿Estás seguro?',
      text: "¡No podrás revertir esta acción!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = url;
      }
    });
  }
  