from django.urls import path

from accounts.views import CustomUserListView, CustomUserDeleteView, CustomUserDetailView, CustomUserCreateView, \
    CustomUserUpdateView, CustomUserSignUpView

urlpatterns = [
    path('', CustomUserListView.as_view(), name='custom_user_list'),
    path('<int:pk>', CustomUserDetailView.as_view(), name='custom_user_detail'),
    path('<int:pk>/delete', CustomUserDeleteView.as_view(), name='custom_user_delete'),
    path('<int:pk>/update', CustomUserUpdateView.as_view(), name='custom_user_update'),
    path('create/', CustomUserCreateView.as_view(), name='custom_user_create'),
    path('signup/', CustomUserSignUpView.as_view(), name='custom_user_signup'),

]