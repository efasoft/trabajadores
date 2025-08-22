from django import forms
from .models import Trabajador, Provincia, Ciudad
from .validators import ProvinciaModel, CiudadModel

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
        }),
        error_messages={
            "required": "Debe ingresar una fecha",
            "invalid": "Formato de fecha inválido. Use DD/MM/AAAA"
        }
    )

    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Provincia",
        error_messages={
            "required": "Debe seleccionar una provincia"
        }
    )

    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Ciudad",
        error_messages={
            "required": "Debe seleccionar una ciudad"
        }
    )

    codigo_postal = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 28001'}),
        required=True,
        label="Código Postal",
        error_messages={
            "required": "Debe ingresar un código postal"
        }
    )    

    class Meta:
        model = Trabajador
        exclude = ['sueldo_bruto']
        error_messages = {
            "nombres": {"required": "Debe ingresar un nombre"},
            "apellidos": {"required": "Atencion: Debe ingresar un apellido"},
            "email": {"required": "Debe ingresar un correo electrónico", "invalid": "Correo electrónico inválido"},
            "telefono_movil": {"required": "Debe ingresar un teléfono móvil"},
            "edad": {"required": "Debe ingresar la edad", "invalid": "La edad debe ser un número"},
            "sueldo_base": {"required": "Debe ingresar el sueldo base"},
            "comision": {"required": "Debe ingresar la comisión"},
            "password": {"required": "Debe ingresar una contraseña"},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['ciudad'].queryset = Ciudad.objects.none()
        elif self.instance.pk and self.instance.provincia:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia=self.instance.provincia).order_by('nombre')

    def clean(self):
        cleaned_data = super().clean()

        try:
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
                "codigo_postal": cleaned_data.get("codigo_postal"),
            })

            cleaned_data["sueldo_bruto"] = validated.sueldo_base + validated.comision

        except PydanticValidationError as e:
            for error in e.errors():
                field = error['loc'][0]
                msg = str(error['msg']).replace("Value error,", "").strip()
                self.add_error(field, msg)

        return cleaned_data


class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        fields = ['nombre']
        error_messages = {
            "nombre": {"required": "Debe ingresar un nombre de provincia"}
        }


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre', 'provincia']
        error_messages = {
            "nombre": {"required": "Debe ingresar un nombre de ciudad"},
            "provincia": {"required": "Debe seleccionar una provincia"}
        }





