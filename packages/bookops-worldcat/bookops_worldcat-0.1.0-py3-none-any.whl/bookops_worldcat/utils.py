# -*- coding: utf-8 -*-

# various utilities to be used with session and responds


def remove_sensitive_data(data):
    """
    Removes token or WSkey from url and token from a request header.
    WSkey has always 80 characters.

    Args:
        obj: str or dict,   response or request url, or request.header attribute
    """
    if type(data) == str:
        # WSkey scenario
        start_pos = data.index("wskey=")
        data = f"{data[:start_pos + 6]}WSKEY-HERE{data[start_pos + 86:]}"
    elif type(data) == dict:
        # token in a request header scenario
        try:
            data["Authorization"] = "AUTH-HERE"
        except IndexError:
            # no Autorization key set
            pass
    return data
