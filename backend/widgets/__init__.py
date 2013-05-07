from OnOff import OnOff
from OnOffDimLevel import OnOffDimLevel
from OnOffColorWheel import OnOffColorWheel

def getWidget(device, ui='default'):
    if 'color_wheel' in device.object.SUPPORTED_ACTIONS:
        return OnOffColorWheel(ui=ui, device=device)
    elif 'dim_level' in device.object.SUPPORTED_ACTIONS:
        return OnOffDimLevel(ui=ui, device=device)
    else:
        return OnOff(ui=ui)