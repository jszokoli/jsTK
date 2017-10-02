import maya.cmds as cmds
############################
###js_DMC_Calculator v1.0###
############################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create a shelf icon, move js_DMC_Calculator.py to your scripts folder and assign the following command to the shelf.
#import js_DMC_Calculator
#reload(js_DMC_Calculator)

#Version Number################
versionNumber = 'v1.0'###
###############################

### ChangeLog: ################################################################################
###v1.0 Initial Release

def calculateSamples(args=None):
    AA_MAXInput= cmds.intSliderGrp('AAMaxSlider', query=True, value=1)
    AA_MINInput= cmds.intSliderGrp('AAMinSlider', query=True, value=1)
    
    MinShadingRate= cmds.intSliderGrp('AAMinShadeSlider', query=True, value=1)
    
    DMC_Adaptive= cmds.floatSliderGrp('DMCadaptiveAmountSlider', query=True, value=1)
    DMCsubdivMult= cmds.floatSliderGrp('DMCsubdivsMultSlider', query=True, value=1)
    
    DMCminSamples= cmds.intSliderGrp('DMCminSamplesSlider', query=True, value=1)
    localSubdiv= cmds.intSliderGrp('localSubdivSlider', query=True, value=1)
    divideShading = cmds.checkBox('AAshadeDivideOption',query=True,value=1)
 
    AAMax=AA_MAXInput*AA_MAXInput
    
    AAMin=AA_MINInput*AA_MINInput
    
    if AAMin<MinShadingRate:
        AAMin = MinShadingRate
        
    if divideShading == 1:
        DMCMaxImage=localSubdiv*localSubdiv*DMCsubdivMult/AAMax
    else:
        DMCMaxImage=localSubdiv*localSubdiv*DMCsubdivMult
        
    DMCMinImage=DMCMaxImage*(1-DMC_Adaptive)
    
    if DMCMinImage < DMCminSamples:
        DMCMinImage = DMCminSamples
    
    DMCMaxPixel=AAMax*DMCMaxImage
    DMCMinPixel=AAMin*DMCMinImage
    
    outValues = [AAMax,AAMin,DMCMaxImage,DMCMinImage,DMCMaxPixel,DMCMinPixel]
    cmds.textFieldGrp('AAMaxField', edit = True, text=round(AAMax))
    cmds.textFieldGrp('AAMinField', edit = True, text=round(AAMin))
    cmds.textFieldGrp('DMCMaxImageField', edit = True, text=round(DMCMaxImage))
    cmds.textFieldGrp('DMCMinImageField', edit = True, text=round(DMCMinImage))
    cmds.textFieldGrp('DMCMaxPixelField', edit = True, text=round(DMCMaxPixel))
    cmds.textFieldGrp('DMCMinPixelField', edit = True, text=round(DMCMinPixel))



def copyTo(args=None):
    AA_MAXInput= cmds.intSliderGrp('AAMaxSlider', query=True, value=1)
    cmds.setAttr('vraySettings.dmcMaxSubdivs',AA_MAXInput)
    
    AA_MINInput= cmds.intSliderGrp('AAMinSlider', query=True, value=1)
    cmds.setAttr('vraySettings.dmcMinSubdivs',AA_MINInput)
    
    MinShadingRate= cmds.intSliderGrp('AAMinShadeSlider', query=True, value=1)
    cmds.setAttr('vraySettings.minShadeRate',MinShadingRate)
    
    DMC_Adaptive= cmds.floatSliderGrp('DMCadaptiveAmountSlider', query=True, value=1)
    cmds.setAttr('vraySettings.dmcs_adaptiveAmount',DMC_Adaptive)
    
    DMCsubdivMult= cmds.floatSliderGrp('DMCsubdivsMultSlider', query=True, value=1)
    cmds.setAttr('vraySettings.dmcs_subdivsMult',DMCsubdivMult)
    
    DMCminSamples= cmds.intSliderGrp('DMCminSamplesSlider', query=True, value=1)
    cmds.setAttr('vraySettings.dmcs_adaptiveMinSamples',DMCminSamples)
    
    divideShading = cmds.checkBox('AAshadeDivideOption',query=True,value=1)
    cmds.setAttr('vraySettings.divShadeSubdivs',divideShading)


def copyFrom(args=None):
    get1=cmds.getAttr('vraySettings.dmcMaxSubdivs')
    AA_MAXInput= cmds.intSliderGrp('AAMaxSlider', edit=True, value=get1)
    
    get2=cmds.getAttr('vraySettings.dmcMinSubdivs')
    AA_MINInput= cmds.intSliderGrp('AAMinSlider', edit=True, value=get2)
    
    get3=cmds.getAttr('vraySettings.minShadeRate')
    MinShadingRate= cmds.intSliderGrp('AAMinShadeSlider', edit=True, value=get3)
    
    get4=cmds.getAttr('vraySettings.dmcs_adaptiveAmount')
    DMC_Adaptive= cmds.floatSliderGrp('DMCadaptiveAmountSlider', edit=True, value=get4)
    
    get5=cmds.getAttr('vraySettings.dmcs_subdivsMult')
    DMCsubdivMult= cmds.floatSliderGrp('DMCsubdivsMultSlider', edit=True, value=get5)

    get6=cmds.getAttr('vraySettings.dmcs_adaptiveMinSamples')
    DMCminSamples= cmds.intSliderGrp('DMCminSamplesSlider', edit=True, value=get6)

    get7=cmds.getAttr('vraySettings.divShadeSubdivs')
    divideShading = cmds.checkBox('AAshadeDivideOption',edit=True,value=get7)
    calculateSamples()




