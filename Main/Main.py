from colorama import*

global valores
valores=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
init(autoreset=True)

def interface():
    global valores
    print("-------- Proyecto 1: Codigo Hamming --------\n")
    running=True
    while(running):
        numero=input("Ingrese un numero hexadecimal de 3 digitos (ingrese -1 para salir): ")
        if(numero=="-1"):
            print("Gracias por utilizar el programa!")
            break
        while(True):
            if(len(numero)!=3):
                print("El valor ingresado debe tener 3 digitos!\n")
                break;
            else:

                numero=numero.lower()
                allFound=True
                for digito in numero:
                    if(digito not in valores):
                        print("El simbolo "+digito+" ingresado no es un valor valido en el alfabeto hexadecimal!\n ")
                        allFound=False
                        break;
                if(allFound):
                    binaryValue=hexToBinary(numero)
                    print("Numero convertido a binario: "+binaryValue)
                    print("Numero binario convertido a octal: "+binaryToOctal(binaryValue))
                    print("Numero binario convertido a decimal: " + binaryToDecimal(binaryValue))
                    print("Representacion NZRI: \n")
                    print(toNZRI(binaryValue)+"\n")
                    paridad=-1
                    while(True):
                        print("---- Paridad ----\n"
                              "1-> Par\n"
                              "0-> Impar\n")
                        paridad=input("Por favor seleccione un tipo de paridad: ")
                        if(paridad!="1" and paridad!="0"):
                            print("Por favor seleccione una opcion de paridad valida! ")
                        else:
                            break;
                    even=True
                    if(paridad=="1"):
                        print("Paridad par seleccionada!\n")
                        even=False
                    else:
                        print("Paridad impar seleccionada!\n")
                    print(Fore.GREEN+"Codificacion Hamming: "+hammingCodifier(binaryValue,even)+"\n")

                    genTabla1(binaryValue,hammingCodifier(binaryValue,even))

                    print("Desea inducir un error en la secuencia anteriormente presentada:\n"
                          "1-> Si\n"
                          "2-> No\n")
                    inducir=False
                    while(True):
                        seleccion=input("Por favor seleccione una de las opciones anteriores: ")
                        if(seleccion=="1"):
                            inducir=True
                            break;
                        elif(seleccion=="2"):
                            break

                    if(inducir):
                        bit=-1
                        while(True):
                            bit=int(input("Ingrese un numero de bit entre 1 y 17 que desea cambiar: "))
                            if(bit>0 and bit<=17):
                                break
                            print("Numero de bit invalido!\n")
                        codified=hammingCodifier(binaryValue,even)
                        bit=bit-1
                        codified=list(codified)
                        codified[bit]=str(abs(int(codified[bit])-1))
                        codified= "".join(codified)
                        hammingFixer(codified,even)

                break;

def hexToBinary(hex):
    global valores
    output=""
    for digito in hex:
        converted=""
        realValue=valores.index(digito)
        while(realValue!=0):
            converted=str(realValue%2)+converted
            realValue=realValue//2
        while(len(converted)<4):
            converted="0"+converted
        output+=converted
    return output

def binaryToOctal(binary):
    while(len(binary)%3!=0):
        binary="0"+binary
    output=""
    while(binary!=""):
        fragment=binary[0:3]
        binary=binary[3:]
        ind=2
        convertedFrag=0
        for digito in fragment:
            convertedFrag+=int(digito)*(2**ind)
            ind-=1
        output+=str(convertedFrag)
    return output

def binaryToDecimal(binary):
    ind=len(binary)-1
    output=0
    for digito in binary:
        output+=int(digito)*2**ind
        ind-=1
    return str(output)

def decimalToBinary(decimal):
    output=""
    while(decimal!=0):
        output+=str(decimal%2)
        decimal=decimal//2
    output=output[::-1]
    while(len(output)<5):
        output="0"+output
    return output


