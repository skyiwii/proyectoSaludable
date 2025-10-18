from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import (
    Usuario, CategoriaProducto, Direccion, CentroDistribucion, Producto, 
    ProductoValorNutricional, Inventario, HistorialInventario, 
    ContactoCentro, Proveedor, FavoritoCliente
)
from .forms import (
    CategoriaProductoForm, DireccionForm, CentroDistribucionForm, ProductoForm, 
    ProductoValorNutricionalForm, InventarioForm, HistorialInventarioForm, 
    ContactoCentroForm, ProveedorForm, FavoritoClienteForm
)

# --- Vistas Principales ---
def index(request):
    # Obtener los 3 productos más recientes
    productos_recientes = Producto.objects.all().order_by('-id')[:3]
    return render(request, "verdeLimonTemplates/index.html", {"productos_recientes": productos_recientes})

def productos(request):
    productos = Producto.objects.all()
    favoritos_ids = []

    if request.user.is_authenticated:
        favoritos = FavoritoCliente.objects.filter(id_usuario=request.user.id)
        
        favoritos_ids = []
        for f in favoritos:
            try:
                producto = Producto.objects.get(pk=f.id_producto)
                favoritos_ids.append(producto.id)
            except Producto.DoesNotExist:
                continue
    return render(request, "verdeLimonTemplates/productos.html", {
        "productos": productos, 
        "favoritos_ids": favoritos_ids
    })

def nosotros(request):
    """Renderiza la página 'Sobre Nosotros'."""
    return render(request, "verdeLimonTemplates/nosotros.html")

def contacto(request):
    """Renderiza la página de contacto."""
    return render(request, "verdeLimonTemplates/contacto.html")

import json
from django.core.serializers import serialize

def distribucion(request):
    centros_distribucion = CentroDistribucion.objects.all()
    
    centros_distribucion_data = []
    for centro in centros_distribucion:
        # Obtener contactos del centro
        direccion = Direccion.objects.filter(id=centro.id_direccion).first()
        #contactos
        contactos = ContactoCentro.objects.filter(id_centro=centro.id)
        contactos_data = [{"contaco_tipo": c.contacto_tipo, "contacto_valor": c.contacto_valor} for c in contactos]

        
        # Obtener productos disponibles en este centro
        inventarios = Inventario.objects.filter(id_centro=centro.id, inventario_cantidad__gt=0)
        productos_data = []
        for inv in inventarios:
            producto = Producto.objects.filter(id=inv.id_producto).first()
            if producto:
                productos_data.append({
                    'producto_nombre': producto.producto_nombre,
                    'producto_precio': float(producto.producto_precio),
                    'inventario_cantidad': inv.inventario_cantidad,
                    'producto_imagen': producto.producto_imagen.url if producto.producto_imagen else None,
                })
        
        centros_distribucion_data.append({
            'id': centro.id,
            'centro_nombre': centro.centro_nombre,
            'centro_tipo': centro.centro_tipo,
            'centro_descripcion': centro.centro_descripcion,
            'centro_imagen': centro.centro_imagen.url if centro.centro_imagen else None,
            'direccion': {
                'direccion_calle': direccion.direccion_calle if direccion else "N/A",
                'direccion_ciudad': direccion.direccion_ciudad if direccion else "N/A",
                'direccion_region': direccion.direccion_region if direccion else "N/A",
                'direccion_pais': direccion.direccion_pais if direccion else "N/A",
                'direccion_codigo_postal': direccion.direccion_codigo_postal if direccion else "N/A",
            },
            'contactos': contactos_data,
            'productos': productos_data,
        })

    contexto = {
        "centros_distribucion": centros_distribucion,
        "centros_distribucion_json": json.dumps(centros_distribucion_data)
    }
    return render(request, "verdeLimonTemplates/distribucion.html", contexto)



