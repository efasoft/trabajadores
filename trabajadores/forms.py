# forms.py
from django import forms
from .models import Trabajador, Provincia, Ciudad
from datetime import datetime


class TrabajadorForm(forms.Form):
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
            'class': 'form-control',
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
    correo = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Correo electrónico"
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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 28001'}),
        required=False,
        label="Código Postal"
    )

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', None)
        if data and 'email' in data:
            data = data.copy()
            data['correo'] = data['email']
            kwargs['data'] = data

        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # ===== CORRECCIÓN 1: INICIALIZAR SIEMPRE LAS OPCIONES DE PROVINCIA =====
        # Cargar TODAS las provincias siempre
        provincias_choices = [('', 'Seleccione una provincia')]
        provincias_choices.extend([(p.id, p.nombre) for p in Provincia.objects.all().order_by('nombre')])
        self.fields['provincia'].widget.choices = provincias_choices

        # ===== CORRECCIÓN 2: INICIALIZAR OPCIONES DE CIUDAD =====
        ciudades_choices = [('', 'Seleccione una ciudad')]
        
        # Inicializar valores si hay instancia
        if self.instance:
            # 1. Asignar todos los campos directamente
            for field in self.fields:
                if hasattr(self.instance, field):
                    value = getattr(self.instance, field)
                    if value is not None:
                        self.fields[field].initial = value

            # 2. Asignar email explícitamente (por si no se asignó)
            if self.instance.email:
                self.fields['correo'].initial = self.instance.email

            # 3. Asignar provincia y ciudad
            if self.instance.provincia:
                self.fields['provincia'].initial = self.instance.provincia.id
                # ===== CORRECCIÓN 3: CARGAR CIUDADES DE LA PROVINCIA EXISTENTE =====
                ciudades = Ciudad.objects.filter(provincia=self.instance.provincia).order_by('nombre')
                ciudades_choices.extend([(c.id, c.nombre) for c in ciudades])
                
            if self.instance.ciudad:
                self.fields['ciudad'].initial = self.instance.ciudad.id
                # ===== CORRECCIÓN 4: ASEGURAR QUE LA CIUDAD ESTÁ EN LAS OPCIONES =====
                ciudad_ya_en_lista = any(choice[0] == self.instance.ciudad.id for choice in ciudades_choices)
                if not ciudad_ya_en_lista:
                    ciudades_choices.append((self.instance.ciudad.id, self.instance.ciudad.nombre))

        # ===== CORRECCIÓN 5: MANEJO DE POST DATA =====
        # Actualizar ciudades dinámicamente si hay POST
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
                ciudades_choices = [('', 'Seleccione una ciudad')]
                ciudades_choices.extend([(c.id, c.nombre) for c in ciudades])
            except (ValueError, TypeError):
                ciudades_choices = [('', 'Seleccione una ciudad')]

        # ===== ASIGNAR LAS OPCIONES FINALES =====
        self.fields['ciudad'].widget.choices = ciudades_choices

        if self.instance and self.instance.email:
            self.fields['correo'].initial = self.instance.email                

    def clean(self):
        cleaned_data = super().clean()

        # Validar con Pydantic
        from .validators import TrabajadorModel
        from pydantic import ValidationError as PydanticValidationError

        try:
            data_for_pydantic = {
                "nombres": cleaned_data.get("nombres"),
                "apellidos": cleaned_data.get("apellidos"),
                "edad": cleaned_data.get("edad"),
                "fecha": cleaned_data.get("fecha"),
                "email": cleaned_data.get("correo"),
                "telefono_casa": cleaned_data.get("telefono_casa"),
                "telefono_movil": cleaned_data.get("telefono_movil"),
                "sueldo_base": cleaned_data.get("sueldo_base"),
                "comision": cleaned_data.get("comision"),
                "password": cleaned_data.get("password"),
                "foto": cleaned_data.get("foto"),
                "activo": cleaned_data.get("activo", True),
                "provincia": cleaned_data.get("provincia"),
                "ciudad": cleaned_data.get("ciudad"),
                "codigo_postal": cleaned_data.get("codigo_postal"),
            }

            validated = TrabajadorModel(**data_for_pydantic)
            cleaned_data["sueldo_bruto"] = validated.sueldo_base + validated.comision

        except PydanticValidationError as e:
            for error in e.errors():
                loc = error.get('loc', ())
                field = loc[0] if loc else "nombres"
                msg = str(error['msg']).replace("Value error,", "").strip()

                if field == "email":
                    self.add_error("correo", msg)
                elif field in self.fields:
                    self.add_error(field, msg)
                else:
                    self.add_error("nombres", msg)
        except Exception as e:
            self.add_error(None, "Error en los datos ingresados. Revise todos los campos.")


        return cleaned_data

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("No se puede guardar un formulario inválido")

        if self.instance is None:
            instance = Trabajador()
        else:
            instance = self.instance

        # Campos a asignar directamente
        fields_to_assign = [
            'nombres', 'apellidos', 'edad',
            'telefono_casa', 'telefono_movil', 'sueldo_base',
            'comision', 'password', 'foto', 'activo', 'codigo_postal'
        ]
        for field in fields_to_assign:
            value = self.cleaned_data.get(field)
            if value is not None:
                setattr(instance, field, value)

        # ✅ ASIGNACIÓN EXPLÍCITA Y SEGURA DEL EMAIL
        correo_value = self.cleaned_data.get("correo")
        if correo_value is not None:
            instance.email = correo_value  # ← ¡Forzamos la asignación!
        else:
            instance.email = ""  # O deja como estaba

        # ✅ Manejo de fecha (DD/MM/AAAA → date)
        fecha_str = self.cleaned_data.get("fecha")
        if fecha_str:
            try:
                fecha_date = datetime.strptime(fecha_str, '%d/%m/%Y').date()
                instance.fecha = fecha_date
            except ValueError:
                self.add_error("fecha", "Fecha inválida. Usa el formato DD/MM/AAAA")
                return instance

        # ✅ Asignar provincia y ciudad (ForeignKey)
        if self.cleaned_data.get("provincia"):
            instance.provincia_id = self.cleaned_data["provincia"]
        if self.cleaned_data.get("ciudad"):
            instance.ciudad_id = self.cleaned_data["ciudad"]
        print("Valor de correo en cleaned_data:", self.cleaned_data.get("correo"))
        if commit:
            instance.save()
        return instance

