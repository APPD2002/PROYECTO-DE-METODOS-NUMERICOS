#Proyecto elaborado por estudiantes de 3ero de ITIN de la ESPE sede Santo Domingo de los Tsachilas
#Elaborado en python 3.10
#INTEGRANTES: Josue Espinoza, Darwin Toapanta, Angel Patiño y Jeffry Villegas. 
#Tester: Jericko
from ast import While
import colorama
from types import NoneType
import numpy as np 
import time
import speech_recognition as sr #Reconocimiento de voz
import copy
import pyttsx3 #reconimiento de texto a voz Libreria
engine = pyttsx3.init()
volumen = engine.getProperty('volume')
engine.setProperty('volume', 1) #Volumen alto y bajo 1 / 0
engine.setProperty('rate',125) #Velocidad de Voz
#-----------------------------------------MIni base de datos-----------------------------------------------
parametros = {'&':0,'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9,
              'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'ñ':15, 'o':16, 'p':17, 'q':18, 'r':19, 's':20
              , 't':21, 'u':22, 'v':23, 'w':24, 'x':25, 'y':26, 'z':27, ' ':28, ',':29,'.':30,'1':31
              ,'2':32,'3':33,'4':34,'5':35,'6':36,'7':37,'8':38,'9':39,'0':40,'-':41,'/':42,'+':43,'*':44,'A':45
              ,'B':46,'C':47,'D':48,'E':49,'F':50,'G':51,'H':52,'I':53,'J':54,'K':55,'L':56,'M':57,'N':58,'Ñ':59,'O':60,'P':61
              ,'Q':62,'R':63,'S':64,'T':65,'U':66,'V':67,'W':68,'X':69,'Y':70,'Z':71, 'á':72, 'é':73, 'í':74, 'ó':75, 'ú':76, '¿':77,'?':78,'¡':79, '!':80, ':':81}

