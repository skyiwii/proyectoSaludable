from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from django.contrib.auth import authenticate

class RegistroForm(UserCreationForm):
    usuario_nombre = forms.CharField(max_length=50, required=True)
    usuario_apellido = forms.CharField(max_length=50, required=True)
    usuario_rut = forms.CharField(max_length=12, required=True, help_text="Formato: 12345678-9")
    usuario_email = forms.EmailField(required=True)
    usuario_rol = forms.ChoiceField(choices=Usuario.ROLES, required=True, initial='cliente')

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + (
            'usuario_nombre',
            'usuario_apellido',
            'usuario_rut',
            'usuario_email',
            'usuario_rol',
        )

    def clean_usuario_rut(self):
        rut = self.cleaned_data.get('usuario_rut')
        if rut:
            # Validar formato de RUT chileno
            if not self.validar_rut(rut):
                raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut
    
    def validar_rut(self, rut):
        """Validar RUT chileno correctamente"""
        rut = rut.replace('.', '').replace('-', '').strip().lower()
        
        if len(rut) < 8:
            return False

        numero = rut[:-1]
        dv = rut[-1]

        if not numero.isdigit():
            return False

        suma = 0
        multiplicador = 2

        for i in range(len(numero) - 1, -1, -1):
            suma += int(numero[i]) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)
        if resto == 11:
            dv_calculado = '0'
        elif resto == 10:
            dv_calculado = 'k'
        else:
            dv_calculado = str(resto)

        return dv == dv_calculado


    def clean_username(self):
        # Eliminar la validación de username ya que usamos email como USERNAME_FIELD
        return self.cleaned_data.get('username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['usuario_email'] # Usar email como username
        user.email = self.cleaned_data['usuario_email']
        user.usuario_nombre = self.cleaned_data['usuario_nombre']
        user.usuario_apellido = self.cleaned_data['usuario_apellido']
        user.usuario_rut = self.cleaned_data['usuario_rut']
        user.usuario_rol = self.cleaned_data['usuario_rol']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo Electrónico")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo Electrónico'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data



from .models import CategoriaProducto, Direccion, CentroDistribucion, Producto, ProductoValorNutricional, Inventario, HistorialInventario, ContactoCentro, Proveedor, FavoritoCliente

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ["categoria_nombre", "categoria_descripcion"]

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ["direccion_calle", "direccion_ciudad", "direccion_region", "direccion_pais", "direccion_codigo_postal"]

class CentroDistribucionForm(forms.ModelForm):
    class Meta:
        model = CentroDistribucion
        fields = ["centro_nombre", "id_direccion", "centro_tipo", "centro_descripcion", "centro_imagen"]

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["producto_nombre", "producto_descripcion", "id_categoria", "producto_precio", "producto_estado", "producto_imagen"]

class ProductoValorNutricionalForm(forms.ModelForm):
    class Meta:
        model = ProductoValorNutricional
        fields = ["id_producto", "valor_calorias", "valor_proteinas", "valor_carbohidratos", "valor_grasas", "valor_fibra", "valor_sodio", "valor_azucar"]

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ["id_centro", "id_producto", "inventario_cantidad"]

class HistorialInventarioForm(forms.ModelForm):
    class Meta:
        model = HistorialInventario
        fields = ["id_inventario", "id_usuario", "historial_tipo_movimiento", "id_centro_destino", "historial_cantidad"]


class ContactoCentroForm(forms.ModelForm):
    contacto_valor = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: +56 9 1234 5678 para teléfono, correo@ejemplo.com para correo'
        }),
        help_text="Ingrese el valor del contacto (teléfono, correo electrónico, etc.)"
    )
    
    class Meta:
        model = ContactoCentro
        fields = ["id_centro", "contacto_tipo", "contacto_valor"]
        widgets = {
            'contacto_tipo': forms.Select(attrs={'class': 'form-control'}),
            'id_centro': forms.Select(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["proveedor_nombre", "proveedor_rut", "proveedor_email", "proveedor_telefono", "id_direccion"]

class FavoritoClienteForm(forms.ModelForm):
    class Meta:
        model = FavoritoCliente
        fields = ["id_usuario", "id_producto"]

