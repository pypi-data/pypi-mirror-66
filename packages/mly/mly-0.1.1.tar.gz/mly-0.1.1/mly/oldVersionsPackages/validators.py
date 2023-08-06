import matplotlib as mpl
mpl.use('Agg')

from math import ceil
import os
from random import shuffle
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy import io

from scipy.signal import spectrogram
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict    

from .simulateddetectornoise import *
from .__init__ import *

null_path=nullpath()


################################################################################
#################### DOCUMENTATION OF FAR_test  ################################
################################################################################
#                                                                              #
# model:           (model|string) If you running the function at the same scri #
#                  pt you just assign the model object. If you load it from fi #
#                  le you give the path to the model after the model_source_pa #
#                  th                                                          #
#                                                                              #
# length:          (float) The length in seconds of the generated instantiatio #
#                  ns of data.                                                 #
#                                                                              #
# fs:              (int) The sample frequency of the data. Use powers of 2 for #
#                  faster calculations.                                        #
#                                                                              #
# detectors:       (string) A string with the initial letter of the detector y #
#                  ou want to include. H for LIGO Hanford, L for LIGO Livingst #
#                  on, V for Virgo and K for KAGRA. Example: 'HLV' or 'HLVK' o # 
#                  r 'LV'.                                                     #
#                                                                              #
# noise_file:      (optional if noise_type is 'optimal'/ [str,str]) The name o #
#                  f the real data file you want to use as source. The path is #
#                  setted in load_noise function on emily.py. THIS HAS TO BE   #
#                  FIXED LATER!                                                #
#                  The list includes ['date_folder', 'name_of_file']. Date_fol #
#                  der is inside ligo data and contains segments of that day w #
#                  ith the name witch should be the name_of_file.              #
#                                                                              #
# batch_size:      (odd int)The number of instantiations we will use for one b #
#                  atch. To make our noise instanstiation indipendent we need  #
#                  a specific number given the detectors. For two detectors gi #
#                  ves n-1 andf or three n(n-1) indipendent instantiations.    #
#                                                                              #
# starting_point:  (int) The time from whitch you want to start using the data #
#                  from the noise_file, in seconds.                            #
#                                                                              #
# size:            (int|'all') The amound of instantiations you want to genera #
#                  te. Powers of are more convinient. If equals to 'all' it wi #
#                  ll load it all.                                             #
#                                                                              #
# t:               (optinal except psd_mode='default/ float)The duration of th # 
#                  e envelope of every instantiation used to generate the psd. # 
#                  It is used in psd_mode='default'. Prefered to be integral o #
#                  f power of 2. Default is 32.                                #
#                                                                              #
# spec:            (optional/boolean): The option to also generate spectrogram #
#                  s. Default is false. If true it will generate a separate da #
#                  taset with pictures of spectrograms of size related to the  #
#                  variable res below.                                         #
#                                                                              #
# phase:           (optional/boolean): Additionaly to spectrograms you can gen #
#                  erate phasegrams. Default is false. If true it will generat #
#                  e an additional picture under the spectrograms with the sam #
#                  e size. The size will be the same as spectrogram.           #
#                                                                              #
# res:             NEED MORE INFO HERE.                                        #
#                                                                              #
# name:            (optional/string) A special tag you might want to add to yo #
#                  ur saved dataset files. Default is ''.                      #
#                                                                              #
# model_source_path: (optional) This is the source path of the models.         #
#                                                                              #
# destination_path:(optional/string) The path where the dataset will be saved, # 
#                  the default is null_path+'/datasets/'                       #
#                                                                              #
################################################################################

def FAR_test(model           
             ,length        
             ,fs                          
             ,detectors      
             ,noise_file  
             ,lags     
             ,starting_point=0
             ,size='all'      
             ,t=32             
             ,spec=False
             ,phase=False
             ,res=128
             ,model_source_path = null_path+'/trainings/'):
    
    from mly.generators import load_noise, index_combinations
    from keras.models import load_model
    from operator import itemgetter

    import time

    
    ## INPUT CHECKING ##########
    #
    
    #model
    
    #length
    if (not (isinstance(length,float) or isinstance(length,int)) and length>0):
        raise ValueError('The length value has to be a possitive float or'
                         +' integer.')
        
    # fs
    if not isinstance(fs,int) or fs<=0:
        raise ValueError('Sample frequency has to be a positive integer.')
    
    # detectors
    for d in detectors:
        if (d!='H' and d!='L' and d!='V' and d!='K'): 
            raise ValueError('Not acceptable character for detector.'
            +' You should include: \nH for LIGO Hanford\nL for LIGO'
            +' Livingston \nV for Virgo \nK for KAGRA\nFor example: \'HLV\','
            +' \'HLVK\'')
            
    # res
    if not isinstance(res,int):
        raise ValueError('Resolution variable (res) can only be integral')
    
    # noise_file    
    if noise_file==None:
        raise TypeError('You need a real noise file as a source.')         
    if (noise_file!=None and len(noise_file)==2 
        and isinstance(noise_file[0],str) and isinstance(noise_file[1],str)):
        for d in detectors:
            if os.path.isdir(null_path
                             +'/ligo_data/'+str(fs)+'/'+noise_file[0]+'/'
                             +d+'/'+noise_file[1]+'.txt'):
                raise FileNotFoundError('No such file or directory:'+'\''
                                +null_path+'/ligo_data/'+str(fs)+'/'
                                +noise_file[0]+'/'+d+'/'+noise_file[1]+'.txt\'')
                
    # t
    if not isinstance(t,int):
        raise ValueError('t needs to be an integral')
        
    # batch size:
    if not (isinstance(lags, int) and lags%2!=0):
        raise ValueError('lags has to be an odd integer')

    #                        
    ########## INPUT CHECKING ##  


    
    if isinstance(model,str):
        trained_model = load_model(model_source_path+ model +'.h5')
    else:
        trained_model = model    #If model is not already in the script you import it my calling the name    
    
    

    if 'H' in detectors: noise_segH=load_noise(fs,noise_file[0]
                                               ,'H',noise_file[1])   
    if 'L' in detectors: noise_segL=load_noise(fs,noise_file[0]
                                               ,'L',noise_file[1])
    if 'V' in detectors: noise_segV=load_noise(fs,noise_file[0]
                                               ,'V',noise_file[1])
        
    gps0=int(noise_file[1].split('_')[1])

        
    if size=='all':
        if lags==1: 
            size= int((len(noise_segH)/fs-t-starting_point)/length)
        else: 
            size= int((len(noise_segH)/fs-t-starting_point)
                      /length)*(batch_sise-1)


    ind=index_combinations(detectors = detectors
                           ,lags = lags
                           ,length = length
                           ,fs = fs
                           ,size = size
                           ,start_from_sec=starting_point)
    
    predictions_and_times=[]
    nancounter=0
    
    t0=time.time()
    
    for i in range(0,size):
        
        data_instantiation=[]
        local_dict={}


        if 'H'in detectors:
            # Calling the real noise segments
            noiseH=noise_segH[ind['H'][i]:ind['H'][i]+t*fs]
            # Making the noise a TimeSeries
            H_back=TimeSeries(noiseH,sample_rate=fs)
            # Calculating the ASD so tha we can use it for whitening later       
            asdH=H_back.asd(1,0.5)                                    
            # Whitening data                                                     
            h=H_back.whiten(1,0.5,asd=asdH)[int(((t-length)/2)*fs):
                                            int(((t+length)/2)*fs)]
            gpsH=gps0+ind['H'][i]/fs+(t-length)/2

        if 'L'in detectors:

            # Calling the real noise segments
            noiseL=noise_segL[ind['L'][i]:ind['L'][i]+t*fs]
            # Making the noise a TimeSeries
            L_back=TimeSeries(noiseL,sample_rate=fs)
            # Calculating the ASD so tha we can use it for whitening later      
            asdL=L_back.asd(1,0.5)                                    
            # Whitening data                                                    
            l=L_back.whiten(1,0.5,asd=asdL)[int(((t-length)/2)*fs):
                                            int(((t+length)/2)*fs)]
            gpsL=gps0+ind['L'][i]/fs+(t-length)/2



        if 'V'in detectors:
            
            # Calling the real noise segments
            noiseV=noise_segV[ind['V'][i]:ind['V'][i]+t*fs]
            # Making the noise a TimeSeries
            V_back=TimeSeries(noiseV,sample_rate=fs)
            # Calculating the ASD so tha we can use it for whitening later 
            asdV=V_back.asd(1,0.5)                                    
            # Whitening data                                                    
            v=V_back.whiten(1,0.5,asd=asdV)[int(((t-length)/2)*fs):
                                            int(((t+length)/2)*fs)] 
            gpsV=gps0+ind['V'][i]/fs+(t-length)/2


        dumie=[]
        if 'H' in detectors: dumie.append(np.array(h))
        if 'L' in detectors: dumie.append(np.array(l))
        if 'V' in detectors: dumie.append(np.array(v))

        data=np.array([dumie])
        label=np.array([0])

        label=label.reshape(1,1)
        #data=data.reshape(1,3,fs*length)
        
        
        data = data.transpose((0,2,1))
        
        #print(data.shape,label.shape)

        pandt=[]
        pred = trained_model.predict_proba(data, batch_size=1, verbose=0)
        if not (np.isnan(pred[0][0]) or np.isnan(pred[0][1])):
                    
            pandt.append(np.squeeze(np.array(pred))[1])
            if 'H' in detectors: pandt.append(gpsH)
            if 'L' in detectors: pandt.append(gpsL)
            if 'V' in detectors: pandt.append(gpsV)
            
            predictions_and_times.append(pandt)

        else:
            nancounter+=1
        
        if time.time()-t0>=0.1 or i==size-1:
            print(end='\r')
            print(str(i+1)+'/'+str(size),end='')

    predictions_and_times=np.array(sorted(predictions_and_times, key=lambda x: x[0],reverse=True))
    pr={}
    pr['scores']=predictions_and_times[:,0]
    if 'H' in detectors: pr['H']=predictions_and_times[:,1]
    if 'L' in detectors: pr['L']=predictions_and_times[:,2]
    if 'V' in detectors: pr['V']=predictions_and_times[:,3]
    
    
    print('\n\n'+str(nancounter)+' nan resaults found')
    return(pr)


