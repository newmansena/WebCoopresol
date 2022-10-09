from django.conf import settings
from  django.urls import URLPattern, path
from . import views
from django.conf.urls.static import static


urlpatterns=[
    path('',views.Administracion,name="administracion"),
    path('autenticar',views.autenticacion,name="autenticar"),
    path('cerrarSesio/',views.cerrarSesion,name='cerrarSesion'),
    path('usuarios',views.usuarios,name='usuarios'),
    path('eliminarSuarios/Detalles<str:pk>',views.eliminarUsuario,name='EliminarUsuario'),
    path('editarusuario',views.editarUsuario,name='editarusuario'),
    path('registroU',views.crearUsuario,name='registroU'),


    path('ProyectosAdmin',views.ProyectosAdmin,name="ProyectosAdmin"),
    path('proyectos/Detalles<str:pk>',views.Proyecto,name="proyecto"),

    path('EquipoA',views.PaginaEquipo,name="Equipo"),
    path('ProyectosAdmin/<str:model>/Detalles<str:pk>',views.detalles,name="Detalles"),
    path('Videos',views.VideosPagina,name="Aula"),
    path('Correos',views.Correos,name="Correos"),
    path('Correos/Detalles<str:pk>',views.detalleCorreo,name="Leer"),

    path('ProyectosAdmin/Detalles<str:pk>',views.eliminarSolicitudFisica,name="EliminarFisica"),
    path('EliminarSolicitud/Detalles<str:pk>',views.eliminarSolicitudJuridica,name="EliminarJuridica"),
    path('EliminarVideo/Detalles<str:pk>',views.eliminarVideos,name="EliminarVideo"),
    path('EliminarCategoria/Detalles<str:pk>',views.eliminarCategoria,name="EliminarCategoria"),
    path('EliminarPersona/Detalles<str:pk>',views.EliminarPersona,name="EliminarPersona"),
    path('EliminarProyecto/Detalles<str:pk>',views.EliminarProyecto,name="EliminarProyecto"),
    path('EliminarIdea/Detalles<str:pk>',views.EliminarIdea,name="EliminarIdea"),

    path('<str:model>/Detalles<str:pk>',views.detalleSolicitudes,name="Solicitud"),
    path('Reporte',views.Repotes,name="Reporte"),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)