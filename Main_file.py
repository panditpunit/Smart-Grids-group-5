### put all the varaibles here ###

V_HV = 220 #kilo-V base voltage
P_nuc = 450 #active power of nuclear poweirr 
Q_dis = 0
PF=0.98



#Basic net
net = pp.create_empty_network(f_hz='50.0', sn_mva=1, add_stdtypes=True)


pp.create_bus(net, name='Nuclear PP MV', vn_kv = 25, geodata=(100,0))         #0
pp.create_bus(net, name='Nuclear PP HV', vn_kv = V_HV, geodata=(100,0))       #1

pp.create_bus(net, name='Type II B1 MV', vn_kv = 36, geodata=(100,100))       #2
pp.create_bus(net, name='Type II B1 HV', vn_kv = V_HV, geodata=(100,100))     #3

pp.create_bus(net, name='Type II B2 MV', vn_kv = 36, geodata=(0,200))         #4
pp.create_bus(net, name='Type II B2 HV', vn_kv = V_HV, geodata=(0,200))       #5

pp.create_bus(net, name='Type II B3 MV', vn_kv = 36, geodata=(150,200))       #6
pp.create_bus(net, name='Type II B3 HV', vn_kv = V_HV, geodata=(150,200))     #7

pp.create_bus(net, name='Type I B1 MV', vn_kv = 36, geodata=(100,150))       #8
pp.create_bus(net, name='Type I B1 HV', vn_kv = V_HV, geodata=(100,150))      #9

pp.create_bus(net, name='Interconnection', vn_kv = V_HV, geodata=(250,150))  #10

pp.create_bus(net, name='Dismantled plant MV', vn_kv = 25, geodata=(150,150)) #11
pp.create_bus(net, name='Dismantled plant HV', vn_kv = V_HV, geodata=(150,150)) #12


#Incoming exercises

#pp.create_bus(net, vn_kv = V_HV, name='PV PP ', geodata=(50, 250))
#pp.create_bus(net, vn_kv = V_MV, name='PV PP', geodata=(50, 250))

#pp.create_bus(net, vn_kv = V_HV, name='Wind PP', geodata=(0, 50))
#pp.create_bus(net, vn_kv = V_MV, name='Wind PP', geodata=(0, 50))

#pp.create_bus(net, vn_kv = V_HV, name='Storage Plant', geodata=(250, 50))
#pp.create_bus(net, vn_kv = V_MV, name='Storage Plant', geodata=(250, 50))




### Generator Definition ###

pp.create_gen(net, 0, name='Nuclear PP', vm_pu=1.05, p_mw=P_nuc)
pp.create_gen(net, 11, name='Dismantled Plant', vm_pu = 1, p_mw=0, q_mw=Q_dis)
pp.create_ext_grid(net, 10)  #Slack bus will be bus 10

#Incoming exercises

#pp.create_gen(net, ????, name='Wind PP', name='Wind Power Plant')
#pp.create_gen(net, ????, name='PV PP', name='Solar PV Power plant')
#pp.create_gen(net, ????, name='Storage Plant', name='Storage Plant')
net.gen



### Load definition ###

def get_reactive(P,PF):
    Q = P*np.tan(np.arccos(PF))
    return Q


pp.create_load(net, 2, name = 'Type II B2', vm_pu=1, p_mw=P_II, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 4, name = 'Type II B4', vm_pu=1, p_mw=P_II, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 6, name = 'Type II B6', vm_pu=1, p_mw=P_II, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 8, name = 'Type I B8', vm_pu=1, p_mw=P_I, q_mvar=get_reactive(P_I, PF))




pp.create_line_from_parameters(net, from_bus = 1, to_bus = 1, length_km = L, r_ohm_per_km = r01_km, x_ohm_per_km = x01_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, name='01')
pp.create_line_from_parameters(net, from_bus = 0, to_bus = 2, length_km = L, r_ohm_per_km = r02_km, x_ohm_per_km = x02_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, name='02')
pp.create_line_from_parameters(net, from_bus = 1, to_bus = 3, length_km = L, r_ohm_per_km = r13_km, x_ohm_per_km = x13_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, name='13')
pp.create_line_from_parameters(net, from_bus = 2, to_bus = 3, length_km = L, r_ohm_per_km = r23_km, x_ohm_per_km = x23_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, name='23')




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



#LINES LENGHT
Long1=100
Long2=50
Long3=(Long1**2 + Long2**2)**(1/2)
Long4=(Long2**2 + Long2**2)**(1/2)

#CONDUCTOR MAX I [KA]
max_i=888.98/1000



pp.create_line_from_parameters(net, from_bus = 1, to_bus = 3, length_km = Long1, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = max_i, name='01')
pp.create_line_from_parameters(net, from_bus = 3, to_bus = 9, length_km = Long2, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = max_i, name='02')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 12, length_km = Long2, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='03')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 5, length_km = Long3, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='04')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 7, length_km = Long4, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='03')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 5, length_km = Long3, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='04')
