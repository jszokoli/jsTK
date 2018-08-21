sys.path.append("/usr/lib64/python2.6/site-packages")
import PyOpenColorIO as ocio
R_in = .245
G_in = .325
B_in = .644


###ACES to sRGB

def Aces2sRGB(R_in,G_in,B_in):
    config = ocio.GetCurrentConfig()
    proccessor = config.getProcessor("ACES - ACEScg", "Utility - Rec.709 - Display")
    
    postVal =  proccessor.applyRGB([R_in,G_in,B_in])
    
    proccessor2 = config.getProcessor("Utility - Rec.709 - Camera", "Utility - Linear - sRGB")
    postVal2 =  proccessor2.applyRGB([ postVal[0],postVal[1],postVal[2] ])
    return postVal2


def sRGB2Aces(R_in,G_in,B_in):
    config = ocio.GetCurrentConfig()
    proccessor = config.getProcessor("Utility - Linear - sRGB", "Utility - Rec.709 - Camera")
    
    postVal =  proccessor.applyRGB([R_in,G_in,B_in])
    
    proccessor2 = config.getProcessor("Utility - Rec.709 - Display","ACES - ACEScg")
    postVal2 =  proccessor2.applyRGB([ postVal[0],postVal[1],postVal[2] ])
    return postVal2


### Non OCIO


    
###ACES to rec709

R_out =  1.70499877 * R_in +  -0.62174759 * G_in +  -0.08325146 * B_in
G_out =  -0.13025872 * R_in +  1.14080169 * G_in + -0.01054445 * B_in
B_out =  -0.02400747 * R_in +  -0.12898279 * G_in +  1.15299059 * B_in

print R_out, G_out, B_out

#ACES to rec709 TO
MatrixTransform> {matrix: [0.952552, 0, 9.36786e-05, 0, 0.343966, 0.728166, -0.0721325, 0, 0, 0, 1.00883, 0, 0, 0, 0, 1]}
#ACES to rec709 Inverse
MatrixTransform> {matrix: [3.2096, -1.55743, -0.495805, 0, -0.970989, 1.88517, 0.0394894, 0, 0.0597193, -0.210104, 1.14312, 0, 0, 0, 0, 1]}
