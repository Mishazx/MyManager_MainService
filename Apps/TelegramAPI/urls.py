from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenerateTelegramLinkView, get_main_keyboard, link_telegram_user, TelegramUserCreateAPIView, TelegramUserViewSet, unlink_telegram_user, webhook

router = DefaultRouter()
router.register(r'telegram_users', TelegramUserViewSet, basename='telegramuser')

urlpatterns = [
    path('', include(router.urls)),
    path('create_user/', TelegramUserCreateAPIView.as_view(), name='create-user'),
    path('generate_link/', GenerateTelegramLinkView.as_view(), name='generate-link'),
    path('link/', link_telegram_user, name='link'),
    path('unlink/', unlink_telegram_user, name='unlink'),
    path('get_main_keyboard/', get_main_keyboard, name='get_main_keyboard'),
    path('webhook/', webhook, name='webhook'),
]
