from rest_framework import routers
from .views import TodoViewSet

router = routers.SimpleRouter()
router.register(r'todo', TodoViewSet, basename='todo')
