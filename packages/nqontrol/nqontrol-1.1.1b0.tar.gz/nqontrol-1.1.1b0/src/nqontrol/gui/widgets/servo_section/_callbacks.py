import logging as log
from dash.exceptions import PreventUpdate
from fastnumbers import fast_real
from nqontrol.general import settings
from nqontrol.gui.dependencies import DEVICE

############################################################
#################### Autolock Widget #######################
############################################################


#################### Getters ###############################


def getLockString(servo):
    """Return a string description of the autolock state. This will be updated on a by-second interval. Contains information for the GUI on search state, relock and locked state.

    Parameters
    ----------
    servo : :obj:`int`
        The servo index.

    Returns
    -------
    :obj:`String`
        The description string.

    Raises
    ------
    TypeError
        `servo` needs to be an integer.
    ValueError
        `servo` has to be in the correct range fom 1 to the max number of servos (depends on your settings).
    """
    if not isinstance(servo, int):
        raise TypeError(f"servo parameter needs to be an integer, was {servo}")
    if not servo in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise ValueError(
            f"servoNumber has to be in range 1 to (including) {settings.NUMBER_OF_SERVOS}."
        )
    servo = DEVICE.servo(servo)
    lockstatus = servo.lockSearch
    locked = servo.locked
    relock = servo.relock
    return f"search {int(lockstatus)} relock {int(relock)} locked {int(locked)}"


def getLockRange(servo):
    """Returns a list containing minimum and maximum value of the autolock sections RangeSlider.abs

    The AutoLock options are located in the servo section.

    Parameters
    ----------
    servo : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    obj:`list`
        [min, max]

    """
    servo = DEVICE.servo(servo)
    return [servo.lockSearchMin, servo.lockSearchMax]


def getLockThreshold(servo):
    """Returns the threshold value of the autolock.

    The AutoLock options are located in the servo section.

    Parameters
    ----------
    servo : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    obj:`float`
        The voltage value.

    """
    servo = DEVICE.servo(servo)
    return servo.lockThreshold


def getLockGreater(servo):
    """Return the initial value of the lock condition of a servo.
    The boolean translates to greater (True) or lesser than (False) the threshold.
    Part of the servo section.

    Parameters
    ----------
    servo : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`bool`
        The lock condition as a boolean.

    """
    servo = DEVICE.servo(servo)
    return int(servo.lockGreater)


def getLockRelock(servo):
    """Return whether auto-relock is on or off for a given servo.

    Parameters
    ----------
    servo : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`list`
        Empty list means `False`, element in list means `True`.

    """
    result = []
    if DEVICE.servo(servo).relock:
        result.append("on")
    return result


#################### Callbacks #############################


def callLockState(n_clicks, servoNumber):
    """Enables the auto-lock feature on given servo.
    Ramp is not compatible with Autolock (Essentially, the autolock should be a better ramp).

    GUI wise, the button is located in the individual autolock section.

    Parameters
    ----------
    n_clicks : :obj:`bool`
        Times the button has been clicked for toggling functionality.
    servo : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        Return the new button label.

    """
    # check whether list is empty
    servo = DEVICE.servo(servoNumber)
    if n_clicks is None:
        raise PreventUpdate()
    current = servo.lockSearch
    if current:
        servo.lockSearch = 0
    else:
        servo.lockSearch = 1  # setting state to 1 starts searching for peak
    return servo.lockSearch
    # the servo autolock function will automatically disable the ramp if it is active on that channel


def callLockButtonLabel(servoNumber):
    """Callback handle for the autolock button. Only sets the label of the button according to the current search status.

    Parameters
    ----------
    servoNumber : :obj:`int`
        The servo index.

    Returns
    -------
    :obj:`String`
        Button Label.
    """
    servo = DEVICE.servo(servoNumber)
    if servo.lockSearch:
        s = "Turn off lock"
    else:
        s = "Trigger lock"
    return s


def callLockRange(lockRange, servoNumber):
    """Sets the search range for the autolock feature of a given servo based on UI.

    Parameters
    ----------
    lockRange : :obj:`list`
        Contains floats [start, end].
    servo : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        Return new label containing information.

    """
    servo = DEVICE.servo(servoNumber)
    start = lockRange[0]
    end = lockRange[1]
    if start > end:
        raise PreventUpdate("Start value should be bigger.")
    servo.lockSearchRange = [start, end]

    return f"Search from {servo.lockSearchMin:.2f} V to {servo.lockSearchMax:.2f} V"


