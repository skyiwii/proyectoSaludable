# proyectoSaludable



Proyecto Inicial para la empresa Green Limons centrada en la distribución de productos y sistema administrativo para empleados.

Día 1:

Acción 1:

El commit inicial se hizo para subir el avance del proyecto y subir su estructura hasta ahora.

La estructura del proyecto hasta el momento contempla solamente las templates de la homepage.

La carpeta estática solamente posee los estilos de la homepage como css

proyectoSaludable/
├── static/
│   ├── css/
│   │   └── ...
│   └── images/
│       └── ...
├── templates/
├──── static/
│     └── verdeLimonTemplates
│       └── Archivos html que componen la homepage
├── verdeLimonApp/
├── manage.py


Acción 1.1:

Se le integro la capacidad de mostrar el logo de la página en la homepage y en las pestañas.

Acción 1.2:

Se modifico la pestaña de navegación de contacto.html para que quedase acorde a el estilo general de la homepage.

Acción 1.3:

Se "modernizo" el aspecto general de la página en su styles.css (principal) y se reorganizo la página completa para más lógica como centro distributivo/tienda.

Acción 1.4:

Se terminó la pestaña de contacto.html y se creó un css aparte del main para organizar el estilo de contactos por separado.


Día 2:

En este día se terminará la pestaña de "Distribución" con datos relevantes y el menú desplegable que después deberá usarse con la base de datos.

Acción 1:

Se modificó la pestaña de distribución tal que contenga una vista funcional.

Acción 1.1:

Se adjuntaron los íconos faltantes de redes en la página "contacto.html"

Acción 1.2:

Vista de distribución: agregado menú desplegable para poder seleccionar el centro de distribución que se desea.
En este sentido, por el momento se contempla las 3 principales ciudades de la región: copiapó, vallenar, caldera


Acción 1.3:

En la vista views.py, los datos son cargados como dummy para demostrar que funciona el menú desplegable.

Las imágenes se deberán agregar cuando se estime conveniente.

Los datos cargados fueron: ubicaciones = [
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

Dia 3:

Acción 1:

Se agregó el archivo de texto requirements.txt con el comando pip3 freeze > requirements.txt

Acción 1.1:

Se agregó el login/registro básico con datos dummy precargados para simular el inicio y sesión de usuarios/admin

Está sujeto a cambios del lado de administradores.

Acción 1.2:

A este login se le agregó el dashboard que también está sujeto a cambios.


Día 4:

-Se completo el contenido de la pagina nosotros.html con histroia, objetivos, vision, alcance e invitación de la empresa.
-se creó el archivo nosotros.css para aplicar un diseño personalizado con colores naturales enfocados en alimentación  saludable.
-se modifico productos.html:
    -se añadieron imagenes de los productos (Pan de Centeno Integral, Barra  de Cereal Saludable y Miel Natural).
    -Se incorporaron descripciones breves y botones de cotizacion.
    -Se agregó un boton de '⭐ En Favoritos' en cada producto con funcionalidad visual.
-Se creo productos.css para dar estilo al catalogo de productos:
    -Diseño en cuadricula responsiva con tarjetas uniformes.
    -Colores cálidos y verdes naturales.
    -Bordes visibles en imagenes y tarjetas.
    -Estilo para el boton de favoritos con efecto de activación.
-Se implemento un script en productos.html para la funcionalidad de favoritos (marcar/desmarcar productos de forma visual)


Día 5 (Final):


Acción 1:

Se implemento el crud para dashboard de usuarios (favoritos) y administradores (inventario de las distribuidoras/tiendas).

# Usuarios ya creados dentro del sistema: 
# admin1 1234 Para vista admin
# user1 abcd Para vista usuario

Para testear y probar el sistema