import pywhatkit
from datetime import datetime

telefone="+5581993519027"
minuto = datetime.now().minute+1
# Substitua '+558193519027' pelo número de telefone do destinatário, incluindo o código do país
pywhatkit.sendwhatmsg(telefone, "Olá, isso é uma mensagem automática!\n ",datetime.now().hour, minuto,7,True,5)



# Create your tests here.
