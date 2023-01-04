import numpy as np
import pandapower as pp
import pandas as pd
from pandapower.plotting import simple_plotly, pf_res_plotly
from math import sqrt, pi , log
from LineCalculations import LineParam

### put all the varaibles here ###

V_HV = 220 #kilo-V base voltage
P_nuc = 450 #active power of nuclear poweirr 
P_I = 300
P_II = 120

Q_dis = 200
PF=0.98



#Basic net


net = pp.create_empty_network(f_hz=50, sn_mva=1, add_stdtypes=True)


pp.create_bus(net, name='Nuclear PP MV', vn_kv = 25, geodata=(100,-10))         #0
pp.create_bus(net, name='Nuclear PP HV', vn_kv = V_HV, geodata=(100,0))       #1

pp.create_bus(net, name='Type II B1 MV', vn_kv = 36, geodata=(90,100))       #2
pp.create_bus(net, name='Type II B1 HV', vn_kv = V_HV, geodata=(100,100))     #3

pp.create_bus(net, name='Type II B2 MV', vn_kv = 36, geodata=(0,210))         #4
pp.create_bus(net, name='Type II B2 HV', vn_kv = V_HV, geodata=(0,200))       #5

pp.create_bus(net, name='Type II B3 MV', vn_kv = 36, geodata=(150,210))       #6
pp.create_bus(net, name='Type II B3 HV', vn_kv = V_HV, geodata=(150,200))     #7

pp.create_bus(net, name='Type I B1 MV', vn_kv = 36, geodata=(100,160))       #8
pp.create_bus(net, name='Type I B1 HV', vn_kv = V_HV, geodata=(100,150))      #9

pp.create_bus(net, name='Interconnection', vn_kv = V_HV, geodata=(250,150))  #10

pp.create_bus(net, name='Dismantled plant MV', vn_kv = 25, geodata=(160,150)) #11
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
pp.create_sgen(net, 11, name='Dismantled Plant', p_mw=0, q_mvar=Q_dis)
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


pp.create_load(net, 2, name = 'Type II B2', p_mw=P_II, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 4, name = 'Type II B4', p_mw=P_II, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 6, name = 'Type II B6', p_mw=P_II, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 8, name = 'Type I B8', p_mw=P_I, q_mvar=get_reactive(P_I, PF))




### Trafo definition ###


pp.create_transformer_from_parameters(net, hv_bus = 1, lv_bus = 0, sn_mva = 500, vn_hv_kv = 220, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'Trafo_NuclearPP')
pp.create_transformer_from_parameters(net, hv_bus = 3, lv_bus = 2, sn_mva = 150, vn_hv_kv = 220, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'Trafo_II_1')
pp.create_transformer_from_parameters(net, hv_bus = 5, lv_bus = 4, sn_mva = 150, vn_hv_kv = 220, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'Trafo_II_2')
pp.create_transformer_from_parameters(net, hv_bus = 7, lv_bus = 6, sn_mva = 150, vn_hv_kv = 220, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'Trafo_II_3')
pp.create_transformer_from_parameters(net, hv_bus = 9, lv_bus = 8, sn_mva = 350, vn_hv_kv = 220, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'Trafo_I_1')
pp.create_transformer_from_parameters(net, hv_bus = 12, lv_bus = 11, sn_mva = 200, vn_hv_kv = 220, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'Trafo_DismantledPlant')



#####################################################################################

#LINES LENGHT
Long1=100
Long2=50
Long3=(Long1**2 + Long2**2)**(1/2)
Long4=(Long2**2 + Long2**2)**(1/2)

#CONDUCTOR MAX I [KA]
max_i=888.98/1000



#dbLine = DoubleLineParam()
#sLine = SimpleLineParam()


a = 9   #m
b = 7   #m
c = a   #m
d = 6.5 #m
e = d   #m

dbLine = LineParam(
        A_coord= [[-a/2,d],[c/2,-e]],
        B_coord=[[-b/2,0],[b/2,0]],
        C_coord=[[-c/2,-e],[a/2,d]],
        Rac= 0.062,
        kg=0.809,
        radius=0.03040/2,
        bundled= False,
        )


a = 9 #m
b = 3 #m

sLine = LineParam(

        A_coord= [[-a/2,0]],
        B_coord=[[0,b]],
        C_coord=[[a/2,0]],

        Rac= 0.062,
        kg=0.809,
        radius=0.03040/2,
        bundled= False,
        )
    

pp.create_line_from_parameters(net, from_bus = 1, to_bus = 3, length_km = Long1, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = 2*max_i, name='1_3')
pp.create_line_from_parameters(net, from_bus = 3, to_bus = 9, length_km = Long2, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = 2*max_i, name='3_9')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 12, length_km = Long2, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='9_12')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 5, length_km = Long3, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='9_5')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 7, length_km = Long4, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = 2*max_i, name='9_7')
pp.create_line_from_parameters(net, from_bus = 7, to_bus = 10, length_km = Long3, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='7_10')





pp.runpp(net, max_iteration=10)

lines=net.res_line
buses=net.res_bus
trafos=net.res_trafo


pp.diagnostic(net)
print(net.load)
print(net.bus)
print(net.trafo)
print(net.line)
pp.to_json(net,'net.json')
pf_res_plotly(net)
