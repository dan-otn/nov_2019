import numpy as np
import scipy
from statsmodels.stats.weightstats import _tconfint_generic
R_clients = set() 
AF_clients = set()
R_sum = np.array([])# транзакции для сегмента R
AF_sum = np.array([])# транзакции для сегмента AF
with open("rf","r") as input_file:
    for line in input_file: #читаем построчно,т к файл большой
        # в каждой строке  читаем id клиента, объем транзакции, сегмент
        client_id, transact, segment = line.split(",")[1], line.split(",")[2], line.split(",")[3]
        if segment[:-1] == "R":# срез до -1 элемента так как последним в строке символ \n
            R_clients.add(client_id)
            R_sum = np.append(R_sum,int(transact))
        if segment[:-1] == "AF":
            AF_clients.add(client_id)
            AF_sum = np.append(AF_sum,int(transact))
          
       
R_transact_mean_std = R_sum.std(ddof=1)/np.sqrt(len(R_sum))           
R_transact_mean = R_sum.mean()

AF_transact_mean_std = AF_sum.std(ddof=1)/np.sqrt(len(R_sum))           
AF_transact_mean = AF_sum.mean()

print (u"Количество клиентов сегмента R:",len(R_clients))
print (u"Количество клиентов сегмента AF:",len(AF_clients))
print(u"Средний объем отдельной транзакции в сегменте R:", sum(R_sum)/len(R_sum))
print(u"Средний объем отдельной транзакции в сегменте AF:", sum(AF_sum)/len(AF_sum))

print ("90%% доверительный интервал для среднего объема отдельной транзакции в сегменте R:", 
       _tconfint_generic(R_transact_mean, R_transact_mean_std, len(R_sum) - 1,
                                                                       0.1, 'two-sided'))
print ("90%% доверительный интервал для среднего объема отдельной транзакции в сегменте AF:", 
       _tconfint_generic(AF_transact_mean, AF_transact_mean_std, len(AF_sum) - 1,
                                                                       0.1, 'two-sided'))

p_val = scipy.stats.ttest_ind(a, b, equal_var = False)[1] #p-value для гипотезы о равенстве средних
if p_val <0.1:
    print(u"Отвергаем гипотезу о равенстве средних")
else:
    print (u"Гипотезу о равенстве средних нельзя отвергнуть")