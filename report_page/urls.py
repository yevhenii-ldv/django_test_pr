from django.urls import path, include

from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('reports/', views.ReportListView.as_view()),
    path('reports/<slug:date_first>/<slug:date_last>', views.ReportDateFilterView.as_view()),
    path('reports/<int:pk>/', views.ReportDetail.as_view()),
    path('reports/weeks/', views.ReportPerWeekView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]