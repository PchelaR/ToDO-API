from django.urls import path, include
from .routers import router
from .views import RegisterView, LoginView, LogoutView, IndexView, APIRootView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/v1/', APIRootView.as_view(), name='api-root'),
    path('api/v1/todo-auth/login/', LoginView.as_view(), name='login'),
    path('api/v1/todo-auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/todo-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
]
