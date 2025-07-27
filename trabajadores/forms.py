from django import forms
from .models import Trabajador

' Esto hace que se tome las vallidacione de validators.py'
from .validators import TrabajadorModel
from pydantic import ValidationError as PydanticValidationError
from django.core.exceptions import ValidationError

class TrabajadorForm(forms.ModelForm):
    fecha = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'DD/MM/AAAA',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = Trabajador
        exclude = ['sueldo_bruto']

    def clean(self):
        cleaned_data = super().clean()

        try:
            # Validación con Pydantic
            validated = TrabajadorModel(**{
                "nombres": cleaned_data.get("nombres"),
                "apellidos": cleaned_data.get("apellidos"),
                "edad": cleaned_data.get("edad"),
                "fecha": cleaned_data.get("fecha"),
                "email": cleaned_data.get("email"),
                "telefono_casa": cleaned_data.get("telefono_casa"),
                "telefono_movil": cleaned_data.get("telefono_movil"),
                "sueldo_base": cleaned_data.get("sueldo_base"),
                "comision": cleaned_data.get("comision"),
                "password": cleaned_data.get("password"),
                "foto": cleaned_data.get("foto"),
                "activo": cleaned_data.get("activo"),
            })

            # Calcula sueldo bruto automáticamente
            cleaned_data["sueldo_bruto"] = validated.sueldo_base + validated.comision

        except PydanticValidationError as e:
            for error in e.errors():
                field = error['loc'][0]
                msg = str(error['msg']).replace("Value error,", "").strip()
                self.add_error(field, msg)

        return cleaned_data


"""
from django import forms
from .models import Trabajador
from .validators import TrabajadorModel
from pydantic import ValidationError
from django.forms.widgets import DateInput

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = [
            'nombres', 'apellidos', 'edad', 'fecha', 'email',
            'telefono_casa', 'telefono_movil', 'sueldo_base',
            'comision', 'password', 'foto', 'activo'
        ]
        widgets = {
'fecha' : forms.DateField(
    label="Fecha de ingreso",
    widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    input_formats=['%Y-%m-%d'],
    required=True
),
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
                message = str(error['msg']).replace("Value error,", "").strip()
                self.add_error(field, message)
        return cleaned_data

"""
''' 


except ValidationError as e:
    for error in e.errors():
        mensaje = str(error['msg']).replace("Value error,", "").strip()
        messages.error(request, mensaje)

        return cleaned_data

    def get_errores(self):
        """Retorna errores de Pydantic si los hay."""
        return getattr(self, '_pydantic_errors', [])

'''




