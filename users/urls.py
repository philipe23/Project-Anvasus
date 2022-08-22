from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('account', views.accountView, name='account'),
    path('course/<str:pk>', views.courseView, name='course'),
    path('topic/<str:pk>', views.topicView, name='topic'),
    path('topic_register/<str:pk>', views.topicRegister, name='topic_register'),
    path('topic_delete/<str:pk>/<str:pk2>', views.topicDelete, name='topic_delete'),
    path('course_register/<str:pk>', views.courseRegister, name="course_register"),
    path('course_update/<str:pk>', views.courseUpdate, name="course_update"),
    path('course_delete/<str:pk>', views.courseDelete, name="course_delete"),
    path('certificado/<str:pk>/<str:pk2>', views.certificado, name='certificado'),
    path('pdf/<str:pk>/<str:pk2>', views.pdf, name="pdf"),
    path('confirmacao', views.confirmacao, name="confirmacao")
]