def toNZRI(binary):
    "------ "
    "      |"
    "      |      |"
    "       ------ "
    firstLine= "-------"
    secondLine="      "
    thirdLine= "      "
    fourthLine="      "
    fifthLine="      "
    high=True
    change=False
    for digito in binary:
        if(digito=="1"):
            high=not high
            change=True

        if(high):
            if(change):
                firstLine+= "-------"
                secondLine+="|     "
                thirdLine+= "|     "
                fourthLine+="     "
                fifthLine +="  "+digito+"  "
                change=False
            else:
                firstLine+= "-------"
                secondLine+="       "
                thirdLine+= "       "
                fourthLine+="       "
                fifthLine +="   "+digito+"   "
        else:
            if (change):
                firstLine +="     "
                secondLine+="|     "
                thirdLine+= "|     "
                fourthLine+="-------"
                fifthLine +="   "+digito+"   "
                change = False
            else:
                firstLine+= "       "
                secondLine+="       "
                thirdLine +="       "
                fourthLine+="-------"
                fifthLine +="   "+digito+"   "

    return Fore.LIGHTCYAN_EX+firstLine+"\n"+secondLine+"\n"+thirdLine+"\n"+fourthLine+"\n"+Fore.LIGHTGREEN_EX+fifthLine

def hammingCodifier(binary,even):
    binary="00"+binary[0]+"0"+binary[1:4]+"0"+binary[4:11]+"0"+binary[11]
    parityPositions=[0,1,3,7,15]
    ind = 4
    for parity in parityPositions:
        counter=0
        for index in range(len(binary)+1):
            if(index!=0 and index!=parity+1):
                if(decimalToBinary(index)[ind]=="1"):
                    counter+=int(binary[index-1])
        if(even):
            if(counter%2==0):
                binary = list(binary)
                binary[parity]="1"
                binary="".join(binary)
            else:
                binary=list(binary)
                binary[parity]="0"
                binary="".join(binary)
        else:
            if (counter%2==0):
                binary = list(binary)
                binary[parity]="0"
                binary="".join(binary)
            else:
                binary = list(binary)
                binary[parity]="1"
                binary="".join(binary)
        ind-=1
    return binary

def hammingFixer(binary,even):
    ind = 4
    erroneousBit=""
    tests=[]
    results=[]
    for parity in range(5):
        counter = 0
        for index in range(len(binary) + 1):
            if (decimalToBinary(index)[ind] == "1"):
                counter += int(binary[index-1])
        if(even):
            if(counter%2==1):
                erroneousBit+="0"
                tests.append("0")
                results.append("Correcto")
            else:
                erroneousBit+="1"
                results.append("ERROR   ")
                tests.append("1")
        else:
            if (counter % 2 == 1):
                erroneousBit += "1"
                results.append("ERROR   ")
                tests.append("1")
            else:
                erroneousBit += "0"
                tests.append("0")
                results.append("Correcto")
        ind -= 1
    genTabla2(binary, tests, results)
    erroneousBit=erroneousBit[::-1]
    erroneousBit=int(binaryToDecimal(erroneousBit))
    if(erroneousBit!=0):
        print("\nEl bit numero "+str(erroneousBit)+" es incorrecto!\n")

        temp=""

        for digito in binary:
            temp+=digito+"   "
        print(Fore.RED+"Secuencia corrupta: "+temp)
        binary=list(binary)
        binary[erroneousBit-1] =str(abs(int(binary[erroneousBit-1])-1))
        binary = "".join(binary)
        temp = ""
        for digito in binary:
            temp += digito + "   "
        print(Fore.GREEN+"Secuencia reparada: "+temp+"")
        print(3*"      "+erroneousBit*"\t"+Fore.LIGHTCYAN_EX+"^\n")

