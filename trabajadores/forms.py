from django import forms
from .models import Trabajador
from .validators import TrabajadorModel
from pydantic import ValidationError

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = [
            'nombres', 'apellidos', 'edad', 'fecha', 'email',
            'telefono_casa', 'telefono_movil', 'sueldo_base',
            'comision', 'password', 'foto', 'activo'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(render_value=True),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Capturar la ruta del archivo si está disponible
        foto = cleaned_data.get('foto')
        foto_value = foto.name if foto else None
        cleaned_data['foto'] = foto_value

        try:
            TrabajadorModel(**cleaned_data)
        except ValidationError as e:
            for error in e.errors():
                loc = error.get('loc', [])
                field = loc[0] if loc else '__all__'
                message = error['msg']
                self.add_error(field, message)
        return cleaned_data



