
translator_dict = {'А': 'A', 'Б': 'B', 'Д': 'D', 'Е': 'E', 'Ф': 'F', 'Г': 'G', 'Х': 'H', 'И': 'I', 'К': 'K',
                   'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'В': 'V',
                   'Й': 'Y', 'З': 'Z', 'Ё': 'E', 'Ж': 'ZH', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '',
                   'Ь': 'Y', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA', "Ы": "Y", " ": " "}

def translator(string: str) -> str:
    string = string.upper()
    translated_text = ""
    for i in string:
        translated_text += translator_dict[i]
    if translated_text.endswith("IY"):
        translated_text = translated_text.replace("IY", "Y", 1)
    return translated_text.lower().capitalize()



