import requests
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView, csrf_exempt
from rest_framework.permissions import IsAuthenticated
from Apps.Main.authentication import APIKeyAuthentication
from Apps.Main.serializers import GroupSerializer
from .models import LinkKey, TelegramUser
from .serializers import TelegramUserSerializer



class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    authentication_classes = [APIKeyAuthentication]


class TelegramUserCreateAPIView(generics.CreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    authentication_classes = [APIKeyAuthentication]
    
    def create(self, request, *args, **kwargs):
        userid = request.data.get('userid')
        if TelegramUser.objects.filter(userid=userid).exists():
            return Response({'detail': 'User with this userid already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)


class GenerateTelegramLinkView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def get(self, request, userid):
        try:
            tg_user = TelegramUser.objects.filter(userid=userid).first()
            key = LinkKey.objects.get(user=tg_user)
            return JsonResponse({'msg': 'Key already exists'})
        except TelegramUser.DoesNotExist:
            return JsonResponse({'msg': 'Telegram User does not exist'})
        except LinkKey.DoesNotExist:
            return JsonResponse({'msg': 'Key does not exist'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    def post(self, request):
        userid = request.data.get('userid')
        # print(request.data)
        if not userid:
            return JsonResponse({'error': 'userid is required'}, status=400)
        
        tg_user = TelegramUser.objects.filter(userid=userid).first()
        if not tg_user:
            return JsonResponse({'error': 'User not found'}, status=404)

        key, created = LinkKey.objects.get_or_create(user=tg_user, defaults={'token': uuid.uuid4().hex})
        key_str = key.token
        telegram_link = f"{settings.DOMAIN_SERVICE_URL}/telegram/link?token={key_str}"
        
        return JsonResponse({'link': telegram_link})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def link_telegram_user(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    
    token = request.GET.get('token')
    if not token:
        return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': 'Token not provided'}))

    try:
        user = request.user
        link_key = LinkKey.objects.get(token=token)
        tg_username = link_key.user.username

        usertg = TelegramUser.objects.get(username=tg_username)
        if usertg.user is None:
            usertg.user = user
            usertg.save()
            if link_key.id is not None:
                link_key.delete()
            return redirect(reverse('result_page', kwargs={'status': 'ok', 'message': 'Success'}))
        else:
            return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': 'User already linked'}))

    except LinkKey.DoesNotExist:
        return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': 'Invalid token'}))

    except TelegramUser.DoesNotExist:
        return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': 'Telegram user not found'}))

    except Exception as e:
        return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': str(e)}))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlink_telegram_user(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    try:
        user = request.user
        tg_user = TelegramUser.objects.get(user=user)
        tg_user.user = None
        tg_user.save()
        return redirect(reverse('result_page', kwargs={'status': 'ok', 'message': 'Success'}))
    except TelegramUser.DoesNotExist:
        return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': 'Telegram user not found'}))
    except Exception as e:
        return redirect(reverse('result_page', kwargs={'status': 'fail', 'message': str(e)}))


@api_view(['GET'])
# @authentication_classes([APIKeyAuthentication]) 
@permission_classes([IsAuthenticated])
def get_main_keyboard(request):
    user = request.user
    groups = user.groups.all()
    serializer = GroupSerializer(groups, many=True)
    keyboard = [
        [{"text": group['name']}] for group in serializer.data
    ]
    return Response({
        "keyboard": keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": True
    })
    
    
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        bot_server_url = settings.BOT_SERVER_URL 
        response = requests.post(bot_server_url, data=request.body, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error'}, status=response.status_code)
    else:
        return JsonResponse({'status': 'bad request'}, status=400)