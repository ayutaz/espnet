# Copyright 2024 ESPnet Contributors
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

"""Test JETS Japanese TTS functionality."""

import pytest
import torch
from typing import List

from espnet2.text.phoneme_tokenizer import pyopenjtalk_g2p_prosody, pyopenjtalk_plus_g2p_prosody


class TestJETSJapanese:
    """JETS日本語固有のテスト"""
    
    def test_prosody_g2p_basic_output(self):
        """基本的な韻律付きG2Pの出力形式テスト"""
        text = "こんにちは。"
        # Try pyopenjtalk_plus first, fallback to standard
        try:
            phonemes = pyopenjtalk_plus_g2p_prosody(text)
        except:
            phonemes = pyopenjtalk_g2p_prosody(text)
        
        # 開始・終了記号の確認
        assert phonemes[0] == "^", f"Expected start symbol '^', got {phonemes[0]}"
        assert phonemes[-1] == "$", f"Expected end symbol '$', got {phonemes[-1]}"
        
        # 基本的な音素が含まれているか
        phoneme_set = set(phonemes)
        expected_phonemes = {"k", "o", "n", "i", "ch", "w", "a"}
        assert any(p in phoneme_set for p in expected_phonemes), \
            f"Expected some of {expected_phonemes} in {phonemes}"
    
    def test_question_intonation(self):
        """疑問文のイントネーション記号テスト"""
        text = "元気ですか？"
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # 疑問符が最後にあることを確認
        assert phonemes[-1] == "?", \
            f"Expected question mark at the end, got {phonemes[-5:]}"
    
    def test_pause_handling(self):
        """ポーズ記号の処理テスト"""
        text = "こんにちは、元気ですか。"
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # ポーズ記号（_）が含まれているか
        assert "_" in phonemes, \
            f"Expected pause symbol '_' in {phonemes}"
    
    def test_pitch_accent_markers(self):
        """ピッチアクセントマーカーのテスト"""
        text = "日本語は難しいです。"
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # ピッチの上昇[や下降]マーカーが含まれているか
        has_pitch_markers = "[" in phonemes or "]" in phonemes
        assert has_pitch_markers, \
            f"Expected pitch markers [ or ] in {phonemes}"
    
    def test_phrase_boundary_markers(self):
        """フレーズ境界マーカーのテスト"""
        text = "今日は良い天気ですね。明日も晴れるでしょう。"
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # フレーズ境界マーカー（#）が含まれているか
        assert "#" in phonemes, \
            f"Expected phrase boundary marker '#' in {phonemes}"
    
    def test_empty_text_handling(self):
        """空のテキスト処理のテスト"""
        text = ""
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # 空のリストが返されるか、最小限の記号のみか
        assert len(phonemes) <= 2, \
            f"Expected minimal output for empty text, got {phonemes}"
    
    def test_special_characters_handling(self):
        """特殊文字の処理テスト"""
        test_cases = [
            ("こんにちは！", "exclamation"),
            ("こんにちは...", "ellipsis"),
            ("「こんにちは」", "quotation"),
            ("こんにちは（笑）", "parentheses"),
        ]
        
        for text, case_name in test_cases:
            phonemes = pyopenjtalk_g2p_prosody(text)
            # 少なくとも開始・終了記号と音素が含まれているか
            assert len(phonemes) >= 3, \
                f"Failed for {case_name}: {text} -> {phonemes}"
            assert phonemes[0] == "^" and (phonemes[-1] in ["$", "?"]), \
                f"Incorrect boundary symbols for {case_name}: {phonemes}"
    
    def test_long_text_handling(self):
        """長いテキストの処理テスト"""
        text = "これは長いテキストのテストです。" * 10
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # 適切に処理されているか
        assert len(phonemes) > 100, \
            f"Expected many phonemes for long text, got {len(phonemes)}"
        assert phonemes[0] == "^", "Missing start symbol"
        assert phonemes[-1] in ["$", "?"], "Missing or incorrect end symbol"
    
    def test_mixed_kana_kanji(self):
        """ひらがな・カタカナ・漢字混在テキストのテスト"""
        text = "ひらがなとカタカナと漢字のテストです。"
        phonemes = pyopenjtalk_g2p_prosody(text)
        
        # 正常に変換されているか
        assert len(phonemes) > 10, \
            f"Expected reasonable number of phonemes, got {len(phonemes)}"
        assert "^" in phonemes and "$" in phonemes, \
            "Missing boundary symbols"
    
    def test_number_handling(self):
        """数字の処理テスト"""
        test_cases = [
            ("123個", "integer"),
            ("3.14", "decimal"),
            ("2024年", "year"),
            ("1月1日", "date"),
        ]
        
        for text, case_name in test_cases:
            phonemes = pyopenjtalk_g2p_prosody(text)
            # 数字が音素に変換されているか
            assert len(phonemes) > 3, \
                f"Failed to convert numbers in {case_name}: {text} -> {phonemes}"


