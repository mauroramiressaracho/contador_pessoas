#PROJETO FACULDADE ESTACIO DE SÁ
#PROJETO CONTADOR DE PESSOAS, 4º SEMESTRE - MATERIA PYTHON IOT 4.0 INDUSTRIA
#CAMPO GRANDE MS - ALUNOS
# ALUNOS DO PROJETO - MAURO, CAIQUE, GABRIEL, GUSTAVO, YUNES, BELMANTE, WANDERLEY

# Importando a biblioteca OpenCV, que é usada para processar vídeos e imagens.
import cv2

# Definindo uma função para calcular o centro de um retângulo.
def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Inicializando a captura de vídeo a partir de um arquivo chamado 'entrada_loja.mp4'.
cap = cv2.VideoCapture('entrada_loja.mp4')

# Criando um objeto de subtração de fundo.
fgbg = cv2.createBackgroundSubtractorMOG2()

# Uma lista vazia para rastrear as detecções.
detects = []

# Configurando uma linha na imagem para contar as pessoas.
posL = 150
offset = 30

# Coordenadas para desenhar uma linha horizontal.
xy1 = (20, posL)
xy2 = (300, posL)

# Inicializando contadores para rastrear pessoas.
total = 0
up = 0
down = 0

# Loop principal que processa cada quadro do vídeo.
while 1:
    ret, frame = cap.read()  # Lendo um quadro do vídeo.

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertendo o quadro para escala de cinza.

    fgmask = fgbg.apply(gray)  # Aplicando subtração de fundo para destacar objetos em movimento.

    # Thresholding para criar uma imagem binária.
    retval, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

    # Aplicando operações de morfologia para melhorar a detecção.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)
    dilation = cv2.dilate(opening, kernel, iterations=8)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=8)

    # Desenhando linhas e contando objetos.
    cv2.line(frame, xy1, xy2, (255, 0, 0), 3)
    cv2.line(frame, (xy1[0], posL - offset), (xy2[0], posL - offset), (255, 255, 0), 2)
    cv2.line(frame, (xy1[0], posL + offset), (xy2[0], posL + offset), (255, 255, 0), 2)

    # Encontrando contornos na imagem.
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0

    # Loop para processar cada contorno encontrado.
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        if int(area) > 3000:
            centro = center(x, y, w, h)

            # Desenhando um retângulo e um círculo ao redor do objeto detectado.
            cv2.putText(frame, str(i), (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.circle(frame, centro, 4, (0, 0, 255), -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Verificando se o objeto está próximo da linha.
            if len(detects) <= i:
                detects.append([])

            if centro[1] > posL - offset and centro[1] < posL + offset:
                detects[i].append(centro)
            else:
                detects[i].clear()
            i += 1

    if i == 0:
        detects.clear()

    i = 0

    if len(contours) == 0:
        detects.clear()
    else:
        for detect in detects:
            for (c, l) in enumerate(detect):
                # Verificando se um objeto cruzou a linha.
                if detect[c - 1][1] < posL and l[1] > posL:
                    detect.clear()
                    up += 1
                    total += 1
                    cv2.line(frame, xy1, xy2, (0, 255, 0), 5)
                    continue

                if detect[c - 1][1] > posL and l[1] < posL:
                    detect.clear()
                    down += 1
                    total += 1
                    cv2.line(frame, xy1, xy2, (0, 0, 255), 5)
                    continue

                if c > 0:
                    cv2.line(frame, detect[c - 1], l, (0, 0, 255), 1)

    # Exibindo informações na tela.
    cv2.putText(frame, "TOTAL: " + str(total), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    cv2.putText(frame, "SAINDO: " + str(up), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, "ENTRANDO: " + str(down), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Exibindo o quadro com as informações.
    cv2.imshow("frame", frame)

    # Esperando até que a tecla 'q' seja pressionada para encerrar o programa.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberando a captura de vídeo e fechando todas as janelas.
cap.release()
cv2.destroyAllWindows()
