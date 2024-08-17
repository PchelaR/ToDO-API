from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Todo
from .permissions import IsOwnerOrReadOnly
from .serializers import TodoSerializer, RegisterSerializer


class IndexView(TemplateView):
    template_name = 'todoapp/index.html'


class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'todo-list': reverse('todo-list', request=request),
            'todo-detail': reverse('todo-detail', request=request, kwargs={'pk': 1}),
            'register': reverse('register', request=request),
            'login': reverse('login', request=request),
            'logout': reverse('logout', request=request),
        })

class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    Просмотр и управление задачами пользователя.
    """
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает задачи, принадлежащие текущему аутентифицированному пользователю.
        """
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Устанавливает текущего пользователя в качестве владельца задачи при создании.
        """
        serializer.save(user=self.request.user)


class LoginView(APIView):
    """
    Логин пользователя с использованием сессии.
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Выход пользователя из системы.
    """

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
