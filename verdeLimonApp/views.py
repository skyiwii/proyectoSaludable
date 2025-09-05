from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "verdeLimonTemplates/index.html")

def productos(request):
    return render(request, "verdeLimonTemplates/productos.html")

def nosotros(request):
    return render(request, "verdeLimonTemplates/nosotros.html")

def contacto(request):
    return render(request, "verdeLimonTemplates/contacto.html")

def distribucion(request):
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