def ROC_test(model,sets,sizes, plots=False):
    
    from mly.mlTools import test_model
    
    data=data_fusion(sets,sizes)
    labels=data[1]
    

    pr=test_model(model,test_data=data)

    
    size=len(pr)
    
    ROC=[]
    x,y=[],[]
    dist=[]

    thr =np.sort(pr[:,1])[::int(sum(sizes)/100)]

    for threshold in thr:
        TP,FP,TN,FN=0,0,0,0
        CP,CN=0,0

        for i in np.arange(0,len(labels)):
            if labels[i]==1: # CONDITION POSITIVE
                
                # pr[i][1] is the signal probability
                if pr[i][1] >= threshold: TP+=1    
                elif pr[i][1]< threshold: FN+=1
                CP+=1 # Counting true possitives

            if labels[i]==0: # CONDITION NEGATIVE
                if pr[i][1] >= threshold: FP+=1
                elif pr[i][1]< threshold: TN+=1
                CN+=1 # Counting true negatives
                
        # Turning countings to rates        
        TPR, FNR = TP/CP, FN/CP  
        TNR, FPR = TN/CN, FP/CN  
        x.append(FPR)
        y.append(TPR)
        #dist.append(np.sqrt((0-FPR)**2+(1-TPR)**2))
    
    if plots==True:
        plt.figure(figsize=(10,5))
        plt.xlabel('FPR')
        plt.ylabel('TPR')
        plt.semilogx(x,y,'r*')
        plt.semilogx(np.arange(0,1.1,0.1),np.arange(0,1.1,0.1),'k--')

        f = interp1d(x, y)
        x_int=np.arange(x[x.index(min(x))],x[x.index(max(x))],0.001)

        plt.semilogx(x_int,f(x_int))
        plt.xlim([1/sum(sizes),1])
        plt.ylim([1/sum(sizes),1])
        plt.show()

    return(x_int,f(x_int))