def genTabla1 (data, arr):
    print("--------------------------------------------------------------------------------------------\n"
          "Tabla No 1: Calculo de los bits de paridad en el codigo Hamming\n"
          "--------------------------------------------------------------------------------------------\n"
          "|--| p1 | p2 | d1 | p3 | d2 | d3 | d4 | p4 | d5 | d6 | d7 | d8 | d9 | d10 | d11 | p5 | d12 |\n"
          "--------------------------------------------------------------------------------------------")
    while(len(data)<17):
        data=data+ "-"

    print("Dato  -    -    "+data[0]+"    -    "+data[1]+"    "+data[2]+"    "+data[3]+"    -    "+data[4]+"    "+data[5]+"    "+data[6]+"    "+data[7]+"    "+data[8]+"     "+data[9]+"     "+data[10]+"    -     "+data[11])

    while(len(arr)<17):
        arr=arr+ "-"

    print("p1    "+arr[0]+"    -    "+data[0]+"    -    "+data[1]+"    -    "+data[3]+"    -    "+data[4]+"    -    "+data[6]+"    -    "+data[8]+"     -     "+data[10]+"    -     "+data[11]+"\n"
          "p2    -    "+arr[1]+"    "+data[0]+"    -    -    "+data[2]+"    "+data[3]+"    -    -    "+data[5]+"    "+data[6]+"    -    -     "+data[9]+"     "+data[10]+"    -     -\n"
          "p3    -    -    -    "+arr[3]+"    "+data[1]+"    "+data[2]+"    "+data[3]+"    -    -    -    -    "+data[7]+"    "+data[8]+"     "+data[9]+"     "+data[10]+"    -     -\n"
          "p4    -    -    -    -    -    -    -    "+arr[7]+"    "+data[4]+"    "+data[5]+"    "+data[6]+"    "+data[7]+"    "+data[8]+"     "+data[9]+"     "+data[10]+"    -     -\n"
          "p5    -    -    -    -    -    -    -    -    -    -    -    -    -     -     -    "+arr[15]+"     "+data[11]+"\n"                                                                                                                                                                  
          "--------------------------------------------------------------------------------------------\n"                                                                                                                                                              
          "Tot.  "+arr[0]+"    "+arr[1]+"    "+arr[2]+"    "+arr[3]+"    "+arr[4]+"    "+arr[5]+"    "+arr[6]+"    "+arr[7]+"    "+arr[8]+"    "+arr[9]+"    "+arr[10]+"    "+arr[11]+"    "+arr[12]+"     "+arr[13]+"     "+arr[14]+"    "+arr[15]+"     "+arr[16]+"\n"
          "--------------------------------------------------------------------------------------------\n")


def genTabla2(arr2,tests,results):
    print("\n-------------------------------------------------------------------------------")
    print("Tabla No 2: Comprobacion de los Bits de Paridad")
    print("-------------------------------------------------------------------------------")
    print('|--|', 'p1', 'p2', 'd1', 'p3', 'd2', 'd3', 'd4', 'p4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', "d11", 'p5',
          'd12', 'Prueba ', 'Bit')
    while(len(arr2) < 17):
            arr2 = arr2 + "-"
    print('Dato', arr2[0], '', arr2[1], '', arr2[2], '', arr2[3], '', arr2[4], '', arr2[5], '', arr2[6], '', arr2[7],
          '', arr2[8], '', arr2[9], '', arr2[10], '', arr2[11], '', arr2[12], '', arr2[13], '  ', arr2[14], ' ',
          arr2[15], ' ', arr2[16])
    print('p1', ' ', arr2[0], ' - ', arr2[2], ' - ', arr2[4], ' - ', arr2[6], ' - ', arr2[8], ' - ', arr2[10], ' - ',
          arr2[12], ' -   ', arr2[14], '  -  ', arr2[16], results[0], '', tests[0])
    print('p2', ' ', '- ', arr2[1], '', arr2[2], ' -  -', '', arr2[5], '', arr2[6], ' -  -', '', arr2[9], '', arr2[10],
          ' -  -', '', arr2[13], '  ', arr2[14], '  -   -', results[1], '', tests[1])
    print('p3', ' ', '-  -  -', '', arr2[3], '', arr2[4], '', arr2[5], '', arr2[6], ' -  -  -  - ', arr2[11], '',
          arr2[12], '', arr2[13], '  ', arr2[14], '  -   -', results[2], '', tests[2])
    print('p4', '  -  -  -  -  -  -  -', '', arr2[7], '', arr2[8], '', arr2[9], '', arr2[10], '', arr2[11], '',
          arr2[12], '', arr2[13], '  ', arr2[14], '  -   -', results[3], '', tests[3])
    print('p5', '  -  -  -  -  -  -  -', '','-', '','-', '','-', '','-', '','-', '',
          '-', '','-', '  ','-', '  -  ',arr2[16], results[4], '', tests[4])
    print("-------------------------------------------------------------------------------\n"
          +Fore.RED+"Bit erroneo: "+"".join(tests[::-1]))
    print("-------------------------------------------------------------------------------\n")

interface()


