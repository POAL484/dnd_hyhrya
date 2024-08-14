import PIL.ImageFont as fonts

defFont = fonts.truetype("Roboto-Regular.ttf", 100)

def get_by_keys(dictonary: dict, keys: list):
    if len(keys) > 1: return get_by_keys(dictonary[keys[0]], keys[1:])
    else: return dictonary[keys[0]] 

def calcFontByWidth(target_width: float, text: str, font: fonts.FreeTypeFont = defFont):
    prop_width = font.getlength(text)
    prop_height = font.size
    return (target_width*prop_height)/prop_width