# --- Vistas de Autenticación ---
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.usuario_rol == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = RegistroForm()
    return render(request, 'verdeLimonTemplates/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.usuario_rol == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                pass
    else:
        form = LoginForm()
    return render(request, 'verdeLimonTemplates/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

# --- Vistas de Dashboard ---
@login_required
@user_passes_test(lambda u: u.usuario_rol == 'admin', login_url='/user-dashboard/')
def admin_dashboard(request):
    total_productos = Producto.objects.count()
    total_movimientos = HistorialInventario.objects.count()
    total_centros = CentroDistribucion.objects.count()
    ultimos_movimientos = HistorialInventario.objects.order_by('-historial_fecha')[:5]

    context = {
        'total_productos': total_productos,
        'total_movimientos': total_movimientos,
        'total_centros': total_centros,
        'ultimos_movimientos': ultimos_movimientos,
    }
    return render(request, "verdeLimonTemplates/admin_dashboard.html", context)

@login_required

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    favoritos = FavoritoCliente.objects.filter(id_usuario=request.user.id)

    productos_favoritos = []
    for favorito in favoritos:
        producto = Producto.objects.filter(id=favorito.id_producto).first()
        if producto:
            productos_favoritos.append({
                "id_producto": producto.id,
                "producto": producto,
                "fecha_agregado": favorito.fecha_agregado
            })

    return render(request, "verdeLimonTemplates/user_dashboard.html", {
        "productos_favoritos": productos_favoritos
    })



# --- Vistas para Favoritos (AJAX) ---
@login_required

def add_to_favorites(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        FavoritoCliente.objects.get_or_create(id_usuario=request.user.id, id_producto=product_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

@login_required

def remove_from_favorites(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        FavoritoCliente.objects.filter(id_usuario=request.user.id, id_producto=product_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# Vistas CRUD para CategoriaProducto
class CategoriaProductoListView(ListView):
    model = CategoriaProducto
    template_name = 'verdeLimonTemplates/crud/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaProductoCreateView(CreateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = 'verdeLimonTemplates/crud/categoria_form.html'
    success_url = reverse_lazy('categoria_list')

class CategoriaProductoUpdateView(UpdateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = 'verdeLimonTemplates/crud/categoria_form.html'
    success_url = reverse_lazy('categoria_list')

class CategoriaProductoDeleteView(DeleteView):
    model = CategoriaProducto
    template_name = 'verdeLimonTemplates/crud/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')

# Vistas CRUD para Direccion
class DireccionListView(ListView):
    model = Direccion
    template_name = 'verdeLimonTemplates/crud/direccion_list.html'
    context_object_name = 'direcciones'

class DireccionCreateView(CreateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'verdeLimonTemplates/crud/direccion_form.html'
    success_url = reverse_lazy('direccion_list')

class DireccionUpdateView(UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'verdeLimonTemplates/crud/direccion_form.html'
    success_url = reverse_lazy('direccion_list')

class DireccionDeleteView(DeleteView):
    model = Direccion
    template_name = 'verdeLimonTemplates/crud/direccion_confirm_delete.html'
    success_url = reverse_lazy('direccion_list')

# Vistas CRUD para CentroDistribucion
class CentroDistribucionListView(ListView):
    model = CentroDistribucion
    template_name = 'verdeLimonTemplates/crud/centro_distribucion_list.html'
    context_object_name = 'centros_distribucion'

class CentroDistribucionCreateView(CreateView):
    model = CentroDistribucion
    form_class = CentroDistribucionForm
    template_name = 'verdeLimonTemplates/crud/centro_distribucion_form.html'
    success_url = reverse_lazy('centro_distribucion_list')

class CentroDistribucionUpdateView(UpdateView):
    model = CentroDistribucion
    form_class = CentroDistribucionForm
    template_name = 'verdeLimonTemplates/crud/centro_distribucion_form.html'
    success_url = reverse_lazy('centro_distribucion_list')

class CentroDistribucionDeleteView(DeleteView):
    model = CentroDistribucion
    template_name = 'verdeLimonTemplates/crud/centro_distribucion_confirm_delete.html'
    success_url = reverse_lazy('centro_distribucion_list')

# Vistas CRUD para Producto
class ProductoListView(ListView):
    model = Producto
    template_name = 'verdeLimonTemplates/crud/producto_list.html'
    context_object_name = 'productos'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'verdeLimonTemplates/crud/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'verdeLimonTemplates/crud/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'verdeLimonTemplates/crud/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

# Vistas CRUD para ProductoValorNutricional
class ProductoValorNutricionalListView(ListView):
    model = ProductoValorNutricional
    template_name = 'verdeLimonTemplates/crud/producto_valor_nutricional_list.html'
    context_object_name = 'valores_nutricionales'

class ProductoValorNutricionalCreateView(CreateView):
    model = ProductoValorNutricional
    form_class = ProductoValorNutricionalForm
    template_name = 'verdeLimonTemplates/crud/producto_valor_nutricional_form.html'
    success_url = reverse_lazy('producto_valor_nutricional_list')

class ProductoValorNutricionalUpdateView(UpdateView):
    model = ProductoValorNutricional
    form_class = ProductoValorNutricionalForm
    template_name = 'verdeLimonTemplates/crud/producto_valor_nutricional_form.html'
    success_url = reverse_lazy('producto_valor_nutricional_list')

class ProductoValorNutricionalDeleteView(DeleteView):
    model = ProductoValorNutricional
    template_name = 'verdeLimonTemplates/crud/producto_valor_nutricional_confirm_delete.html'
    success_url = reverse_lazy('producto_valor_nutricional_list')

# Vistas CRUD para Inventario
class InventarioListView(ListView):
    model = Inventario
    template_name = 'verdeLimonTemplates/crud/inventario_list.html'
    context_object_name = 'inventarios'

class InventarioCreateView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'verdeLimonTemplates/crud/inventario_form.html'
    success_url = reverse_lazy('inventario_list')

class InventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'verdeLimonTemplates/crud/inventario_form.html'
    success_url = reverse_lazy('inventario_list')

class InventarioDeleteView(DeleteView):
    model = Inventario
    template_name = 'verdeLimonTemplates/crud/inventario_confirm_delete.html'
    success_url = reverse_lazy('inventario_list')

# Vistas CRUD para HistorialInventario
class HistorialInventarioListView(ListView):
    model = HistorialInventario
    template_name = 'verdeLimonTemplates/crud/historial_inventario_list.html'
    context_object_name = 'historial_movimientos'

class HistorialInventarioCreateView(CreateView):
    model = HistorialInventario
    form_class = HistorialInventarioForm
    template_name = 'verdeLimonTemplates/crud/historial_inventario_form.html'
    success_url = reverse_lazy('historial_inventario_list')

class HistorialInventarioUpdateView(UpdateView):
    model = HistorialInventario
    form_class = HistorialInventarioForm
    template_name = 'verdeLimonTemplates/crud/historial_inventario_form.html'
    success_url = reverse_lazy('historial_inventario_list')

class HistorialInventarioDeleteView(DeleteView):
    model = HistorialInventario
    template_name = 'verdeLimonTemplates/crud/historial_inventario_confirm_delete.html'
    success_url = reverse_lazy('historial_inventario_list')


# Vistas CRUD para ContactoCentro
class ContactoCentroListView(ListView):
    model = ContactoCentro
    template_name = 'verdeLimonTemplates/crud/contacto_centro_list.html'
    context_object_name = 'contactos_centros'

class ContactoCentroCreateView(CreateView):
    model = ContactoCentro
    form_class = ContactoCentroForm
    template_name = 'verdeLimonTemplates/crud/contacto_centro_form.html'
    success_url = reverse_lazy('contacto_centro_list')

class ContactoCentroUpdateView(UpdateView):
    model = ContactoCentro
    form_class = ContactoCentroForm
    template_name = 'verdeLimonTemplates/crud/contacto_centro_form.html'
    success_url = reverse_lazy('contacto_centro_list')

class ContactoCentroDeleteView(DeleteView):
    model = ContactoCentro
    template_name = 'verdeLimonTemplates/crud/contacto_centro_confirm_delete.html'
    success_url = reverse_lazy('contacto_centro_list')

# Vistas CRUD para Proveedor
class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'verdeLimonTemplates/crud/proveedor_list.html'
    context_object_name = 'proveedores'

class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'verdeLimonTemplates/crud/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'verdeLimonTemplates/crud/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'verdeLimonTemplates/crud/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')

# Vistas CRUD para FavoritoCliente
class FavoritoClienteListView(ListView):
    model = FavoritoCliente
    template_name = 'verdeLimonTemplates/crud/favorito_cliente_list.html'
    context_object_name = 'favoritos_clientes'

class FavoritoClienteCreateView(CreateView):
    model = FavoritoCliente
    form_class = FavoritoClienteForm
    template_name = 'verdeLimonTemplates/crud/favorito_cliente_form.html'
    success_url = reverse_lazy('favorito_cliente_list')

class FavoritoClienteUpdateView(UpdateView):
    model = FavoritoCliente
    form_class = FavoritoClienteForm
    template_name = 'verdeLimonTemplates/crud/favorito_cliente_form.html'
    success_url = reverse_lazy('favorito_cliente_list')

class FavoritoClienteDeleteView(DeleteView):
    model = FavoritoCliente
    template_name = 'verdeLimonTemplates/crud/favorito_cliente_confirm_delete.html'
    success_url = reverse_lazy('favorito_cliente_list')

