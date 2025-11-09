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
        """Validar RUT chileno correctamente."""
        # Eliminar puntos y guión
        rut = rut.replace('.', '').replace('-', '').lower()

        # Debe tener mínimo 8 caracteres
        if len(rut) < 8:
            return False

        cuerpo = rut[:-1]
        dv_ingresado = rut[-1]

        # Cuerpo debe ser numérico
        if not cuerpo.isdigit():
            return False

        # Calcular dígito verificador
        suma = 0
        multiplicador = 2

        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2

        resto = suma % 11
        dv_calculado = 11 - resto

        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 10:
            dv_calculado = 'k'
        else:
            dv_calculado = str(dv_calculado)

        return dv_ingresado == dv_calculado


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
        fields = [
            "direccion_calle",
            "direccion_ciudad",
            "direccion_region",
            "direccion_pais",
            "direccion_codigo_postal",
        ]

    def clean_direccion_calle(self):
        calle = self.cleaned_data.get("direccion_calle", "").strip()
        if len(calle) < 3:
            raise forms.ValidationError("La calle debe tener al menos 3 caracteres.")
        return calle

    def clean_direccion_ciudad(self):
        ciudad = self.cleaned_data.get("direccion_ciudad", "").strip()
        if not ciudad.replace(" ", "").isalpha():
            raise forms.ValidationError("La ciudad solo debe contener letras.")
        return ciudad

    def clean_direccion_region(self):
        region = self.cleaned_data.get("direccion_region", "").strip()
        if not region.replace(" ", "").isalpha():
            raise forms.ValidationError("La región solo debe contener letras.")
        return region

    def clean_direccion_pais(self):
        pais = self.cleaned_data.get("direccion_pais", "").strip()
        if not pais.replace(" ", "").isalpha():
            raise forms.ValidationError("El país solo debe contener letras.")
        return pais

    def clean_direccion_codigo_postal(self):
        cp = self.cleaned_data.get("direccion_codigo_postal")
        if cp:
            cp = cp.strip()
            if not cp.isdigit():
                raise forms.ValidationError("El código postal debe ser numérico.")
            if len(cp) < 4 or len(cp) > 10:
                raise forms.ValidationError("El código postal debe tener entre 4 y 10 dígitos.")
        return cp


class CentroDistribucionForm(forms.ModelForm):
    class Meta:
        model = CentroDistribucion
        fields = ["centro_nombre", "id_direccion", "centro_tipo", "centro_descripcion", "centro_imagen"]

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "producto_nombre",
            "producto_descripcion",
            "id_categoria",
            "producto_precio",
            "producto_estado",
            "producto_imagen",
        ]

    # --- Validar nombre ---
    def clean_producto_nombre(self):
        nombre = self.cleaned_data.get("producto_nombre", "").strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del producto debe tener al menos 3 caracteres.")
        return nombre

    # --- Validar descripción (si existe) ---
    def clean_producto_descripcion(self):
        descripcion = self.cleaned_data.get("producto_descripcion", "")
        if descripcion and len(descripcion.strip()) < 5:
            raise forms.ValidationError("La descripción debe tener al menos 5 caracteres si es ingresada.")
        return descripcion

    # --- Validación adicional opcional de precio ---
    def clean_producto_precio(self):
        precio = self.cleaned_data.get("producto_precio")
        if precio is not None and precio > 1_000_000:
            raise forms.ValidationError("El precio es demasiado alto para un producto normal.")
        return precio

class ProductoValorNutricionalForm(forms.ModelForm):

    class Meta:
        model = ProductoValorNutricional
        fields = [
            "id_producto",
            "valor_calorias",
            "valor_proteinas",
            "valor_carbohidratos",
            "valor_grasas",
            "valor_fibra",
            "valor_sodio",
            "valor_azucar",
        ]

    # --- VALIDACIÓN GENÉRICA: todos deben ser >= 0 y valores lógicos ---
    def _validar_rango(self, valor, campo, max_value):
        if valor is None:
            return valor
        if valor < 0:
            raise forms.ValidationError(f"{campo} no puede ser negativo.")
        if valor > max_value:
            raise forms.ValidationError(f"{campo} excede el valor máximo permitido ({max_value}).")
        return valor

    def clean_valor_calorias(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_calorias"),
            "Calorías",
            5000   # 5000 kcal es un límite razonable
        )

    def clean_valor_proteinas(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_proteinas"),
            "Proteínas (g)",
            500   # 500g ya es absurdo pero seguro
        )

    def clean_valor_carbohidratos(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_carbohidratos"),
            "Carbohidratos (g)",
            500
        )

    def clean_valor_grasas(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_grasas"),
            "Grasas (g)",
            300
        )

    def clean_valor_fibra(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_fibra"),
            "Fibra (g)",
            200
        )

    def clean_valor_sodio(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_sodio"),
            "Sodio (mg)",
            5000
        )

    def clean_valor_azucar(self):
        return self._validar_rango(
            self.cleaned_data.get("valor_azucar"),
            "Azúcar (g)",
            300
        )

