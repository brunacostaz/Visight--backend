from tensorflow.keras.models import load_model

# Tente carregar o modelo
model = load_model('visao/keras_model.h5')


# Acessar a versão do Keras
print("Versão do Keras:", model.keras_version)

# Acessar a configuração do modelo
config = model.get_config()
print("Configuração do Modelo:", config)
