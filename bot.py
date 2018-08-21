# -*- coding: utf-8 -*-
import emoji
import telebot,os,time,speech_recognition as sr, pydub as p,googletrans,sqlite3,random,operator as oper
from telethon import TelegramClient
if os.path.isdir("tmp") == False:
        os.makedirs("tmp")
if os.path.isdir("downloads") == False:
        os.makedirs("downloads")
def recognize(name,message):
    global half,sound,num_mins
    r = sr.Recognizer()
    div=20
    t=0
    def get_audio(filename):
        global half,sound,num_mins
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        return audio
    def recogn(filename):
        global half,sound,num_mins
        audio=get_audio(filename)
        a=""
        if num_mins == 0:
                a=r.recognize_google(audio,None,"ru_RU")
        else:
                a+=r.recognize_google(audio,None,"ru_RU")
        half=0
        return a
    def cut(name):
        global half,sound,num_mins
        half=0
        sound=p.AudioSegment.from_file("downloads/"+name,format=name.split(".")[-1])
        if int(len(sound)/1000) > div:
            num_mins=int(len(sound)/1000/div)
            if int(len(sound)/1000) > num_mins* div:
                num_mins+=1
            for i in range(1,num_mins+1):
                if len(sound)/1000-div*i > 0 and i == num_mins:
                    half-=div
                    s=sound[half*1000:]
                    s.export("tmp/test"+str(i)+".wav",format="wav")
                else:
                    s=sound[half*1000:half*1000+div*1000]
                    s.export("tmp/test"+str(i)+".wav",format="wav")
                half+=div 
        half=0
        return half,sound,num_mins
    half=0
    sound=0
    num_mins=0
    t=name
    half,sound,num_mins=cut(t)
    a=""
    if num_mins !=0:
            for i in range(1,num_mins+1):
                try:
                    a+=recogn("tmp/test"+str(i)+".wav")
                except (Exception, ValueError,sr.UnknownValueError) as e:
                    print("Гугл не смог распознать аудио, возможно-это музыка без текста"+str(type(e)))
    else:
        name=name.split(".")
        name=name[0]+".wav"
        sound.export("downloads/"+name,format="wav")
        try:
            a=recogn("downloads/"+name)
        except (Exception, ValueError,sr.UnknownValueError) as e:
                print(name+": Ошибка: "+str(type(e)))
                bot.send_message(message.chat.id,"Не удалось распознать ваше сообщение")
    return a
