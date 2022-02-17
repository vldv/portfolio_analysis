# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:05:53 2021

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import numpy as np
import matplotlib.pyplot as plt

M = .021 # %age moyen de retour journalier
S = 3 # variation quotidienne du %age
NJ = 365*15 # nombre de jours de simul
MIN_CAP = 10 # %age du cap en dessous duquel on est out

def simul(n_jours=NJ, m=M, s=S, div=1):
    """ """
    mus = [m]*div ; sigmas = [s]*div
    n_invest = len(mus)
    return_tot = 0
    for mu, sigma in zip(mus, sigmas):
        return_perc = 1 + np.random.randn(n_jours)*sigma/100.+mu/100.
        return_tot += np.cumprod(return_perc)/n_invest
    bust = return_tot >= MIN_CAP/100.
    return return_tot * np.cumprod(bust) * 100


def simul_n(N, n_jours=NJ, mus=M, sigmas=S, div=1):
    out = np.zeros((N, n_jours))
    for i in range(N): out[i] = simul(n_jours, mus, sigmas, div)
    return out

if 0:
    s10_3 = simul_n(N=1000, div=10)
    s3_3 = simul_n(N=1000, div=3)
    s1_3 = simul_n(N=1000, div=1)
    s10_2 = simul_n(N=1000, sigmas=2, div=10)
    s3_2 = simul_n(N=1000, sigmas=2, div=3)
    s1_2 = simul_n(N=1000, sigmas=2, div=1)
    
    res = 100
    t = (np.arange(NJ)/30.417)[::res]
    
    plt.figure()
    plt.plot(t, (s10_3).mean(0)[::res], 'g', label='10 stocks, 3% var')
    plt.plot(t, (s3_3).mean(0)[::res], 'C1', label='3 stocks, 3% var')
    plt.plot(t, (s1_3).mean(0)[::res], 'r', label='1 stocks, 3% var')
    plt.plot(t, (s10_2).mean(0)[::res], 'g--o', label='10 stocks, 2% var')
    plt.plot(t, (s3_2).mean(0)[::res], 'C1--o', label='3 stocks, 2% var')
    plt.plot(t, (s1_2).mean(0)[::res], 'r--o', label='1 stocks, 2% var')
    plt.legend()
    plt.xlabel('temps (mois)')
    plt.ylabel('Gain moyen (%)')
    plt.title('gain journalier moyen @ 0.021% +/- 2 ou 3% sur 15 ans')

    plt.figure()
    plt.plot(t, 100*(s10_3>50).mean(0)[::res], 'g', label='10 stocks, 3% var')
    plt.plot(t, 100*(s3_3>50).mean(0)[::res], 'C1', label='3 stocks, 3% var')
    plt.plot(t, 100*(s1_3>50).mean(0)[::res], 'r', label='1 stocks, 3% var')
    plt.plot(t, 100*(s10_2>50).mean(0)[::res], 'g--o', label='10 stocks, 2% var')
    plt.plot(t, 100*(s3_2>50).mean(0)[::res], 'C1--o', label='3 stocks, 2% var')
    plt.plot(t, 100*(s1_2>50).mean(0)[::res], 'r--o', label='1 stocks, 2% var')
    plt.legend()
    plt.xlabel('temps (mois)')
    plt.ylabel('Proportion investisseurs avec perte >50%')
    plt.title('gain journalier moyen @ 0.021% +/- 2 ou 3% sur 15 ans')
    
    plt.figure()
    plt.plot(t, 100*(s10_3>200).mean(0)[::res], 'g', label='10 stocks, 3% var')
    plt.plot(t, 100*(s3_3>200).mean(0)[::res], 'C1', label='3 stocks, 3% var')
    plt.plot(t, 100*(s1_3>200).mean(0)[::res], 'r', label='1 stocks, 3% var')
    plt.plot(t, 100*(s10_2>200).mean(0)[::res], 'g--o', label='10 stocks, 2% var')
    plt.plot(t, 100*(s3_2>200).mean(0)[::res], 'C1--o', label='3 stocks, 2% var')
    plt.plot(t, 100*(s1_2>200).mean(0)[::res], 'r--o', label='1 stocks, 2% var')
    plt.legend()
    plt.xlabel('temps (mois)')
    plt.ylabel('Proportion investisseurs avec gains >100%')
    plt.title('gain journalier moyen @ 0.021% +/- 2 ou 3% sur 15 ans')
    
    