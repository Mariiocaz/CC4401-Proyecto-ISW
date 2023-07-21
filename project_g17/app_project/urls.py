from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('register/', views.register_user, name='register_user'), 
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user_account/', views.transacciones, name='user-account'), 
    path('list_transacciones/', views.list_transacciones, name='list_transacciones'),     
    path('delete_transaccion/', views.delete_transaccion, name='delete_transaccion'), 
    path('modify_transaccion/', views.modify_transaccion, name='modify_transaccion'),     
    path('user_account/<slug:error_id>/', views.transacciones, name='error-transaccion')
]     