if cmds.window('DMCCalculator',exists=True):
    cmds.deleteUI('DMCCalculator')

window = cmds.window('DMCCalculator',menuBar=True, title= 'DMC Calculator_%s' %(versionNumber) , w=330, h=100) #, s = False
cmds.columnLayout(adj=1)
#cmds.text('Image Sampler / Anti-Aliasing')
cmds.frameLayout( label='Image Sampler / Anti-Aliasing' )
cmds.columnLayout(adj=1)
AAMinSlider = cmds.intSliderGrp('AAMinSlider', field=True, label='Min Subdivs', minValue=1, fieldMinValue=0,maxValue=10, fieldMaxValue=1000, value=1,cc=calculateSamples)
AAMaxSlider = cmds.intSliderGrp('AAMaxSlider', field=True, label='Max Subdivs', minValue=1, fieldMinValue=0,maxValue=10, fieldMaxValue=1000, value=8,cc=calculateSamples)
AAMinShadeSlider = cmds.intSliderGrp('AAMinShadeSlider', field=True, label='Min Shading Rate', minValue=1,maxValue=10, fieldMinValue=0, fieldMaxValue=1000, value=2,cc=calculateSamples)
AAshadeDivideOption = cmds.checkBox('AAshadeDivideOption', label='Divide Shading Subdivs',v=1,cc=calculateSamples)
cmds.setParent('..')
cmds.setParent('..')

#cmds.text('DMC Sampler')
cmds.frameLayout( label='DMC Sampler' )
cmds.columnLayout(adj=1)
DMCadaptiveAmountSlider = cmds.floatSliderGrp('DMCadaptiveAmountSlider', label='Adaptive Amount', field=True, minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, value=.850 ,pre=3,cc=calculateSamples)
DMCminSamplesSlider = cmds.intSliderGrp('DMCminSamplesSlider', field=True, label='Adaptive Min Samples', minValue=1,maxValue=64, fieldMinValue=0, fieldMaxValue=1000, value=4,cc=calculateSamples)
DMCsubdivsMultSlider = cmds.floatSliderGrp('DMCsubdivsMultSlider', label='DMC Subdivs Multiplier', field=True, minValue=1, maxValue=64, fieldMinValue=1, fieldMaxValue=1000, value=80,pre=3,cc=calculateSamples)
cmds.setParent('..')
cmds.setParent('..')

cmds.frameLayout( label='Local Subivs (Lights, Shaders, etc.)' )
cmds.columnLayout(adj=1)
#cmds.text('Local Subivs(Lights Shaders etc.)')
localSubdivSlider = cmds.intSliderGrp('localSubdivSlider', field=True, label='Local Subdivs', minValue=1,maxValue=64, fieldMinValue=0, fieldMaxValue=1000, value=8,cc=calculateSamples)
cmds.setParent('..')
cmds.setParent('..')

cmds.frameLayout( label='Copy to, or From Render Settings' )
cmds.columnLayout(adj=1)
cmds.button('copyToBut',label='Copy To Globals:', c=copyTo)
cmds.button(label = 'Copy From Globals:', c=copyFrom)
cmds.setParent('..')
cmds.setParent('..')


cmds.frameLayout( label='Resulting Sampling' )
cmds.textFieldGrp('AAMaxField', label='Max AA Samples:  ', text='', editable=False ,bgc=[.2,.2,.2])
cmds.textFieldGrp('AAMinField', label='Min AA Samples:  ', text='', editable=False ,bgc=[.2,.2,.2])
cmds.textFieldGrp('DMCMaxImageField', label='Image Max Sampling:  ', text='', editable=False ,bgc=[.2,.2,.2])
cmds.textFieldGrp('DMCMinImageField', label='Image Min Sampling:  ', text='', editable=False ,bgc=[.2,.2,.2])
cmds.textFieldGrp('DMCMaxPixelField', label='Pixel Max Sampling:  ', text='', editable=False ,bgc=[.2,.2,.2])
cmds.textFieldGrp('DMCMinPixelField', label='Pixel Min Sampling:  ', text='', editable=False ,bgc=[.2,.2,.2])
cmds.setParent('..')
cmds.setParent('..')

cmds.window('DMCCalculator',edit=True, title= 'js_DMC_Calculator %s' %(versionNumber) , w=330, h=100)
calculateSamples()
cmds.showWindow( window )
