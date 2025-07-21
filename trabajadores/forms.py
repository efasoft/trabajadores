from django import forms
from .models import Trabajador
from .validators import TrabajadorSchema
from pydantic import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

class TrabajadorForm(forms.ModelForm):
    fecha = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-AAAA'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    foto = forms.ImageField(required=False)

    class Meta:
        model = Trabajador
        exclude = ['sueldo_bruto', 'eliminado']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_movil': forms.TextInput(attrs={'class': 'form-control'}),
            'sueldo_base': forms.TextInput(attrs={'class': 'form-control'}),
            'comision': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        try:
            trabajador_schema = TrabajadorSchema(**cleaned_data)
        except ValidationError as e:
            raise DjangoValidationError({err['loc'][0]: err['msg'] for err in e.errors()})
        return cleaned_data

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if not self.instance.pk and not foto:
            raise forms.ValidationError("Debe cargar una imagen.")
        return foto

