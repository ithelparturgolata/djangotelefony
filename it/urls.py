from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('dashboard_it/', views.dashboard_it, name='dashboard_it'),
	path('user/<int:user_id>/', views.user_detail_it, name='user_detail_it'),
	path('search/', views.search_it, name='search_it'),
	path('update/<int:user_id>/', views.update_user_it, name='update_user_it'),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
						  document_root=settings.MEDIA_ROOT)
