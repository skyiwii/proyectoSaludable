
from django.shortcuts import render, redirect
from django.http import JsonResponse

# --- Datos Dummy (simulando una base de datos) ---
# Lista de productos dummy
productos_dummy = [
    {
        'id': 1,
        'nombre': 'Manzanas Orgánicas',
        'descripcion': 'Manzanas rojas orgánicas cultivadas sin pesticidas',
        'categoria': 'Frutas',
        'precio': 2500.00,
        'stock': 45,
        'valor_nutricional': 'Calorías: 52 por 100g, Fibra: 2.4g, Vitamina C: 4.6mg, Potasio: 107mg',
        'centro_distribucion': 'Pulso Verde Copiapó',
        'fecha_creacion': '2024-01-15',
        'imagen': 'images/manzana.png'
    },
    {
        'id': 2,
        'nombre': 'Palta Hass',
        'descripcion': 'Paltas Hass premium, perfectas para ensaladas y tostadas',
        'categoria': 'Frutas',
        'precio': 1800.00,
        'stock': 23,
        'valor_nutricional': 'Calorías: 160 por 100g, Grasas saludables: 15g, Fibra: 7g, Potasio: 485mg',
        'centro_distribucion': 'Marea Sana Caldera',
        'fecha_creacion': '2024-01-20',
        'imagen': 'images/palta.png'
    },
    {
        'id': 3,
        'nombre': 'Quinoa Real',
        'descripcion': 'Quinoa boliviana de alta calidad, rica en proteínas',
        'categoria': 'Cereales',
        'precio': 3200.00,
        'stock': 8,
        'valor_nutricional': 'Calorías: 368 por 100g, Proteínas: 14g, Fibra: 7g, Hierro: 4.6mg',
        'centro_distribucion': 'Valle Verde Vallenar',
        'fecha_creacion': '2024-02-01',
        'imagen': 'images/quinua.png'
    }
]

# Lista de movimientos de inventario dummy
movimientos_dummy = [
    {
        'id': 1,
        'producto': 'Manzanas Orgánicas',
        'tipo_movimiento': 'entrada',
        'cantidad': 50,
        'motivo': 'Stock inicial del producto',
        'usuario': 'admin',
        'fecha': '2024-01-15 10:30:00',
        'stock_anterior': 0,
        'stock_nuevo': 50
    },
    {
        'id': 2,
        'producto': 'Palta Hass',
        'tipo_movimiento': 'entrada',
        'cantidad': 30,
        'motivo': 'Stock inicial del producto',
        'usuario': 'admin',
        'fecha': '2024-01-20 14:15:00',
        'stock_anterior': 0,
        'stock_nuevo': 30
    },
    {
        'id': 3,
        'producto': 'Quinoa Real',
        'tipo_movimiento': 'entrada',
        'cantidad': 15,
        'motivo': 'Stock inicial del producto',
        'usuario': 'admin',
        'fecha': '2024-02-01 09:45:00',
        'stock_anterior': 0,
        'stock_nuevo': 15
    },
    {
        'id': 4,
        'producto': 'Palta Hass',
        'tipo_movimiento': 'salida',
        'cantidad': 7,
        'motivo': 'Venta a cliente',
        'usuario': 'vendedor1',
        'fecha': '2024-02-05 16:20:00',
        'stock_anterior': 30,
        'stock_nuevo': 23
    },
    {
        'id': 5,
        'producto': 'Quinoa Real',
        'tipo_movimiento': 'salida',
        'cantidad': 7,
        'motivo': 'Venta a cliente',
        'usuario': 'vendedor2',
        'fecha': '2024-02-10 11:30:00',
        'stock_anterior': 15,
        'stock_nuevo': 8
    }
]

# Usuarios dummy para simulación de acceso
usuarios_dummy = {
    'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Administrador'},
    'user1': {'password': 'user123', 'role': 'user', 'name': 'Usuario Regular'},
    'vendedor1': {'password': 'vend123', 'role': 'user', 'name': 'Vendedor 1'},
    'vendedor2': {'password': 'vend123', 'role': 'user', 'name': 'Vendedor 2'}
}

# --- Vistas Principales ---

