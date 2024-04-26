from SweepSine import SweepSine, Deconvolve
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import deconvolve
import sounddevice as sd
from ASIO import PlayRecord

fs = 44100 #Hz
sweep_dur = 5.0 #seconds
sweep_range = [10, 8000] #frequency
start_silence = 1.0 #seconds
end_silence = 1.0 #seconds
sampling = 1024 #samples
amplitude = 1 #From 0 to 1

invfilter,Lp, sinsweep, t = SweepSine(fs,sweep_dur,sweep_range,start_silence,end_silence,amplitude)
plt.figure(1)
plt.plot(t, sinsweep)
Recording = PlayRecord(sinsweep,fs,sampling)
Recording = Recording.reshape(-1)/np.max(np.abs(Recording))
time = np.linspace(0,Recording.shape[0]/fs,Recording.shape[0])


plt.plot(time, Recording)
plt.title('Sinusoidal Sweep and Recorded Response (Normalized)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

RIR, _ = deconvolve(invfilter, Recording, Lp)
RIR = RIR/np.max(np.abs(RIR))
time_2 = np.linspace(0,RIR.shape[0]/fs,RIR.shape[0])

plt.figure(2)
plt.plot(time_2, RIR)
plt.title('Impulse Response (Normalized)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()