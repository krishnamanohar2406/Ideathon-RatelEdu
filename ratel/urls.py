"""
URL configuration for ratel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.conf import settings
# from django.conf.urls.static import static
# import debug_toolbar
# from django.contrib import admin
# from django.urls import path, include
# admin.site.site_header = "Storefront Admin"
# admin.site.index_title="Admin"

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('details/', include('details.urls')),
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.jwt')),
#     path('__debug__/', include(debug_toolbar.urls)),
# ]


from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', include('accounts.urls')), 
    path('api/', include('details.urls')),
]