def index(request):
    """Renderiza la página de inicio."""
    return render(request, "verdeLimonTemplates/index.html")

def productos(request):
    """Renderiza la página de productos con datos dummy."""
    return render(request, "verdeLimonTemplates/productos.html", {"productos": productos_dummy})

def nosotros(request):
    """Renderiza la página 'Sobre Nosotros'."""
    return render(request, "verdeLimonTemplates/nosotros.html")

def contacto(request):
    """Renderiza la página de contacto."""
    return render(request, "verdeLimonTemplates/contacto.html")

def distribucion(request):
    """Renderiza la página de distribución con ubicaciones dummy."""
    ubicaciones = [
        # ------------------- Copiapó -------------------
        {
            "nombre": "Pulso Verde Copiapó",
            "tipo": "Centro de Distribución",
            "ciudad": "Copiapó",
            "direccion_corta": "Av. Atacama 1234",
            "direccion_completa": "Av. Atacama 1234, Centro, Copiapó, Región de Atacama, Chile",
            "imagen": "images/copiapo_centro.jpg",
            "descripcion": "Distribución al por mayor de frutas, verduras y productos naturales de la región de Atacama.",
            "productos": ["Frutas frescas", "Verduras locales", "Jugos naturales", "Snacks saludables"]
        },
        {
            "nombre": "Frutalía",
            "tipo": "Supermercado",
            "ciudad": "Copiapó",
            "direccion_corta": "Calle Prat 567",
            "direccion_completa": "Calle Prat 567, Centro, Copiapó, Región de Atacama, Chile",
            "imagen": "images/copiapo_supermercado.jpg",
            "descripcion": "Supermercado especializado en productos orgánicos y saludables.",
            "productos": ["Frutas orgánicas", "Verduras orgánicas", "Cereales integrales", "Bebidas naturales"]
        },
        {
            "nombre": "Raíces y Semillas",
            "tipo": "Bazar",
            "ciudad": "Copiapó",
            "direccion_corta": "Av. Chacabuco 890",
            "direccion_completa": "Av. Chacabuco 890, Barrio Norte, Copiapó, Región de Atacama, Chile",
            "imagen": "images/copiapo_bazar.jpg",
            "descripcion": "Bazar con productos saludables, snacks y artesanías locales.",
            "productos": ["Snacks naturales", "Miel local", "Infusiones", "Aceites esenciales"]
        },
        {
            "nombre": "Bocado Vital",
            "tipo": "Kiosco",
            "ciudad": "Copiapó",
            "direccion_corta": "Plaza de Armas 12",
            "direccion_completa": "Plaza de Armas 12, Centro, Copiapó, Región de Atacama, Chile",
            "imagen": "images/copiapo_kiosco1.jpg",
            "descripcion": "Kiosco con frutas listas para llevar y productos saludables.",
            "productos": ["Frutas cortadas", "Barras de cereales", "Jugos naturales"]
        },
        {
            "nombre": "Verde Express",
            "tipo": "Kiosco",
            "ciudad": "Copiapó",
            "direccion_corta": "Av. Copayapu 45",
            "direccion_completa": "Av. Copayapu 45, Sector Norte, Copiapó, Región de Atacama, Chile",
            "imagen": "images/copiapo_kiosco2.jpg",
            "descripcion": "Kiosco con productos frescos y snacks saludables para llevar.",
            "productos": ["Frutas frescas", "Frutos secos", "Bebidas naturales"]
        },

        # ------------------- Caldera -------------------
        {
            "nombre": "Marea Sana",
            "tipo": "Centro de Distribución",
            "ciudad": "Caldera",
            "direccion_corta": "Av. del Mar 101",
            "direccion_completa": "Av. del Mar 101, Centro, Caldera, Región de Atacama, Chile",
            "imagen": "images/caldera_centro.jpg",
            "descripcion": "Distribución de productos saludables con enfoque en pescado, omega3 y productos marinos.",
            "productos": ["Pescados frescos", "Aceite de pescado", "Alimentos funcionales", "Snacks marinos"]
        },
        {
            "nombre": "Omega Market",
            "tipo": "Supermercado",
            "ciudad": "Caldera",
            "direccion_corta": "Calle Prat 22",
            "direccion_completa": "Calle Prat 22, Centro, Caldera, Región de Atacama, Chile",
            "imagen": "images/caldera_supermercado.jpg",
            "descripcion": "Supermercado con productos ricos en omega3 y alimentos saludables del mar.",
            "productos": ["Pescados y mariscos", "Suplementos de omega3", "Frutas frescas", "Verduras locales"]
        },
        {
            "nombre": "Coral Vital",
            "tipo": "Bazar",
            "ciudad": "Caldera",
            "direccion_corta": "Av. Pacífico 77",
            "direccion_completa": "Av. Pacífico 77, Barrio Puerto, Caldera, Región de Atacama, Chile",
            "imagen": "images/caldera_bazar.jpg",
            "descripcion": "Bazar con productos del mar, snacks saludables y artesanías locales.",
            "productos": ["Snacks de algas", "Miel local", "Infusiones", "Aceites naturales"]
        },
        {
            "nombre": "Brisa Marina",
            "tipo": "Kiosco",
            "ciudad": "Caldera",
            "direccion_corta": "Plaza del Puerto 5",
            "direccion_completa": "Plaza del Puerto 5, Centro, Caldera, Región de Atacama, Chile",
            "imagen": "images/caldera_kiosco1.jpg",
            "descripcion": "Kiosco con productos frescos y saludables del mar y tierra.",
            "productos": ["Pescado en conserva", "Frutas locales", "Jugos naturales"]
        },
        {
            "nombre": "Sol del Pacífico",
            "tipo": "Kiosco",
            "ciudad": "Caldera",
            "direccion_corta": "Av. Sol 12",
            "direccion_completa": "Av. Sol 12, Sector Norte, Caldera, Región de Atacama, Chile",
            "imagen": "images/caldera_kiosco2.jpg",
            "descripcion": "Kiosco con productos saludables y snacks listos para llevar.",
            "productos": ["Frutas frescas", "Barras de cereales", "Snacks marinos"]
        },

        # ------------------- Vallenar -------------------
        {
            "nombre": "Valle Verde",
            "tipo": "Centro de Distribución",
            "ciudad": "Vallenar",
            "direccion_corta": "Av. Atacama 300",
            "direccion_completa": "Av. Atacama 300, Centro, Vallenar, Región de Atacama, Chile",
            "imagen": "images/vallenar_centro.jpg",
            "descripcion": "Distribución de frutas, verduras y productos naturales para la provincia del Huasco.",
            "productos": ["Frutas frescas", "Verduras locales", "Jugos naturales", "Snacks saludables"]
        },
        {
            "nombre": "Huasco Natural",
            "tipo": "Supermercado",
            "ciudad": "Vallenar",
            "direccion_corta": "Calle O'Higgins 45",
            "direccion_completa": "Calle O'Higgins 45, Centro, Vallenar, Región de Atacama, Chile",
            "imagen": "images/vallenar_supermercado.jpg",
            "descripcion": "Supermercado con productos saludables y orgánicos.",
            "productos": ["Frutas orgánicas", "Verduras locales", "Cereales integrales", "Bebidas naturales"]
        },
        {
            "nombre": "Tierra Viva",
            "tipo": "Bazar",
            "ciudad": "Vallenar",
            "direccion_corta": "Av. Los Pinos 78",
            "direccion_completa": "Av. Los Pinos 78, Barrio Sur, Vallenar, Región de Atacama, Chile",
            "imagen": "images/vallenar_bazar.jpg",
            "descripcion": "Bazar con productos saludables y snacks locales.",
            "productos": ["Snacks naturales", "Miel local", "Infusiones", "Aceites esenciales"]
        },
        {
            "nombre": "Fresco & Saludable",
            "tipo": "Kiosco",
            "ciudad": "Vallenar",
            "direccion_corta": "Plaza Central 2",
            "direccion_completa": "Plaza Central 2, Centro, Vallenar, Región de Atacama, Chile",
            "imagen": "images/vallenar_kiosco1.jpg",
            "descripcion": "Kiosco con productos frescos listos para llevar.",
            "productos": ["Frutas frescas", "Barras de cereales", "Jugos naturales"]
        },
        {
            "nombre": "Rincón Verde",
            "tipo": "Kiosco",
            "ciudad": "Vallenar",
            "direccion_corta": "Av. Norte 15",
            "direccion_completa": "Av. Norte 15, Sector Norte, Vallenar, Región de Atacama, Chile",
            "imagen": "images/vallenar_kiosco2.jpg",
            "descripcion": "Kiosco con snacks y productos saludables para llevar.",
            "productos": ["Frutas frescas", "Frutos secos", "Bebidas naturales"]
        }
    ]

    contexto = {"ubicaciones": ubicaciones}
    return render(request, "verdeLimonTemplates/distribucion.html", contexto)