class TestJETSDataConsistency:
    """JETS学習データの整合性テスト"""
    
    def test_phoneme_token_mapping(self):
        """音素とトークンのマッピング整合性テスト"""
        # 予想される音素セット
        expected_phonemes = {
            # 母音
            "a", "i", "u", "e", "o",
            "A", "I", "U", "E", "O",  # 無声化母音
            # 子音
            "k", "g", "s", "z", "t", "d", "n", "h", "b", "p", "m",
            "y", "r", "w", "N",  # 撥音
            "ch", "sh", "ts", "f", "j", "v",
            # 特殊記号
            "^", "$", "[", "]", "#", "_", "?",
            "pau", "cl",  # ポーズ、促音
        }
        
        # テストテキストで実際に生成される音素を確認
        test_texts = [
            "あいうえお",
            "かきくけこ",
            "がぎぐげご",
            "さしすせそ",
            "たちつてと",
            "なにぬねの",
            "はひふへほ",
            "まみむめも",
            "やゆよ",
            "らりるれろ",
            "わをん",
            "ぱぴぷぺぽ",
        ]
        
        all_phonemes = set()
        for text in test_texts:
            phonemes = pyopenjtalk_g2p_prosody(text)
            all_phonemes.update(phonemes)
        
        # 生成された音素が期待される音素セットのサブセットか
        unexpected_phonemes = all_phonemes - expected_phonemes
        assert len(unexpected_phonemes) == 0 or all(p in ["'", '"', "-"] for p in unexpected_phonemes), \
            f"Unexpected phonemes found: {unexpected_phonemes}"
    
    def test_text_length_consistency(self):
        """テキスト長と音素列長の整合性テスト"""
        test_cases = [
            ("あ", 1, 5),  # 最小: ^, a, $
            ("あいうえお", 5, 15),  # 5文字
            ("こんにちは", 5, 20),  # 5文字
        ]
        
        for text, char_count, max_phonemes in test_cases:
            phonemes = pyopenjtalk_g2p_prosody(text)
            
            # 文字数に対して妥当な音素数か
            assert len(phonemes) >= char_count + 2, \
                f"Too few phonemes for '{text}': {len(phonemes)}"
            assert len(phonemes) <= max_phonemes, \
                f"Too many phonemes for '{text}': {len(phonemes)}"


if __name__ == "__main__":
    # 直接実行時の簡易テスト
    import sys
    
    print("Running JETS Japanese tests...")
    
    # テストクラスのインスタンス化
    test_basic = TestJETSJapanese()
    test_consistency = TestJETSDataConsistency()
    
    # 基本テストの実行
    try:
        test_basic.test_prosody_g2p_basic_output()
        print("✓ Basic prosody G2P test passed")
        
        test_basic.test_question_intonation()
        print("✓ Question intonation test passed")
        
        test_basic.test_pause_handling()
        print("✓ Pause handling test passed")
        
        test_basic.test_pitch_accent_markers()
        print("✓ Pitch accent markers test passed")
        
        test_consistency.test_phoneme_token_mapping()
        print("✓ Phoneme token mapping test passed")
        
        print("\nAll tests passed!")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)