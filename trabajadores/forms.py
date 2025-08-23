# forms.py
from django import forms
from .models import Trabajador, Provincia, Ciudad


class TrabajadorForm(forms.ModelForm):
    # Todos los campos como CharField sin validación de tipo
    nombres = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    fecha = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'DD/MM/AAAA',
            'autocomplete': 'off'
        }),
        required=False
    )
    telefono_casa = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    telefono_movil = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    foto = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    activo = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    # Campos clave: sin validaciones de Django
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    edad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    sueldo_base = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=False
    )
    comision = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    provincia = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label="Provincia"
    )
    ciudad = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label="Ciudad"
    )
    codigo_postal = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 28001'}),
        required=False,
        label="Código Postal"
    )

    class Meta:
        model = Trabajador
        fields = [
            'nombres', 'apellidos', 'email', 'fecha', 'edad', 'telefono_casa', 'telefono_movil',
            'foto', 'activo', 'sueldo_base', 'comision', 'password', 'provincia', 'ciudad', 'codigo_postal'
        ]
        exclude = ['sueldo_bruto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['ciudad'].widget.choices = [
                    (c.id, c.nombre) for c in Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
                ]
            except (ValueError, TypeError):
                self.fields['ciudad'].widget.choices = []
        elif self.instance.pk and self.instance.provincia:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia=self.instance.provincia).order_by('nombre')

    def clean(self):
        cleaned_data = super().clean()

        # Convertir tipos manualmente
        try:
            edad = cleaned_data.get("edad")
            if edad not in (None, "", "0"):
                cleaned_data["edad"] = int(edad)
            else:
                cleaned_data["edad"] = None

            sueldo_base = cleaned_data.get("sueldo_base")
            if sueldo_base not in (None, "", "0"):
                cleaned_data["sueldo_base"] = float(sueldo_base)
            else:
                cleaned_data["sueldo_base"] = None

            comision = cleaned_data.get("comision")
            if comision not in (None, "", "0"):
                cleaned_data["comision"] = float(comision)
            else:
                cleaned_data["comision"] = None

            provincia = cleaned_data.get("provincia")
            if provincia not in (None, "", "0"):
                cleaned_data["provincia"] = int(provincia)
            else:
                cleaned_data["provincia"] = None

            ciudad = cleaned_data.get("ciudad")
            if ciudad not in (None, "", "0"):
                cleaned_data["ciudad"] = int(ciudad)
            else:
                cleaned_data["ciudad"] = None

        except (ValueError, TypeError):
            self.add_error(None, "Todos los campos numéricos deben tener valores válidos.")
            return cleaned_data

        # Validar con Pydantic
        from .validators import TrabajadorModel
        from pydantic import ValidationError as PydanticValidationError

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
                "provincia": cleaned_data.get("provincia"),
                "ciudad": cleaned_data.get("ciudad"),
                "codigo_postal": cleaned_data.get("codigo_postal"),
            })

            cleaned_data["sueldo_bruto"] = validated.sueldo_base + validated.comision

        except PydanticValidationError as e:
            for error in e.errors():
                field = error['loc'][0]
                msg = str(error['msg']).replace("Value error,", "").strip()
                self.add_error(field, msg)
        except Exception as e:
            self.add_error(None, "Error en los datos ingresados. Revise todos los campos.")

        return cleaned_data


# Formularios adicionales
class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        fields = ['nombre']


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre', 'provincia']