# --- Vistas de Dashboard ---

# Usuarios ya creados dentro del sistema: 
# admin1 1234 Para vista admin
# user1 abcd Para vista usuario


def dashboard_view(request):
    """Redirige al dashboard de admin o usuario según el parámetro 'user_type'."""
    user_type = request.GET.get('user_type', 'user')
    if user_type == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')

def admin_dashboard(request):
    """Dashboard para administradores: permite agregar productos y ver historial de inventario."""
    # Simulación de restricción de acceso: Solo permite el acceso si el usuario es 'admin'

    # Verificar acceso de administrador usando parámetro user_type o sesión
    user_type = request.GET.get("user_type")
    session_user_type = request.session.get("user_type")
    
    # Si no es admin, redirigir al dashboard de usuario
    if user_type != "admin" and session_user_type != "admin":
        # Establecer mensaje de error en la sesión
        request.session['error_message'] = "Acceso denegado. Se requieren privilegios de administrador."
        return redirect("user_dashboard")
    
    # Establecer el tipo de usuario en la sesión para futuras verificaciones
    if user_type == "admin":
        request.session["user_type"] = "admin"

    if request.method == 'POST':
        # Lógica para agregar un nuevo producto (simulado)
        nuevo_producto = {
            'id': len(productos_dummy) + 1,
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'categoria': request.POST.get('categoria'),
            'precio': float(request.POST.get('precio')),
            'stock': int(request.POST.get('stock')),
            'valor_nutricional': request.POST.get('valor_nutricional'),
            'centro_distribucion': request.POST.get('centro_distribucion'),
            'fecha_creacion': '2024-03-15',
            'imagen': 'images/' # Imagen por defecto
        }
        productos_dummy.append(nuevo_producto)
        
        # Simular registro de movimiento de inventario
        nuevo_movimiento = {
            'id': len(movimientos_dummy) + 1,
            'producto': nuevo_producto['nombre'],
            'tipo_movimiento': 'entrada',
            'cantidad': nuevo_producto['stock'],
            'motivo': 'Stock inicial del producto',
            'usuario': 'admin',
            'fecha': '2024-03-15 12:00:00',
            'stock_anterior': 0,
            'stock_nuevo': nuevo_producto['stock']
        }
        movimientos_dummy.append(nuevo_movimiento)
        
        # Establecer mensaje de éxito
        request.session['success_message'] = f"Producto '{nuevo_producto['nombre']}' agregado exitosamente."

    return render(request, "verdeLimonTemplates/admin_dashboard.html", {
        "productos": productos_dummy,
        "movimientos": movimientos_dummy
    })

def user_dashboard(request):
    """Dashboard para usuarios: permite ver y gestionar productos favoritos."""
    favoritos_ids = request.session.get('favoritos', [])
    productos_favoritos = [p for p in productos_dummy if p['id'] in favoritos_ids]
    return render(request, "verdeLimonTemplates/user_dashboard.html", {
        "productos": productos_dummy,
        "productos_favoritos": productos_favoritos
    })

# --- Vistas para Favoritos (AJAX) ---

def add_to_favorites(request):
    """Agrega un producto a la lista de favoritos del usuario (simulado con sesión)."""
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        favoritos = request.session.get('favoritos', [])
        if product_id not in favoritos:
            favoritos.append(product_id)
            request.session['favoritos'] = favoritos
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def remove_from_favorites(request):
    """Quita un producto de la lista de favoritos del usuario (simulado con sesión)."""
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        favoritos = request.session.get('favoritos', [])
        if product_id in favoritos:
            favoritos.remove(product_id)
            request.session['favoritos'] = favoritos
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
