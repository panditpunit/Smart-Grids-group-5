import math

#--------------------------------------------------------------------#
# Simple Line
#--------------------------------------------------------------------#

# Distances

a = 9 #m
b = 3 #m

d_AB = math.sqrt((a/2)**2 + b**2) #m
d_AC = a    #m
d_BC = d_AB #m




# Conductor Characteristics

# 54Al + 7Ac
# Type Cardenal

R = 0.062   # Ohms/km (AC resistance)
d = 30.40   # diameter in mm
kg = 0.809  #
G = 0 # In this case we consider Admittance negligible

# Inductance calculation

GMD = (d_AB+d_BC+d_AC) ** (1/3) 
GMR = kg*(d/2)
L = 0.2*math.log((GMD*1000)/GMR) #mH/km  / Should give around 1 mH/km


# Capacitance

Req = d/2
C = 1000/(18*math.log(GMD*1000/Req)) # nF/kn / around 0-20nF/km in overhead lines

print('Finished')