def callLockGreater(greater, servoNumber):
    """Return a binary value signifying the test direction for the autolock criteria.

    `1`: "lock when greater than threshold,
    `0`: "lock when below threshold"

    Parameters
    ----------
    greater : :obj:`bool`
        Should be a boolean, but will also translate other options to boolean, so 5 will count as True etc., according to python's bool conversion.
    servoNumber : :obj:`int`
        The servo index.

    Returns
    -------
    :obj:`int`
        The binary value of `greater`, since all callbacks need a return. Should also signify that the write to ADwin actually worked because it gets called directly from the device.

    Raises
    ------
    PreventUpdate
        If `greater` parameter is `None`, might happen on start-up.
    """
    if greater is None:
        raise PreventUpdate()
    servo = DEVICE.servo(servoNumber)
    servo.lockGreater = greater
    return servo.lockGreater


def callLockThresholdInfo(threshold, greater, servoNumber):
    """Return a string for the UI containing information on threshold and threshold direction (`lockGreater`). If no values are passed will get the values directly from the device.

    Makes sure the current values are displayed in the UI.

    Parameters
    ----------
    threshold : :obj:`float` or :obj:`int`
        The autolock threshold value.
    greater : :obj:`bool` or :obj:`int`
        Boolean indicating the direction of the lock. Also accepts `1` or `0` instead of True/False.
    servoNumber : :obj:`int`
        The servo index.

    Returns
    -------
    :obj:`String`
        The label string.
    """
    servo = DEVICE.servo(servoNumber)
    if greater is None:
        greater = servo.lockGreater
    if threshold is None:
        threshold = servo.lockThreshold
    if greater:
        greaterstring = ">"
    else:
        greaterstring = "<"
    return f"Threshold {greaterstring}{threshold:.2f} V"


def callLockRelock(values, servo):
    """Set whether the AutoLock should relock automatically whenever falling
    above/below threshold for a given servo.

    Parameters
    ----------
    values : :obj:`list`
        As with all Dash checklists, even though this is for a single element,
        the callback input is a list. Empty list means off, none-empty means on.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`bool`
        The relock value, since the UI requires a return.

    """
    servo = DEVICE.servo(servo)
    if values:
        servo.relock = True
    else:
        servo.relock = False
    return servo.relock


def callLockThreshold(threshold, servo):
    """Set the autolock threshold value for a servo.

    Parameters
    ----------
    value : :obj:`float`
        The threshold value.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`int`
        The relock value, since the UI requires a return.

    """
    try:
        threshold = fast_real(threshold, raise_on_invalid=True)
    except (ValueError, TypeError):
        raise PreventUpdate("Input must be a real number.")
    if not -10 <= threshold <= 10:
        log.warning(f"Must be a value between -10 and 10, was {threshold}")
        raise PreventUpdate(f"Must be a value between -10 and 10, was {threshold}")
    servo = DEVICE.servo(servo)
    servo.lockThreshold = threshold
    return servo.lockThreshold


############################################################
######################## Ramp Widget #######################
############################################################


#################### Getters ###############################


def getServoAmplitude(servoNumber):
    """Return the ramp amplitude setting for the specified :obj:`servo`.
    Load from save or default to `0.1`.

    Concerns the servo ramp section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        Amplitude as float.

    """
    servo = DEVICE.servo(servoNumber)
    amplitude = servo.rampAmplitude
    return amplitude


def getServoFrequency(servoNumber):
    """Return the ramp frequency setting for specified :obj:`servo`.
    Load from save or defaukt to `20`.

    Concerns the servo ramp section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    type
        Description of returned object.

    """
    servo = DEVICE.servo(servoNumber)
    frequency = servo.rampFrequency
    return frequency


#################### Callbacks #############################


def callRamp(amp, freq, context, servoNumber):
    """Send ramp parameters entered in servo control section of the UI to
    the corresponding :obj:`nqontrol.Servo`.

    Parameters
    ----------
    amp : :obj:`float`
        Ramp amplitude.
    freq : :obj:`float`
        Ramp frequency.
    context : :obj:'json'
        Dash callback context. Please check the dash docs for more info.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        UI label string describing current ramp state.

    """
    servo = DEVICE.servo(servoNumber)
    triggered = context.triggered[0]["prop_id"].split(".")[0]
    if "ramp_amp" in triggered:
        servo.rampAmplitude = amp
    if "ramp_freq" in triggered:
        servo.rampFrequency = freq
    amp = servo.rampAmplitude
    freq = servo.rampFrequency
    return f"Amplitude: {amp:.2f} V | Frequency: {freq:.2f} Hz"


############################################################
################## Servo Switches Widget ###################
############################################################


#################### Getters ###############################


