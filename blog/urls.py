from django.urls import path

from . import views
#app_name="blog"

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('author/<name>', views.getauthor.as_view(), name="author"),
    path('article/<int:id>', views.getsingle.as_view(), name="single_post"),
    path('topic/<name>', views.getTopic.as_view(), name="topic"),
    path('login', views.getLogin.as_view(), name="login"),
    path('logout', views.getlogout.as_view(), name="logout"),
    path('create', views.getcreate, name="create"),
    path('profile', views.getProfile, name="profile"),
    path('update/<int:id>', views.getUpdate, name="update"),
    path('delete/<int:id>', views.getDelete, name="delete"),
    path('register', views.getRegister, name="register"),
    path('category', views.getCategory.as_view(), name="category"),
    path('create/topic', views.createTopic, name="createTopic")
    #path('updatecat/<int:id>', views.updateTopics, name="updatecat"),

]
