from playwright.sync_api import expect
from config import BASE_URL
from pages.character_page import CharacterPage
import pytest

@pytest.mark.serial
@pytest.mark.smoke
def test_battle_success(reset, page):
    character = CharacterPage(page)
    character.open()
    
    expect(character.coin()).to_have_text("500")
    before_coin = character.get_coin()
    
    character.battle()
    expect(character.battle_result()).to_be_visible()
    
    result = character.result().text_content()
    reward = int(result.split()[4]) #83
    
    assert 50<= reward <= 100, f"Expect reward between 50-100 but got {reward}"
    
    expected_coin = before_coin + reward #583
    
    expect(character.coin()).to_have_text(str(expected_coin)) #wait "583" showup
     
    after_coin = character.get_coin()
    assert after_coin == expected_coin # 583 == 583

def test_character_initial_coin(reset, page):
    character = CharacterPage(page)
    character.open()
    expect(character.coin()).to_have_text("500")
    coin = character.get_coin()
    assert coin == 500, f"Expected coin 500 but got {coin}"