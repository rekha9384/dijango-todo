from django.contrib import admin
from django.urls import path
from todo import views   # ✅ IMPORTANT

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    # 🔐 ADD THESE 👇
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('complete/<int:id>/', views.complete_task, name='complete'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
]