def get_param_as_text(parameter):
    """gets a parameter as a string"""

    if isinstance(parameter, str):
        param_str = parameter
    elif isinstance(parameter, bool):
        param_str = str(parameter)
    else:
        param_str = parameter.valueAsText

    return param_str


def write_message(messages, str_message: str, severity: int = 0) -> None:
    """
    Write a message to arcpy terminal or the python console. severity: 0 Message/1 Warning/2 Error

    :param messages: arcpy messages object
    :param str_message: Message to display
    :param severity: Message/Warning/Error - 0/1/2
    """
    if messages is None:
        print(str_message)
    elif severity == 0:
        messages.addMessage(str_message)
    elif severity == 1:
        messages.addWarningMessage(str_message)
    elif severity == 2:
        messages.addErrorMessage(str_message)
    else:
        raise ValueError("Invalid severity")
