from OnOff import OnOff
from OnOffDimLevel import OnOffDimLevel

def getWidget(device, ui='default'):
    if 'dim_level' in device.object.SUPPORTED_ACTIONS:
        return OnOffDimLevel(ui=ui, device=device)
    else:
        return OnOff(ui=ui)