def TAR_test(model
           ,parameters        
           ,length           
           ,fs               
           ,size             
           ,detectors='HLV'  
           ,spec=True
           ,phase=True
           ,res=128
           ,noise_file=None  
           ,t=32             
           ,lags=11
           ,starting_point=0
           ,name=''          
           ,destination_path=null_path+'/datasets/'
           ,demo=False):       

    
    from mly.generators import load_noise, load_inj, dirlist, SNR, index_combinations
    from keras.models import Sequential, load_model, Model


    ## INPUT CHECKING ##########
    #
    
    # parameters
    if not (isinstance(parameters[0],str) and isinstance(parameters[1],str) 
            and len(parameters)==3):
        
        raise ValueError('The parameters have to be three and in the form:'
                         +' [list, list , float/int]')
             
    if not (os.path.isdir(null_path+'/injections/'+parameters[0])):
        
        raise FileNotFoundError('No such file or directory: \''+null_path
                                +'/injections/'+parameters[0]) 
        
    if (parameters[1]!='optimal' and parameters[1]!='sudo_real'
        and parameters[1]!='real'): 
        
        raise ValueError('Wrong type of noise, the only acceptable are:'
                         +' \n\'optimal\'\n\'sudo_real\'\n\'real\'')
        
    #length
    if (not (isinstance(length,float) or isinstance(length,int)) and length>0):
        raise ValueError('The length value has to be a possitive float or'
                         +' integer.')
        
    # fs
    if not isinstance(fs,int) or fs<=0:
        raise ValueError('Sample frequency has to be a positive integer.')
    
    # detectors
    for d in detectors:
        if (d!='H' and d!='L' and d!='V' and d!='K'): 
            raise ValueError('Not acceptable character for detector.'
                +' You should include: \nH for LIGO Hanford\nL for LIGO'
                +' Livingston \nV for Virgo \nK for KAGRA\nFor example:'
                +' \'HLV\', \'HLVK\'')
    # res
    if not isinstance(res,int):
        raise ValueError('Resolution variable (res) can only be integral')
    
    # noise_file    
    if ((parameters[1]=='sudo_real' or parameters[1]=='real')
        and noise_file==None):
        raise TypeError('If you use suno_real or real noise you need a real'
                +' noise file as a source.')         
    if (noise_file!=None and len(noise_file)==2 
        and isinstance(noise_file[0],str) and isinstance(noise_file[1],str)):
        
        for d in detectors:
            if os.path.isdir(null_path+'/ligo_data/'
                +str(fs)+'/'+noise_file[0]+'/'+d+'/'+noise_file[1]+'.txt'):
                
                raise FileNotFoundError('No such file or directory: '
                        +'\''+null_path+'/ligo_data/'+str(fs)
                        +'/'+noise_file[0]+'/'+d+'/'+noise_file[1]+'.txt\'')
                
    # t
    if not isinstance(t,int):
        raise ValueError('t needs to be an integral')
        
    # batch size:
    if not (isinstance(lags, int) and lags%2!=0):
        raise ValueError('lags has to be an odd integer')

    # name
    if not isinstance(name,str): 
        raise ValueError('name optional value has to be a string')
    
    # destination_path
    if not os.path.isdir(destination_path): 
        raise ValueError('No such path '+destination_path)
    #                        
    ########## INPUT CHECKING ## 
    
    

    dataset = parameters[0]
    noise_type = parameters[1]
    snr_list = parameters[2]
    
    inj_type = dataset.split('/')[1].split('_')[0]

    
    # Making a list of the injection names, so that we can sample randomly from them
    if 'H' in detectors: injectionH=random.sample(dirlist(null_path+'/injections/'+dataset
                                                          +'/H'),size)
    if 'L' in detectors: injectionL=random.sample(dirlist(null_path+'/injections/'+dataset
                                                          +'/L'),size)
    if 'V' in detectors: injectionV=random.sample(dirlist(null_path+'/injections/'+dataset
                                                          +'/V'),size)
        
        
    # Integration limits for the calculation of analytical SNR    
    fl, fm=20, int(fs/2)   

    # Magic number to mach the analytical computation of SNR and the match 
    # filter one: There was a mis-match which I coulndnt resolve how to fix this
    # and its not that important, if we get another nobel I will address that.
    
    magic={2048: 2**(-23./16.), 4096: 2**(-25./16.), 8192: 2**(-27./16.)}
                      

    DATA={}
    


    ##########################
    #                        #
    # CASE OF OPTIMAL NOISE  #       
    #                        #
    ##########################
     
    if noise_type=='optimal':
        param=magic[fs]   

        for SNR_FIN in snr_list:
            
            DATA[str(SNR_FIN)]=[]
        
            for i in range(0,size):
                
                if 'H' in detectors: inj_ind=i
                elif 'L' in detectors: inj_ind=i  
                elif 'V' in detectors: inj_ind=i

                if 'H' in detectors:

                    # Creation of the artificial noise.
                    PSDH,XH,TH=simulateddetectornoise('aligo',t,fs,10,fs/2) 
                    # Calling the templates generated with PyCBC
                    injH=load_inj(dataset,injectionH[inj_ind],'H')        
                    # Saving the length of the injection
                    inj_len=len(injH)/fs

                    # I put a random offset for all injection so that
                    # the signal is not always in the same place
                    if inj_len>length: injH = injH[int(inj_len-length)*fs:]
                    if inj_len<length: injH = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injH
                                    ,np.zeros(int(fs*(length-inj_len)/2))))            
                    if 'H' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injH = injH=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injH[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injH = injH=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injH[:disp]
                                    ,np.zeros(int(fs*(t-length)/2)))) 
                    # Making the noise a TimeSeries
                    H_back=TimeSeries(XH,sample_rate=fs) 
                    # Calculating the ASD so tha we can use it for whitening later
                    asdH=H_back.asd(1,0.5)                                    
                    # Calculating the one sided fft of the template,                
                    injH_fft_0=np.fft.fft(injH)
                    # we get rid of the DC value and everything above fs/2.
                    injH_fft_0N=np.abs(injH_fft_0[1:int(t*fs/2)+1]) 

                    SNR0H=np.sqrt(param*2*(1/t)
                         *np.sum(np.abs(injH_fft_0N*injH_fft_0N.conjugate())
                        [t*fl-1:t*fm-1]/PSDH[t*fl-1:t*fm-1]))


                if 'L' in detectors:

                    # Creation of the artificial noise.
                    PSDL,XL,TL=simulateddetectornoise('aligo',t,fs,10,fs/2) 
                    # Calling the templates generated with PyCBC
                    injL=load_inj(dataset,injectionL[inj_ind],'L')        
                    # Saving the length of the injection
                    inj_len=len(injL)/fs

                    # I put a random offset for all injection
                    # so that the signal is not always in the same place.
                    if inj_len>length: injL = injL[int(inj_len-length)*fs:]
                    if inj_len<length: injL = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injL
                                    ,np.zeros(int(fs*(length-inj_len)/2))))           
                    if 'L' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injL = injL=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injL[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injL = injL=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injL[:disp]
                                    ,np.zeros(int(fs*(t-length)/2)))) 
                    # Making the noise a TimeSeries
                    L_back=TimeSeries(XL,sample_rate=fs) 
                    # Calculating the ASD so tha we can use it for whitening later
                    asdL=L_back.asd(1,0.5)                                    
                    # Calculating the one sided fft of the template,                
                    injL_fft_0=np.fft.fft(injL)
                    # we get rid of the DC value and everything above fs/2.
                    injL_fft_0N=np.abs(injL_fft_0[1:int(t*fs/2)+1]) 

                    SNR0L=np.sqrt(param*2*(1/t)
                         *np.sum(np.abs(injL_fft_0N*injL_fft_0N.conjugate())
                        [t*fl-1:t*fm-1]/PSDL[t*fl-1:t*fm-1]))

                if 'V' in detectors:

                    # Creation of the artificial noise.
                    PSDV,XV,TV=simulateddetectornoise('aligo',t,fs,10,fs/2) 
                    # Calling the templates generated with PyCBC
                    injV=load_inj(dataset,injectionV[inj_ind],'V')        
                    # Saving the length of the injection
                    inj_len=len(injV)/fs

                    # I put a random offset for all injection
                    # so that the signal is not always in the same place.
                    if inj_len>length: injV = injV[int(inj_len-length)*fs:]
                    if inj_len<length: injV = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injV
                                    ,np.zeros(int(fs*(length-inj_len)/2))))
                    if 'V' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injV = injV=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injV[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injV = injV=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injV[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))  
                    # Making the noise a TimeSeries
                    V_back=TimeSeries(XV,sample_rate=fs) 
                    # Calculating the ASD so tha we can use it for whitening later
                    asdV=V_back.asd(1,0.5)                                    
                    # Calculating the one sided fft of the template,                
                    injV_fft_0=np.fft.fft(injV)
                    # we get rid of the DC value and everything above fs/2.
                    injV_fft_0N=np.abs(injV_fft_0[1:int(t*fs/2)+1]) 

                    SNR0V=np.sqrt(param*2*(1/t)
                         *np.sum(np.abs(injV_fft_0N*injV_fft_0N.conjugate())
                        [t*fl-1:t*fm-1]/PSDV[t*fl-1:t*fm-1]))

                # Calculation of combined SNR    
                SNR0=0
                if 'H' in detectors: SNR0+=SNR0H**2
                if 'L' in detectors: SNR0+=SNR0L**2     
                if 'V' in detectors: SNR0+=SNR0V**2
                SNR0=np.sqrt(SNR0)


            # Tuning injection amplitude to the SNR wanted

                if 'H' in detectors:

                    fftH_cal=(SNR_FIN/SNR0)*injH_fft_0         
                    injH_cal=np.real(np.fft.ifft(fftH_cal*fs))
                    HF=TimeSeries(XH+injH_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    h=HF.whiten(1,0.5,asd=asdH)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)] 

                if 'L' in detectors:

                    fftL_cal=(SNR_FIN/SNR0)*injL_fft_0         
                    injL_cal=np.real(np.fft.ifft(fftL_cal*fs))
                    LF=TimeSeries(XL+injL_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    l=LF.whiten(1,0.5,asd=asdL)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)] 

                if 'V' in detectors:

                    fftV_cal=(SNR_FIN/SNR0)*injV_fft_0         
                    injV_cal=np.real(np.fft.ifft(fftV_cal*fs))
                    VF=TimeSeries(XV+injV_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    v=VF.whiten(1,0.5,asd=asdV)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)] 

                dumie=[]
                if 'H' in detectors: dumie.append(np.array(h))
                if 'L' in detectors: dumie.append(np.array(l))
                if 'V' in detectors: dumie.append(np.array(v))
            
                DATA[str(SNR_FIN)].append(dumie)
            DATA[str(SNR_FIN)]=np.array(DATA[str(SNR_FIN)]).transpose((0,2,1))

            
            
        ############################
        #                          #
        # CASE OF SUDO-REAL NOISE  #       
        #                          #
        ############################
            
    if noise_type=='sudo_real':
        
        param=1
        
        if 'H' in detectors: noise_segH=load_noise(fs,noise_file[0],'H',noise_file[1])
        if 'L' in detectors: noise_segL=load_noise(fs,noise_file[0],'L',noise_file[1])
        if 'V' in detectors: noise_segV=load_noise(fs,noise_file[0],'V',noise_file[1])
        
        
        for SNR_FIN in snr_list:
            
            DATA[str(SNR_FIN)]=[]
            
            ind=index_combinations(detectors = detectors
                       ,lags = 1
                       ,length = length
                       ,fs = fs
                       ,size = size
                       ,start_from_sec=starting_point)
        
            for i in range(0,size):
                
                if 'H' in detectors: inj_ind=i
                elif 'L' in detectors: inj_ind=i  
                elif 'V' in detectors: inj_ind=i

                if 'H' in detectors:
                    # Calling the real noise segments
                    noiseH=noise_segH[ind['H'][i]:ind['H'][i]+t*fs]  
                    # Generating the PSD of it
                    dum_fig=plt.figure()
                    p, f = plt.psd(noiseH, Fs=fs, NFFT=fs, visible=False) 
                    p, f=p[1::],f[1::]
                    plt.close(dum_fig) 
                    # Feeding the PSD to generate the sudo-real noise.            
                    PSDH,XH,TH=simulateddetectornoise([f,p],t,fs,10,fs/2)  
                    # Calling the templates generated with PyCBC
                    injH=load_inj(dataset,injectionH[inj_ind],'H')
                    # Saving the length of the injection
                    inj_len=len(injH)/fs                                  

                    # I put a random offset for all injection, so that
                    # the signal is not always in the same place
                    if inj_len>length: injH = injH[int(inj_len-length)*fs:]
                    if inj_len<length: injH = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injH
                                    ,np.zeros(int(fs*(length-inj_len)/2))))            
                    if 'H' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injH = injH=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injH[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injH = injH=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injH[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))  
                    # Making the noise a TimeSeries
                    H_back=TimeSeries(XH,sample_rate=fs)
                    # Calculating the ASD so tha we can use it for whitening later
                    asdH=H_back.asd(1,0.5)                                    
                    # Calculating the one sided fft of the template and
                    # we get rid of the DC value and everything above fs/2.
                    injH_fft_0=np.fft.fft(injH)                       
                    injH_fft_0N=np.abs(injH_fft_0[1:int(t*fs/2)+1]) 

                    SNR0H=np.sqrt(param*2*(1/t)*np.sum(np.abs(injH_fft_0N
                             *injH_fft_0N.conjugate())[t*fl-1
                                :t*fm-1]/PSDH[t*fl-1:t*fm-1]))

                if 'L' in detectors:


                    # Calling the real noise segments
                    noiseL=noise_segL[ind['L'][i]:ind['L'][i]+t*fs]  
                    # Generating the PSD of it
                    dum_fig=plt.figure()
                    p, f = plt.psd(noiseL, Fs=fs, NFFT=fs, visible=False) 
                    p, f=p[1::],f[1::]
                    plt.close(dum_fig) 
                    # Feeding the PSD to generate the sudo-real noise.            
                    PSDL,XL,TL=simulateddetectornoise([f,p],t,fs,10,fs/2)  
                    # Calling the templates generated with PyCBC
                    injL=load_inj(dataset,injectionL[inj_ind],'L')
                    # Saving the length of the injection
                    inj_len=len(injL)/fs   

                    # I put a random offset for all injection, so that
                    # the signal is not always in the same place
                    if inj_len>length: injL = injL[int(inj_len-length)*fs:]
                    if inj_len<length: injL = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injL
                                    ,np.zeros(int(fs*(length-inj_len)/2))))           
                    if 'L' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injL = injL=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injL[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injL = injL=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injL[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))  
                    # Making the noise a TimeSeries
                    L_back=TimeSeries(XL,sample_rate=fs)
                    # Calculating the ASD so tha we can use it for whitening later
                    asdL=L_back.asd(1,0.5)                                    
                    # Calculating the one sided fft of the template and
                    # we get rid of the DC value and everything above fs/2.
                    injL_fft_0=np.fft.fft(injL)                       
                    injL_fft_0N=np.abs(injL_fft_0[1:int(t*fs/2)+1]) 

                    SNR0L=np.sqrt(param*2*(1/t)*np.sum(np.abs(injL_fft_0N
                             *injL_fft_0N.conjugate())[t*fl-1:t*fm-1]
                                 /PSDL[t*fl-1:t*fm-1]))


                if 'V' in detectors:

                    # Calling the real noise segments
                    noiseV=noise_segV[ind['V'][i]:ind['V'][i]+t*fs]  
                    # Generating the PSD of it
                    dum_fig=plt.figure()
                    p, f = plt.psd(noiseV, Fs=fs, NFFT=fs, visible=False) 
                    p, f=p[1::],f[1::]
                    plt.close(dum_fig) 
                    # Feeding the PSD to generate the sudo-real noise.            
                    PSDV,XV,TV=simulateddetectornoise([f,p],t,fs,10,fs/2)  
                    # Calling the templates generated with PyCBC
                    injV=load_inj(dataset,injectionV[inj_ind],'V')
                    # Saving the length of the injection
                    inj_len=len(injV)/fs   

                    # I put a random offset for all injection, so that
                    # the signal is not always in the same place
                    if inj_len>length: injV = injV[int(inj_len-length)*fs:]
                    if inj_len<length: injV = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injV
                                    ,np.zeros(int(fs*(length-inj_len)/2))))
                    if 'V' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injV = injV=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injV[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injV = injV=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injV[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))     
                    # Making the noise a TimeSeries
                    V_back=TimeSeries(XV,sample_rate=fs)
                    # Calculating the ASD so tha we can use it for whitening later
                    asdV=V_back.asd(1,0.5)                                    
                    # Calculating the one sided fft of the template and
                    # we get rid of the DC value and everything above fs/2.
                    injV_fft_0=np.fft.fft(injV)                       
                    injV_fft_0N=np.abs(injV_fft_0[1:int(t*fs/2)+1]) 

                    SNR0V=np.sqrt(param*2*(1/t)*np.sum(np.abs(injV_fft_0N
                             *injV_fft_0N.conjugate())[t*fl-1:t*fm-1]
                                 /PSDV[t*fl-1:t*fm-1]))


                # Calculation of combined SNR   
                SNR0=0
                if 'H' in detectors: SNR0+=SNR0H**2
                if 'L' in detectors: SNR0+=SNR0L**2     
                if 'V' in detectors: SNR0+=SNR0V**2
                SNR0=np.sqrt(SNR0)

                if 'H' in detectors:
                    # Tuning injection amplitude to the SNR wanted
                    fftH_cal=(SNR_FIN/SNR0)*injH_fft_0         
                    injH_cal=np.real(np.fft.ifft(fftH_cal*fs))
                    HF=TimeSeries(XH+injH_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    h=HF.whiten(1,0.5,asd=asdH)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)] 

                if 'L' in detectors:
                    # Tuning injection amplitude to the SNR wanted
                    fftL_cal=(SNR_FIN/SNR0)*injL_fft_0         
                    injL_cal=np.real(np.fft.ifft(fftL_cal*fs))
                    LF=TimeSeries(XL+injL_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    l=LF.whiten(1,0.5,asd=asdL)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)] 

                if 'V' in detectors:
                    # Tuning injection amplitude to the SNR wanted
                    fftV_cal=(SNR_FIN/SNR0)*injV_fft_0        
                    injV_cal=np.real(np.fft.ifft(fftV_cal*fs))
                    VF=TimeSeries(XV+injV_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    v=VF.whiten(1,0.5,asd=asdV)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)] 

                dumie=[]
                if 'H' in detectors: dumie.append(np.array(h))
                if 'L' in detectors: dumie.append(np.array(l))
                if 'V' in detectors: dumie.append(np.array(v))


                DATA[str(SNR_FIN)].append(dumie)
            
            DATA[str(SNR_FIN)]=np.array(DATA[str(SNR_FIN)]).transpose((0,2,1))
        #######################
        #                     #
        # CASE OF REAL NOISE  #       
        #                     #
        #######################

    if noise_type=='real':
        
        param=1
        
        if 'H' in detectors: noise_segH=load_noise(fs,noise_file[0],'H',noise_file[1])
        if 'L' in detectors: noise_segL=load_noise(fs,noise_file[0],'L',noise_file[1])
        if 'V' in detectors: noise_segV=load_noise(fs,noise_file[0],'V',noise_file[1])
        
        
        for SNR_FIN in snr_list:
            
            DATA[str(SNR_FIN)]=[]
            
            ind=index_combinations(detectors = detectors
                       ,lags = 1
                       ,length = length
                       ,fs = fs
                       ,size = size
                       ,start_from_sec=starting_point)
        
            for i in range(0,size):
                
                
                if 'H' in detectors: inj_ind=i
                elif 'L' in detectors: inj_ind=i  
                elif 'V' in detectors: inj_ind=i
                
                if 'H' in detectors:

                    # Calling the real noise segments
                    noiseH=noise_segH[ind['H'][i]:ind['H'][i]+t*fs]  
                    # Calculatint the psd of FFT=1s
                    dum_fig=plt.figure()
                    p, f = plt.psd(noiseH, Fs=fs,NFFT=fs)
                    plt.close(dum_fig) 
                    # Interpolate so that has t*fs values
                    psd_int=interp1d(f,p)                                     
                    PSDH=psd_int(np.arange(0,fs/2,1/t))
                    # Calling the templates generated with PyCBC
                    injH=load_inj(dataset,injectionH[inj_ind],'H')
                    # Saving the length of the injection
                    inj_len=len(injH)/fs                                  

                    # I put a random offset for all injection so that 
                    # the signal is not always in the same place.
                    if inj_len>length: injH = injH[int(inj_len-length)*fs:]
                    if inj_len<length: injH = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injH
                                    ,np.zeros(int(fs*(length-inj_len)/2))))            
                    if 'H' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injH = injH=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injH[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injH = injH=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injH[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))    
                    # Making the noise a TimeSeries
                    H_back=TimeSeries(noiseH,sample_rate=fs)
                    # Calculating the ASD so tha we can use it for whitening later
                    asdH=H_back.asd(1,0.5)                                    

                    # Calculating the one sided fft of the template and
                    # we get rid of the DC value and everything above fs/2.
                    injH_fft_0=np.fft.fft(injH)                       
                    injH_fft_0N=np.abs(injH_fft_0[1:int(t*fs/2)+1])  

                    SNR0H=np.sqrt(param*2*(1/t)*np.sum(np.abs(injH_fft_0N
                            *injH_fft_0N.conjugate())[t*fl-1:t*fm-1]
                                    /PSDH[t*fl-1:t*fm-1]))

                if 'L' in detectors:

                    # Calling the real noise segments
                    noiseL=noise_segL[ind['L'][i]:ind['L'][i]+t*fs]  
                    # Calculatint the psd of FFT=1s
                    dum_fig=plt.figure()
                    p, f = plt.psd(noiseL, Fs=fs,NFFT=fs)
                    plt.close(dum_fig) 
                    # Interpolate so that has t*fs values
                    psd_int=interp1d(f,p)                                     
                    PSDL=psd_int(np.arange(0,fs/2,1/t))
                    # Calling the templates generated with PyCBC
                    injL=load_inj(dataset,injectionL[inj_ind],'L')
                    # Saving the length of the injection
                    inj_len=len(injL)/fs  

                    # I put a random offset for all injection so that
                    # the signal is not always in the same place.
                    if inj_len>length: injL = injL[int(inj_len-length)*fs:]
                    if inj_len<length: injL = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injL
                                    ,np.zeros(int(fs*(length-inj_len)/2))))           
                    if 'L' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injL = injL=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injL[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injL = injL=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injL[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))  
                    # Making the noise a TimeSeries
                    L_back=TimeSeries(noiseL,sample_rate=fs)
                    # Calculating the ASD so tha we can use it for whitening later
                    asdL=L_back.asd(1,0.5)                                    

                    # Calculating the one sided fft of the template and
                    # we get rid of the DC value and everything above fs/2.
                    injL_fft_0=np.fft.fft(injL)                       
                    injL_fft_0N=np.abs(injL_fft_0[1:int(t*fs/2)+1])

                    SNR0L=np.sqrt(param*2*(1/t)*np.sum(np.abs(injL_fft_0N
                            *injL_fft_0N.conjugate())[t*fl-1:t*fm-1]
                                    /PSDL[t*fl-1:t*fm-1]))

                if 'V' in detectors:

                    # Calling the real noise segments
                    noiseV=noise_segV[ind['V'][i]:ind['V'][i]+t*fs]  
                    # Calculatint the psd of FFT=1s
                    dum_fig=plt.figure()
                    p, f = plt.psd(noiseV, Fs=fs,NFFT=fs)
                    plt.close(dum_fig) 
                    # Interpolate so that has t*fs values
                    psd_int=interp1d(f,p)                                     
                    PSDV=psd_int(np.arange(0,fs/2,1/t))
                    # Calling the templates generated with PyCBC
                    injV=load_inj(dataset,injectionV[inj_ind],'V')
                    # Saving the length of the injection
                    inj_len=len(injV)/fs  

                    # I put a random offset for all injection so that
                    # the signal is not always in the same place.
                    if 'H' not in detectors:
                        if length==inj_len:                                   
                            disp = np.random.randint(0,int(length*fs/2))      
                        elif length > inj_len:                      
                            disp = np.random.randint(-int(fs*(length-inj_len)/2)   
                                                     ,int(fs*(length-inj_len)/2)) 
                    # I put a random offset for all injection so that 
                    # the signal is not always in the same place.
                    if inj_len>length: injV = injV[int(inj_len-length)*fs:]
                    if inj_len<length: injV = np.hstack((np.zeros(int(fs*(length
                                    -inj_len)/2))
                                    , injV
                                    ,np.zeros(int(fs*(length-inj_len)/2))))
                    if 'V' == detectors[0]:

                        disp = np.random.randint(-int(fs*(length-inj_len)/2)
                                                 ,int(inj_len*fs/2))

                    if disp >= 0: injV = injV=np.hstack((np.zeros(int(fs*(t
                                    -length)/2))
                                    , injV[disp:]
                                    ,np.zeros(int(fs*(t-length)/2)+disp)))

                    if disp < 0: injV = injV=np.hstack((np.zeros(int(fs*(t
                                    -length)/2)-disp)
                                    , injV[:disp]
                                    ,np.zeros(int(fs*(t-length)/2))))    
                    # Making the noise a TimeSeries
                    V_back=TimeSeries(noiseV,sample_rate=fs)
                    # Calculating the ASD so tha we can use it for whitening later
                    asdV=V_back.asd(1,0.5)                                    

                    # Calculating the one sided fft of the template and
                    # we get rid of the DC value and everything above fs/2.
                    injV_fft_0=np.fft.fft(injV)                       
                    injV_fft_0N=np.abs(injV_fft_0[1:int(t*fs/2)+1])

                    SNR0V=np.sqrt(param*2*(1/t)*np.sum(np.abs(injV_fft_0N
                            *injV_fft_0N.conjugate())[t*fl-1:t*fm-1]
                                    /PSDV[t*fl-1:t*fm-1]))



                # Calculation of combined SNR
                SNR0=0
                if 'H' in detectors: SNR0+=SNR0H**2
                if 'L' in detectors: SNR0+=SNR0L**2     
                if 'V' in detectors: SNR0+=SNR0V**2
                SNR0=np.sqrt(SNR0)

                if 'H' in detectors:

                    # Tuning injection amplitude to the SNR wanted
                    fftH_cal=(SNR_FIN/SNR0)*injH_fft_0         
                    injH_cal=np.real(np.fft.ifft(fftH_cal*fs))
                    HF=TimeSeries(noiseH+injH_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    h=HF.whiten(1,0.5,asd=asdH)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)]

                if 'L' in detectors:

                    # Tuning injection amplitude to the SNR wanted
                    fftL_cal=(SNR_FIN/SNR0)*injL_fft_0         
                    injL_cal=np.real(np.fft.ifft(fftL_cal*fs))
                    LF=TimeSeries(noiseL+injL_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    l=LF.whiten(1,0.5,asd=asdL)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)]

                if 'V' in detectors:

                    # Tuning injection amplitude to the SNR wanted
                    fftV_cal=(SNR_FIN/SNR0)*injV_fft_0         
                    injV_cal=np.real(np.fft.ifft(fftV_cal*fs))
                    VF=TimeSeries(noiseV+injV_cal,sample_rate=fs,t0=0)
                    #Whitening final data
                    v=VF.whiten(1,0.5,asd=asdV)[int(((t-length)/2)*fs):
                                                int(((t+length)/2)*fs)]


                dumie=[]
                if 'H' in detectors: dumie.append(np.array(h))
                if 'L' in detectors: dumie.append(np.array(l))
                if 'V' in detectors: dumie.append(np.array(v))


                DATA[str(SNR_FIN)].append(dumie)
            DATA[str(SNR_FIN)]=np.array(DATA[str(SNR_FIN)]).transpose((0,2,1))
     
    snrs=[]
    acc=[]
    error=[]
    score_f=[]
    
    if isinstance(model,str):
        trained_model = load_model('/home/vasileios.skliris/EMILY/trainings/'+model +'.h5')
    else:
        trained_model = model    #If model is not already in the script you import it my calling the name 
        
    for SNR_FIN in snr_list:
        
        data=DATA[str(SNR_FIN)]
        scores=trained_model.predict_proba(data, batch_size=1, verbose=0)[:,1]

        
        snrs.append(SNR_FIN)
        error.append(np.std(scores))
        acc.append(np.mean(scores))
        score_f.append(scores)
        
    
    
    
    snrs=np.array(snrs)
    acc=np.array(acc)
    error=np.array(error)
    score_f=np.array(score_f)
    
    plot={'snrs':snrs, 'acc': acc, 'error' :error, 'scores':score_f}
        
    return(DATA,plot)


