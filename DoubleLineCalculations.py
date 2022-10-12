import math

#--------------------------------------------------------------------#
# Double line Line
#--------------------------------------------------------------------#

# Distances

a = 9   #m
b = 7   #m
c = a   #m
d = 6.5 #m
e = d   #m

d_A1A2 = math.sqrt((d+e)**2 + a**2) #m
d_A1B1 = math.sqrt((abs(b-a)/2)**2 + d**2)    #m
d_A1B2 = math.sqrt(((a+b)/2)**2 + d**2)    #m
d_A2B1 = math.sqrt(((b+c)/2)**2 + e**2)   #m
d_A2B2 = math.sqrt((abs(b-c)/2)**2 + e**2)    #m
d_A1C1 = math.sqrt((abs(c-a)/2)**2 + (d+e)**2)    #m  / Suposition that a = c
d_A1C2 = a    #m
d_A2C1 = c    #m
d_A2C2 = d_A1C1    #m
d_B1B2 = b    #m
d_B1C1 = d_A2B2  #m
d_B1C2 = d_A1B2    #m
d_B2C1 = d_A2B1  #m
d_B2C2 = d_A1B1  #m
d_C1C2 = d_A1A2  #m

print('Finished')