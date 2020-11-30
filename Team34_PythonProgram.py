#Team 34 Members [MAC IDs]: donnisom, hassas48, scappatc, sundarrr
import math

teamNumber = 34
bodyWeight = 84.0 * 9.81 #Jackie Chiles has a mass of 84kg
outerDia = 35 #mm
canalDiameter = 18 #mm
canalOffset = 52 #mm
modulusBone = 17.6 #GPa, [1] 
ultTenStrength = 422 #MPa, refer to Materials
modulusImplant = 11.4 #GPa, refer to Materials
stemDia = 16

def home():
    choice = 0
    while choice != 4:
        print("\n================================================================")
        print("\nHIP IMPLANT ASSESSMENT PROGRAM:")
        print("\n1. Minimum Diameter")
        print("2. Fatigue Life")
        print("3. Time Until Failure")
        print("4. Exit from program")

        choice = int(input("\nPlease select an option: #"))

        if choice == 1:
            subprogram1()
        elif choice == 2:
            subprogram2()
        elif choice == 3:
            subprogram3()
        elif choice == 4:
            print("\nNow exiting...")
        else:
            print("ERROR: Invalid input")
            print("\t- Please enter a value from 1 to 4")

def subprogram1():
    print("\n\tPatient's Body Weight:",round(bodyWeight,2),"N")
    print("\tFemoral Canal Diameter:",canalDiameter,"mm")
    print("\tUltimate Tensile Strength of Femoral Bone:",ultTenStrength,"MPa")

    stemDia = canalDiameter
    appTenStress = 0
    
    while appTenStress < (ultTenStrength*1000000):
        load = 3.5 * bodyWeight
        csa = ((math.pi)/4) * ((stemDia/1000) ** 2)

        stressAxl = -1*(load/csa)
        
        moment = load*(canalOffset/1000)
        inertia = ((math.pi)/64) * ((stemDia/1000) ** 4)
        stressBend = (moment*(0.5*stemDia/1000)) / inertia

        appTenStress = stressAxl + stressBend

        stemDia -= 0.0001

    minStemDia = stemDia

    print("\n\tMinimum Implant Stem Diameter:",round(minStemDia,3),"mm")
    print("\tAssosciated Applied Tensile Stress:",round(appTenStress/1000000,3),"MPa")

def subprogram2():
    file = open('SN-Data-Sample-Metal.txt','r')
    data_list = file.readlines()
    file.close()

    snData = []
    
    for data in data_list:
        dataPair = data.split()
        sn = [float(dataPair[0]),float(dataPair[1])]
        snData.append(sn)

    stemDia = 16
    maxCycLoad = 10 * bodyWeight
    minCycLoad = (-10) * bodyWeight
    csa = ((math.pi)/4) * ((stemDia/1000) ** 2)

    stressMax = maxCycLoad / csa
    stressMin = minCycLoad / csa
    stressAmp = ((stressMax - stressMin) / 2) / 1000000

    x = 1
    cyclesFail = 0
    while x < (len(snData) - 1):
        if stressAmp >= snData[0][0]:
            cyclesFail = snData[0][1]
        elif stressAmp > snData[x][0] and stressAmp < snData[x-1][0]:
            cyclesFail = (snData[x][1] + snData[x-1][1]) / 2

        x += 1

    if cyclesFail == 0:
        print("\n\tThe implant material will not fail")
        #print("\tStress Amplitude:",round(stressAmp,3),"MPa")
    elif cyclesFail == snData[0][1]:
        stressFactor = 6 + ((math.log10(cyclesFail)) ** (teamNumber/30))
        stressFail = stressFactor * stressAmp
        print("\n\tCycles to Failure of Implant: <=",cyclesFail)
        print("\tImplant's Failure Stress: <=",round(stressFail,3),"MPa")
    else:
        stressFactor = 6 + ((math.log10(cyclesFail)) ** (teamNumber/30))
        stressFail = stressFactor * stressAmp
        print("\n\tCycles to Failure of Implant:",cyclesFail)
        print("\tImplant's Failure Stress:",round(stressFail,3),"MPa")

def subprogram3():
    stemDia = 16
    csa = ((math.pi)/4) * ((outerDia/1000) ** 2 - (canalDiameter/1000) ** 2)
    stressComp = (30 * bodyWeight) / csa

    stressReduc = stressComp * (((2 * modulusBone) / (modulusBone + modulusImplant)) ** 0.5) / 1000000

    Eratio = math.sqrt(modulusImplant/modulusBone)

    compStrength = 0
    x = 0
    while stressReduc >= compStrength:
        compStrength = (0.001 * x ** 2) - (3.437 * x * Eratio + 181.72)
        x += 0.001

    stressFail = compStrength
    yrsFail = x

    print("\n\tYears Until Implant Failure:",int(yrsFail))
    print("\tStress Applied at Failure:",round(stressFail,3),"MPa")
    
home()

#Materials
#   Implant Stem
#       Ti-22Nb-6Zr:
#           Ultimate Tensile Strength: 422 MPa
#           Young's Modulus: 11.4 GPa
#
#Citations
#   Modulus of Bone
#       [1] S. Pal, "Mechanical Properties of Biological Materials," in Design of Artificial
#       Human Joints & Organs, Boston, United States: Springer, 2014, ch. 2, sec. 5, pp. 30


