from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QWidget, QLabel,
    QComboBox, QApplication)
from PyQt5.QtWidgets import QMessageBox 

from PyQt5.QtCore import QCoreApplication, Qt 
Form, _ = uic.loadUiType("untitled.ui") 

import requests 
import json
import time
import pyperclip 
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal


class WorkThread(QThread):
      trigger = pyqtSignal()
      def __init__(self):
          super(WorkThread, self).__init__()
      
      def run(self):
          self.trigger.emit()


class WorkThread2(QThread):
      trigger2 = pyqtSignal()
      def __init__(self):
          super(WorkThread2, self).__init__()
      
      def run(self):
          self.trigger2.emit()


class WorkThread3(QThread):
      trigger3 = pyqtSignal()

      def __init__(self):
          super(WorkThread3, self).__init__()
      
      def run(self):
          self.trigger3.emit() 


class Ui(QtWidgets.QMainWindow, Form):
      def __init__(self):
         super(Ui,self).__init__()
         self.setupUi(self)

         self.comboBox.addItem('BITCOIN')  
         self.comboBox.addItem('ETHERIUM')  
         self.comboBox.addItem('Z-CASH')  
         self.comboBox.addItem('DASH') 
         self.comboBox.addItem('LITECOIN')
         self.comboBox.addItem('DOGECOIN') 
 
         self.label_4.setAlignment(Qt.AlignCenter)
         self.label_5.setAlignment(Qt.AlignCenter)
         self.label_6.setAlignment(Qt.AlignCenter)
         self.label_7.setAlignment(Qt.AlignCenter)
         self.pushButton.clicked.connect(self.check)
         self.pushButton_2.clicked.connect(self.paste)
         self.pushButton_3.clicked.connect(self.reset)

         self.comboBox.currentTextChanged.connect(self.set)
         self.comboBox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
         
      def set(self):
          get_text = self.comboBox.currentText() 
          self.label_2.setText('0 USD')
          self.label_3.setText('0 RUB')

          if get_text == 'BITCOIN':
             self.label.setText('0 BTC')
             self.label_6.setText('BTC')
          if get_text == 'ETHERIUM':
             self.label.setText('0 ETH')
             self.label_6.setText('ETH')
          if get_text == 'Z-CASH':
             self.label.setText('0 ZEC')
             self.label_6.setText('ZEC')
          if get_text == 'DASH':
             self.label.setText('0 DASH')
             self.label_6.setText('DASH')
          if get_text == 'LITECOIN':
             self.label.setText('0 LTC')
             self.label_6.setText('LTC')
          if get_text == 'DOGECOIN':
             self.label.setText('0 DOGE')
             self.label_6.setText('DOGE')

      def handle_trigger(self):
          #Диалоговое окно
          msg = QMessageBox()
          msg.setWindowTitle("ОШИБКА!")                     #Заголовок
          msg.setText("Пустое поле\nВведите адрес кошелька")#Текст
          msg.setIcon(QMessageBox.Warning)                  #Warning
          msg.exec_()
          self.frame_4.setStyleSheet('border: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(5, 54, 107, 255), stop:1 rgba(8, 96, 190, 255)); ') 
          self.label_7.setText('0%')


      def dialog(self):
          #Диалоговое окно
          msg = QMessageBox()
          msg.setWindowTitle("ОШИБКА!")                     #Заголовок
          msg.setText("Не правильный формат кошелька")      #Текст
          msg.setIcon(QMessageBox.Warning)                  #Warning
          msg.exec_()
          self.frame_4.setStyleSheet('border: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(5, 54, 107, 255), stop:1 rgba(8, 96, 190, 255)); ') 
          self.label_7.setText('0%')


      def dialog2(self):
          #Диалоговое окно
          msg = QMessageBox()
          msg.setWindowTitle("ОШИБКА!")                     #Заголовок
          msg.setText("Нет подключения к интернету")        #Текст
          msg.setIcon(QMessageBox.Warning)                  #Warning
          msg.exec_()
          self.frame_4.setStyleSheet('border: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(5, 54, 107, 255), stop:1 rgba(8, 96, 190, 255)); ') 
          self.label_7.setText('0%')


      #Функция для обработки ошибки
      def error(self,cod_error):     
          if cod_error == 503:
             self.weather = WorkThread3()
             self.weather.start()
             self.weather.trigger3.connect(self.dialog2)
          
          if cod_error == 501:
             self.weather = WorkThread2()
             self.weather.start()
             self.weather.trigger2.connect(self.dialog)
       
          if cod_error == 500:
             thread1 = Thread(target=self.signal, args=())
             thread1.start()


      #Дробление чисел
      def divider(self,number):
          number = str(number)      
          number = number.split('.')
          number = number[0]        
          
          if len(number) > 3:
             counter = 0            
             result=''              
             number = number[::-1]  
             for li in number:
                 counter += 1         
                 result = result + li 
                 if counter == 3:     
                    result = result +' '
                    counter = 0       
             result = result[::-1]    
             result = result.strip()   
          else: result = number 
          return result                
      

      #Курс криптовалюты к доллару/рублю
      def exchange(self,sum,cripta,currenci):
          url = 'https://min-api.cryptocompare.com/data/price?fsym='+cripta+'&tsyms='+currenci
          data = json.loads(requests.get(url=url).text)
          data = data[currenci]
          sum = float(sum)
          data = data * sum 
          data = float('{:.2f}'.format(data))
          result = self.divider(data)
          return result
      
      def urls(self,number_wallet):
          get_text = self.comboBox.currentText() 
          if get_text == 'BITCOIN': url = 'https://blockchain.info/balance?active='+number_wallet
          if get_text == 'ETHERIUM':url = 'https://api.ethplorer.io/getAddressInfo/'+number_wallet+'?apiKey=freekey'
          if get_text == 'DASH':    url = 'https://sochain.com/api/v2/get_address_balance/DASH/'+number_wallet
          if get_text == 'Z-CASH':  url = 'https://sochain.com/api/v2/get_address_balance/ZEC/'+number_wallet
          if get_text == 'LITECOIN':url = 'https://sochain.com/api/v2/get_address_balance/LTC/'+number_wallet
          if get_text == 'DOGECOIN':url = 'https://sochain.com/api/v2/get_address_balance/DOGE/'+number_wallet
          
          try:   
              get_info = requests.get(url=url,)
              result = json.loads(get_info.text)
              return result
          except: return 0

      def progress_bar(self):
          self.frame_4.setStyleSheet('border: 0px; background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.399 rgba(65, 229, 131, 255), stop:0.4 rgba(0, 76, 69,255)); ')
          self.label_7.setText('42%')
          number_wllet = self.lineEdit.text().strip()
          '''
          try:
              requests.get(url='https://blockchain.com',timeout=1) #Проверка подключения к инету
          except: 
                 self.error(503)#Ошибка - "Нет интернета"
                 return
          '''
          get_info = self.urls(number_wllet) 
          coin = 'BTC'
         
          try:
              get_text = self.comboBox.currentText()
            
              if get_text == 'BITCOIN': 
                 data = get_info[number_wllet]['final_balance']
                 coin = 'BTC'
              if get_text == 'ETHERIUM':
                 data = get_info['ETH']['balance']
                 coin = 'ETH'
              if get_text == 'DASH':    
                 data = get_info['data']['confirmed_balance']
                 coin = 'DASH'
              if get_text == 'Z-CASH':   
                 data = get_info['data']['confirmed_balance']
                 coin = 'ZEC'
              if get_text == 'LITECOIN':
                 data = get_info['data']['confirmed_balance']
                 coin = 'LTC'
              if get_text == 'DOGECOIN':
                 data = get_info['data']['confirmed_balance']
                 coin = 'DOGE'
          except: 
                 self.error(501)#Ошибка - "Не правильный формат данных"
                 return
    

          self.frame_4.setStyleSheet('border: 0px; background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.499 rgba(65, 229, 131, 255), stop:0.5 rgba(0, 76, 69,255)); ')
          self.label_7.setText('51%')
          if get_text == 'BITCOIN': data = data/100000000
          self.label.setText(str(data)+' '+coin) 
          time.sleep(0.2)

          self.frame_4.setStyleSheet('border: 0px; background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.699 rgba(65, 229, 131, 255), stop:0.7 rgba(0, 76, 69,255)); ')
          self.label_7.setText('73%')
          result = self.exchange(data,coin,'USD')
          self.label_2.setText(str(result)+' USD')

          self.frame_4.setStyleSheet('border: 0px;  background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.96 rgba(65, 229, 131, 255), stop:0.97 rgba(0, 76, 69,255)); ')
          self.label_7.setText('98%')
          result = self.exchange(data,coin,'RUB')
          self.label_3.setText(str(result)+' RUB')
          
          self.frame_4.setStyleSheet('border: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(5, 54, 107, 255), stop:1 rgba(8, 96, 190, 255)); ') 
          self.label_7.setText('0%')


      #Функция проверки количества монет в крипто-кошельке
      def check(self):
          if len(self.lineEdit.text()) == 0:
              self.error(500)
              return
          thread2 = Thread(target=self.progress_bar, args=())
          thread2.start()


      #Красный сигнал в поле
      def signal(self):
          sig = 0
          while True:
                sig += 1
                if sig == 4: 
                   self.lineEdit.setStyleSheet('color: rgb(16, 184, 255); background-color: rgb(7, 48, 89); border:1px solid rgb(130, 158, 189)')
                   break
                time.sleep(0.2)
                self.lineEdit.setStyleSheet('border:2px solid #ff0060; ')
                time.sleep(0.2) 
                self.lineEdit.setStyleSheet('border:1px solid rgb(130, 158, 189); background-color: rgb(7, 48, 89);')      
                
          self.weather = WorkThread()
          self.weather.start()
          self.weather.trigger.connect(self.handle_trigger)


      #Вставляем текст из буфера обмена в поле, атак же 4 начальных и 4 конечных символа
      def paste(self):
          self.lineEdit.setText(pyperclip.paste())
          bufer = pyperclip.paste()               

          if len(bufer) > 0:
             bufer = bufer.strip()    
             res1 = bufer[0:4]         
             res2 = bufer[-4:-1] + bufer[-1][0]
             self.label_4.setText(res1) 
             self.label_5.setText(res2) 


      #Удаляем текст с поля для ввода номера кошелька
      def reset(self):
          self.label_4.setText('0')
          self.label_5.setText('0')
          self.lineEdit.clear()
          self.set()


      

if __name__=="__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
   
