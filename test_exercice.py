#-*- coding:utf-8 -*-
from exercice import *


#def fake_raw_input(char):
    #"""To enable tests with raw_input"""
    #if char == "a":
        #return "あ"
    #if char == "A":
        #return "ア"


def test_find_kana():
    """Test for the find_kana function"""
    char_to_find = "a"
    assert find_kana(char_to_find, lambda x: "あ") == "Good job !"
    char_to_find = "A"
    assert find_kana(char_to_find, lambda x: "ア") == "Good job !"