def  rellenador(relleno,ARellenar):
    """Rellena con 28's si el largo de la lista no es divisible para el parametro relleno hasta que sea así.
    Parametros:
    relleno= entero (Int)
    ARellenar= Lista de una dimensión (list)
    La Función no devuelve nada, sino que edita la lista que se da como parametro.""" 
    if len(ARellenar)%relleno!=0: #Si el largo de la lista no es divisible para el relleno, agrega espacios (28) hasta que sea asi.
        for i in range((len(ARellenar)//relleno +1)*relleno -len(ARellenar)):
            ARellenar.append(28)
def encriptador(texto, filas, c=False):
    
    """Cambia cada valor del texto por un numero y lo devuelve en una matriz de filas como se indiquen en el parametro filas.
    Si el parametro 'c' es verdadero, retorna una matriz con la misma cantidad de columnas y filas (Esto es usado para la contra).
    Parametros:
    texto= Str ==> Este es el texto que se va a transformar en matriz
    filas= Int ==> Indica el número de filas que la matriz tendrá
    c= Boolean ==> Si está activo la matriz tendrá la misma cantidad de columnas como de filas.
    Devuelve un numpy Array debido a que se usa la función "Reshape" de numpy
    """
    lista=[parametros[i] for i in texto] #ingresa el valor (numero) de cada llave (letra) en una lista
    if len(lista)<7: #Hace que el tamaño minimo que pueda tener la matriz, sea de 3x3  
      rellenador(9,lista)
    if c==True: #Si es verdad, la matriz tendrá la misma cantidad de columnas y filas
        raizRedondeadaContra=(len(lista)**0.5)//1 #Devuelve la raiz sin decimales
        if raizRedondeadaContra**2>=len(lista): #Si hay espacio suficiente para almacenar todo los valores de la lista en una matriz cuadrada, redimensiona la lista
            lista=np.reshape(lista, (int(len(lista)**0.5),int(len(lista)**0.5)))
        else: #Si no hay espacios suficientes, entonces la matriz se le aumentará una fila y columna más y se rellenará para poderla redimensionar correctamento
            rellenador(int((raizRedondeadaContra+1)**2),lista) #Rellena valores hasta que la matriz se pueda redimencionar con "reshape" 
            lista=np.reshape(lista, (int(raizRedondeadaContra+1),int(raizRedondeadaContra+1))) #La matriz tendrá el mismo largo de filas que de columnas que se guardará en la variable "lista" como un objeto Nadarray (Lista de numpy)
    else: #Si es falso, tendrá la cantidad de filas indicada por el parámetro 'filas' y tantas columnas como largo sea el texto a encriptar
        rellenador(filas,lista) #Hace que la matriz pueda ser redimensionada a la cantidad de filas
        lista=np.reshape(lista, (filas,(len(lista)//filas))) #Redimensiona la la lista
    return lista 
def getKeyByValue(valorDeLaLetra): 
    """Devuelve la letra que esta en el diccionario de datos que representa el número que se pasa como parámetro 'valorDeLaLetra'.
    valorDeLaLetra= Int ==> Valor en número que la letra tiene según el diccionario
    Devuelve una variable str con la letra solicitada"""
    for letra,numero in parametros.items(): 
      if numero==valorDeLaLetra: return letra
def Redondear(Matriz): 
  """Redondea cada valor de la matriz pasada por parametro. Se usa después de obtener la inversa para que los valores sean enteros y no decimales"""
  
  lista=[round(np.round(i)) for i in np.nditer(Matriz)] #Itera cada valor y los devuelve en una lista, pero redondeados. Uso el redodneador numpy y el de python para evitar errores
  return lista
def Inversador2(Mtrz):
  """Obtiene la inversa de la matriz pasada por parámetro""" 
  M=[[j for j in i] for i in Mtrz] #Si la matriz o array es de numpy, la transforma a una matriz normal para que sea compatible con el codigo
  filas=range(len(M)); cntr=1;time=0 
  Iden=[[1 if i ==j else 0 for j in filas ] for i in filas] #Crea la matriz identidad (la que tiene uno's en medio)
  def cereador(D,ma): 
    
    """No retorna nada, sobreescribe la matriz pasada por parametro"""
    for d in range(len(M[0])): ma[j][d]-=D*ma[i][d]
  def intercambiar(ma): 
    """Si hay una fila con 0 que imposibilita hacer la operación, se cambia esa fila por otra hasta haber probado con todas las filas.
    No retorna nada, reescribe la matriz pasada por parametros"""
    nonlocal cntr
    ma[i], ma[i+cntr]=ma[i+cntr], ma[i];cntr+=1

  for i in filas: #Añade al final la matriz identidad a la matriz a invertir.
    for j in filas:
      M[i].append(Iden[i][j])

  for i in filas: 
    for j in filas:
      if j == i: continue 
      if j>=len(M): continue 
      while M[i][i]==0: #llama a la función de intercambiar por otra fila hasta que el valor ya no sea. Si no hay ninguna fila sin ceros, entonces la matriz no tiene inversa,por lo tanto, retorna "No"
        try:
          intercambiar(M)
        except(IndexError):
          if time==1: return "No" #Time es un contador para ver cuántas si ya pasó una vez a cada fila de la matriz
          time+=1;cntr=1;i=0 #i=0 hace que comience a iterar nuevamente la fila después de haber cambiadola por otra
      Di=M[j][i]/M[i][i] #Es usado para hallar un número que multiplicado por el primer valor de la fila que se va a restar dé el mismo valor de el número A convertir a cero, para que así al restarlo por ella, dé cero
      cereador(Di,M)
  for i in filas: #Luego de convertir todos los valores que no pertenecen a la diagonal principal, se divide a cada fila por el valor de la diagonal perteneciente a esa fila para transformarla en uno y así terminar de convertirla en los valores de la matriz identidad  
    Numed=copy.copy(M[i][i]) #Copia el valor para aún luego de haberlo modificado no se cambie y poder dividir por lo mismo a los demás número de la misma fila
    for j in range(len(M[0])):
      if M[i][j]==0: continue
      M[i][j]=M[i][j]/Numed
  inversa=[[M[i][j+len(M)] for j in filas] for i in filas] #Separa los valores de la matriz inversa de lo demás 
  return inversa
def Inversador3(Mtrz): #i|| A
 M=[[j for j in i] for i in Mtrz]
 filas=range(len(M)); cntr=1;time=0
 Iden=[[1 if i ==j else 0 for j in filas ] for i in filas]
 def cereador(D,ma):
  for d in filas: ma[j][d]-=D*ma[i][d]
 def intercambiar(ma):
  nonlocal cntr
  ma[i], ma[i+cntr]=ma[i+cntr], ma[i];cntr+=1
 for i in filas:
  for j in filas:
   if j == i: continue
   while M[i][i]==0:
    try:
     intercambiar(M);intercambiar(Iden)
    except(IndexError):
     if time==1: return "No"
     time+=1;cntr=1;i=0
   Di=M[j][i]/M[i][i]
   cereador(Di,M); cereador(Di,Iden)
 for i in filas:
  for j in filas: Iden[i][j]/=M[i][i]
 return Iden
def di(textoADecir, imprimir=False):
    if imprimir==True:
        print(textoADecir)
    engine.say(textoADecir)
    engine.runAndWait()

#---Colores del texto---
C=colorama.Fore.CYAN
R=colorama.Fore.RED
B=colorama.Fore.RESET
Y= colorama.Fore.YELLOW
espe = '\n\n                                          --------UNIVERSIDAD DE LAS FUERZAS ARMADAS--------'
voz = '\n                  Bienvenido al Proyecto de Métodos Numéricos sobre mensajes encriptados, ¡qué lo disfrutes mucho!'
print (C+espe)
print(C+voz)
di(espe)
di(voz)

Menu=C+'\nMenu de opciones: \n1.- Simulacion de Mensajes\n2.- Encriptar mensajes\n3.- Desencriptar mensajes\n4.- Salir'
print(Menu)
eligiendo="¿Qué te gustaría hacer?"
di(eligiendo)
opcion = C+'Su opción es: '
escogido=str(input(opcion+B))
    
    



engine.runAndWait()
textoN='Escriba su contraseña: ' 
textoInseguro=R+'''La contraseña no es segura:
      1. La contraseña debe ser mayor a 3 caracteres
      2. Todos los caracteres no pueden ser el mismo
      3. Digite letras y numeros
Ingrese una contraseña más segura: '''
Contrainvalida=R+"El texto ingresado contiene carateres no validos, por favor ingresela nuevamente: "

def preguntacontra():
    def Entrada(texto): #Decide qué texto se imprimira en el input que se creará para la contraseña según si la matriz no tiene inversa.
        global contra
        global contraTransformada
        while True:
            contra=input(texto+B)
            try:
                contraTransformada= encriptador(contra,3, c=True)
                break
            except(KeyError):
                di("Texto no valido")
                print(R+Contrainvalida+B)
    Entrada(C+textoN)
    contraInsegura="La contraseña no es segura. Sigue las instrucciones y prueba con otra"
    while True:
        contraInv=Inversador2(contraTransformada) #Invierte la Matriz
        if contraInv=="No": #Si la matriz retorna "No" es porque no tiene inversa. Por lo tanto pedirá la contraseña nuevamente.
            
            di(contraInsegura)
            Entrada(textoInseguro+B)
        if contraInv!="No": #Si la matriz no returna "No" significa que sí tiene inversa, por lo tanto saldrá del bucle.
            break
    return contraInv
while True: #Pregunta por un número que corresponde a la opción que se elija. Si el dato no es válido, lo vuelve a preguntar.
    if escogido =="1": #Si la opción es la primera, empezará a encriptar el mensaje. 
        entusiasmo="¡Buena elección! Empecemos"
        di(entusiasmo)
        voz = textoN
        di(voz)
        
        Inversa=preguntacontra()
        print(C,"La Matriz contraseña es: \n", contraTransformada)

        voz1 = ('Escriba el mensaje a enviar: ')
        di(voz1)
        
        
        columnas= np.shape(contraTransformada)
        while True:
            mensaje=input(C+'Escriba el mensaje a enviar: '+B)
            try:
                mensajeTransformado= encriptador(mensaje,columnas[1]) #Crea una Matriz con tantas filas como columna tenga la Matriz contra
                break
            except(KeyError):
                di("Texto no valido")
                print(Contrainvalida)
        print(C,"La matriz de la contraseña es: \n", contraTransformada)
        time.sleep(2)
        print(C,"La matriz del mensajes es: \n",mensajeTransformado)
        time.sleep(2)
        mensajeEncriptado= np.matrix(contraTransformada).dot(np.matrix(mensajeTransformado))
        print(C,'\nMatriz Encriptado:\n',mensajeEncriptado)
        time.sleep(2)
        print(C,'El mensaje encriptado es:',Y)
        for i in Redondear(mensajeEncriptado):
            for j in str(i):
                print(getKeyByValue(int(j)), end="")
            print("%&", end="")
        print('\n')
        logrado="¡Listo!, Este es el mensaje encriptado"
        di(logrado)
        #Pregunta si contraseña es correcta
        mnsjEmisor=mensaje
        time.sleep(1)
        pedirContraEmisor="Escribe la contraseña del emisor: "
        di("Ahora"+pedirContraEmisor)
        contraemisor=input(C+pedirContraEmisor+B)
        di(contraemisor)
        while contraemisor!=contra:
            contraincorrecta="Su contraseña es incorrecta, intente con otra: "
            di(contraincorrecta)
            otraContra=input(R+contraincorrecta+B)
            if otraContra==contra:
                ContraCorrecta="La contraseña es correcta"
                di(ContraCorrecta)
                print(C+ContraCorrecta)
                break
        print (C+'La matriz inversa es: \n',np.matrix(Inversa))
        mensajedesencrip=f"El mensaje desencriptado es:\n"+mensaje
        
        print(Y,mensajedesencrip)
        di(mensajedesencrip)
        print(C+"\n\n------------------------------------------------------------Proceso terminado------------------------------------------------------------")
        
        time.sleep(2)
        cambio="Bien, ¿qué te gustaría hacer ahora?"
        di(cambio)
        print(Menu)
        escogido=str(input(opcion+B))
    elif escogido=="2":
        COnfidencial="Seguro es información confidencial. Será mejor encriptarla"
        di(COnfidencial)
        voz = textoN
        di(voz)
        
        Inversa=preguntacontra()

        voz1 = ('Escriba el mensaje a enviar: ')
        di(voz1)
        columnas= np.shape(contraTransformada)
        MensajeInvalido="EL mensaje contiene caracteres no válidos, por favor intente con uno diferente"
        
        while True:
            mensaje=input(C+'Escriba el mensaje a enviar: '+B)
            try:
                mensajeTransformado= encriptador(mensaje,columnas[1]) #Crea una Matriz con tantas filas como columna tenga la Matriz contra
                break
            except(KeyError):
                di(MensajeInvalido)
                print(R+MensajeInvalido)
        print(C,"La matriz contraseña es: \n", contraTransformada)
        time.sleep(2)
        print(C,"La matriz de mensaje es: \n",mensajeTransformado)
        time.sleep(2)
        mensajeEncriptado= np.matrix(contraTransformada).dot(np.matrix(mensajeTransformado))
        print(C,'\nMatriz encriptada:\n',mensajeEncriptado)
        time.sleep(2)
        print(C,'El mensaje encriptado es:',Y)
        for i in Redondear(mensajeEncriptado):
            for j in str(i):
                print(getKeyByValue(int(j)), end="")
            print("%&", end="")
        print('\n')
        logrado="¡Listo!, Este es el mensaje encriptado"
        di(logrado)
        print(C+"\n\n------------------------------------------------------------Proceso terminado------------------------------------------------------------")
        
        time.sleep(2)
        cambio="Bien, ¿qué te gustaría hacer ahora?"
        di(cambio)
        print(Menu)
        escogido=str(input(opcion+B))
    elif escogido=="3":
        def MnsEncriptAMatriz(mnsjEmisor):
            mnsjSep=mnsjEmisor.split(sep="%&")
            mnsjMatrizado=[]
            for letras in mnsjSep:
                numero=""
                for letra in letras:
                    numero+=str(parametros[letra]) 
                if numero=="":continue
                mnsjMatrizado.append(int(numero))
            return mnsjMatrizado
        MensajeInvalido='El mensaje ingresado contiene carateres no validos, por favor ingrese uno distinto: '
        acertijo="¿Así que te has topado con un acertijo...? ¡Te ayudaré a descifrarlo!"
        di(acertijo)
        mnsjEmisor=input(C+"Digite el mensaje encriptado: "+B)
        
        while True:
            try:
                mnsjMatrizado=MnsEncriptAMatriz(mnsjEmisor)
                break
            except(KeyError):
                mnsjEmisor=input(R+MensajeInvalido+B)
        voz2 = '¿Cuál crees podría ser su posible contraseña? Escríbela por favor'
        di(voz2)
        Invertida=preguntacontra()
        
        texto2=C,"\nEscriba la contraseña del emisor: "
        rellenador(len(contraTransformada),mnsjMatrizado)
        mnsjMatrizado=np.reshape(mnsjMatrizado, (len(contraTransformada),(len(mnsjMatrizado)//len(contraTransformada))))
        print (C,'La matriz inversa es: \n',np.matrix(Invertida))
        MatrizDesencriptada=np.matrix(Invertida).dot(mnsjMatrizado) #Se multilican para obtener el mensaje desencritada
        print(C,'El mensaje desencritado es:\n',Y)
        try: 
          mensajefinal=""
          Matrizdesencrpt=Redondear(MatrizDesencriptada)
          for i in Matrizdesencrpt:
              try:
                  mensajefinal+=getKeyByValue(abs(i))
              except(TypeError):
                  pass
        except(TypeError):
                  pass
        print(mensajefinal)
        victoria=f"¡El mensaje desencriptado es, {mensajefinal}..Si el mensaje no fue el esperado, quizá la contraseña no fue la correcta. Preciona 3 para intentar nuevamente"
        print (C,"Si el mensaje no fue el esperado, quizá la contraseña no fue la correcta. Preciona 3 para intentar nuevamente")
        di(victoria)
        print("\n------------------------------------------------------------Proceso terminado------------------------------------------------------------\n")
        time.sleep(2)
        reelige="¿Qué te gustaría intentar ahora"
        di(reelige)
        print(Menu)
        escogido=str(input(opcion+B))
    elif escogido=="4":
        Despedida="Espero haberte sido de ayuda, ¡Nos vemos!"
        di(Despedida)
        break
    else:
        enojado="Parece que te has equivocado al escribir, elige nuevamente."
        di(enojado)
        print(R,"Opcion no valida\n")
        print(Menu)
        escogido=str(input(opcion))