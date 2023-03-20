from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('regi/', views.register, name='register'),
    path('create_post/', views.create_post, name='create_post'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/',views.update,name='update'),
    path('<int:id>/like/', views.like_post, name='like_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('<int:id>/comment/',views.comment_view,name='comment_view'),
    path('<int:id>/like_comment/',views.like_comment,name='like_comment'),
    path('<int:id>/reply/', views.reply, name="reply"),
    path('<int:id>/like_reply/',views.like_reply,name='like_reply'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('delete_reply/<int:id>/', views.delete_reply, name='delete_reply'),
    path('post_view/<int:id>/',views.post_view,name='post_view')
    # path('update_post/',views.update_post,name='update_post')
    # path('<slug:post>/',views.comment_view,name="comment_view")
    # path('<int:id/reply/', views.reply_view, name='reply_comment'),
    # path('post/<int:id>/comment/', comment_view, name='add_comment')
    # path('add_comment_to_post/<int:pk>/', views.add_comment_to_post, name='add_comment_to_post')
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
