from google.cloud import vision
import io
import cv2

#CÓDIGO TESTE API

# Inicializa o cliente da API
client = vision.ImageAnnotatorClient()

def detect_labels(image_path):
    """Detecta labels em uma imagem"""
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(f'{response.error.message}')

def capture_image():
    """Captura uma imagem da webcam e salva no disco"""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        cap.release()
        cv2.destroyAllWindows()
        return 'captured_image.jpg'
    else:
        cap.release()
        cv2.destroyAllWindows()
        raise Exception("Não foi possível capturar a imagem.")

# Captura a imagem
image_path = capture_image()

# Detecta labels na imagem capturada
detect_labels(image_path)
