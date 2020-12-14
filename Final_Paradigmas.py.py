import csv
import os.path
import datetime

def readFile(file):
    try:
        fileData = open(file, 'r', encoding='UTF-8')
        file_csv = csv.DictReader(fileData)          
        return file_csv            
    except IOError:
        print("Error al intentar leer el archivo")

def loadFile():
    file_dic = {'clientes': "",'viajes': ""}   
    for file in file_dic:
        while file_dic[file] == "":
            file_dic[file] = input(f"Ingrese el nombre del archivo de {file} con su extencion \n> ") 
            file_exist = os.path.isfile(file_dic[file]) 
            if not file_exist: # file doesn't exist 
                print(f'{file_dic[file]} no existe, ingrese un nombre valido')
                file_dic[file] = ""
            elif file == 'clientes':
                csv_data = readFile(file_dic[file])
                counter_line = 1
                for line in csv_data: # validations
                    counter_line+=1
                    if len(line['Documento']) < 7 or len(line['Documento']) > 8:
                        print(f"Documento invalido en la linea {counter_line} del archivo, modifique o cargue otro archivo \n")
                        file_dic[file] = ""                  
                    if len(line['Nombre']) == 0 or len(line['Dirección']) == 0 or len(line['Fecha Alta']) == 0 or len(line['Correo Electrónico']) == 0 or len(line['Empresa']) == 0:
                        print(f"Existen campos vacios en la linea {counter_line} del archivo, modifique o cargue otro archivo \n")
                        file_dic[file] = ""                   
                    if '@' not in line['Correo Electrónico'] or '.' not in line['Correo Electrónico']:
                        print(f"Email Erroneo en la linea {counter_line} del archivo, modifique o cargue otro archivo \n")
                        file_dic[file] = ""
            elif file == 'viajes':
                csv_data = readFile(file_dic[file])
                counter_line = 1
                for line in csv_data: # validations
                    counter_line+=1                 
                    if len(line['Documento']) == 0 or len(line['fecha']) == 0 or len(line['monto']) == 0:
                        print(f"Existen campos vacios en la linea {counter_line} del archivo, modifique o cargue otro archivo \n")
                        file_dic[file] = ""
                    try:
                        if len(line['monto'].split('.')[1]) != 2:
                            print(f"El precio en la linea {counter_line} del archivo,no contiene 2 decimales, modifique o cargue otro archivo \n")
                            file_dic[file] = ""
                    except IndexError:
                        print(f"El precio en la linea {counter_line} del archivo,no contiene 2 decimales, modifique o cargue otro archivo \n")
                        file_dic[file] = ""
    print("Archivos validados \n")
    return file_dic  

def ActionLog(action):
    try:
        with open ("logs.log", "a", newline='') as log:
            hora = str(datetime.datetime.now())
            log.write(f"{hora}: {action}\n")
    except IOError:
        print("Ocurrio un error con el archivo log de la aplicación")

def getClientForName(file):
    name = input("Ingresa el nombre a buscar: \n> ")
    match = findData(name,"Nombre",file['clientes'])    
   
    if len(match) == 0:
        print('El cliente que intentas buscar no existe \n')
    else :
        for client_data in match:
            print(client_data)  

def findData(find, field, file):
    match = []
    csv_data = readFile(file)
    if field != "Documento":
        for line in csv_data:
            if find.upper() in line[field].upper():
                match.append(line)
    else:
        for line in csv_data:
            if find in line[field]:
                match.append(line)
    return match

def getClientForCompany(file):
    name = input("Ingresa el nombre de la empresa: \n> ")
    match = findData(name, "Empresa", file['clientes'])
    if len(match) > 0:
        name = match[0]["Empresa"]
        print("------------------------------------------------------------------------")
        print(f"Empresa {name}")
        print(f"Total de usuarios: {len(match)}")
        print("------------------------------------------------------------------------")
        print("[Nombre, dirección, documento, fecha de alta, correo electrónico, empresa]")
        for cliente in match:
            print(cliente)
        print("\n")
    else: 
        print('La empresa que intentas buscar no existe \n')

def getTravelMoneyForCompany(file):
    mount = 0
    name = input("Ingresa el nombre de la empresa: \n> ")
    matchClient = findData(name, "Empresa", file['clientes'])
    if len(matchClient) > 0:
        for lineClient in matchClient:
            matchTravel = findData(lineClient["Documento"], "Documento", file['viajes'])
            if len(matchTravel) > 0:
                for lineTavel in matchTravel:
                    mount += float(lineTavel["monto"])
    else:
        print('La empresa que intentas buscar no existe \n')    
    if mount > 0:
        print(f"\n{name}: {mount:.2f} \n")
    else:
        print("La empresa no tiene monto en viajes")

def getTravelForDocument(file):
    mount = 0
    document = input("Ingresa el Docuemnto: \n> ")
    matchClient = findData(document, "Documento", file['clientes'])
    if len(matchClient) > 0:
        for lineClient in matchClient:
            matchTravel = findData(document, "Documento", file['viajes'])
            if len(matchTravel) > 0:
                for lineTavel in matchTravel:
                    mount += float(lineTavel["monto"])
    else: 
        print('El Docuemnto no existe \n')

    if mount > 0:
            print(f"\nDocumento: {document}")
            print("--------------------------------------------------------------------------")
            print("[Nombre, dirección, documento, fecha de alta, correo electrónico, empresa]")
            print(f"{matchClient}")
            print("--------------------------------------------------------------------------")
            print(f"Total de viajes: {len(matchTravel)}, Monto Total: ${mount}")
            print("--------------------------------------------------------------------------")
            for travel in matchTravel:
                print(travel)
            print("")
    else:
        print("El cliente no tiene viajes")

def menu():
    files = {}
    while True:
        ActionLog('Menu')
        print("Menu: \n 1. Cargar Archivo \n 2. Buscar cliente por nombre \n 3. Total de usuarios por empresa \n 4. Total de dinero de viajes por empresa \n 5. Cantidad total de viajes por documento \n 6. Salir")
        try:
            option = int(input("> ")) 
            if option == 6:
                ActionLog('Salir')
                exit()
            elif option == 1:
                ActionLog('Cargar Archivo')
                files = loadFile()
            elif option == 2:
                ActionLog('Busqueda de cliente por nombre')
                getClientForName(files) if files else print("no hay archivos cargados")
            elif option == 3:
                ActionLog('Total de usuarios por empresa')
                getClientForCompany(files) if files else print("no hay archivos cargados")
            elif option == 4:
                ActionLog('Total de dinero de viajes por empresa')
                getTravelMoneyForCompany(files) if files else print("no hay archivos cargados")
            elif option == 5:
                ActionLog('Cantidad total de viajes por documento')
                getTravelForDocument(files) if files else print("no hay archivos cargados")
            else:
                print("Por favor ingrese una opcion correcta \n")
        
        except ValueError:
            print("Ingrese un numero entero \n")
menu()
