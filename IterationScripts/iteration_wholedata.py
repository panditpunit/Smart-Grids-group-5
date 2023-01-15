import pandas as pd
import numpy as np
import pandapower as pp
import copy
from pandapower.plotting import simple_plotly, pf_res_plotly
import random

#Base net is generated in a different file, and stored in a json file.
net = pp.from_json('net.json')

data = pd.read_excel('data.xlsx')

demand_profile = data['Demand'].to_list()
PV_profile = data['PV'].to_list()
Wind_profile = data['Wind'].to_list()

net.sgen['q_mvar'][0] = 0

#Pending to substitute the actual power installed considering space, and the wind timeseries.
Wind_power = 100
PV_power = 100

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
        #pf_res_plotly(up_net)
        
        #Adding the voltages of the buses, an dthe lines and trafo loadings to the result dataframe
        for j in range(len(net.bus)):
            results['V'+str(j)][i] = up_net.res_bus['vm_pu'][j]
            results['Th'+str(j)][i] = up_net.res_bus['va_degree'][j]
        
        for j in range(len(net.line)):
            results['L'+str(j)][i] = up_net.res_line['loading_percent'][j]
       
        for j in range(len(net.trafo)):
            results['T'+str(j)][i] = up_net.res_trafo['loading_percent'][j]
    results.to_excel('final_grid_alldata_220.xlsx')
    return results




def interrumpibility():
    cost = 0
    counter = 0
    col = []
    line_fail = []
    traf = []
    trafo_fail = []
    #Tracking the hours out of service
    for line in range(len(net.line)):
        col.append('L'+str(line))
        line_fail.append(0)
        
    for trafo in range(len(net.trafo)):
        traf.append('T'+str(trafo))
        trafo_fail.append(0)
        
    col = col + traf
    col.append('%Demand not covered')
    col.append('Total Blackout')
    col.append('Cumulative cost')
    res = pd.DataFrame(columns = col)
    
    #Simulated for a year long
    for season in range(4):
        #Hourly data, using the same day
        for i in range(len(demand_profile)):
            
            incidences = False
            up_net=pp.pandapowerNet(copy.deepcopy(net))
            up_net.load['p_mw'] = net.load['p_mw'] * demand_profile[i] 
            
            for j in range(len(net.line)):
                #Rate of failure depends on length
                rate = up_net.line['length_km'][j]*0.05/8760
                a = random.random()
                failure = rate > a
                if line_fail[j] >= 2:
                    line_fail[j] = 0
                #A line is out of service if the random number lies inside the probability of failure, or if the time of failure is 1 (at 2 it is repaired)
                if failure == True or line_fail[j] in range(1,3):
                    incidences = True
                    line_fail[j] += 1
                    up_net.line['in_service'][j]=False
                    
                
                
            for t in range(len(net.trafo)):
                
                rate = 0.15/8760
                a = random.random()
                failure = rate > a
                
                if trafo_fail[t] >= 8:
                    trafo_fail[t] = 0
                #Same as for lines, but the time of repair is 8 hours instead
                if failure == True or trafo_fail[t] in range(1,9):
                    incidences = True
                    trafo_fail[t] += 1
                    up_net.trafo['in_service'][t]=False
                
                    
            #We attempt to solve the grid. Sometimes it is solvable, but not all the grid is in service
            try:
                pp.runpp(up_net, max_iteration=10)
                non_covered = up_net.load['p_mw'].sum()-up_net.res_load['p_mw'].sum()
                cost += 150*non_covered
                perc = 1 - up_net.res_load['p_mw'].sum()/up_net.load['p_mw'].sum()
                if non_covered !=0:
                    
                    r = line_fail + trafo_fail
                    r.append(perc*100)
                    if perc >= 0.99:
                        r.append(True)
                    else:
                        r.append(False)
                    r.append(cost)
                    res.loc[len(res)] = r
                    pf_res_plotly(up_net)
                else:
                    if incidences == True:
                        counter+=1
                    
            #Some other times, the grid doesn't converge
            except:
                
                non_covered = up_net.load['p_mw'].sum()
                cost += 150*non_covered
                
                
                r=line_fail+trafo_fail
                r.append(100)
                r.append(True)
                r.append(cost)
                res.loc[len(res)] = r
                    

    res.to_excel('interrumpibility_report_improved_alldata.xlsx')
    return cost, counter

