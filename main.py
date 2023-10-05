from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
import secrets, string, os
from PIL import Image, ImageDraw, ImageFont
from vk_maria.upload import Upload

current_file = os.path.realpath(__file__)
path = os.path.dirname(current_file)

class Generator:
    def generate_picture(self, balance):
        im = Image.open(path + '/picture.jpg')
        width, height = im.size
        draw = ImageDraw.Draw(im)
        fontsize = 20
        print(path)
        font = ImageFont.load_default() #ImageFont.truetype(path + "/font.ttf", fontsize)
        print(font)
        img_fraction = 0.25

        breakpoint = img_fraction * im.size[0]
        print(breakpoint)
        jumpsize = 80
        
        if int(balance) >= 10000000:
           balance = '%.2e' % int(balance)
           
        while True:
            if font.getsize(f"{balance}")[0] < breakpoint:
               fontsize += jumpsize
            else:
               jumpsize = jumpsize // 2
               fontsize -= jumpsize
            font = ImageFont.truetype(path + '/font.ttf', fontsize)
            if jumpsize <= 1:
               break

        draw.text((width / 2 + 600, height / 2 +150), f"{balance}", anchor="mm", font=font)

        alphabet = string.ascii_letters + string.digits
        pic_id = ''.join(secrets.choice(alphabet) for i in range(8))
        im.save(path + f'/{pic_id}.png')
        return pic_id

vk = Vk(access_token='vk1.a.brLhf7WQOIu7ntgNvYAWhW_kW-BgwiTjmQMcVo7vOrHTuOj8g8j7ZQnnEou2EnYHxg-G5qb6808avj_qv6JFDLIpdd9QjBngqiGVa-DAIchkv2mRHxwPNwgHFX9eu64gRgRkdjlLtsqGKMmnmXcUvyi_ay8juJCMSbfuNwtF9peWNE3QWFa8w2D-GVAtpGhA1nsnS_JZd6-gyM2cgDcLtQ')
upload = Upload(vk)
dp = Dispatcher(vk)

generator = Generator()

@dp.message_handler()
def send_welcome(event: types.Message):
    message = event.message.text.split()
    
    one = event.message.text.lower().replace("пример", "").replace(" ", "")
    
    if message[0].lower() == "пример":
       try:
           number = str(eval(one))
           photo = generator.generate_picture(number)
       
           image = types.FileSystemInputFile(path + "/" + photo + ".png")
           send = upload.photo(image)

           vk.messages_send(user_id=event.message.from_id, attachment=send)
       
           os.remove(path + "/" + photo + ".png")
       except:
       	event.answer("Произошла непредвиденная ошибка!")
       	try: 
       	    os.remove(path + "/" + photo + ".png")
       	except:
       		pass
       	

if __name__ == '__main__':
    print("Bot start!")
    dp.start_polling(debug=True)  