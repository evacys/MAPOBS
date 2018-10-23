from django.urls import path, include
from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView


app_name = 'app'
urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    # Search form
    path('<str:feature_type>/search/', views.search, name='search'),
    # Admin pannel
    path('admin/', views.admin, name='admin'),
    # Add feature page (admin pannel)
    path('add/<str:feature_type>/', views.add, name='add'),
    # Change feature page (admin pannel)
    path('modify/<str:feature_type>/<int:feature_id>', views.modify, name='modify'),
    # List of available features
    path('<str:feature_type>/', views.get_features, name='features'),
    # Feature details
    path('<str:feature_type>/<int:feature_id>/', views.detail, name='detail'),
    # List of related features
    path('<str:feature_type>/<int:feature_id>/<str:output_feature_type>/', views.get_related_features, name='related_features'),
    # Related feature details
    path('<str:feature_type>/<int:feature_id>/<str:output_feature_type>/<output_feature_id>', views.related_features_detail, name='related_features_detail'),

]
