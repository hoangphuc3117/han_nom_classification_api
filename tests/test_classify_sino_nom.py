import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.services.classify_sino_nom import classify_sino_nom, ScriptType
from src.config import NOM_THRESHOLD_TXT

@pytest.mark.parametrize(
    "text,expected_type",
    [
        ("Xin chào thế giới", ScriptType.NON_SINO_NOM), 
        ('''你好，世界！昔商家至盤庚五遷。周室迨成王三徙。
            豈三代之數君徇于己私。妄自遷徙。
            以其圖大宅中。爲億萬世子孫之計。
            上謹天命。下因民志。
            苟有便輒改。故國祚延長。
            風俗富阜。而丁黎二家。
            乃徇己私。忽天命。
            罔蹈商周之迹。常安厥邑于茲。
            致世代弗長。筭數短促。
            百姓耗損。萬物失宜。
            朕甚痛之。不得不徙。
            况高王故都大羅城。宅天地區域之中。
            得龍蟠虎踞之勢。正南北東西之位。
            便江山向背之宜。其地廣而坦平。
            厥土高而爽塏。民居蔑昏墊之困。
            萬物極繁阜之豐。遍覽越邦。
            斯爲勝地。誠四方輻輳之要會。
            爲萬世帝王之上都。朕欲因此地利以定厥居。
            卿等如何。''', ScriptType.SINO),
        ('''告疾示眾
            春去百花落，
            春到百花開。
            事逐眼前過，
            老從頭上來。
            莫謂春殘花落盡，
            庭前昨夜一枝梅。''', ScriptType.SINO),
        ('''南國山河
            南國山河南帝居
            截然定分在天書
            如何逆虜來侵犯
            汝等行看取敗虛''', ScriptType.SINO),
        ('''𤾓 𢆥 𥪞 𡎝 𠊛 些 
            𫳘 才 𫳘 命 窖 󰑼 恄 𠑬 
            𣦰 戈 󰜋 局 𣷭 橷 
            仍 調 𬂙 𧡊 㐌 𤴬 疸 𢚸 
            𨓐 咦 彼 嗇 斯 豐 
            𡗶 撑 悁 貝 𦟐 紅 打 慳 
            稿 𦹳 吝 󰇾 𠓀 畑 
            風 情 固 錄 羣 傳 史 撑 
            浪 𢆥 嘉 靖 朝 明 
            𦊚 方 滂 𣼽 𠄩 京 凭 鐄 
            固 茄 員 外 户 王 
            家 資 𠉝 拱 常 常 堛 中 ''', ScriptType.NOM),
        ('''詠菓機
            身㛪如菓機𨕭𣘃
            胳奴多仕䋦奴
            君子固腰辰揀
            吀停緍𢱖預器𢬣''', ScriptType.NOM),
    ]
)
def test_classify_sino_nom(text, expected_type):
    result = classify_sino_nom(text, NOM_THRESHOLD_TXT)
    assert result == expected_type, f"For input '{text}', expected {expected_type}, got {result}"
