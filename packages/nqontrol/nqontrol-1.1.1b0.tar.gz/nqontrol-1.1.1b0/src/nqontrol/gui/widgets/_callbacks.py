import logging as log

from ADwin import ADwinError
from dash.exceptions import PreventUpdate

from nqontrol.general import settings
from nqontrol.gui.dependencies import DEVICE

############################################################
########################## ui.py ###########################
############################################################


#################### Getters ###############################


def getCurrentSaveName():
    """Return name of save file as string if one has been specified.

    Concerns the header section of the UI.

    Returns
    -------
    :obj:`String`
        Name of the save file or empty string

    """
    if settings.SETTINGS_FILE is not None:
        return settings.SETTINGS_FILE
    return ""


def getCurrentRampLocation():
    """Return current channel of ADwin ramp from save. Default is None.

    Concerns the header section of the UI.


    Returns
    -------
    :obj:`int`
        Channel number of :obj:`servo` on which ramp is active.

    """
    return DEVICE.rampEnabled


####################### Callbacks ###########################


def callReboot(clicks):
    """Reboot the ADwin device.

    Return a :obj:`String` with information on reboot.
    Return `None` if button hasn't been pressed
    (to accound for Dash callbacks firing on start-up).

    Parameters
    ----------
    clicks : :obj:`int`
        Description of parameter `clicks`.

    Returns
    -------
    :obj:`String`
        Information on the reboot process for the UI.

    """
    if clicks is not None:
        try:
            dev = DEVICE
            dev.reboot()
            return "Rebooted successfully."
        except ADwinError:
            return "Reboot encountered an error."
    else:
        return None


def callSave(clicks, filename):
    """Save the :obj:`nqontrol.ServoDevice` to the
    "./src"-directory using the filename provided.

    If no filename was provided saves a 'untitled_device'.

    Parameters
    ----------
    clicks : :obj:`int`
        Description of parameter `clicks`.
    filename : :obj:`String`
        Specify a `String` as the potential filename. If not provided, save to 'untitled_device'.

    Returns
    -------
    :obj:`String`
        Text info on save process.

    """
    if (clicks is not None) and (clicks > 0):
        try:
            if filename is None:
                filename = "untitled_device"
            dev = DEVICE
            dev.saveDeviceToJson(filename)
            log.info(f"Saved device as JSON in: {filename}")
            return f"Saved as {filename}."
        except Exception as e:
            log.warning(e)
            raise PreventUpdate()
    else:
        raise PreventUpdate()


def callWorkloadTimestamp():
    """Handle callback for Workload and Timestamp output in the UIs header section.

    Parameters
    ----------

    Returns
    -------
    :obj:`String`
        The workload and timestamp in a String description.

    """
    try:
        return f"Workload: {DEVICE.workload} Timestamp: {DEVICE.timestamp}"
    except ADwinError:
        return "Workload: ERR Timestamp: ERR"


def callToggleRamp(targetInput):
    """Set the ramp of ADwin to one of the possible channels.

    Parameters
    ----------
    targetInput : :obj:`int`
        Target servo channel. `False` if set to Off in the UI,
        as the servo defines the state that way.

    Returns
    -------
    :obj:`String`
        Information string as callback needs some output. Basically a dummy.

    """
    if not targetInput:
        DEVICE.servo(1).disableRamp()
        return "Disabled"
    servo = DEVICE.servo(targetInput)
    if servo.lockSearch:
        log.warning("Autolock is active, ramp was not activated.")
        return "Lock active, could not update ramp"
    if not servo.rampEnabled:
        servo.enableRamp()
    return "Ramp on channel " + str(targetInput)
