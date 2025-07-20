 // Creeado por IA
 
 document.addEventListener('DOMContentLoaded', function() {
    // Manejo de mensajes de Django con SweetAlert2
    const djangoMessages = document.getElementById('django-messages');
    if (djangoMessages) {
        const messages = djangoMessages.children;
        for (let i = 0; i < messages.length; i++) {
            const message = messages[i];
            const text = message.textContent.trim();
            const tags = message.classList[1]; // alert-success, alert-danger, etc.

            let icon = 'info';
            let title = '';
            let customClass = '';

            if (tags.includes('success')) {
                icon = 'success';
                title = '¡Éxito!';
                customClass = 'swal2-success';
            } else if (tags.includes('error')) {
                icon = 'error';
                title = '¡Error!';
                customClass = 'swal2-error';
            } else if (tags.includes('warning')) {
                icon = 'warning';
                title = '¡Advertencia!';
                customClass = 'swal2-warning';
            } else {
                icon = 'info';
                title = 'Información';
                customClass = 'swal2-info';
            }

            Swal.fire({
                icon: icon,
                title: title,
                text: text,
                showConfirmButton: false,
                timer: 3000,
                customClass: {
                    icon: customClass
                },
                // Añadir iconos de Font Awesome
                didOpen: () => {
                    const iconElement = Swal.getIcon();
                    if (iconElement) {
                        iconElement.innerHTML = ''; // Limpiar el icono por defecto de SweetAlert2
                        let faIcon = document.createElement('i');
                        faIcon.classList.add('fas');
                        if (icon === 'success') {
                            faIcon.classList.add('fa-check-circle');
                        } else if (icon === 'error') {
                            faIcon.classList.add('fa-exclamation-circle');
                        } else if (icon === 'warning') {
                            faIcon.classList.add('fa-exclamation-triangle');
                        } else if (icon === 'info') {
                            faIcon.classList.add('fa-info-circle');
                        }
                        iconElement.appendChild(faIcon);
                    }
                }
            });
        }
    }

    // Toggle de visibilidad de contraseña
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const passwordField = document.getElementById(targetId);
            const icon = this.querySelector('i');

            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // Confirmación de eliminación con SweetAlert2
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const empleadoId = this.dataset.id;
            const empleadoName = this.dataset.name;
            const form = document.getElementById('delete-form');
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            Swal.fire({
                title: '¿Estás seguro?',
                text: `¡No podrás revertir la eliminación de ${empleadoName}!`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#dc3545',
                cancelButtonColor: '#6c757d',
                confirmButtonText: '<i class="fas fa-trash-alt"></i> Sí, eliminarlo',
                cancelButtonText: '<i class="fas fa-times-circle"></i> Cancelar',
                customClass: {
                    icon: 'swal2-warning' // Clase personalizada para el icono de advertencia
                },
                didOpen: () => {
                    const iconElement = Swal.getIcon();
                    if (iconElement) {
                        iconElement.innerHTML = ''; // Limpiar el icono por defecto de SweetAlert2
                        let faIcon = document.createElement('i');
                        faIcon.classList.add('fas', 'fa-exclamation-triangle');
                        iconElement.appendChild(faIcon);
                    }
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    // Envía el formulario para realizar el soft delete
                    form.action = `/empleados/eliminar/${empleadoId}/`;
                    form.submit();
                }
            });
        });
    });

    // Tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});