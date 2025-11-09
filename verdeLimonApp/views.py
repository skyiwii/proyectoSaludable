from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.db.models import Prefetch
import json

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

# ----------------------------------------------------------
#                   VISTAS PRINCIPALES
# ----------------------------------------------------------

def index(request):
    productos_recientes = Producto.objects.all().order_by('-id')[:3]
    return render(request, "verdeLimonTemplates/index.html", {
        "productos_recientes": productos_recientes
    })


def productos(request):
    productos = Producto.objects.all()

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = list(
            FavoritoCliente.objects.filter(id_usuario=request.user)
            .values_list('id_producto__id', flat=True)
        )

    return render(request, "verdeLimonTemplates/productos.html", {
        "productos": productos,
        "favoritos_ids": favoritos_ids
    })


def nosotros(request):
    return render(request, "verdeLimonTemplates/nosotros.html")


def contacto(request):
    return render(request, "verdeLimonTemplates/contacto.html")


def distribucion(request):
    centros_distribucion = (
        CentroDistribucion.objects
        .select_related('id_direccion')
        .prefetch_related(
            Prefetch('contactocentro_set', queryset=ContactoCentro.objects.all(), to_attr='pref_contactos'),
            Prefetch('inventario_set',
                     queryset=Inventario.objects.filter(inventario_cantidad__gt=0).select_related('id_producto'),
                     to_attr='pref_inventarios')
        )
    )

    centros_distribucion_data = []

    for centro in centros_distribucion:
        contactos_data = [
            {
                'contacto_tipo': c.contacto_tipo,
                'contacto_valor': c.contacto_valor
            } for c in centro.pref_contactos
        ]

        productos_data = [
            {
                'producto_nombre': inv.id_producto.producto_nombre,
                'producto_precio': float(inv.id_producto.producto_precio or 0),
                'inventario_cantidad': inv.inventario_cantidad,
                'producto_imagen': inv.id_producto.producto_imagen.url if inv.id_producto.producto_imagen else None
            } for inv in centro.pref_inventarios
        ]

        centros_distribucion_data.append({
            'id': centro.id,
            'centro_nombre': centro.centro_nombre,
            'centro_tipo': centro.centro_tipo,
            'centro_descripcion': centro.centro_descripcion,
            'centro_imagen': centro.centro_imagen.url if centro.centro_imagen else None,
            'direccion': {
                'direccion_calle': centro.id_direccion.direccion_calle,
                'direccion_ciudad': centro.id_direccion.direccion_ciudad,
                'direccion_region': centro.id_direccion.direccion_region,
                'direccion_pais': centro.id_direccion.direccion_pais,
                'direccion_codigo_postal': centro.id_direccion.direccion_codigo_postal,
            },
            'contactos': contactos_data,
            'productos': productos_data
        })

    return render(request, "verdeLimonTemplates/distribucion.html", {
        "centros_distribucion": centros_distribucion,
        "centros_distribucion_json": json.dumps(centros_distribucion_data)
    })


# ----------------------------------------------------------
#                    AUTENTICACIÓN
# ----------------------------------------------------------

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin_dashboard' if user.usuario_rol == 'admin' else 'user_dashboard')
    else:
        form = RegistroForm()

    return render(request, 'verdeLimonTemplates/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('admin_dashboard' if user.usuario_rol == 'admin' else 'user_dashboard')
    else:
        form = LoginForm()

    return render(request, 'verdeLimonTemplates/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


# ----------------------------------------------------------
#                      DASHBOARDS
# ----------------------------------------------------------

@login_required
@user_passes_test(lambda u: u.usuario_rol == 'admin', login_url='/user-dashboard/')
def admin_dashboard(request):
    return render(request, "verdeLimonTemplates/admin_dashboard.html", {
        'total_productos': Producto.objects.count(),
        'total_movimientos': HistorialInventario.objects.count(),
        'total_centros': CentroDistribucion.objects.count(),
        'ultimos_movimientos': HistorialInventario.objects.order_by('-historial_fecha')[:5],
    })


@login_required
def user_dashboard(request):
    favoritos = FavoritoCliente.objects.filter(id_usuario=request.user).select_related('id_producto')
    return render(request, "verdeLimonTemplates/user_dashboard.html", {
        'productos_favoritos': favoritos
    })


# ----------------------------------------------------------
#                     FAVORITOS (AJAX)
# ----------------------------------------------------------

@login_required
def add_to_favorites(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    product_id = request.POST.get('product_id')
    producto = get_object_or_404(Producto, id=product_id)

    favorito, created = FavoritoCliente.objects.get_or_create(
        id_usuario=request.user,
        id_producto=producto
    )

    return JsonResponse({
        'success': True,
        'added': created
    })


@login_required
def remove_from_favorites(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    product_id = request.POST.get('product_id')
    producto = get_object_or_404(Producto, id=product_id)

    deleted, _ = FavoritoCliente.objects.filter(
        id_usuario=request.user,
        id_producto=producto
    ).delete()

    return JsonResponse({
        'success': True,
        'removed': deleted > 0
    })


# ----------------------------------------------------------
#                 CRUD: CATEGORIA PRODUCTO
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                          CRUD: DIRECCIÓN
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                    CRUD: CENTRO DISTRIBUCIÓN
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                         CRUD: PRODUCTO
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#             CRUD: PRODUCTO VALOR NUTRICIONAL
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                         CRUD: INVENTARIO
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                   CRUD: HISTORIAL INVENTARIO
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                     CRUD: CONTACTO CENTRO
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                         CRUD: PROVEEDOR
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#                       CRUD: FAVORITO CLIENTE
# ----------------------------------------------------------

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
