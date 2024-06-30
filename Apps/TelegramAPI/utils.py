from .models import TelegramUser
import io
# from aiogram from Bot

# def save_user_data(message):
#     user_id = message.id
#     photos = bot.get_user_profile_photos(user_id)
#     if photos.photos:
#         photo = photos.photos[0]  # Берем только первую фотографию
#         file_id = photo[0].file_id
#         file_info = bot.get_file(file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
                
#         user_info = bot.get_chat_member(message.id, user_id)
#         username = user_info.user.username
#         first_name = user_info.user.first_name
#         last_name = user_info.user.last_name
        
#         with io.BytesIO() as byte_stream:
#             byte_stream.write(downloaded_file)
#             byte_stream.seek(0)
#             byte_data = byte_stream.read()
        
#         # print(byte_data)
        
#         telegram_user, created = TelegramUser.objects.get_or_create(
#             userid=user_id,
#             defaults={
#                 'username': username,
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'image_data': byte_data
#             }
#         )
#         if not created:
#             telegram_user.image_data = downloaded_file
#             telegram_user.save()