def FAR_gen(model
           ,date_ini
           ,size
           ,length
           ,fs
           ,t
           ,detectors
           ,lags):
    
    from mly.generators import dirlist
    
    model_ref_name=model.split('.')[0]
    num_of_sets=1
    date_list=dirlist( null_path+'/ligo_data/2048')

    # Generating a list with all the available dates
    date=date_list[date_list.index(date_ini)]
    # Calculating the index of the initial date
    counter=date_list.index(date_ini)             


    # Calculation of the duration 
    # Here we infere the duration needed given the lags used in the method

    if lags==1:
        duration_need = size*num_of_sets*length
        tail_crop=0
    if lags%2 == 0:
        duration_need = ceil(size*num_of_sets/(lags*(lags-2)))*lags*length
        tail_crop=lags*length
    if lags%2 != 0 and lags !=1 :
        duration_need = ceil(size*num_of_sets/(lags*(lags-1)))*lags*length
        tail_crop=lags*length


    # Creation of lists that indicate characteristics of the segments based on the duration needed. 
    # These are used for the next step.

    duration_total = 0
    duration, gps_time, seg_list=[],[],[]

    while duration_need > duration_total:
        counter+=1
        segments=dirlist( null_path+'/ligo_data/'+str(fs)+'/'+date+'/H')
        print(date)
        for seg in segments:
            for j in range(len(seg)):
                if seg[j]=='_': 
                    gps, dur = seg[j+1:-5].split('_')
                    break

            duration.append(int(dur))
            gps_time.append(int(gps))
            seg_list.append([date,seg])

            duration_total+=(int(dur)-3*t-tail_crop)
            print('    '+seg)

            if duration_total > duration_need: break
        if counter==len(date_list): counter==0        
        date=date_list[counter]

    size_list=[]            # Sizes for each generation of noise 
    starting_point_list=[]  # Starting points for each generation of noise(s)
    seg_list_2=[]           # Segment names for each generation of noise
    number_of_set=[]        # No of set that this generation of noise will go
    name_list=[]            # List with the name of the set to be generated
    number_of_set_counter=0 # Counter that keeps record of how many                                         
                            # instantiations have left to be generated 
                            # to complete a set


    set_num=1

    for i in range(len(np.array(seg_list)[:,1])):

        # local size indicates the size of the file left for generation of  
        # datasets, when it is depleted the algorithm moves to the next 
        # segment. Here we infere the local size given the lags used in the             # method

        if lags==1:    # zero lag case
            local_size=ceil((duration[i]-3*t-tail_crop)/length)
        if lags%2 == 0:
            local_size=ceil((duration[i]-3*t-tail_crop
                            )/length/lags)*lags*(lags-2)
        if lags%2 != 0 and lags !=1 :
            local_size=ceil((duration[i]-3*t-tail_crop
                            )/length/lags)*lags*(lags-1)

        # starting point always begins with the window of the psd 
        # to avoid deformed data of the begining    
        local_starting_point=t

        # There are three cases when a segment is used.        date=date_list[counter]

        # 1. That it has to fill a previous set first and then 
        # move to the next
        # 2. That it is the first set so there is no previous set to fill
        # 3. It is the too small to fill so its only part of a set.
        # Some of them go through all the stages

        if (len(size_list) > 0 and number_of_set_counter > 0 
            and local_size >= size-number_of_set_counter):

            # Saving the size of the generation
            size_list.append(size-number_of_set_counter)
            # Saving the name of the date file and seg used
            seg_list_2.append(seg_list[i])
            # Saving the startint_point of the generation
            starting_point_list.append(local_starting_point)      

            # Update the the values for the next set
            local_size-=(size-number_of_set_counter)
            if lags==1: 
                local_starting_point+=(size-number_of_set_counter)*length

            if lags%2 == 0:
                local_starting_point+=(ceil((size-number_of_set_counter)
                /lags/(lags-2))*lags*length)

            if lags%2 != 0 and lags !=1 :
                local_starting_point+=(ceil((size-number_of_set_counter)
                /lags/(lags-1))*lags*length)

            number_of_set_counter+=(size-number_of_set_counter)

            # If this generation completes the size of a whole set 
            # (with size=size) it changes the labels
            if number_of_set_counter == size:
                number_of_set.append(set_num)
                if size_list[-1]==size: 
                    name_list.append(str(set_num))
                else:
                    name_list.append('part_of_'+str(set_num))
                set_num+=1
                number_of_set_counter=0
                if set_num > num_of_sets: break

            elif number_of_set_counter < size:
                number_of_set.append(set_num)
                name_list.append('part_of_'+str(set_num))

        if (len(size_list) == 0 or number_of_set_counter==0):
            while local_size >= size:
                # Generate data with size 10000 with final name of       
                # 'name_counter'
                size_list.append(size)
                seg_list_2.append(seg_list[i])
                starting_point_list.append(local_starting_point)

                #Update the the values for the next set
                local_size-=size
                if lags==1: local_starting_point+=size*length
                if lags%2 == 0:
                    local_starting_point+=(ceil(size/lags/(lags-2))
                                           *lags*length)
                if lags%2 != 0 and lags !=1 : 
                    local_starting_point+=(ceil(size/lags
                    /(lags-1))*lags*length)

                number_of_set_counter+=size

                # If this generation completes the size of a whole set
                # (with size=size) it changes the labels
                if number_of_set_counter == size:
                    number_of_set.append(set_num)
                    if size_list[-1]==size: 
                        name_list.append(str(set_num))
                    else:
                        name_list.append('part_of_'+str(set_num))
                    set_num+=1
                    if set_num > num_of_sets: break
                    number_of_set_counter=0

        if (local_size < size and local_size >0 and set_num <= num_of_sets):

            # Generate data with size 'local_size' with local name 
            # to be fused with later one
            size_list.append(local_size)
            seg_list_2.append(seg_list[i])
            starting_point_list.append(local_starting_point)

            # Update the the values for the next set

            # Saving a value for what is left for the next seg to generate
            number_of_set_counter+=local_size  

            # If this generation completes the size of a whole set 
            # (with size=size) it changes the labels
            if number_of_set_counter == size:
                number_of_set.append(set_num)
                if size_list[-1]==size: 
                    name_list.append(str(set_num))
                else:
                    name_list.append('part_of_'+str(set_num))
                set_num+=1
                if set_num > num_of_sets: break
                number_of_set_counter=0

            elif number_of_set_counter < size:
                number_of_set.append(set_num)
                name_list.append('part_of_'+str(set_num))

    d={'segment' : seg_list_2, 'size' : size_list 
       , 'start_point' : starting_point_list, 'set' : number_of_set
       , 'name' : name_list}

    print('These are the details of the datasets to be generated: \n')
    #print((d['segment']), (d['size']),(d['start_point']) ,(d['name']))
    for i in range(len(d['segment'])):
        print(d['segment'][i], d['size'][i], d['start_point'][i] ,d['name'][i])
    
    print('Should we proceed to the FAR test?'
            +' data y/n ? \n \n')

    answer=input()

    if answer in ['no','n']:
        print('Exiting procedure')
        return

    elif answer in ['yes','y']:

        print('Of course lord commander ...')
        print('Type the name of the FAR test directory:')

        dir_name=input()

        path= os.getcwd()+'/'


        print('The current path of the directory is: \n'+path+'\n')
        print('Do you wanna change the path y/n ?')

        answer2=input()

        if answer2 in ['yes','y']:
            print('Insert complete new path ex. /home/....')
            path=input()
            if path=='exit': return

            while not (os.path.isdir(path)):
                print('Path: '+path+' is not existing. Try again or type '
                      +'exit to exit the procedure.')
                path=input()
                if path=='exit': return

        if answer2 in ['no','n']:
            if os.path.isdir(path+dir_name):
                print('Already existing '+dir_name+' directory, do want to'
                      +' delete it? y/n')
                answer3=input()
                if answer3=='y':
                    os.system('rm -r '+path+dir_name)
                elif answer3=='n':
                    return
            print('Initiating procedure ...')
            os.system('mkdir '+path+dir_name)
            print('Creation of directory complete: '+path+dir_name)

        os.system('cd '+path+dir_name)


        for i in range(len(d['segment'])):
         
            with open(path+dir_name+'/'+'far_test_'+d['name'][i]+'_'
                +str(d['size'][i])+'.py','w') as f:

                f.write('import sys \n')
                f.write('try: \n')
                f.write('    import mly \n')
                f.write('except: \n')
                f.write('    sys.path.append(\'/home/vasileios.skliris/mly/\')\n')# # # #
                f.write('from mly.generators import * \n')
                f.write('from mly.validators import FAR_test \n' )
                f.write('import os \n')
                f.write('import pickle \n')

            
                comand=(
                'pr=FAR_test(model=\''+model+'\''+
                           ',length='+str(length)+           
                           ',fs='+str(fs)+              
                           ',size='+str(d['size'][i])+             
                           ',detectors=\''+detectors+'\''
                           ',spec=False'+
                           ',phase=False'+
                           ',res=128'+
                           ',noise_file='+str(d['segment'][i])+
                           ',t='+str(t)+             
                           ',lags='+str(lags)+
                           ',starting_point='+str(d['start_point'][i])+
                           ',model_source_path=\''+str(os.getcwd())+'/\')')

                f.write(comand+'\n')
                
                f.write('with open(\''+path+dir_name+'/'+model_ref_name+'_'+str(d['size'][i])+'.pkl\',\'wb\') as f:\n')
                f.write('    pickle.dump(pr, f, pickle.HIGHEST_PROTOCOL)')

        with open(path+dir_name+'/'+'far_test.sh','w') as f2:

            f2.write('#!/bin/sh \n\n')
            for i in range(len(d['segment'])):
                
                f2.write('nohup python '+path+dir_name+'/'+'far_test_'+d['name'][i]
                    +'_'+str(d['size'][i])+'.py > ' +path+dir_name+'/out_'
                    +d['name'][i]+'_'+str(d['size'][i])+'.out & \n' )


    #     with open(path+dir_name+'/info.txt','w') as f3:
    #         f3.write('INFO ABOUT DATASETS GENERATION \n\n')
    #         f3.write('fs: '+str(fs)+'\n')
    #         f3.write('length: '+str(length)+'\n')
    #         f3.write('window: '+str(t)+'\n')
    #         f3.write('lags: '+str(lags)+'\n'+'\n')

    #         for i in range(len(d['segment'])):
    #             f3.write(d['segment'][i][0]+' '+d['segment'][i][1]
    #                      +' '+str(d['size'][i])+' '
    #                      +str(d['start_point'][i])+'_'+d['name'][i]+'\n')

        print('All set. Initiate dataset generation y/n?')
        answer4=input()

        if answer4 in ['y','Y']:
            os.system('sh '+path+dir_name+'/far_test.sh')
            #return
        else:
            print('Data generation canceled')
            os.system('cd')
            os.system('rm -r '+path+dir_name)
            return

    return



