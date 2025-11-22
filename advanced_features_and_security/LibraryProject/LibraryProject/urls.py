from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include the app urls at root so '' resolves to the app's urls
    path('', include('relationship_app.urls')),
]
