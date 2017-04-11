# *-* encoding: utf-8 *-*

import random
import threading
import time


numElfos = 0
numRenos = 0


mutexConta = threading.Semaphore(1) #Mutex asociado a contadores
semElfos = threading.Semaphore(0) #Semaforo para atender a los elfos.
mutexElfos = threading.Semaphore(1) #Mutex que evita que un grupo vea a santa, cuando esta con otro.
semSanta = threading.Semaphore(0) #Semaforo que despierta a Santa.
semRenos = threading.Semaphore(0) #Semaforo que envia renos a vacacionar.

def elfos(n):
	global numElfos
	print "Llego el elfo %d para ir con Santa." % n
	mutexElfos.acquire() #Se activa mutex para evitar que se junten mas, en caso de que el que llegue sea el tercero
	mutexConta.acquire() #Aumenta el contador del mutex.
	numElfos += 1
	if numElfos == 3:
		print "Estan completos los elfos, pueden despertar a Santa."
		semSanta.release()
	else:
		mutexElfos.release() #Libera mutex para juntar otro elfo
	mutexConta.release() #Libera el contador para el elfo que entre.
	

	semElfos.acquire() #Se atiende a los elfos
	print "El elfo %d fue atendido" % n

	mutexConta.acquire() #Activa el mutex para disminuir el numero de elfos
	numElfos -= 1

	if numElfos == 0: #Si el numero de elfos es cero, se libera el mutex para darselo a los que esperan.
		mutexElfos.release()
	mutexConta.release()

def santaAtiende():
	print "Dime tus dudas Elfito"
	time.sleep(0.3)
	print "¡Termine!, a dormir"

def renos(n):
	global numRenos
	while True:
		print "Reno regresa de playas del Caribe"  
		
		mutexConta.acquire() #Activa contador de renos
		numRenos += 1
		
		if numRenos == 9:
			print "Renos completos, Santa se va a entregar regalos"
			semSanta.release()
		

		mutexConta.release()

		semRenos.acquire()

		regresaAplaya(n)

def aRepartir():
	print "¡Nos vamos a repartir juguetes!"
	time.sleep(2)
	print "¡Hemos vuelto!"

def regresaAplaya(n):
	print "Yo, el reno %d me voy a la playa" %n
	time.sleep(random.random()*10)

def santa():
	global numRenos
	global numElfos
	while True:
		semSanta.acquire() #Se activa para despertar a Santa
		mutexConta.acquire() #Se revisa contador

		if numElfos == 3: #Si el numero de elfos es de 3, atiende sus dudas
			santaAtiende()
			for i in range(3):
				semElfos.release()
		elif numRenos == 9: #En caso contrario, si el numero de renos es de 9, se va a repartir.
			aRepartir()
			numRenos -= 9
			for i in range(9):
				semRenos.release()
		mutexConta.release() #Libera el semaforo.


#Se inicializan 9 hilos, que corresponden a los renos.
for a in range(1,10):
	threading.Thread(target=renos, args=[a]).start()

#Se inicializa un numero no definido de hilos, correspondientes a los elfos
creaElfos = 0

while True:
	time.sleep(0.5)
	if random.random() < 1.5:
		threading.Thread(target=elfos, args=[creaElfos]).start()
		creaElfos += 1

#Hilo para declarar a Santa
threading.Thread(target=santa, args=[]).start()


