from enum import Enum
from src.config import TOP_PURE_NOM

NOT_COUNT_CHARACTERS = ['。', '\n',' ']

class ScriptType(Enum):
    NOM = (1, "nom")
    SINO = (2, "sino")
    NON_SINO_NOM = (3, "non_sino_nom")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    def __str__(self):
        return self.label

    @property
    def int_value(self):
        return self.value

    @property
    def str_value(self):
        return self.label
    
def contains_sino_char(text: str) -> bool:
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)

def classify_sino_nom(text: str, nom_threshold : int) -> ScriptType:
    if not text:
        return ScriptType.NON_SINO_NOM
    
    if not contains_sino_char(text):
        return ScriptType.NON_SINO_NOM
        
    # Count all characters
    filtered_chars = []
    for char in text:
        if char not in NOT_COUNT_CHARACTERS:
            filtered_chars.append(char)

    filtered_text = ''.join(filtered_chars)

    total_chars = len(filtered_text)
    
    # Count Nom characters
    nom_count = sum(1 for char in filtered_text if char in TOP_PURE_NOM)
    
    if total_chars == 0:
        return ScriptType.NONE_SINONOM
    
    nom_percentage = (nom_count / total_chars) * 100
    # print(f'Nom percentage: {nom_percentage:.2f}%')
    
    if nom_percentage >= nom_threshold:
        return ScriptType.NOM
    else:
        return ScriptType.SINO