n=0
token=os.environ["BOT_API_TOKEN"]
bot_username="@mrnaifbot"
global mats
mats=["гав"]
bot = telebot.AsyncTeleBot(token)
api_id=274851
api_hash="80ac08391d48da6eda25cca9d65480fe"
client = TelegramClient('session_name', api_id, api_hash)
client.start()
logger=telebot.logger
translator=googletrans.Translator()
markup=telebot.types.InlineKeyboardMarkup()
types=telebot.types
item_photo=types.InlineKeyboardButton("1",callback_data="1")
item_video=types.InlineKeyboardButton("2",callback_data="2")
item_game=types.InlineKeyboardButton("3",callback_data="3")
item_photo_2=types.InlineKeyboardButton("4",callback_data="4")
item_audio=types.InlineKeyboardButton("5",callback_data="5")
item_top=types.InlineKeyboardButton("6",callback_data="6")
markup.row(item_photo,item_video,item_game)
markup.row(item_photo_2,item_audio,item_top)
global markup2
markup2=telebot.types.InlineKeyboardMarkup()
item_1=types.InlineKeyboardButton("Отправлять сообщения",callback_data="01")
item_2=types.InlineKeyboardButton("Отправлять медиафайлы",callback_data="02")
item_3=types.InlineKeyboardButton("Отправлять стикеры и GIF",callback_data="03")
item_4=types.InlineKeyboardButton("Предпросмотр ссылок",callback_data="04")
item_5=types.InlineKeyboardButton("Готово",callback_data="05")
markup2.row(item_1,item_2)
markup2.row(item_3,item_4)
markup2.row(item_5)
#Описание переменных блокировки и других переменных
global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block,welcome
voice_block=0
text_block=0
photo_2_block=2
photo_block=0
game_block=0
video_block=0
top_block=0
welcome=0
#Хэндлеры
@bot.message_handler(content_types=["voice"])
def voice(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[1] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator" or message.chat.type != "supergroup")) and data_chat[1] != 2:
            if message.from_user.username != None:
                print(emoji.demojize("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил голосовое сообщение"))
            else:
                print(emoji.demojize("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил голосовое сообщение"))
            file_info = bot.get_file(message.voice.file_id).wait()
            downloaded_file = bot.download_file(file_info.file_path).wait()
            name=file_info.file_path.split("/")[-1]
            name=name.split(".")
            name=name[0]+".ogg"
            with open("downloads/"+name,"wb") as f:
                f.write(downloaded_file)
            a=recognize(name,message)
            if a != "":
                    bot.send_message(message.chat.id,a,reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id,"Не было распознано никакого текста",reply_to_message_id=message.message_id)
@bot.message_handler(content_types=["audio"])
def audio(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[1] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator" or message.chat.type != "supergroup")) and data_chat[1] != 2:
        if message.from_user.username != None:
            print(emoji.demojize("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил аудио"))
        else:
            print(emoji.demojize("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил аудио"))
        file_info = bot.get_file(message.audio.file_id).wait()
        downloaded_file = bot.download_file(file_info.file_path).wait()
        name=file_info.file_path.split("/")[-1]
        with open("downloads/"+name,"wb") as f:
            f.write(downloaded_file)
        a=recognize(name,message)
        if a != "":
            bot.send_message(message.chat.id,a,reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id,"Не было распознано никакого текста",reply_to_message_id=message.message_id)
@bot.message_handler(commands=["help","start"])
def help(message):
        register_group(message)
        print(emoji.demojize(message.from_user.first_name))
        bot.send_message(message.chat.id,
                         '''Привет, я Naif Bot!
Я умею распознавать речь и переводить текст на любой из языков мира!
Команды:
/help - выводит эту справку
/photo - отправляет кучу фото
/game - отправляет кучу музыки
/video - отправляет кучу видео
/translate - переводит текст. Полный список языков:
https://cloud.google.com/translate/docs/languages
/upload - загружает ваши файлы на сервер (они могут получены с помощью команд /photo, /audio и /video)
/clear_user_data - очищает все данные пользователей на сервере (нужно быть администратором)
/lock - изменяет настройки доступа к командам (нужно быть администратором)
Бот создан пользователем MrNaif (@MrNaif_bel)
Большое спасибо за идеи пользователю @IIAIIITET''')
@bot.message_handler(commands=["lock"])
def lock(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block,data
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat = i
    if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator" or message.chat.type != "supergroup" or message.from_user.id == 524253028:
        global back
        sent=bot.send_message(message.chat.id,"Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"1. Команда /photo - "+str(data_chat[3])+"\n"+"2. Команда /video - "+str(data_chat[5])+"\n"+"3. Команда /game - "+str(data_chat[4])+"\n"+"4. Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"5. Распознавание речи - "+str(data_chat[1])+"\n"+"6. Рейтинговая система и команда /top - "+str(data_chat[6]),reply_markup=markup)
        back=sent.wait()
    else:
        bot.delete_message(message.chat.id,message.message_id)
@bot.callback_query_handler(func=lambda sent: True)
def test(sent):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block,back,data
    global text,text2,msg,media,gif,links,markup2
    register_group(sent.message)
    for i in data:
        if i[0] == sent.message.chat.id:
            data_chat=i
    if bot.get_chat_member(sent.message.chat.id,sent.from_user.id).wait().status == "administrator" or bot.get_chat_member(sent.message.chat.id,sent.from_user.id).wait().status == "creator" or sent.message.chat.type != "supergroup" or sent.from_user.id == 524253028:
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        data_chat=list(data_chat)
        try:
            if sent.data == "1":
                if data_chat[3] == 0:
                    data_chat[3]=1
                elif data_chat[3] == 1:
                    data_chat[3]=2
                elif data_chat[3] == 2:
                    data_chat[3]=0
            if sent.data == "2":
                if data_chat[5] == 0:
                    data_chat[5]=1
                elif data_chat[5] == 1:
                    data_chat[5]=2
                elif data_chat[5] == 2:
                    data_chat[5]=0
            if sent.data == "3":
                if data_chat[4] == 0:
                    data_chat[4]=1
                elif data_chat[4] == 1:
                    data_chat[4]=2
                elif data_chat[4] == 2:
                    data_chat[4]=0
            if sent.data == "4":
                if data_chat[2] == 0:
                    data_chat[2]=1
                elif data_chat[2] == 1:
                    data_chat[2]=2
                elif data_chat[2] == 2:
                    data_chat[2]=0
            if sent.data == "5":
                if data_chat[1] == 0:
                    data_chat[1]=1
                elif data_chat[1] == 1:
                    data_chat[1]=2
                elif data_chat[1] == 2:
                    data_chat[1]=0     
            if sent.data == "6":
                if data_chat[6] == 0:
                    data_chat[6]=1        
                elif data_chat[6] == 1:
                    data_chat[6]=2
                elif data_chat[6] == 2:
                    data_chat[6]=0
            if sent.data in ["01","02","03","04"]:
                if sent.data == "01":
                    if msg == True:
                        msg=False
                    elif msg == False:
                        msg=True
                if sent.data == "02":
                    if media == True:
                        media=False
                    elif media == False:
                        media=True
                if sent.data == "03":
                    if gif == True:
                        gif=False
                    elif gif == False:
                        gif=True
                if sent.data == "04":
                    if links == True:
                        links=False
                    elif links == False:
                        links=True
                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройте ограничения для "+text+"(0-отключено,1-включено):"+"\n"+"Отправлять сообщения - "+str(int(msg))+"\n"+"Отправлять медиафайлы - "+str(int(media))+"\n"+"Отправлять стикеры и GIF - "+str(int(gif))+
                                 "\n"+"Предпросмотр ссылок - "+str(int(links)),reply_markup=markup2)
            if sent.data == "05":
                sentt=bot.send_message(sent.message.chat.id,"Успешно ограничил пользователя "+text+" на "+text2+" секунд!")
                restrict(sent.message)
            try:
                if sent.data in ["1","2","3","4","5","6"]:
                    bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"1. Команда /photo - "+str(data_chat[3])+"\n"+"2. Команда /video - "+str(data_chat[5])+"\n"+"3. Команда /game - "+str(data_chat[4])+"\n"+"4. Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"5. Распознавание речи - "+str(data_chat[1])+"\n"+"6. Рейтинговая система и команда /top - "+str(data_chat[6]),reply_markup=markup)
                    sql='''UPDATE chats SET voice_block = {0}, photo_2_block = {1}, photo_block = {2}, game_block = {3}, video_block = {4}, top_block = {5} WHERE chat_id = {6}'''.format(data_chat[1],data_chat[2],data_chat[3],data_chat[4],data_chat[5],data_chat[6],back.chat.id)
                    cursor.execute(sql)
                    connection.commit()
                    data=cursor.execute("SELECT * FROM chats").fetchall()
            except NameError:
                pass
        except NameError as e:
            print(e)
            print("Бот был перезапущен. Запустите команду /lock еще раз")
            bot.send_message(sent.message.chat.id,"Бот был перезапущен. Запустите команду /lock еще раз",reply_to_message_id=sent.message.message_id)
        connection.close()
@bot.message_handler(commands=["photo","video","game","translate","upload","clear_user_data","restrict"])
def ask(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    text=message.text
    text=text.split("/")[-1]
    if text.split("/")[-1] == "photo" or text.split("/")[-1] == "photo"+bot_username:
        if ((data_chat[3] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[3] != 2:
            sent=bot.send_message(message.chat.id,"Сколько фото отправить?")
            bot.register_next_step_handler(sent.wait(),photo)
        else:
            bot.delete_message(message.chat.id,message.message_id)
    if message.text.split("/")[-1] == "video" or message.text.split("/")[-1] == "video"+bot_username:
        if ((data_chat[5] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[5] != 2:
            sent=bot.send_message(message.chat.id,"Сколько видео отправить?")
            bot.register_next_step_handler(sent.wait(),video)
        else:
            bot.delete_message(message.chat.id,message.message_id)
    if message.text.split("/")[-1] == "game" or message.text.split("/")[-1] == "game"+bot_username:
        if ((data_chat[4] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[4] != 2:
            sent=bot.send_message(message.chat.id,"Сколько аудио отправить?")
            bot.register_next_step_handler(sent.wait(),game)
        else:
            bot.delete_message(message.chat.id,message.message_id)
    if message.text.split("/")[-1] == "translate" or message.text.split("/")[-1] == "translate"+bot_username:
        sent=bot.send_message(message.chat.id,"Введите сообщение для перевода:")
        bot.register_next_step_handler(sent.wait(),translate_ask)
    if message.text.split("/")[-1] == "upload" or message.text.split("/")[-1] == "upload"+bot_username:
        sent=bot.send_message(message.chat.id,"Пришлите файл для загрузки на сервер:")
        bot.register_next_step_handler(sent.wait(),upload)
    if message.text.split("/")[-1] == "clear_user_data" or message.text.split("/")[-1] == "clear_user_data"+bot_username:
        if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator"  or message.chat.type != "supergroup":
            sent=bot.send_message(message.chat.id,"Вы уверены, что хотите очистить данные пользователей?(Варианты ответов: да и нет)")
            bot.register_next_step_handler(sent.wait(),clear_user_data)
        else:
            bot.delete_message(message.chat.id,message.message_id)
    if message.text.split("/")[-1] == "restrict" or message.text.split("/")[-1] == "restrict"+bot_username:
        if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator" :
            sent=bot.send_message(message.chat.id,"Кого вы хотите ограничить?")
            bot.register_next_step_handler(sent.wait(),restrict_ask)
        else:
            bot.delete_message(message.chat.id,message.message_id)
def game(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block
    text=message.text
    try:
        text=int(text)
        max_=message.text
        max_=int(max_)
        for i in os.listdir("user_audio/"):
            if max_ > 0:
                with open("user_audio/"+i,"rb") as v:
                    bot.send_voice(message.chat.id,v,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        for i in os.listdir("ogg/"):
            if max_ > 0:
                with open("ogg/"+i,"rb") as v:
                    bot.send_voice(message.chat.id,v,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        bot.send_message(message.chat.id, "Все отправлено: аудио")
        print("Все отправлено: аудио")
    except ValueError:
        print("Введите цифры")
        bot.send_message(message.chat.id,"Введите цифры",reply_to_message_id=message.message_id)
def photo(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block
    text=message.text
    try:
        text=int(text)
        max_=message.text
        max_=int(max_)
        for i in os.listdir("user_photo/"):
            if max_ > 0:
                with open("user_photo/"+i,"rb") as p:
                    bot.send_photo(message.chat.id,p,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        for i in os.listdir("фото_робопарк/"):
            if i.split(".")[-1] == "jpg" and max_ > 0:
                with open("фото_робопарк/"+i,"rb") as p:
                    bot.send_photo(message.chat.id,p,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        for i in os.listdir("2018-05/"):
            if i.split(".")[-1] == "png" and max_ > 0:
                with open("2018-05/"+i,"rb") as p:
                    bot.send_photo(message.chat.id,p,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        for i in os.listdir("2018-04/"):
            if i.split(".")[-1] == "png" and max_ > 0:
                with open("2018-04/"+i,"rb") as p:
                    bot.send_photo(message.chat.id,p,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        bot.send_message(message.chat.id, "Все отправлено: фото")
        print("Все отправлено: фото")
    except ValueError:
        print("Введите цифры")
        bot.send_message(message.chat.id,"Введите цифры",reply_to_message_id=message.message_id)
def video(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,top_block
    text=message.text
    try:
        text=int(text)
        max_=message.text
        max_=int(max_)
        '''for i in os.listdir("user_video/"):
            if max_ > 0:
                with open("user_video/"+i,"rb") as vid:
                    vid.seek(0, os.SEEK_END)
                    size=vid.tell()
                    if size < 50000000:
                        vid.seek(0)
                        bot.send_video(message.chat.id,vid,None,timeout=2000)
                        print("Удачно отправлено:",i)
                        time.sleep(5)
                    else:
                        print(i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                        bot.send_message(message.chat.id,i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                max_-=1'''

        for i in os.listdir("фото_робопарк/"):
            if i.split(".")[-1] == "mp4" and max_ > 0:
                with open("фото_робопарк/"+i,"rb") as vid:
                    vid.seek(0, os.SEEK_END)
                    size=vid.tell()
                    if size < 50000000:
                        vid.seek(0)
                        bot.send_video(message.chat.id,vid,None,timeout=2000)
                        print("Удачно отправлено:",i)
                        time.sleep(5)
                    else:
                        print(i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                        bot.send_message(message.chat.id,i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                max_-=1
        for i in os.listdir("2018-05/"):
            if i.split(".")[-1] == "mp4" and max_ > 0:
                with open("2018-05/"+i,"rb") as vid:
                    bot.send_video(message.chat.id,vid,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        for i in os.listdir("2018-04/"):
            if i.split(".")[-1] == "mp4" and max_ > 0:
                with open("2018-04/"+i,"rb") as vid:
                    bot.send_video(message.chat.id,vid,None)
                    print("Удачно отправлено:",i)
                    time.sleep(3)
                max_-=1
        bot.send_message(message.chat.id, "Все отправлено: видео")
        print("Все отправлено: видео")
    except ValueError:
        print("Введите цифры")
        bot.send_message(message.chat.id,"Введите цифры",reply_to_message_id=message.message_id)
def translate_ask(message):
    global text
    text=message.text
    sent=bot.send_message(message.chat.id,"На какой язык перевести?(Например, Русcкий - ru, английский - en) Список всех языков: https://cloud.google.com/translate/docs/languages")
    bot.register_next_step_handler(sent.wait(),translate)
def translate(message):
    global text
    try:
        a=translator.translate(text,dest=message.text).text
        bot.send_message(message.chat.id,a,reply_to_message_id=message.message_id)
        if message.from_user.username != None:
            print(emoji.demojize("@"+message.from_user.username+"("+message.from_user.first_name+"): "+a))
        else:
            print(emoji.demojize("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+a))
    except ValueError:
        bot.send_message(message.chat.id,"Нет такого языка, попробуйте еще раз!",reply_to_message_id=message.message_id)
@bot.message_handler(commands=["document"])
def doc(message):
    for i in os.listdir("user_docs/"):
        with open("user_docs/"+i,"rb") as f:
            bot.send_document(message.chat.id,f)
@bot.message_handler(content_types=["new_chat_members"])
def register_group(message):
    global data,welcome
    r=0
    for i in data:
        if i[0] == message.chat.id:
            r=1
    if r == 0:
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        sql='''INSERT INTO chats(chat_id,voice_block,photo_2_block,photo_block,game_block,video_block,top_block,welcome,name)
              VALUES(?,?,?,?,?,?,?,?,?)'''
        cursor.execute(sql,(message.chat.id,0,2,0,0,0,0,welcome,message.chat.title))
        connection.commit()
        data=cursor.execute("SELECT * FROM chats").fetchall()
        connection.close()
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    welcome=data_chat[7]
    if message.content_type == "new_chat_members":
            if welcome == "0" or welcome == 0 or welcome == None:
                bot.send_message(message.chat.id, "Добро пожаловать в "+message.chat.title+"!")
            else:
                bot.send_message(message.chat.id, welcome)
@bot.message_handler(commands=["top"])
def top(message):
    global data,users,top_block
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[6] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[6] != 2:
        tmp={}
        for i in users:
            if i[0] == message.chat.id:
                tmp[i[1]]=i[2]
        top=sorted(tmp.items(),key=oper.itemgetter(1))
        top=top[::-1]
        for i in range(0,len(top)):
            if i > 9:
                top.pop(i)
        a=""
        iii=1
        for i in range(0,len(top)):
            if bot.get_chat_member(message.chat.id,top[i][0]).wait().user.username != None:
                a+=str(iii)+". "+str(bot.get_chat_member(message.chat.id,int(top[i][0])).wait().user.username)+": "+str(top[i][1])+"\n"
            else:
                a+=str(iii)+". "+str(bot.get_chat_member(message.chat.id,int(top[i][0])).wait().user.first_name)+": "+str(top[i][1])+"\n"
            iii+=1
        if top != {}:
            bot.send_message(message.chat.id,"Топ участников:\n"+a)
        else:
            bot.send_message(message.chat.id,"Пока что топа нет!")
@bot.message_handler(commands=["leave"])
def leave(message):
        if message.from_user.id == 524253028:
                bot.send_message(message.chat.id,"Прощайте!")
                bot.leave_chat(message.chat.id)
                
@bot.message_handler(commands=["my_rating"])
def my_rating(message):
        register_group(message)
        for i in data:
            if i[0] == message.chat.id:
                data_chat=i
        for i in users:
                if i[0] == message.chat.id and i[1] == message.from_user.id:
                        rating=i[2]
        if ((data_chat[6] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[6] != 2:
            try:
                    bot.send_message(message.chat.id,rating,reply_to_message_id=message.message_id)
            except UnboundLocalError:
                    bot.send_message(message.chat.id,"У вас пока нет рейтинга!",reply_to_message_id=message.message_id)
def restrict_ask(message):
    global text,markup2
    text=message.text
    sent=bot.send_message(message.chat.id,"На сколько ограничить?")
    bot.register_next_step_handler(sent.wait(),restrict_ask_2)
def restrict_ask_2(message):
    global text,text2,msg,media,gif,links,markup2
    text2=message.text
    msg=True
    media=True
    gif=True
    links=True
    bot.send_message(message.chat.id,"Настройте ограничения для "+text+"(0-применить,1-не применять):"+"\n"+"Отправлять сообщения - "+str(int(msg))+"\n"+"Отправлять медиафайлы - "+str(int(media))+"\n"+"Отправлять стикеры и GIF - "+str(int(gif))+
                     "\n"+"Предпросмотр ссылок - "+str(int(links)),reply_markup=markup2)
def restrict(message):
    global text,text2,msg,media,gif,links
    bot.restrict_chat_member(message.chat.id,client.get_entity(text).id,time.time()+float(text2),msg,media,gif,links)
@bot.message_handler(content_types=["left_chat_member"])
def clear_part_of_DB(message):
    global data,users,warns
    data,users,warns=get_data()
    r=0
    for i in users:
        if i[0] == message.chat.id and i[1] == message.from_user.id:
            r=1
    if r == 1:
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        sql='''DELETE FROM users WHERE chat_id = {0} AND user_id = {1}'''.format(message.chat.id,message.from_user.id)
        cursor.execute(sql)
        connection.commit()
        connection.close()
@bot.message_handler(commands=["set_welcome_message"])
def set_welcome_ask(message):
        global data,users,users_user,top_block
        if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator":
            sent=bot.send_message(message.chat.id,"Введите сообщение для новых участников:")
            bot.register_next_step_handler(sent.wait(),set_welcome)
        else:
            bot.send_message(message.chat.id,"Извини, это команда только для админов. Ты не админ",reply_to_message_id=message.message_id)
def set_welcome(message):
        global data,welcome
        welcome=message.text
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        sql="UPDATE chats SET welcome = \"{0}\" WHERE chat_id = {1}".format(welcome,message.chat.id)
        cursor.execute(sql)
        connection.commit()
        data=cursor.execute("SELECT * FROM chats").fetchall()
        connection.close()
        bot.send_message(message.chat.id,"Успешно изменено!")
def upload(message):
    if message.content_type == "photo":
        file_info = bot.get_file(message.photo[2].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        with open("user_photo/"+name,"wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id,"Успешно отправлено!",reply_to_message_id=message.message_id)
    elif message.content_type == "audio":
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        with open("user_audio/"+name,"wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id,"Успешно отправлено!",reply_to_message_id=message.message_id)
    elif message.content_type == "voice":
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        name=name.split(".")
        name=name[0]+".ogg"
        with open("user_audio/"+name,"wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id,"Успешно отправлено!",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Формат файла не был распознан!",reply_to_message_id=message.message_id)
def clear_user_data(message):
    if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator" or message.chat.type != "supergroup":
        if message.text == "да":
            for i in os.listdir("user_photo"):
                os.remove("user_photo/"+i)
            for ii in os.listdir("user_video"):
                os.remove("user_video/"+ii)
            for iii in os.listdir("user_audio"):
                os.remove("user_audio/"+iii)
            bot.send_message(message.chat.id,"Успешно очищено!",reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id,"Нет так нет, ничего не было очищено.",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Извини, это команда только для админов. Ты не админ",reply_to_message_id=message.message_id)
@bot.message_handler(content_types=["photo"])
def repeat_all_photos(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[2] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[2] != 2:
        with open("image.jpg","rb") as ph:
            a=bot.send_photo(message.chat.id,ph,None)
            if message.from_user.username != None:
                print(emoji.demojize("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил фото"))
            else:
                print(emoji.demojize("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил фото"))
    else:
        if message.from_user.username != None:
                print(emoji.demojize("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил фото"))
        else:
                print(emoji.demojize("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил фото"))
@bot.message_handler(content_types=["text"])
def rate_check(message):
    global data,users,users_user,top_block,mats,warns
    register_group(message)
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[6] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).wait().status == "creator")) and data_chat[6] != 2:
        r=0
        rating=0
        if message.reply_to_message != None:
            if message.from_user.username != message.reply_to_message.from_user.username:
                msg=list(message.text)
                res=0
                for i in msg:
                    if i == "+":
                        res+=1
                    if i == "-":
                        res-=1
                for i in users:
                    if i[0] == message.chat.id and i[1] == message.reply_to_message.from_user.id:
                        r=1
                if r == 0:
                    connection=sqlite3.connect("base.db")
                    cursor=connection.cursor()
                    sql='''INSERT INTO users(chat_id,user_id,rating,name)
                    VALUES(?,?,?,?)'''
                    cursor.execute(sql,(message.chat.id,message.reply_to_message.from_user.id,res,message.reply_to_message.from_user.first_name))
                    connection.commit()
                    data=cursor.execute("SELECT * FROM chats").fetchall()
                    users=cursor.execute("SELECT * FROM users").fetchall()
                    connection.close()
                if r == 1:
                    for i in users:
                            if i[0] == message.chat.id and i[1] == message.reply_to_message.from_user.id:
                                users_user=i
                    connection=sqlite3.connect("base.db")
                    cursor=connection.cursor()
                    sql='''UPDATE users SET rating = {0} WHERE chat_id = {1} AND user_id = {2}'''.format(users_user[2]+res,message.chat.id,message.reply_to_message.from_user.id)
                    cursor.execute(sql)
                    connection.commit()
                    data=cursor.execute("SELECT * FROM chats").fetchall()
                    users=cursor.execute("SELECT * FROM users").fetchall()
                    connection.close()
                            
    text=message.text
    for i in mats:
        if i in text:
            bot.delete_message(message.chat.id,message.message_id)
            bot.send_message(message.chat.id,message.from_user.first_name+", не материться!")
            data,users,warns=get_data()
            r=0
            for i in warns:
                if i[0] == message.chat.id and i[1] == message.from_user.id:
                    r=1
                    warns_warn=i
            connection=sqlite3.connect("base.db")
            cursor=connection.cursor()
            if r == 0:
                sql='''INSERT INTO warnings(chat_id,user_id,warn_num,name)
                    VALUES(?,?,?,?)'''
                cursor.execute(sql,(message.chat.id,message.from_user.id,1,message.from_user.first_name))
                connection.commit()
                connection.close()
                warn_n=1
            if r == 1:
                sql='''UPDATE warnings SET warn_num = {0} WHERE chat_id = {1} AND user_id = {2}'''.format(warns_warn[2]+1,message.chat.id,message.from_user.id)
                cursor.execute(sql)
                connection.commit()
                connection.close()
                warn_n=warns_warn[2]+1
            if warn_n == 3:
                if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status != "administrator" and bot.get_chat_member(message.chat.id,message.from_user.id).wait().status != "creator":
                        bot.restrict_chat_member(message.chat.id,message.from_user.id,time.time()+86400,False,False,False,False)
                        bot.send_message(message.chat.id,message.from_user.first_name+", вы ограничены(только чтение) на день! Ещё одно предупреждение и бан!")
                else:
                        bot.send_message(message.chat.id,message.from_user.first_name+", Вы админ, а нарушаете правила! Плохо, но я ничего сделать не могу!")
            if warn_n == 4:
                if bot.get_chat_member(message.chat.id,message.from_user.id).wait().status != "administrator" and bot.get_chat_member(message.chat.id,message.from_user.id).wait().status != "creator":
                        bot.kick_chat_member(message.chat.id,message.from_user.id,29)
                        bot.send_message(message.chat.id,message.from_user.first_name+" был забанен!")
                else:
                        bot.send_message(message.chat.id,message.from_user.first_name+", Вы админ, а нарушаете правила! Плохо, но я ничего сделать не могу!")
                connection=sqlite3.connect("base.db")
                cursor=connection.cursor()
                sql='''DELETE FROM warnings WHERE chat_id = {0} AND user_id = {1}'''.format(message.chat.id,message.from_user.id)
                cursor.execute(sql)
                connection.commit()
                connection.close()
def get_data():
        global welcome
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        data=cursor.execute("SELECT * FROM chats").fetchall()
        users=cursor.execute("SELECT * FROM users").fetchall()
        warns=cursor.execute("SELECT * FROM warnings").fetchall()
        connection.close()
        return data,users,warns
global data,users,warns,users_user
users_user=0
data,users,warns=get_data()
if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(none_stop=True)
        except (Exception,ConnectionResetError,ConnectionError) as e:
            print("Ошибка!!!!\n",str(e))
            logger.error(e)
            time.sleep(15)
