from django.urls import path

from kirjasto import views 

app_name = 'kirjasto'
urlpatterns = [
    path("", views.KirjastoView.as_view(), name="kirjasto"),
    path('lainat/', views.LainaListView.as_view(), name='lainat'),
    path('return_book/<int:pk>/', views.ReturnBookView.as_view(), name='return_book'),
    path('history/', views.LoanHistoryView.as_view(), name='loan_history'),
    path('kirja/<int:pk>/', views.KirjaView.as_view(), name='kirja'),
    path('lainaus/', views.LainaView.as_view(), name='lainaus'),
]