def getInputStates(servoNumber):
    """Return a list of enabled input channels. Either from save or default (empty).

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`list`
        List containing names as strings.

    """
    if not isinstance(servoNumber, int):
        raise TypeError(f"servoNumber needs to be an integer, was {servoNumber}")
    if not servoNumber in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise ValueError(
            f"servoNumber has to be in range 1 to (including) {settings.NUMBER_OF_SERVOS}."
        )
    checklist = []
    servo = DEVICE.servo(servoNumber)
    if servo.inputSw:
        checklist.append("input")
    if servo.offsetSw:
        checklist.append("offset")
    return checklist


def getOffset(servoNumber):
    """Return the servo's saved or default offset.

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        :obj:`servo.offset`

    """
    if not isinstance(servoNumber, int):
        raise TypeError(f"servoNumber needs to be an integer, was {servoNumber}")
    if not servoNumber in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise ValueError(
            f"servoNumber has to be in range 1 to (including) {settings.NUMBER_OF_SERVOS}."
        )
    return DEVICE.servo(servoNumber).offset


def getGain(servoNumber):
    """Return servo's saved or default gain.

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        :obj:`servo.gain`

    """
    if not isinstance(servoNumber, int):
        raise TypeError(f"servoNumber needs to be an integer, was {servoNumber}")
    if not servoNumber in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise ValueError(
            f"servoNumber has to be in range 1 to (including) {settings.NUMBER_OF_SERVOS}."
        )
    return DEVICE.servo(servoNumber).gain


def getActiveFilters(servoNumber):
    """Return list of active filters for filter-checklist.
    Load from save file or default empty list.
    The checklist is part of the servo section.
    Filter labels are loaded in :obj:`controller.getFilterLabels()`.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`list`
        List containing indices of active filters.

    """
    filters = DEVICE.servo(servoNumber).servoDesign.filters
    active = []
    for i, fil in enumerate(filters):
        if fil is not None and fil.enabled:
            active.append(i)
    return active


def getFilterLabels(servoNumber):
    """List containing filter-checklist labels (objects) as used by `Dash`.

    The checklist labels contain the short description of filters or default to `Filter {index}`.
    The checklist is part of the servo section.
    Filter states are loaded in :obj:`controller.getActiveFilters()`.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`list`
        List of labels.

    """
    labels = []
    servo = DEVICE.servo(servoNumber)
    servoDesign = servo.servoDesign
    for i in range(servoDesign.MAX_FILTERS):
        fil = servoDesign.get(i)
        if fil is not None:
            labels.append(fil.description)
        else:
            labels.append(f"Filter {i}")
    return [{"label": labels[i], "value": i} for i in range(servoDesign.MAX_FILTERS)]


def getOutputStates(servoNumber):
    """Return a list of enabled output channels. Either from save or default (empty).

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`list`
        List containing names as strings.
    """
    checklist = []
    servo = DEVICE.servo(servoNumber)
    if servo.auxSw:
        checklist.append("aux")
    # if servo.snapSw:
    #     checklist.append('snap')
    if servo.outputSw:
        checklist.append("output")
    return checklist


def getInputSensitivity(servoNumber):
    """Return :obj:`servo.inputSensitivity`.
    Since each servo outputs 16 bit this basically relates to 'accuracy'.
    Please read the official docs for more information on how-to-use.

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        :obj:`servo.inputSensitivity`

    """
    servo = DEVICE.servo(servoNumber)
    return servo.inputSensitivity


def getAuxSensitivity(servoNumber):
    """Return :obj:`servo.auxSensitivity`.
    Since each servo outputs 16 bit this basically relates to 'accuracy'.
    Please read the official docs for more information on how-to-use.

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        :obj:`servo.auxSensitivity`

    """
    servo = DEVICE.servo(servoNumber)
    return servo.auxSensitivity


#################### Callbacks ##########################


def callOffset(servoNumber, offset):
    """Handle the servo offset input callback for the UI's servo input section.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    offset : :obj:`String`
        String from the input field.

    Returns
    -------
    :obj:`String`
        The offset embedded in a string for the html.P label.

    """
    servo = DEVICE.servo(servoNumber)
    try:
        offset = fast_real(offset, raise_on_invalid=True)
    except (ValueError, TypeError):
        raise PreventUpdate("Empty or no real number input.")
    # Please note that servo checks for correct value.
    servo.offset = offset
    return f"Offset ({servo.offset:.2f} V)"