def finalise_far(path):
    
    from mly.generators import dirlist
    import pickle
    files=dirlist(path)
    merging_flag=False

    print('Running diagnostics for file: '+path+'  ... \n') 
    py, dat=[],[]
    for file in files:
        if file[-3:]=='.py':
            py.append(file)
        if file[-4:]=='.pkl': #In the future the type of file might change
            dat.append(file)

    # Checking if all files that should have been generated 
    # from FAR_gen are here
    
    if len(dat)==len(py):
        print('Files succesfully generated, all files are here')
        print(len(dat),' out of ',len(py))
        merging_flag=True  # Declaring that merging can happen now
    
    elif len(dat)>len(py):
        print('There are some files already merged or finalised\n')
        print('Files succesfully generated, all files are here')
        print(len(dat),' out of ',len(py))
        merging_flag=True  # Declaring that merging can happen now

    
    else:
        failed_py=[]
        for i in range(len(py)):
            py_id=py[i].split('_')[-1][:-3]
            counter=0
            for dataset in dat:
                if py_id in dataset:
                    counter=1
            if counter==0:
                print(py[i],' failed to proceed')
                failed_py.append(py[i])



    if merging_flag==False:
        print('\n\nDo you want to try and run again the failed procedurs? y/n')
        answer1=input()
        
        if answer1 in ['Y','y','yes']:
            with open(path+'/far_test_redo.sh','w') as fnew:
                fnew.write('#!/bin/sh\n\n')
                with open(path+'/far_test.sh','r') as f:
                    for line in f:
                        for pyid in failed_py:
                            if pyid in line:
                                fnew.write(line+'\n')
                                break

            print('All set. The following generators are going to run again:\n')
            for pyid in failed_py:
                print(pyid)

            print('\n\nInitiate dataset generation y/n?')
            answer2=input()

            if answer2 in ['y','Y','yes']:
                os.system('sh '+path+'/far_test_redo.sh')
                return
            else:
                print('Data generation canceled')
                os.system('rm '+path+'/far_test_redo.sh')
                return
            
            
        elif answer1 in ['N','n','no','exit']:
            print('Exiting procedure')
            return
        
    if merging_flag==True:
            
        print('\n Do you wanna proceed to the merging of the FAR test resaults? y/n')
        answer3=input()
              
        if answer3 in ['n','N','no','NO','No']:
            print('Exiting procedure')
            return
        
        elif answer3 in ['y','Y','yes','Yes']:  
            
            pr=[]
            count=0
            for file in files:
                if file[-4:]=='.pkl':
                    with open(path+'/'+file, 'rb') as f:
                        dic = pickle.load(f)

                    if count==0:
                        count+=1
                        for i in range(len(dic.keys())): pr.append([])
                    if count==1:
                        for i in range(len(dic.keys())):
                            pr[i]+=(dic[list(dic.keys())[i]]).tolist()


            pr_s=np.array(sorted(np.transpose(np.array(pr)),  key=lambda x :x[0], reverse=True))


            pr_d={}
            for i in range(pr_s.shape[1]):
                pr_d[list(dic.keys())[i]] = pr_s[:,i]
                
            dir_name=path.split('/')[-1]
                
            with open('/'.join(path.split('/')[:-1])+'/'+dir_name+'.pkl','wb') as f:
                pickle.dump(pr_d, f, pickle.HIGHEST_PROTOCOL)

            print('\n\nFAR test is complete!')
             
                
            # Deleting unnescesary file in the folder
            print('\n Do you want to delete unnecessary files? y/n')
            
            answer4=input()
            if answer4 in ['n','N','no','NO','No']:
                return

            elif answer4 in ['y','Y','yes','Yes']: 
                os.system('rm -r '+path)
                
                print('File is finalised')
                return