class InventarioForm(forms.ModelForm):

    class Meta:
        model = Inventario
        fields = ["id_centro", "id_producto", "inventario_cantidad"]

    # Validar cantidad lógica
    def clean_inventario_cantidad(self):
        cantidad = self.cleaned_data.get("inventario_cantidad")

        if cantidad is None:
            raise forms.ValidationError("Debe ingresar una cantidad.")

        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")

        if cantidad > 50000:  # límite razonable para evitar absurdos
            raise forms.ValidationError("La cantidad es demasiado elevada. Máximo permitido: 50.000 unidades.")

        return cantidad

    # Validar que no exista duplicado (centro + producto)
    def clean(self):
        cleaned_data = super().clean()
        centro = cleaned_data.get("id_centro")
        producto = cleaned_data.get("id_producto")

        if not centro or not producto:
            return cleaned_data

        # Para evitar error al editar (no comparar consigo mismo)
        existing = Inventario.objects.filter(id_centro=centro, id_producto=producto)

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "Este centro de distribución ya tiene registrado este producto en su inventario."
            )

        return cleaned_data



class HistorialInventarioForm(forms.ModelForm):

    class Meta:
        model = HistorialInventario
        fields = ["id_inventario", "id_usuario", "historial_tipo_movimiento", "id_centro_destino", "historial_cantidad"]

    # Validar cantidad
    def clean_historial_cantidad(self):
        cantidad = self.cleaned_data.get("historial_cantidad")

        if cantidad is None:
            raise forms.ValidationError("Debe ingresar una cantidad.")

        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")

        if cantidad > 50000:  # límite razonable
            raise forms.ValidationError("La cantidad es demasiado elevada. Máximo permitido: 50.000.")

        return cantidad

    # Validaciones dependientes del tipo de movimiento
    def clean(self):
        cleaned_data = super().clean()

        tipo = cleaned_data.get("historial_tipo_movimiento")
        cantidad = cleaned_data.get("historial_cantidad")
        inventario = cleaned_data.get("id_inventario")
        centro_destino = cleaned_data.get("id_centro_destino")

        if not tipo or not inventario or not cantidad:
            return cleaned_data

        stock_actual = inventario.inventario_cantidad

        # --- Validación para RETIRAR ---
        if tipo == "retirar":
            if cantidad > stock_actual:
                raise forms.ValidationError(
                    f"No hay suficiente stock para retirar. Stock actual: {stock_actual}."
                )

        # --- Validación para TRASLADO ---
        if tipo == "traslado":
            if not centro_destino:
                raise forms.ValidationError(
                    "Debe seleccionar un centro destino para un movimiento de tipo traslado."
                )
            if cantidad > stock_actual:
                raise forms.ValidationError(
                    f"No hay suficiente stock para trasladar. Stock actual: {stock_actual}."
                )
            if centro_destino == inventario.id_centro:
                raise forms.ValidationError(
                    "El centro destino debe ser diferente al centro origen."
                )

        # --- Validación para AGREGAR ---
        if tipo == "agregar":
            if cantidad > 50000:
                raise forms.ValidationError("Cantidad demasiado alta para agregar al inventario.")

        return cleaned_data

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

    def clean_contacto_valor(self):
        valor = (self.cleaned_data.get("contacto_valor") or "").strip()
        tipo = self.cleaned_data.get("contacto_tipo")

        if tipo in ["telefono", "whatsapp"]:
            import re
            if not re.match(r'^(?:\+?56)?(?:9\d{8}|[2-9]\d{8})$', valor):
                raise forms.ValidationError("Debe ingresar un número chileno válido (ej: +56912345678).")

        
        if tipo == "correo":
            from django.core.validators import validate_email
            try:
                validate_email(valor)
            except:
                raise forms.ValidationError("Correo electrónico inválido.")

        return valor



class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ["proveedor_nombre", "proveedor_rut", "proveedor_email", "proveedor_telefono", "id_direccion"]

    # --- Validar nombre ---
    def clean_proveedor_nombre(self):
        nombre = self.cleaned_data.get("proveedor_nombre", "").strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre del proveedor debe tener al menos 3 caracteres.")
        return nombre

    # --- Validar RUT chileno ---
    def clean_proveedor_rut(self):
        rut = self.cleaned_data.get("proveedor_rut")

        if not rut:
            return rut

        rut = rut.replace(".", "").replace("-", "").lower()

        if len(rut) < 8:
            raise forms.ValidationError("El RUT es demasiado corto.")

        cuerpo = rut[:-1]
        dv = rut[-1]

        if not cuerpo.isdigit():
            raise forms.ValidationError("El RUT debe contener solo números en el cuerpo.")

        # Cálculo del dígito verificador
        suma = 0
        multiplicador = 2
        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2

        resto = suma % 11
        dv_calc = 11 - resto

        if dv_calc == 11:
            dv_calc = '0'
        elif dv_calc == 10:
            dv_calc = 'k'
        else:
            dv_calc = str(dv_calc)

        if dv != dv_calc:
            raise forms.ValidationError("El RUT ingresado no es válido.")

        return self.cleaned_data["proveedor_rut"]
    
    def clean_proveedor_email(self):
        email = self.cleaned_data.get("proveedor_email")

        if not email:
            return email  # se permite email vacío

        from django.core.validators import validate_email
        try:
            validate_email(email)
        except:
            raise forms.ValidationError("El correo del proveedor no es válido.")

        return email
    
    def clean_proveedor_telefono(self):
        tel = self.cleaned_data.get("proveedor_telefono")

        if not tel:
            return tel  # se permite vacío

        import re
        if not re.match(r'^(?:\+?56)?(?:9\d{8}|[2-9]\d{8})$', tel):
            raise forms.ValidationError("Debe ingresar un teléfono chileno válido.")

        
        return tel




class FavoritoClienteForm(forms.ModelForm):
    class Meta:
        model = FavoritoCliente
        fields = ["id_usuario", "id_producto"]

