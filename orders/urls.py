from rest_framework import routers
from .views import CustomerViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet)
router.register(r"customers", CustomerViewSet)

urlpatterns = router.urls
