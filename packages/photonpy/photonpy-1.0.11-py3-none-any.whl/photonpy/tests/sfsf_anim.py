# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 02:39:33 2020

@author: jcnossen1
"""

import numpy as np
import matplotlib.pyplot as plt

import photonpy.smlm.util as su
from photonpy.cpp.context import Context
import photonpy.cpp.gaussian as gaussian

from photonpy.cpp.simflux import SIMFLUX


from matplotlib import animation, rc
from IPython.display import HTML

mod = np.array([
     [0, 1.8, 0, 0.95, 0, 1/6],
     [1.9, 0, 0, 0.95, 0, 1/6],
     [0, 1.8, 0, 0.95, 2*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 2*np.pi/3, 1/6],
     [0, 1.8, 0, 0.95, 4*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 4*np.pi/3, 1/6]
])

        
with Context(debugMode=True) as ctx:
    g = gaussian.Gaussian(ctx)

    roisize=26
    psf = g.CreatePSF_XYZIBg(roisize, gaussian.Gauss3D_Calibration(), cuda=True)
    sf_theta=[[roisize//2, roisize//2, 0.0, 10000, 5]]

    #psf = g.CreatePSF_XYIBg(roisize, sigma=1.8, cuda=True)
    #sf_theta=[[roisize//2, roisize//2, 1000.0, 5]]
    sf_theta=np.repeat(sf_theta,100,0)
    
    #s = np.linspace(-3.0,3.0,len(sf_theta))
    s = np.linspace(0,2*np.pi,len(sf_theta))
    sf_theta[:,0] += 3*np.cos(s)
    sf_theta[:,1] += 3*np.cos(s)
    if psf.NumParams()==5: 
        sf_theta[:,2] = 3*np.sin(s)
    
    offsets = np.zeros((len(mod), psf.NumParams()-2))
    ang = np.linspace(0,2*np.pi, len(mod), endpoint=False)
    R = 7
    offsets[:,0] = R*np.cos(ang)
    offsets[:,1] = R*np.sin(ang)

    s = SIMFLUX(ctx)
    sf_estim = s.CreateSFSFEstimator(psf, mod, offsets, True)
    
    print(sf_estim.sampleshape)
    print(sf_estim.ParamFormat())

    ev = sf_estim.ExpectedValue(sf_theta)  

    deriv, ev = sf_estim.Derivatives(sf_theta)
    deriv=deriv[:,:4]
    fig,ax=plt.subplots(1,deriv.shape[1],sharey=True)
    im = [] 
    for k in range(deriv.shape[1]):
        im.append(ax[k].imshow(deriv[0,k]))
        ax[k].set_title(sf_estim.colnames[k])

    
    # animation function. This is called sequentially
    def animate(fr):
        for k,i in enumerate(im): 
            i.set_data(deriv[fr,k])
        return im


    # call the animator. blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate,
                                   frames=len(deriv), interval=20, blit=True)

    #plt.close();

    fps=20
    anim.save('sfsf.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])

    HTML(anim.to_html5_video())  
    
    print('done')