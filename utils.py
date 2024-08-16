import PIL.ImageFont as fonts

from flet import Page, dropdown

defFont = fonts.truetype("Roboto-Regular.ttf", 100)

def get_by_keys(dictonary: dict, keys: list) -> any:
    if len(keys) > 1: return get_by_keys(dictonary[keys[0]], keys[1:])
    else: return dictonary[keys[0]] 

def calcFontByWidth(target_width: float, text: str, font: fonts.FreeTypeFont = defFont) -> float:
    prop_width = font.getlength(text)
    prop_height = font.size
    return (target_width*prop_height)/prop_width

def tryAttr(obj: object, attr_name: str) -> bool:
    try:
        obj.__getattribute__(attr_name)
        return True
    except AttributeError:
        return False
    
def generateDropdownOptionsKeysEqualValues(options_keys_and_values: list) -> list:
    opts = []
    for okav in options_keys_and_values:
        opts.append(dropdown.Option(okav, okav))
    return opts

def dump_dict(dict_to_dump: dict, char_to_split_key_and_value: str = ": ") -> str:
    vals = []
    for key in dict_to_dump.keys():
        vals.append(f"{key}{char_to_split_key_and_value}{dict_to_dump[key]}")
    return ", ".join(vals)

def rightDictGen(keys: list, values: list) -> dict:
    assert len(keys) == len(values)
    a = {}
    for i in range(len(keys)):
        a[keys[i]] = values[i]
    return a