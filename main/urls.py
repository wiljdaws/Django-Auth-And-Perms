from django.urls import path
from . import views

print(dir(views))

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.signup, name='sign_up'),
    path('courses/', views.courses, name='courses'),
    path('edit_course/<int:id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:id>/', views.delete_course, name='delete_course'),
    path('professors/', views.professors, name='professors'),
    path('edit_professor/<int:id>/', views.edit_professor, name='edit_professor'),
    path('delete_professor/<int:id>/', views.delete_professor, name='delete_professor'),
    path('add_professor/', views.add_professor, name='add_professor'),
    path('add_course/', views.add_course, name='add_course'),
    path('logout/', views.logout_view, name='logout'),
]