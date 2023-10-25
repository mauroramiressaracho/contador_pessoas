#PROJETO FACULDADE ESTACIO DE SÁ
#PROJETO CONTADOR DE PESSOAS, 4º SEMESTRE - MATERIA PYTHON IOT 4.0 INDUSTRIA
#CAMPO GRANDE MS - ALUNOS
# ALUNOS DO PROJETO - MAURO, CAIQUE, GABRIEL, GUSTAVO, YUNES, BELMANTE, WANDERLEY

# Importando as bibliotecas
import cv2
import csv
import datetime
import banco as bd

# Função para calcular o centro de um retângulo
def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Inicialização da captura de vídeo a partir de um arquivo
cap = cv2.VideoCapture('entrada_loja.mp4')

# Inicialização do algoritmo de subtração de fundo
fgbg = cv2.createBackgroundSubtractorMOG2()

# Lista para armazenar detecções
detects = []

# Inicialização de contadores
total = 0
up = 0
down = 0

# Abre um arquivo CSV para escrita e escreve o cabeçalho
with open('registro_entradas.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow('Data e Hora')
   
# Loop principal do programa
while 1:
    ret, frame = cap.read()

    # Posição da linha de referência e deslocamento para a detecção
    posL = 30
    offset = 20

    # Coordenadas para desenhar a linha de referência diagonal para a direita    
    xy1 = (150, 25)  # Canto superior direito (x, y)
    xy2 = (150, 180)  # Canto inferior esquerdo (x, y)

    # Conversão do quadro para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicação do algoritmo de subtração de fundo
    fgmask = fgbg.apply(gray)

    # Limiarização da imagem
    retval, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

    # Criação de um kernel para operações de morfologia
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Aplicação de operações morfológicas
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)
    dilation = cv2.dilate(opening, kernel, iterations=8)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=8)

    # Desenha linhas de referência na imagem
    cv2.line(frame, xy1, xy2, (255, 0, 0), 3)  # Linha diagonal para a direita
    cv2.line(frame, (xy1[0] - offset, xy1[1]), (xy2[0] - offset, xy2[1]), (255, 255, 0), 2)  # Linha esquerda paralela à diagonal
    cv2.line(frame, (xy1[0] + offset, xy1[1]), (xy2[0] + offset, xy2[1]), (255, 255, 0), 2)  # Linha direita paralela à diagonal


    # Encontra contornos na imagem
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0 
    sensibilidade = None   
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        sensibilidade = str(area)
        if int(area) > 2200:
            centro = center(x, y, w, h)
            
            # Desenha informações sobre os objetos detectados
            cv2.putText(frame, str(i), (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.circle(frame, centro, 4, (0, 0, 255), -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Armazena as detecções na lista 'detects'
            if len(detects) <= i:
                detects.append([])              
                
            if centro[1] > posL - offset and centro[1] < posL + offset:
                detects[i].append(centro)                
            else:
                detects[i].clear()
            i += 1

    #Se a imagem tiver toda preta, zera o contorno
    if i == 0:
        detects.clear()
    i = 0    
    if len(contours) == 0:
        detects.clear()
    else:        
        for detect in detects:            
            for (c, l) in enumerate(detect):                
                print()
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
                    
                    # Obtém a data e hora atual
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Abre o arquivo CSV e escreve a data e hora
                    #with open('registro_entradas.csv', mode='a', newline='') as file:
                       #writer = csv.writer(file)
                       #writer.writerow([formatted_datetime])
                    
                    # Insere no Banco Azure na Nuvem   
                    bd.insere_dados(formatted_datetime)
                        
                    continue

                if c > 0:
                    cv2.line(frame, detect[c - 1], l, (0, 0, 255), 1)

    # Exibe informações sobre o número total de objetos detectados
    cv2.putText(frame, "TOTAL: " + str(total), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    cv2.putText(frame, "SAINDO: " + str(up), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, "ENTRANDO: " + str(down), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)   
    #cv2.putText(frame, sensibilidade, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Exibe a imagem com as informações
    cv2.imshow("Contador Pessoas em Claudio!", frame)
    cv2.imshow("Frame", dilation)
    #cv2.imshow("opening", opening)
    #cv2.imshow("closing", closing)

    # Espera até que a tecla 'q' seja pressionada para encerrar o programa
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()
