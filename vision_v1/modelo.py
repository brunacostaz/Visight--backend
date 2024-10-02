import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
 
 
modelo_carregado = load_model("keras_model.h5")
 
# Lista de classes 
classes_cifar10 = ['maçã', 'banana', 'manga', 'melancia', 'cereja', 
                   'morango', 'abacaxi', 'abacate', 'laranja', 'kiwi', 
                   'alface', 'uva', 'cenoura']
 
 
cap = cv2.VideoCapture(0)
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
 
  
    img_resized = cv2.resize(frame, (224, 224))
    img_array = img_to_array(img_resized) 
    img_array = img_array.reshape((1, 224, 224, 3))
 
  
    img_array = img_array / 255.0
 
  
    predicao = modelo_carregado.predict(img_array)
 
   
    classe_predita = np.argmax(predicao)
    nome_classe_predita = classes_cifar10[classe_predita]
 
   
    cv2.putText(frame, f"A classe predita: {nome_classe_predita}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
 
   
    cv2.imshow('Webcam', frame)
 
    # Saia do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
 
cap.release()
cv2.destroyAllWindows()