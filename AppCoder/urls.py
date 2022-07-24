from django.urls import path

from AppCoder import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
   
    path('', views.inicio, name="inicio"), #esta era nuestra primer view
    path('animales', views.animales, name="animales"),
    path('busquedaNombre', views.busquedaNombre, name="busquedaNombre"),
    path('resultadosBusqueda', views.resultadosBusqueda, name="resultadosBusqueda"),
    path('animales/list/', views.AnimalesList.as_view(), name='List'),
    path(r'^animales/(?P<pk>\+)$', views.AnimalesDetalle.as_view(),name='Detail'),
    path(r'^nuevo$', views.AnimalesCreacion.as_view(), name="New"),
    path(r'^editar/(?P<pk>\d+)$',views.AnimalesUpdate.as_view(),name='Edit'),
    path(r'^borrar/(?P<pk>\d+)$',views.AnimalesDelete.as_view(),name='Delete'),
    path('login',views.login_request, name= 'Login'),
    path('register',views.register, name= 'Register'),
    path('logout',LogoutView.as_view(template_name='AppCoder/logout.html'), name='logout'),
    path('editarPerfil', views.editarPerfil,name="editarPerfil"),
    path('blogFormulario', views.blogFormulario, name="blogFormulario"),
    path('blog', views.blog, name="blog"),
    path('blogs/list/', views.BlogList.as_view(), name='blogList'),
    path(r'^blogs/(?P<pk>\+)$', views.BlogDetalle.as_view(),name='blogDetalle')
]

