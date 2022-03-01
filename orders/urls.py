from rest_framework import routers
from .views import CustomerViewSet, OrderViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = router.urls
