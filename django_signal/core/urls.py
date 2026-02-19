from django.urls import path
from .views import test_signal, test_rectangle, async_test_signal

urlpatterns = [
    path("test/", test_signal),
    path("rect/", test_rectangle),
    path("async_test/", async_test_signal),

]
