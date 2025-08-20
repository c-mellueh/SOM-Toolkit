from SOMcreator.templates import UNITS_DICT
def uri_to_code(uri):
    element =  UNITS_DICT.get(uri)
    if not element:
        return ""
    return element.get("Code","")