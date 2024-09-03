import cv2  # Importa a biblioteca OpenCV para processamento de imagens e visão computacional.

# Carregando os classificadores Haar Cascade pré-treinados para faces e sorrisos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Esse classificador é usado para detectar rostos na imagem.

smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
# Esse classificador é usado para detectar sorrisos dentro de regiões faciais.

# Carregar a imagem
image = cv2.imread("caminho.jpg")
# Carrega a imagem do caminho especificado. O OpenCV suporta vários formatos de imagem.

# Converter a imagem para escala de cinza
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Converte a imagem carregada para escala de cinza, pois a detecção de objetos é mais eficiente em imagens em tons de cinza.

# Detectar faces na imagem
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
# Detecta faces na imagem usando o classificador Haar Cascade:
# - scaleFactor: Especifica quanto a imagem é reduzida em cada escala. Um valor de 1.1 significa uma redução de 10%.
# - minNeighbors: Define o número de vizinhos que cada retângulo candidato deve ter para ser mantido. Mais vizinhos resultam em menos detecções, mas mais precisas.
# - minSize: Define o tamanho mínimo da face a ser detectada.

# Para cada rosto detectado, verificamos a presença de sorrisos
for (x, y, w, h) in faces:  # Loop através de cada face detectada.
    # Definir a região de interesse (ROI) para detectar o sorriso
    roi_gray = gray_image[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]
    # Define a Região de Interesse (ROI) onde o sorriso será detectado. A ROI é a área da imagem correspondente ao rosto detectado.

    smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=15, minSize=(25, 25))
    # Detecta sorrisos dentro da região facial (ROI) usando o classificador de sorrisos:
    # - scaleFactor: Aqui está definido como 1.8 para ser mais rigoroso na detecção de sorrisos.
    # - minNeighbors: Um valor mais alto (15) é usado para minimizar falsos positivos na detecção de sorrisos.
    # - minSize: Define o tamanho mínimo que um sorriso deve ter para ser detectado.

    if len(smiles) > 0:  # Se ao menos um sorriso for detectado dentro da ROI:
        cv2.putText(image, "Sorriso detectado", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        # Adiciona o texto "Sorriso detectado" acima da face, com a cor verde (0, 255, 0) indicando uma detecção positiva.
    else:
        cv2.putText(image, "Sem sorriso", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        # Adiciona o texto "Sem sorriso" acima da face, com a cor vermelha (0, 0, 255) indicando que nenhum sorriso foi detectado.

    # Desenhar um retângulo em torno da face
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Desenha um retângulo azul ao redor de cada face detectada.

# Exibir a imagem com as detecções
cv2.imshow('Deteccao de Face e Sorriso', image)
# Exibe a imagem em uma nova janela intitulada 'Deteccao de Face e Sorriso', mostrando as detecções feitas.

cv2.waitKey(0)
# Aguarda que uma tecla seja pressionada para fechar a janela. O '0' significa que a espera é indefinida.

cv2.destroyAllWindows()
# Fecha todas as janelas abertas pelo OpenCV.
