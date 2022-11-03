from math import sqrt, pi , log

#--------------------------------------------------------------------#
# Double line Line
#--------------------------------------------------------------------#

class DoubleLineParam:
    def __init__(self) -> None:
        pass
        # Distances
        a = 9   #m
        b = 7   #m
        c = a   #m
        d = 6.5 #m
        e = d   #m

        d_A1A2 = sqrt((d+e)**2 + self.a**2) #m
        d_A1B1 = sqrt((abs(b-self.a)/2)**2 + d**2)    #m
        d_A1B2 = sqrt(((self.a+b)/2)**2 + d**2)    #m
        d_A2B1 = sqrt(((b+c)/2)**2 + e**2)   #m
        d_A2B2 = sqrt((abs(b-c)/2)**2 + e**2)    #m
        d_A1C1 = sqrt((abs(c-self.a)/2)**2 + (d+e)**2)    #m  / Suposition that self.a = c
        d_A1C2 = self.a    #m
        d_A2C1 = c    #m
        d_A2C2 = d_A1C1    #m
        d_B1B2 = b    #m
        d_B1C1 = d_A2B2  #m
        d_B1C2 = d_A1B2    #m
        d_B2C1 = d_A2B1  #m
        d_B2C2 = d_A1B1  #m
        d_C1C2 = d_A1A2  #m
        # Conductor Characteristics

        # 54Al + 7Ac
        # Type Cardenal
        self.R = 0.062   # Ohms/km (AC resistance)
        d = 30.40   # diameter in mm
        r = d/2
        kg = 0.809  #
        self.G = 0 # In this case we consider Admittance negligible# Conductor Characteristics

        # GMR Calculation


        GMR_A = (kg*r*d_A1A2) ** (1/2)
        GMR_B = (kg*r*d_B1B2) ** (1/2)
        GMR_C = (kg*r*d_C1C2) ** (1/2)
        GMR = (GMR_A*GMR_B*GMR_C) **(1/3)

        # GMD Calculation

        GMD_AB = (d_A1B1*d_A1B2*d_A2B1*d_A2B2) ** (1/4)
        GMD_BC = (d_B1C1*d_B1C2*d_B2C1*d_B2C2) ** (1/4)
        GMD_CA = (d_A1C1*d_A1C2*d_A2C1*d_A2C2) ** (1/4)

        GMD = (GMD_AB*GMD_BC*GMD_CA) **(1/3)

        # Req Calculation

        Req_A = (r*d_A1A2) ** (1/2)
        Req_B = (r*d_B1B2) ** (1/2)
        Req_C = (r*d_C1C2) ** (1/2)

        Req = (Req_A*Req_B*Req_C) ** (1/3)

        # Inductance Calculation

        self.L = 0.2*log((GMD*1000)/GMR) #mH/km  / Should give around 1 mH/km

        f= 50 # Hz
        self.Xl = 2*pi*f*self.L*1000 # Ohm/km

        # Capacitance

        self.C = 1000/(18*log(GMD*1000/Req)) # nF/km / around 0-20nF/km in overhead lines

        # Print results

        print('\u0332Double Line Parameters:\u0332\n',)
        print('R = ',self.R, ' Ohms/km')
        print('L = ',self.L,' mH/km')
        print('Xl = ',self.Xl,' Ohms/km')
        print('C = ',self.C, ' nF/km')
        print('G = ',self.G, ' 1/Ohms·km')

