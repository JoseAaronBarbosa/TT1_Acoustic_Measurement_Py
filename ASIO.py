from sounddevice import default, playrec

def PlayRecord(Sweeptone,fs,sampling):
    #SweepSize = Sweeptone.shape[0]
    default.device = "ASIO4ALL v2, ASIO"
    default.samplerate = fs  
    default.blocksize = sampling
    default.channels = 1
    Recording = playrec(Sweeptone, blocking=True)
    return Recording
