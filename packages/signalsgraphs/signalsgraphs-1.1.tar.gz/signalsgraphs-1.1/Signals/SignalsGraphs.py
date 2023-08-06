import numpy as np
from matplotlib import pyplot as plt


def amsignal(am, ap, fm, fp, mostraSpettro):
    '''
    Calcola il segnale modulato e ne disegna il grafico
    :param am: Ampiezza modulante in V
    :param ap: Ampiezza portante in V
    :param fm: Frequenza modulante in Hz
    :param fp: Frequenza portante in Hz
    :param mostraSpettro: booleano per dire se mostrare lo spettro o no
    :return:
    '''
    t = np.arange(0, 500, 0.01)
    fpMHz = fp/1e6
    fmMHz = fm/1e6
    vpt = ap * np.cos(2 * np.pi * fpMHz * t)
    vmt = am * np.cos(2 * np.pi * fmMHz * t)
    vit = [x + ap for x in vmt]
    vam = (1 / ap) * vpt * vit
    if not mostraSpettro:
        plt.plot(t, vam, color="blue", label="Segnale modulato")
        plt.plot(t, vit, color="orange", label="Segnale inviluppo")
        plt.xlabel("Tempo [us]")
        plt.ylabel("Ampiezza [V]")
        plt.grid()
        plt.legend()
        plt.show()

    else:
        spettro(am, ap, fm, fp)


def spettro(am, ap, fm, fp):
    '''
    Disegna il grafico dello spettro del segnale
    :param am: Ampiezza modulante in V
    :param ap: Ampiezza portante in V
    :param fm: Frequenza modulante in Hz
    :param fp: Frequenza portante in Hz
    '''
    fm = fm/1e3
    fp = fp/1e3
    plt.xlim(fp - fm * 2, fp + fm * 2)
    plt.ylim(0, ap + am / 2)
    plt.xlabel("Frequenza [KHz]")
    plt.ylabel("Volt [V]")
    plt.plot([fp, fp], [0, ap], color="black")
    plt.text(fp - 1, ap + 0.7, "Ap=" + str(ap))
    plt.plot([fp - fm, fp - fm], [0, am / 2], color="black")
    plt.text((fp - fm) - 1, (am / 2) + 0.7, "Am/2=" + str(am / 2))
    plt.plot([fp + fm, fp + fm], [0, am / 2], color="black")
    plt.text((fp + fm) - 1, (am / 2) + 0.7, "Am/2=" + str(am / 2))
    plt.show()

def max(*args):
    max = 0
    for x in args:
        if x > max:
            max = x
    return max