# ===================================
# FORMULARIO: PROVINCIA
# ===================================
class ProvinciaForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not nombre or not nombre.strip():
            raise forms.ValidationError("Debe ingresar un nombre de provincia")
        if len(nombre) > 60:
            raise forms.ValidationError("El nombre no puede superar 60 caracteres")
        return nombre.strip()

    def save(self, commit=True):
        from .models import Provincia
        if self.instance is None:
            instance = Provincia()
        else:
            instance = self.instance
        instance.nombre = self.cleaned_data["nombre"]
        if commit:
            instance.save()
        return instance

# ===================================
# FORMULARIO: CIUDAD
# ===================================
class CiudadForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    provincia = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Provincia"
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Cargar provincias
        self.fields['provincia'].widget.choices = [
            (p.id, p.nombre) for p in Provincia.objects.all().order_by('nombre')
        ]

        if self.instance:
            self.fields['nombre'].initial = self.instance.nombre
            if self.instance.provincia:
                self.fields['provincia'].initial = self.instance.provincia.id

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        provincia = cleaned_data.get("provincia")

        if not nombre or not nombre.strip():
            self.add_error("nombre", "Debe ingresar un nombre de ciudad")
        if not provincia or provincia == "0":
            self.add_error("provincia", "Debe seleccionar una provincia")
        return cleaned_data

    def save(self, commit=True):
        from .models import Ciudad
        if self.instance is None:
            instance = Ciudad()
        else:
            instance = self.instance
        instance.nombre = self.cleaned_data["nombre"]
        if self.cleaned_data["provincia"]:
            instance.provincia_id = int(self.cleaned_data["provincia"])
        if commit:
            instance.save()
        return instance