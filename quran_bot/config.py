# Use environment variables or a secure configuration file for credentials
MYSQL_HOST = 'localhost'
MYSQL_USER = 'toxir'
MYSQL_PASSWORD = '1234'

""" 
@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    if message.photo:  # Check if the message contains a photo
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('photos/{}.jpg'.format(message.message_id), 'wb') as new_file:
            new_file.write(downloaded_file)
        # Sending the received photo back to the user
        bot.send_photo(message.chat.id, file_id)
    elif message.video:  # Check if the message contains a video
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('videos/{}.mp4'.format(message.message_id), 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, 'Video received!')
"""