def callGain(context, servoNumber, gain):
    """Handle the servo gain input callback for the UI's servo input section.

    Parameters
    ----------
    context : :obj:'json'
        Dash callback context. Please check the dash docs for more info.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    gain : :obj: `String`
        String from the input field.

    Returns
    -------
    :obj:`String`
        The gain embedded in a string for the html.P label.

    """
    servo = DEVICE.servo(servoNumber)

    # determining context of input
    triggered = context.triggered[0]["prop_id"].split(".")[0]
    if f"gain_{servoNumber}" in triggered:
        # case when gain is changed by submitting the input with Enter
        try:
            gain = fast_real(gain, raise_on_invalid=True)
        except (ValueError, TypeError):
            raise PreventUpdate("Empty or no real number input.")
        if servo.gain != gain:
            servo.gain = gain
    return f"Gain ({servo.gain:.2f})"


def callServoChannels(servoNumber, inputValues):
    """Handle the checklists for both the input and output section of servo controls.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    inputValues : :obj:`list`
        List for either input or output section.
        Labels for input section are 'input', 'offset'.
        For output section 'aux' and 'output'.

    Returns
    -------
    type
        Description of returned object.

    """
    servo = DEVICE.servo(servoNumber)
    if "input" in inputValues:
        servo.inputSw = True
    else:
        servo.inputSw = False

    if "offset" in inputValues:
        servo.offsetSw = True
    else:
        servo.offsetSw = False

    if "aux" in inputValues:
        servo.auxSw = True
    else:
        servo.auxSw = False

    # if 'snap' in inputValues:
    #     servo.snapSw = True
    # else:
    #     servo.snapSw = False

    if "output" in inputValues:
        servo.outputSw = True
    else:
        servo.outputSw = False

    return ""


def callToggleServoFilters(servoNumber, values):
    """Handle callback of the filter checklist in the servo section of the UI.
    Passes a list of active filters to the :obj:`servo`.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    values : :obj:`list`
        List containing the indices of active filters.

    Returns
    -------
    :obj:`String`
        Just an empty string since UI callback needs an output.

    """
    servoDesign = DEVICE.servo(servoNumber).servoDesign
    changed = False
    for i in range(servoDesign.MAX_FILTERS):
        f = servoDesign.get(i)
        if f is not None:
            old = f.enabled
            if i in values:
                f.enabled = True
            else:
                f.enabled = False
            if not old == f.enabled:
                changed = True
    if changed:
        log.debug("Changed filter enabled states.")
        DEVICE.servo(servoNumber).applyServoDesign()
    return ""


def callInputSensitivity(selected, servoNumber):
    """Apply the input sensitivity as specified by the dropdown
    of the servo section's input options to :obj:`servo.inputSensitivity`
    and return information as a string to update UI.

    Parameters
    ----------
    selected : :obj:`int`
        One of the dropdown options. The mode is specified with ints from `0` to `3`.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        Information formatted for the `html.P()` above the dropdown.
    """
    servo = DEVICE.servo(servoNumber)
    servo.inputSensitivity = selected
    limits = [10, 5, 2.5, 1.25]
    return f"Input sensitivity (Limit: {limits[selected]} V, Mode: {selected})"


def callAuxSensitivity(selected, servoNumber):
    """Apply the aux sensitivity as specified by the dropdown
    of the servo section's output options to :obj:`servo.auxSensitivity`
    and return information as a string to update UI.

    Parameters
    ----------
    selected : :obj:`String`
        One of the dropdown options. The mode is specified with ints from `0` to `3`.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        Information formatted for the `html.P()` above the dropdown.

    """
    servo = DEVICE.servo(servoNumber)
    servo.auxSensitivity = selected
    limits = [10, 5, 2.5, 1.25]
    return f"Aux sensitivity (Limit: {limits[selected]} V, Mode: {selected})"


############################################################
######################## Servo Widget ######################
############################################################


#################### Getters ###############################


def getServoName(servoNumber):
    """Return name attribute of servo: :obj:`servo.name` from Save or if specified in `settings.py`.

    Concerns the servo section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        :obj:`servo.name`

    """
    if not isinstance(servoNumber, int):
        raise TypeError(f"servoNumber needs to be an integer, was {servoNumber}")
    if not servoNumber in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise ValueError(
            f"servoNumber has to be in range 1 to (including) {settings.NUMBER_OF_SERVOS}."
        )
    servo = DEVICE.servo(servoNumber)
    return servo.name


#################### Callbacks #############################


def callServoName(servoNumber, submit, name):
    """Apply the name specified in the servo section's name input
    to the targeted :obj:`servo.name` and return the name string to update the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    submit : :obj:`int`
        Number of times the input's submit event occured (pressing Enter while in input).
        None on startup.
    name : :obj:`String`
        Name for the :obj:`servo` and the UI's servo section.

    Returns
    -------
    :obj:`String`
        :obj:`servo.name`
    """
    if submit is None:
        raise PreventUpdate()
    servo = DEVICE.servo(servoNumber)
    servo.name = name
    return servo.name
