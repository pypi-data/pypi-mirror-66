

from photonpy.cpp.context import Context
import numpy as np
import matplotlib.pyplot as plt
import photonpy.cpp.multi_emitter as multi_emitter
from photonpy.cpp.gaussian import Gaussian, Gauss3D_Calibration
from photonpy.cpp.simflux import SIMFLUX
import photonpy.cpp.com as com

# Simflux modulation patterns
mod = np.array([
     [0, 1.8, 0, 0.95, 0, 1/6],
     [1.9, 0, 0, 0.95, 0, 1/6],
     [0, 1.8, 0, 0.95, 2*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 2*np.pi/3, 1/6],
     [0, 1.8, 0, 0.95, 4*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 4*np.pi/3, 1/6]
])



def generate_positions(N,E,K,roisize):
    """
    Generate a parameter vector with either 2D or 3D layout:
    2D: background, X0, Y0, I0, X1, Y1, I1, ....
    3D: background, X0, Y0, Z0, I0, X1, Y1, Z1, I1, ....
    
    N: Number of ROIs
    E: Number of emitters per ROI
    K: Number of parameters per emitter (3 for 2D or 4 for 3D)
    """
    pts = np.zeros((N,E*K+1))
    pts[:,0] = 10 #bg
    for k in range(E):
        if K==3: # 2D case
            pos = np.random.uniform([3,3,600],[roisize-4,roisize-4,1000],size=(N,K))
        if K==4: # 3D case
            pos = np.random.uniform([3,3,0,600],[roisize-4,roisize-4,0,1000],size=(N,K))

        pts[:,np.arange(K)+k*K+1] = pos

    return pts


images=[]

def debugImage(img,label):
    images.append((img,label))


def plotDebugImages():
    for img,label in images:
        plt.figure()
        plt.imshow( np.concatenate(img,-1) )
        plt.colorbar()
        plt.title(label)


with Context(debugMode=True) as ctx:
    sigma = 1.8
    roisize = 20
    E = 3
    N = 2
    #psf = Gaussian(ctx).CreatePSF_XYIBg(roisize, sigma, True)
    psf = SIMFLUX(ctx).CreateEstimator_Gauss2D(sigma, mod, roisize, len(mod), True)
    K = psf.NumParams()-1
    
    border = 3
    minParam = [border, border, 200, 2]
    maxParam = [roisize-1-border,roisize-1-border, 4000, 20]
    
    ctx.smlm.SetDebugImageCallback(debugImage)

    # Create a list of estimator objects, one for each number of emitters
    max_emitters = E
    estimators = [multi_emitter.CreateEstimator(psf, k, ctx, minParam, maxParam) 
                      for k in range(1+max_emitters)]
    for e in estimators:
        e.SetLevMarParams(1e-19, 50)
        
    true_pos = generate_positions(N, E, K, roisize)

    deriv,ev = estimators[E].Derivatives(true_pos)
    
    smp=np.random.poisson(ev)
    for i in range(10):
        estimators[E].Estimate(smp, initial=true_pos)
    
    sf_param = estimators[1].GetEmitterParams(true_pos, 0)

    if len(psf.sampleshape) == 3:
        ev = np.concatenate(ev,-1)

    plt.figure()
    plt.imshow(ev[0])
    plt.colorbar()
    
    plt.figure()
    plt.imshow(np.vstack(np.concatenate(deriv[0], 2)))    

    plotDebugImages()