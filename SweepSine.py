from scipy.signal import chirp, tukey, fftconvolve
from numpy import linspace, concatenate, zeros, ones, arange, log, sin, exp, abs, flipud
from math import pi as pi
import numpy as np 

def SweepSine(fs,sweep_dur,sweep_range,start_silence,end_silence,amplitude):
    f1 = sweep_range[0]
    f2 = sweep_range[1]
    w1 = 2*pi*f1/fs
    w2 = 2*pi*f2/fs
    numSamples = sweep_dur*fs
    sinsweep = zeros(shape = (numSamples,1))
    taxis = arange(0,numSamples,1)/(numSamples-1)

    lw = log(w2/w1)
    sinsweep = amplitude*sin(w1*(numSamples-1)/lw * (exp(taxis*lw)-1))
    k = flipud(sinsweep)
    error = 1
    counter = 0
    while error > 0.001:
        error = abs(k[counter])
        counter = counter+1
    k = k[counter::]
    sinsweep_hat = flipud(k)
    sinsweep = zeros(shape = (numSamples,))
    sinsweep[0:sinsweep_hat.shape[0]] = sinsweep_hat

    envelope = (w2/w1)**(-taxis) # Holters2009, Eq.(9)
    invfilter = flipud(sinsweep)*envelope
    scaling = pi*numSamples*(w1/w2-1)/(2*(w2-w1)*log(w1/w2))*(w2-w1)/pi # Holters2009, Eq.10

    taperStart = tukey(numSamples,0)
    taperWindow = ones(shape = (numSamples,))
    taperWindow[0:int(numSamples/2)] = taperStart[0:int(numSamples/2)]
    sinsweep = sinsweep*taperWindow

    sinsweep = np.expand_dims(sinsweep,axis = 1)
    zerostart = zeros(shape = (start_silence*fs,1))
    zeroend = zeros(shape = (end_silence*fs,1))
    sinsweep = concatenate((np.concatenate((zerostart, sinsweep), axis = 0), zeroend), axis=0)
    sinsweep = np.transpose(np.tile(np.transpose(sinsweep),1))

    Lp = (start_silence + end_silence + sweep_dur)*fs
    invfilter = invfilter/amplitude**2/scaling
    return invfilter, Lp, sinsweep, taxis

def Deconvolve(invfilter, Recording, Lp):
    tmplen = invfilter.shape[0]+Lp-1
    RIRs = zeros(shape = (tmplen,1))
    sig_reshaped = Recording.reshape[1,Lp]
    sig_avg = np.mean(sig_reshaped,axis=0)

    RIRs = fftconvolve(invfilter,sig_avg)
    return RIRs

