# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:00:46 2020

@author: jcnossen1
"""

from photonpy.cpp.context import Context
import numpy as np
import matplotlib.pyplot as plt
import photonpy.cpp.multi_emitter as multi_emitter
from photonpy.cpp.gaussian import Gaussian, Gauss3D_Calibration
from photonpy.cpp.simflux import SIMFLUX
import photonpy.cpp.com as com

useSimflux = True

# Simflux modulation patterns
mod = np.array([
     [0, 1.8, 0, 0.95, 0, 1/6],
     [1.9, 0, 0, 0.95, 0, 1/6],
     [0, 1.8, 0, 0.95, 2*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 2*np.pi/3, 1/6],
     [0, 1.8, 0, 0.95, 4*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 4*np.pi/3, 1/6]
])



def generate_positions(N,E,K,roisize,bg):
    """
    Generate a parameter vector with either 2D or 3D layout:
    2D: background, X0, Y0, I0, X1, Y1, I1, ....
    3D: background, X0, Y0, Z0, I0, X1, Y1, Z1, I1, ....
    
    N: Number of ROIs
    E: Number of emitters per ROI
    K: Number of parameters per emitter (3 for 2D or 4 for 3D)
    """
    pts = np.zeros((N,E*K+1))
    pts[:,0] = bg #bg
    border = 4
    for k in range(E):
        if K==3: # 2D case
            pos = np.random.uniform([border,border,500],[roisize-1-border,roisize-1-border,800],size=(N,K))
        if K==4: # 3D case
            pos = np.random.uniform([border,border,0,400],[roisize-border-1,roisize-border-1,0,600],size=(N,K))

        pts[:,np.arange(1,K+1)+k*K] = pos

    return pts

def result_to_str(result):
    K = 3
    E = len(result)//K
    xpos = result[1::K]
    ypos = result[2::K]
    I = result[3::K]  # in 3D it would be 4::K
        
    prev = np.get_printoptions()['precision']
    np.set_printoptions(precision=1)
    s = f"{E} emitters: I={I}, X={xpos}, Y={ypos}"
    np.set_printoptions(precision=prev)
    return s


def plot_traces(traces, K):
    numE = traces.shape[1]//K

    fig,axes=plt.subplots(K, 1, sharex=True)

    def plot_param(idx, name):
        ax=axes[idx-1]
        numit = traces.shape[0]
        for e in range(numE):
            ax.plot(np.arange(numit), traces[:,e*K+idx], label=f'{name}{e}')
        ax.set_title(f'Trace for {name} - {numE} emitters')
        ax.legend()
        ax.set_ylabel(name)
    
    plot_param(1, 'X')
    plot_param(2, 'Y')
    if K==3:    
        plot_param(3, 'I')
    else:
        plot_param(3,'Z')
        plot_param(4,'I')
    
    axes[-1].set_xlabel('Iterations')
    
def compute_error(A, B, K):
    # Make an array of [numemitters, K]. 
    spotsA = A[1:].reshape((-1,K))
    spotsB = B[1:].reshape((-1,K))
    
    # Compute all distances from spots A to B
    sqerr = (spotsA[:,None] - spotsB[None,:])**2
    dist = np.sqrt(np.sum(sqerr[:,:,[0,1]], -1))
    
    # Rearrange the spots based on shortest XY distance
    matching = np.argmin(dist,0)
    return spotsA[matching] - spotsB

with Context(debugMode=False) as ctx:
    sigma = 1.8
    roisize = 20
    E = 3
    N = 3
    pixelsize=0.1
    
    psf = Gaussian(ctx).CreatePSF_XYIBg(roisize, sigma, True)
    sf = SIMFLUX(ctx).CreateEstimator_Gauss2D(sigma, mod, roisize, len(mod), True)
    K = psf.NumParams()-1

    bg = 10
    if useSimflux:     #simflux?
        psf = sf
        bg /= len(mod) # in simflux convention, background photons are spread over all frames
    
    border = 3
    minParam = [border, border, 200, 2]
    maxParam = [roisize-1-border,roisize-1-border, 4000, 20]

    # Create a list of estimator objects, one for each number of emitters
    max_emitters = E
    estimators = [multi_emitter.CreateEstimator(psf, k, ctx, minParam, maxParam) for k in range(1+max_emitters)]
    for e in estimators:
        e.SetLevMarParams(1e-16, 50) # Lambda, max number of iterations
        
    true_pos = generate_positions(N, E, K, roisize, bg)
    smp = estimators[E].GenerateSample(true_pos)
    
    if useSimflux:
        plt.figure()
        plt.imshow(np.concatenate(smp[0],-1))
    
    com_estim = com.CreateEstimator(roisize,ctx)
    
    emittercount = np.ones(N,dtype=np.int32)
    for roi in range(N): # go through all ROIs
    
        roi_smp = smp[roi]

        # First state is only background
        current = [np.mean(roi_smp)]
        current_ev = np.ones(psf.sampleshape) * current[0] # times avg background
        
        numEmitters = 0

        for c in np.arange(1, max_emitters+1):
            residual = np.maximum(0, roi_smp - current_ev)
                        
            residual_com = psf.Estimate([residual])[0][0]
            plt.figure()
            
            img = np.concatenate([residual, roi_smp],-1)
            if sf == psf:
                plt.imshow(np.sum(img, 0))
            else:
                plt.imshow(img)
            plt.scatter(current[1::K], current[2::K], label=f'Current state',marker='X', s=50,color='b')
            plt.scatter(roisize+true_pos[roi,1::K], true_pos[roi,2::K], label=f'True positions',s=50, color='k')
            plt.scatter([residual_com[0]], [residual_com[1]], label=f'Added emitter',marker='x', color='r')
            plt.title(f"Residual to initialize {c} emitters")
            plt.legend()

            current = [*current, residual_com[0], residual_com[1], residual_com[2]]

            print(f"Initial estimate for {c} emitters: {residual_com}")
            current = np.array(current)
            
            results, _, traces = estimators[c].Estimate([roi_smp], initial=[current])
            results = results[0]

            if True:
                plot_traces(traces[0], K)
                    
            current_ev = estimators[c].ExpectedValue([results])[0]
            
            chisq = np.sum( (roi_smp-current_ev)**2 / (current_ev+1e-9))
            std_chisq = np.sqrt(2*psf.samplecount + np.sum(1/np.mean(current_ev)))
        
            # If chi-square > expected value + 2 * std.ev, 
            # then the current estimate is a good representation of the sample
            chisq_threshold = psf.samplecount + std_chisq
            
            accepted = chisq < chisq_threshold
            print(f"chisq: {chisq:.1f} < threshold({chisq_threshold:.1f}): {accepted}")
                        
            img = np.concatenate([current_ev, roi_smp],-1)
            if sf == psf:
                fig,ax=plt.subplots(2,1)
                ax[0].imshow(np.sum(img, 0))
                ax[1].imshow(np.hstack(roi_smp))
                scax = ax[0]
            else:
                plt.figure()
                plt.imshow(img)
                scax = plt.gca()
            scax.set_title(f'{c} emitters: Chi-sq: {chisq:.1f}')
            scax.scatter(roisize+current[1::K], current[2::K], label=f'Previous + Residual',color='b')
            scax.scatter(true_pos[roi,1::K], true_pos[roi,2::K], label=f'True positions',color='k')
            scax.scatter(results[1::K], results[2::K], marker= 'x', label=f'Estimate for {c} emitters',color='r')
            scax.legend()

            current = results
            numEmitters += 1

            if accepted:
                break

        print(f'Final result: {result_to_str(results)}')
        print(f'True: {result_to_str(true_pos[roi])}')

        if E==numEmitters:
            err=compute_error(results, true_pos[roi],K)
            print(err)