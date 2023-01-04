import pandas as pd
import numpy as np
import pandapower as pp
import copy
from pandapower.plotting import simple_plotly, pf_res_plotly

#Base net is generated in a different file, and stored in a json file.
net = pp.from_json('net.json')

data = pd.read_excel('day_data.xlsx')

demand_profile = data['Demand'].to_list()
PV_profile = data['PV'].to_list()
Wind_profile = data['Wind'].to_list()

#Pending to substitute the actual power installed considering space, and the wind timeseries.
Wind_power = 10
PV_power = 153

l=[]

for i in range(len(net.bus)):
    l.append('V'+str(i))

for i in range(len(net.bus)):
    l.append('Th'+str(i))

for i in range(len(net.line)):
    l.append('L' + str(i))
    
for i in range(len(net.trafo)):
    l.append('T'+ str(i))
    
results = pd.DataFrame(index = data.index, columns = l)


def grid_iteration():
    #For each timestep considered
    for i in range(len(demand_profile)):
        #Demand and generation update with forecast
        up_net=pp.pandapowerNet(copy.deepcopy(net))
        up_net.load['p_mw'] = net.load['p_mw'] * demand_profile[i] 
        up_net.gen['p_mw'].loc[net.gen['name'] == 'Solar PP'] = PV_power * PV_profile[i]
        up_net.gen['p_mw'].loc[net.gen['name'] == 'Wind PP'] = Wind_power * Wind_profile[i]
        
        pp.runpp(up_net, max_iteration=10)
        pf_res_plotly(up_net)
        
        #Adding the voltages of the buses, an dthe lines and trafo loadings to the result dataframe
        for j in range(len(net.bus)):
            results['V'+str(j)][i] = up_net.res_bus['vm_pu'][j]
            results['Th'+str(j)][i] = up_net.res_bus['va_degree'][j]
        
        for j in range(len(net.line)):
            results['L'+str(j)][i] = up_net.res_line['loading_percent'][j]
       
        for j in range(len(net.trafo)):
            results['T'+str(j)][i] = up_net.res_trafo['loading_percent'][j]
    results.to_excel('iteration_results.xlsx')
    return results
#profiles = 


#net.load['p_mw'] = net.load['p_mw']*1 ###### update with forecast

#net.gen['p_mw'].loc[net.gen['name'] == 'Solar PP']= 1####### update with forecast
#net.gen['p_mw'].loc[net.gen['name'] == 'Wind PP']= 1######### update with forecast