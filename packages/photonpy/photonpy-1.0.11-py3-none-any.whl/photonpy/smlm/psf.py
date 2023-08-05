"""
PSF Utilities
"""


from photonpy.cpp.estimator import Estimator
import numpy as np
import matplotlib.pyplot as plt


def psf_to_zstack(psf:Estimator, zrange, intensity=1, bg=0, plot=False):
    
    assert psf.numparams == 5
    
    params = np.zeros((len(zrange),5))
    params[:,0] = psf.sampleshape[0]/2
    params[:,1] = psf.sampleshape[1]/2
    params[:,2] = zrange
    params[:,3] = intensity
    params[:,4] = bg
    
    ev = psf.ExpectedValue(params)
    
    if plot:
        plt.figure()
        plt.imshow(np.concatenate(ev,-1))
        plt.colorbar()
    
    return ev


def render_to_image(psf:Estimator, imgshape, emitters, constants=None):
    
    assert(len(psf.sampleshape)==2) and psf.sampleshape[0]==psf.sampleshape[1]
    
    yx = psf.ParamIndex(['y','x'])
    
    roi_em = emitters*1
    roisize = psf.sampleshape[0]
    roipos = np.clip((roi_em[:,yx] - roisize/2).astype(int), [0,0], imgshape-roisize)
    roi_em[:,yx] -= roipos
        
    rois = psf.ExpectedValue(roi_em, roipos, constants)
    
    return psf.ctx.smlm.DrawROIs(imgshape, rois, roipos)
    
    