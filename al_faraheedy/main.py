#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
الفراهيدي - Arabic Poetry Analysis System
Converted from PHP to Python
Original concept was developed initially in 2008 by Muktar Sayed Saleh
https://github.com/muktarsayedsaleh/Al-Faraheedy-Project

This time, Muktar himself is converting this to a Python module so he (and others) can use it in various applications.
For Muktar, this is needed for faraheedy.ai project!

Key differences from PHP:
    1. Python uses raw strings for regex patterns
    2. Different escape sequences handling
    3. Unicode handling differences
    4. Group capture syntax differences

"""

import re
import itertools
from typing import List, Dict, Any, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


class PoetryType(Enum):
    CLASSICAL = "classical"  # عمودي
    FREE_VERSE = "free_verse"  # تفعيلة


@dataclass
class AnalysisResult:
    """Result of poetry analysis"""
    shater: str  # الشطر
    arrodi: str  # الكتابة العروضية  
    chars: str  # الحروف
    harakat: str  # الحركات
    rokaz: str  # الرقز والخطيطات
    ba7er_name: str  # اسم البحر
    tafa3eel: List[str]  # التفعيلات


@dataclass
class QafeehAnalysis:
    """Rhyme analysis result"""
    text: str
    type: str
    rawee: str  # الروي
    wasel: str  # الوصل
    kharoog: str  # الخروج
    ta2ses: str  # التأسيس
    dakheel: str  # الدخيل
    redf: str  # الردف
    errors: List[str] = None


class ArabicPoetryAnalyzer:
    """
    Arabic Poetry Analysis System - الفراهيدي
    Fixed version with proper Python regex handling
    """
    
    # Arabic alphabet and diacritics
    ALPHABET = [
        'ا', 'أ', 'إ', 'آ', 'ء', 'ئ', 'ؤ', 'ى', 'ب', 'ت', 'ة', 'ث', 'ج', 'ح', 'خ',
        'د', 'ذ', 'ر', 'ز', 'ش', 'س', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك',
        'ل', 'م', 'ن', 'ه', 'و', 'ي', '#'  # # represents space
    ]
    
    HARAKAT = ['ّ', 'َ', 'ُ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ْ']  # Diacritics
    
    # Fixed meter patterns for Python regex
    METER_PATTERNS = {
        'taweel': re.compile(r"U-[-U]U---U-[U-]U(---|-U-|--)"),
        'baseet': re.compile(r"(--U-|U-U-)(-U-|UU-)--U-(-U-|UU-|--)"),
        'madeed': re.compile(r"[-U]U--[-U]U-(-U--|-U-U|-U-|UU-)"),
        'kamel': re.compile(r"(UU|-)-U-(UU|-)-U-(UU-U-|--U-|UU--|---)"),
        'rajaz': re.compile(r"(--U-|U-U-|-UU-|UUU-)(--U-|U-U-|-UU-|UUU-)(--U-|U-U-|-UU-|UUU-|---)"),
        'ramal': re.compile(r"(-U--|UU--|UU-U|-U-U)(-U--|UU--|UU-U|-U-U)(-U--|-U-|UU-|-U-U)"),
        'saree3': re.compile(r"(--U-|U-U-|-UU-|UUU-)(--U-|U-U-|-UU-|UUU-)(-U-|-U-U)"),
        'khafeef': re.compile(r"(-U--|UU--)(--U-|U-U-)(-U--|UU--|---|UU-)"),
        'wafer': re.compile(r"(U-UU-|U---)(U-UU-|U---)(U--)"),
        'o7othKamel': re.compile(r"(UU-U-|--U-)(UU-U-|--U-)UU-"),
        'munsare7': re.compile(r"(--U-|U-U-|-UU-|UUU-)(---U|-U-U|UU-U)(--U-|-UU-|---)"),
        'mutakareb': re.compile(r"(U--|U-U){3}(U--|U-U|U-)"),
        'mutadarak': re.compile(r"(-U-|UU-|--){4}"),
        'mu5alla3Baseet': re.compile(r"(--U-|U-U-|-UU-)-U-U--"),
        'majzoo2Kamel': re.compile(r"(UU-U-|--U-)(UU-U-|UU--|--U-|UU-U-U|UU-U--)"),
        'majzoo2Baseet': re.compile(r"(--U-|U-U-|-UU-|UUU-)(-U-|UU-)(--U-|---|--U-U)"),
        'majzoo2Ramal': re.compile(r"(-U--|UU--)(-U--|UU--|-U--U|-U-)"),
        'majzoo2Saree3': re.compile(r"(--U-|U-U-|-UU-|UUU-)(-U-|-U-U)"),
        'majzoo2khafeef': re.compile(r"(-U--|UU--)(--U-|U-U-)"),
        'majzoo2Munsare7': re.compile(r"(--U-|U-U-|-UU-|UUU-)(---U|---)"),
        'majzoo2Mutakareb': re.compile(r"(U--|U-U){2}(U--|U-U|U-|-)"),
        'majzoo2Mutadarak': re.compile(r"(-U-|UU-|--){2}(-U-|-U-U|UU--)"),
        'hazaj': re.compile(r"(U---|U--U)(U---|U--U)"),
        'majzoo2Wafer': re.compile(r"(U-UU-|U---)(U-UU-|U---)"),
        'majzoo2Rajaz': re.compile(r"(--U-|U-U-|-UU-|UUU-)(--U-|U-U-|-UU-|UUU-|---|--U--)"),
        'modare3': re.compile(r"(U--U|U-U-)-U--"),
        'moktadab': re.compile(r"-U-U-UU-"),
        'mojtath': re.compile(r"(--U-|U-U-)(-U--|UU--|---)"),
        'manhookRajaz': re.compile(r"(--U-|U-U-|-UU-|UUU-|---)"),
    }

    def __init__(self):
        """Initialize the analyzer"""
        pass

    def _str_to_chars(self, text: str) -> List[str]:
        """Convert string to character array handling Arabic Unicode properly"""
        if not text:
            return []
            
        result = []
        text = text.replace(' ', '#')
        
        # Handle Arabic Unicode properly - each Arabic character is already a single unit
        i = 0
        while i < len(text):
            char = text[i]
            if char == '#':
                result.append('#')
                i += 1
            else:
                # For Arabic text, each character is already properly encoded
                result.append(char)
                i += 1
        
        return result

    def _clean_str(self, text: str) -> str:
        """Clean input text from non-alphabetic characters and diacritics"""
        if not text:
            return '#'
            
        # Ensure text starts with #
        if not text.startswith('#'):
            text = '#' + text
        
        # Remove multiple spaces and replace with #
        text = re.sub(r'\s+', '#', text)
        text = re.sub(r'#+', '#', text)
        
        # Remove punctuation marks
        punctuations = ['؟', '?', '/', '\\\\', '!', ':', '-', '"', ')', '(', ',', '،', '.', '؛', '«', '»']
        for p in punctuations:
            text = text.replace(p, '')
        
        chars = self._str_to_chars(text)
        result = []
        
        for char in chars:
            if char in self.ALPHABET or char in self.HARAKAT:
                result.append(char)
        
        # Ensure text ends with #
        if result and result[-1] != '#':
            result.append('#')
        elif not result:
            result = ['#']
            
        return ''.join(result)

    def _handle_special_cases(self, text: str) -> str:
        """Handle special Arabic grammatical cases with fixed regex"""
        text = self._clean_str(text)
        
        # Define patterns with proper Python regex syntax
        patterns_replacements = [
            # واو الجمع (Plural waw) - Fixed: use raw strings and proper escaping
            (r'و[َُِْ]*ا#', 'وْ#'),
            
            # واو عمرو (Amr's waw) - Fixed: proper Unicode handling
            (r'#عمرٍو#', '#عمْرٍ#'),
            (r'#عمروٍ#', '#عمْرٍ#'),
            (r'#عمرًو#', '#عمْرً#'),
            (r'#عمروً#', '#عمْرً#'),
            (r'#عمرٌو#', '#عمْرٌ#'),
            (r'#عمروٌ#', '#عمْرٌ#'),
            (r'#عمرو#', '#عمْر#'),
            
            # إعادة المدّ إلى أصله (Restore elongated alif)
            (r'آ', 'أا'),
            
            # معالجة لفظ الجلالة (Handle Allah) - Fixed: proper capture groups
            (r'ى#الله#', 'لّاه#'),
            (r'تالله#', 'تلّاه#'),
            (r'ا#الله#', 'لّاه#'),
            (r'اللهُ#', 'الْلاهُ#'),
            (r'اللهَ#', 'الْلاهَ#'),
            (r'اللهِ#', 'الْلاهِ#'),
            (r'الله#', 'الْلاه#'),
            (r'للهِ#', 'للْلاهِ#'),
            (r'لله#', 'للْلاه#'),
            
            # اللهمّ - Fixed: proper group syntax
            (r'#الل[َّ]*هم([َّ]*)#', r'#الْلاهم\1#'),
            
            # الإله
            (r'#الإله([َُِْ]*)#', r'#الإلاه\1#'),
            
            # للإله
            (r'#لل[ْ]*إله([َُِْ]*)#', r'للْإلاه\1#'),
            
            # إله - Fixed: character class syntax
            (r'#إله([َُِْ]*)([يهمنا])([َُِْ]*)#', r'#إلاه\1\2\3#'),
            
            # الرحمن
            (r'الر[َّ]*حمن([َُِْ]*)#', r'الرَّحْمان\1#'),
            
            # للرَّحمن
            (r'للر[َّ]*حمن([َُِْ]*)#', r'لِرَّحْمان\1#'),
            
            # Demonstrative pronouns (أسماء الإشارة) - Fixed: proper character classes
            
            # هذا
            (r'#([فلكب]*)ه[َ]*ذ[َ]*ا[ْ]*#', r'#\1هَاذَا#'),
            
            # هذه
            (r'#([فلكب]*)ه[َ]*ذ[ِ]*ه([َُِ]*)#', r'#\1هَاذِه\2#'),
            
            # هؤلاء
            (r'#([فلكب]*)ه[َُِ]*ؤ[َُِ]*ل[َِ]*ا[ْ]*ء([َُِْ]*)#', r'#\1هَاؤُلَاء\2#'),
            
            # ذلك
            (r'#([فلكب]*)ذ[َُِ]*ل[َُِ]*ك([َِ]*)#', r'#\1ذَالِك\2#'),
            
            # هذي
            (r'#([فلكب]*)ه[َُِ]*ذ[َُِ]*ي([َِ]*)#', r'#\1هَاذِي\2#'),
            
            # هذان
            (r'#([فلكب]*)ه[َُِ]*ذ[َِ]*ا[ْ]*ن([َُِْ]*)#', r'#\1هَاذَان\2#'),
            
            # هذين
            (r'#([فلكب]*)ه[َُِ]*ذ[َِ]*ي[ْ]*ن([َُِْ]*)#', r'#\1هَاذَيْن\2#'),
            
            # ههنا
            (r'#([فلكب]*)ه[َُِ]*ه[َِ]*ن[ْ]*ا([َُِْ]*)#', r'#\1هَاهُنَا#'),
            
            # ههناك
            (r'#([فلكب]*)ه[َُِ]*ه[َِ]*ن[ْ]*ا[ْ]*ك([َُِْ]*)#', r'#\1هَاهُنَاك\2#'),
            
            # هكذا
            (r'#([فلكب]*)ه[َُِ]*ك[َِ]*ذ[ْ]*ا([َُِْ]*)#', r'#\1هَاكَذَا#'),
            
            # لكن ساكنة النون
            (r'#ل[َُِ]*ك[َِ]*ن[ْ]*#', '#لَاْكِنْ#'),
            
            # لكنّ بتشديد النون
            (r'#ل[َُِ]*ك[َِ]*ن[ّ]+#', '#لَاْكِنْنَ#'),
            
            # Relative pronouns (الأسماء الموصولة)
            
            # الذي
            (r'#ا[َُِ]*ل[َُِ]*ذ[َُِ]*ي([َُِْ]*)#', '#اللّذِيْ#'),
            
            # فالذي | بالذي | كالذي 
            (r'#([فبك]+)ا[َُِ]*ل[َُِ]*ذ[َُِ]*ي([َُِْ]*)#', r'#\1اللّذِيْ#'),
            
            # للذي 
            (r'#ل[َُِ]*ل[َُِ]*ذ[َُِ]*ي([َُِْ]*)#', '#لِلْلَذِيْ#'),
            
            # التي
            (r'#ا[َُِ]*ل[َُِ]*ت[َُِ]*ي([َُِْ]*)#', '#اللّتِيْ#'),
            
            # فالتي | بالتي | كالتي
            (r'#([فبك]+)ا[َُِ]*ل[َُِ]*ت[َُِ]*ي([َُِْ]*)#', r'#\1اللّتِيْ#'),
            
            # للتي 
            (r'#ل[َُِ]*ل[َُِ]*ت[َُِ]*ي([َُِْ]*)#', '#لِلْلَتِيْ#'),
            
            # الذين
            (r'#ا[َُِ]*ل[َُِ]*ذ[َُِ]*ي[َُِ]*ن([َِ]*)#', '#اللّذِيْنَ#'),
            
            # فاللذين | كاللذين | باللذين
            (r'#([فبك]+)ا[َُِ]*ل[َُِ]*ذ[َُِ]*ي[َُِ]*ن([َِ]*)#', r'#\1اللّذِيْنَ#'),
            
            # للذين 
            (r'#ل[َُِ]*ل[َُِ]*ذ[َُِ]*ي[َُِ]*ن([َِ]*)#', '#لِلْلَذِيْنَ#'),
            
            # Special names - Fixed: proper optional groups
            
            # داود 
            (r'#د[َُِ]*ا[َُِ]*و[َُِ]*د([ٌٍَِ]*|[اً]*)#', r'#دَاوُوْد\1#'),
            
            # طاوس 
            (r'#ط[َُِ]*ا[َُِ]*و[َُِ]*س([ٌٍَِ]*|[اً]*)#', r'#طَاوُوْس\1#'),
            
            # ناوس 
            (r'#ن[َُِ]*ا[َُِ]*و[َُِ]*س([ٌٍَِ]*|[اً]*)#', r'#نَاوُوْس\1#'),
            
            # طه 
            (r'#ط[َُِ]*ه[َُِ]*#', '#طاها#'),
        ]
        
        # Apply all transformations using proper Python regex
        for pattern, replacement in patterns_replacements:
            try:
                text = re.sub(pattern, replacement, text)
            except re.error as e:
                # Log the error but continue processing
                print(f"Regex error in pattern {pattern}: {e}")
                continue
            
        return text

    def _handle_lunar_solar_lam(self, text: str) -> str:
        """Handle lunar and solar lam with fixed regex"""
        text = self._clean_str(text)
        
        chars = self._str_to_chars(text)
        if len(chars) < 4:
            return text
        
        # Convert back to string for regex processing
        text = ''.join(chars)
        
        # Define lunar and solar letters
        lunar_letters = 'أإبغحجكوخفعقيمه'
        solar_letters = 'تثدذرزسشصضطظلن'
        
        # Fixed patterns with proper Python regex syntax
        patterns_replacements = [
            # Solar lam patterns - Fixed: use f-strings for character classes
            (f'و#ال([{solar_letters}])', r'و#\1ّ'),
            
            # Vowel + solar lam (letters that get deleted)
            (f'(ا[َُِْ]*|ى[َُِْ]*|ي[ُِْ]*|وْ)#ال([{solar_letters}])', r'#\2ّ'),
            
            # ياء + solar lam
            (f'(ي[َّ]*)#ال([{solar_letters}])', r'\1#\2ّ'),
            
            # تاء مربوطة + solar lam
            (f'ة([َُِ]*)#ال([{solar_letters}])', r'ت\1#\2ّ'),
            
            # فكب + solar lam
            (f'#([فكب]*)ال([{solar_letters}])', r'#\1\2ّ'),
            
            # لل + solar lam
            (f'#لل([{solar_letters}])', r'ل#\1ّ'),
            
            # همزة وصل
            (r'#ال(ا)', '#لِ'),
            
            # Lunar lam patterns
            
            # Vowel + lunar lam (letters that get deleted)
            (f'(ا[َُِْ]*|ى[َُِْ]*|ي[ُِْ]*|وْ)#ال([{lunar_letters}])', r'#لْ\2'),
            
            # فكب + lunar lam
            (f'#([فكب]*)ال([{lunar_letters}])', r'#\1لْ\2'),
            
            (f'#ال([{lunar_letters}])', r'#ألْ\1'),
            
            # لل + lunar lam
            (f'#لل([{lunar_letters}])', r'#للْ\1'),
        ]
        
        # Apply transformations
        for pattern, replacement in patterns_replacements:
            try:
                text = re.sub(pattern, replacement, text)
            except re.error as e:
                print(f"Regex error in lunar/solar lam pattern {pattern}: {e}")
                continue
            
        return text

    def _handle_tanween_shaddeh(self, text: str, is_ajez: bool) -> str:
        """Handle tanween and shaddeh with fixed processing"""
        text = self._clean_str(text)
        chars = self._str_to_chars(text)
        
        if not chars:
            return text
        
        # Handle shaddeh - Fixed: proper list iteration
        i = 0
        while i < len(chars):
            if (chars[i] == 'ّ' and i > 0 and 
                chars[i-1] in self.ALPHABET):
                chars[i] = 'ْ' + chars[i-1]
            i += 1
        
        # Handle final vowel lengthening for rhyme
        if len(chars) > 1 and chars[-1] != 'ْ' and chars[-1] in ['ا', 'ى']:
            chars.append('ْ')
        
        # Handle ajez (second hemistich) special cases
        if is_ajez and len(chars) > 0:
            last_char = chars[-1]
            if last_char == '#':
                last_char = chars[-2]
            if last_char not in ['ْ', 'ٌ', 'ً', 'ٍ', 'ْ']:
                extension = 'وْ'
                if last_char == 'َ':
                    extension = "اْ"
                elif last_char == 'ِ':
                    extension = "يْ"
                elif last_char == 'ُ':
                    extension = "وْ"
                chars.append(extension)
        
        text = ''.join(chars)
        
        # Handle tanween with fixed patterns
        tanween_patterns = [
            (r'اً', 'نْ'),
            (r'ةٌ', 'تُنْ'),
            (r'ةً', 'تَنْ'),
            (r'ةٍ', 'تِنْ'),
            (r'ىً', 'نْ'),
            (r'[ًٌٍ]', 'نْ'),  # Fixed: proper character class
        ]
        
        for pattern, replacement in tanween_patterns:
            text = re.sub(pattern, replacement, text)
        
        # Remove any remaining shaddeh
        text = text.replace('ّ', '')
        
        return text

    def _handle_hamzat_wasl(self, text: str) -> str:
        """Handle hamzat wasl with fixed regex"""
        text = self._clean_str(text)
        chars = self._str_to_chars(text)
        
        if not chars:
            return text
        
        # Handle hamzat wasl at beginning
        if (len(chars) > 3 and chars[1] == 'ا' and 
            chars[2] != 'ل' and chars[3] != 'ل'):
            chars[1] = 'إِ'
        
        text = ''.join(chars)
        
        # Fixed patterns for hamzat wasl
        hamzat_patterns = [
            # Special cases for hamzat wasl
            
            # ابن
            (r'([يواى]*)#ا[َُِْ]*ب[َُِْ]*ن', '#بْن'),
            (r'#([فكلب]*)ا[َُِْ]*ب[َُِْ]*ن', r'#\1بْن'),
            
            # امرؤ
            (r'([يواى]*)#ا[َُِْ]*م[َُِْ]*ر', '#مْر'),
            (r'#([فكلب]*)ا[َُِْ]*م[َُِْ]*ر', r'#\1مْر'),
            
            # اثنان
            (r'([يواى]*)#ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ا[َُِْ]*ن', '#ثْنان'),
            (r'#([فكلب]*)ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ا[َُِْ]*ن', r'#\1ثْنان'),
            
            # اثنين
            (r'([يواى]*)#ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ي[َُِْ]*ن', '#ثْنيْن'),
            (r'#([فكلب]*)ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ي[َُِْ]*ن', r'#\1ثْنيْن'),
            
            # اثنتان
            (r'([يواى]*)#ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ت[َُِْ]*ا[َُِْ]*ن', '#ثْنتان'),
            (r'#([فكلب]*)ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ت[َُِْ]*ا[َُِْ]*ن', r'#\1ثْنتان'),
            
            # اثنتين
            (r'([يواى]*)#ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ت[َُِْ]*ي[َُِْ]*ن', '#ثْنتيْن'),
            (r'#([فكلب]*)ا[َُِْ]*ث[َُِْ]*ن[َُِْ]*ت[َُِْ]*ي[َُِْ]*ن', r'#\1ثْنتيْن'),
            
            # است
            (r'([يواى]*)#ا[َُِْ]*س[َُِْ]*ت([َُِْ]*)', r'#سْت\2'),
            (r'#([فكلب]*)ا[َُِْ]*س[َُِْ]*ت([َُِْ]*)', r'#\1سْت\2'),
            
            # Hamzat wasl after vowel (gets deleted)
            (r'(ا|ي|ى)#ا([أإبتثجحخدذرزسشصضطظعغفقكمنهوي])', r'#\2ْ'),
            
            # Hamzat wasl with prefix - Fixed: proper quantifier
            (r'#([فكلب]*)ا([أإبتثجحخدذرزسشصضطظعغفقكمنهوي])([أإبتثجحخدذرزسشصضطظعغفقكلمنهوي]{4,})', r'#\1\2ْ\3'),
            
            # General hamzat wasl
            (r'#ا([أإبتثجحخدذرزسشصضطظعغفقكمنهوي])', r'#\1ْ'),
        ]
        
        # Apply transformations
        for pattern, replacement in hamzat_patterns:
            try:
                text = re.sub(pattern, replacement, text)
            except re.error as e:
                print(f"Regex error in hamzat wasl pattern {pattern}: {e}")
                continue
        
        # Remove double sukun
        text = re.sub(r'ْْ+', 'ْ', text)
        
        return text

    def _get_chars_only(self, text: str) -> str:
        """Extract only alphabetic characters"""
        chars = self._str_to_chars(text)
        result = []
        for char in chars:
            if char in self.ALPHABET and char != '#':
                result.append(char)
        return ''.join(result)

    def _get_harakat_only(self, text: str) -> str:
        """Extract only diacritics (harakat) with fixed logic"""
        chars = self._str_to_chars(text)
        result = []
        
        i = 0
        while i < len(chars):
            char = chars[i]
            next_char = chars[i + 1] if i + 1 < len(chars) else None
            
            if char in self.HARAKAT:
                result.append(char)
                i += 1
            elif char in self.ALPHABET and char != '#':
                # Check if next character is a haraka
                if next_char and next_char in self.HARAKAT:
                    result.append(next_char)
                    i += 2  # Skip both current and next
                else:
                    # No haraka follows, assign default based on character type
                    if char not in ['ى', 'ا']:
                        result.append('َ')  # Default fatha
                    else:
                        result.append('ْ')  # Sukun for alif and ya
                    i += 1
            else:
                i += 1
        
        # Normalize harakat
        result_str = ''.join(result)
        result_str = result_str.replace('ِ', 'َ')  # Convert kasra to fatha
        result_str = result_str.replace('ُ', 'َ')  # Convert damma to fatha
        
        return result_str

    def _get_rokaz_khoutayt(self, harakat: str) -> str:
        """Convert harakat to prosodic notation (U and -)"""
        text = harakat.replace('َْ', '-')  # Fatha + sukun = long syllable
        text = text.replace('َ', 'U')      # Fatha = short syllable
        text = text.replace('ْ', 'U')      # Sukun = short syllable
        return text

    def _get_ba7er(self, rokaz: str) -> str:
        """Identify meter from prosodic pattern with fixed regex matching"""
        # Try to match against each meter pattern
        for meter_name, pattern in self.METER_PATTERNS.items():
            if pattern.search(rokaz):
                return meter_name
        
        return "unknown"

    def _get_truth_values(self, count: int) -> List[List[str]]:
        """Generate truth table for given number of variables"""
        if count <= 0:
            return [['0']]
        if count == 1:
            return [['1'], ['0']]
        
        # Recursive generation
        sub_table = self._get_truth_values(count - 1)
        result = []
        
        # Add '1' prefix to all combinations
        for row in sub_table:
            result.append(['1'] + row)
        
        # Add '0' prefix to all combinations
        for row in sub_table:
            result.append(['0'] + row)
        
        return result

    def _do_eshbaa3_shater(self, text: str) -> Union[Dict[str, Any], str]:
        """New vowel lengthening algorithm using brute force approach"""
        text = '#' + text + '#'
        
        # Find words ending with pronouns that can be lengthened
        # Fixed: use proper regex split with parentheses to capture delimiters
        parts = re.split(r'(هُ|هِ|مُ)#', text)
        positions = []
        
        for i, part in enumerate(parts):
            if part in ['هُ', 'هِ', 'مُ']:
                positions.append(i)
        
        if positions:
            truth_table = self._get_truth_values(len(positions))
        else:
            truth_table = [['0']]
        
        for state in truth_table:
            temp_parts = parts.copy()
            
            for i, bit in enumerate(state):
                if i < len(positions) and bit == '1':
                    pos = positions[i]
                    # Apply vowel lengthening
                    if temp_parts[pos] == 'هُ':
                        temp_parts[pos] += 'وْ'
                    elif temp_parts[pos] == 'هِ':
                        temp_parts[pos] += 'يْ'
                    elif temp_parts[pos] == 'مُ':
                        temp_parts[pos] += 'وْ'
            
            state_text = ''.join(temp_parts)
            # Fixed: use proper regex substitution
            state_text = re.sub(r'#+', '#', state_text)
            
            # Check if this lengthened state is metrically valid
            processed_text = state_text.replace('#', ' ')
            processed_text = re.sub(r'\s+', '', processed_text)
            
            arrodi_written = processed_text
            chars = self._get_chars_only(arrodi_written)
            harakat = self._get_harakat_only(arrodi_written)
            rokaz = self._get_rokaz_khoutayt(harakat)
            ba7er_name = self._get_ba7er(rokaz)
            
            if ba7er_name != 'unknown':
                tafa3eel = self._get_tafa3eel(rokaz, chars, ba7er_name)
                return {
                    "shater": state_text,
                    "arrodi": arrodi_written,
                    "chars": chars,
                    "harakat": harakat,
                    "rokaz": rokaz,
                    'ba7er_name': ba7er_name,
                    'tafa3eel': tafa3eel
                }
        
        return 'unknownAlso'

    def _get_tafa3eel(self, rokaz: str, chars: str, ba7er_name: str) -> List[str]:
        """Get prosodic feet (tafa3eel) for given meter with fixed processing"""
        result = []
        
        if ba7er_name == 'taweel':
            # طويل meter handling
            i = 0
            chars_index = 0
            
            # First foot
            if rokaz.startswith('U--'):
                result.extend(['فَعُوْلُنْ', chars[chars_index:chars_index+10]])
                chars_index += 10
                i = 3
            elif rokaz.startswith('U-U'):
                result.extend(['فَعُوْلُ', chars[chars_index:chars_index+8]])
                chars_index += 8
                i = 3
            
            # Second foot - مَفَاْعِيْلُنْ
            if i < len(rokaz):
                result.extend(['مَفَاْعِيْلُنْ', chars[chars_index:chars_index+14]])
                chars_index += 14
                i += 4
            
            # Third foot
            if i < len(rokaz):
                if rokaz[i:i+3] == 'U--':
                    result.extend(['فَعُوْلُنْ', chars[chars_index:chars_index+10]])
                    chars_index += 10
                    i += 3
                elif rokaz[i:i+3] == 'U-U':
                    result.extend(['فَعُوْلُ', chars[chars_index:chars_index+8]])
                    chars_index += 8
                    i += 3
            
            # Final foot
            remaining = rokaz[i:]
            if remaining == 'U---':
                result.extend(['مَفَاْعِيْلُنْ', chars[chars_index:chars_index+14]])
            elif remaining == 'U-U-':
                result.extend(['مَفَاْعِلُنْ', chars[chars_index:chars_index+12]])
            elif remaining == 'U--':
                result.extend(['فَعُوْلُنْ', chars[chars_index:chars_index+10]])
        
        elif ba7er_name == 'baseet':
            # بسيط meter handling
            i = 0
            chars_index = 0
            
            # First foot
            if rokaz.startswith('--U-'):
                result.extend(['مُسْتَفْعِلُنْ', chars[chars_index:chars_index+14]])
                chars_index += 14
                i = 4
            elif rokaz.startswith('U-U-'):
                result.extend(['مُتَفْعِلُنْ', chars[chars_index:chars_index+12]])
                chars_index += 12
                i = 4
            elif rokaz.startswith('-UU-'):
                result.extend(['مُسْتَعِلُنْ', chars[chars_index:chars_index+12]])
                chars_index += 12
                i = 4
            
            # Second foot
            if i < len(rokaz):
                next_pattern = rokaz[i:i+3]
                if next_pattern == '-U-':
                    result.extend(['فَاْعِلُنْ', chars[chars_index:chars_index+10]])
                    chars_index += 10
                    i += 3
                elif next_pattern == 'UU-':
                    result.extend(['فَعِلُنْ', chars[chars_index:chars_index+8]])
                    chars_index += 8
                    i += 3
            
            # Third foot - مُسْتَفْعِلُنْ
            if i < len(rokaz):
                result.extend(['مُسْتَفْعِلُنْ', chars[chars_index:chars_index+14]])
                chars_index += 14
                i += 4
            
            # Final foot
            remaining = rokaz[i:]
            if remaining == '-U-':
                result.extend(['فَاْعِلُنْ', chars[chars_index:chars_index+10]])
            elif remaining == 'UU-':
                result.extend(['فَعِلُنْ', chars[chars_index:chars_index+8]])
            elif remaining == '--':
                result.extend(['فَاْلُنْ', chars[chars_index:chars_index+8]])
        
        elif ba7er_name == 'kamel':
            # كامل meter handling
            i = 0
            chars_index = 0
            
            while i < len(rokaz):
                if rokaz[i:i+5] == 'UU-U-':
                    result.extend(['مُتَفَاْعِلُنْ', chars[chars_index:chars_index+14]])
                    chars_index += 14
                    i += 5
                elif rokaz[i:i+4] == '--U-':
                    result.extend(['مُسْتَفْعِلُنْ', chars[chars_index:chars_index+14]])
                    chars_index += 14
                    i += 4
                elif rokaz[i:i+4] == 'UU--':
                    result.extend(['مُتَفَاْعِلْ', chars[chars_index:chars_index+12]])
                    chars_index += 12
                    i += 4
                elif rokaz[i:i+3] == '---':
                    result.extend(['مُسْتَفْعِلْ', chars[chars_index:chars_index+12]])
                    chars_index += 12
                    i += 3
                else:
                    # Handle remaining characters
                    result.extend(['????', chars[chars_index:chars_index+2]])
                    chars_index += 2
                    i += 1
        
        elif ba7er_name == 'rajaz':
            # رجز meter handling
            i = 0
            chars_index = 0
            
            while i < len(rokaz):
                if rokaz[i:i+4] == '--U-':
                    result.extend(['مُسْتَفْعِلُنْ', chars[chars_index:chars_index+14]])
                    chars_index += 14
                    i += 4
                elif rokaz[i:i+4] == 'U-U-':
                    result.extend(['مُتَفْعِلُنْ', chars[chars_index:chars_index+12]])
                    chars_index += 12
                    i += 4
                elif rokaz[i:i+4] == '-UU-':
                    result.extend(['مُسْتَعِلُنْ', chars[chars_index:chars_index+12]])
                    chars_index += 12
                    i += 4
                elif rokaz[i:i+4] == 'UUU-':
                    result.extend(['مُتَعِلُنْ', chars[chars_index:chars_index+10]])
                    chars_index += 10
                    i += 4
                elif rokaz[i:i+3] == '---':
                    result.extend(['مُسْتَفْعِلْ', chars[chars_index:chars_index+12]])
                    chars_index += 12
                    break
                else:
                    # Handle remaining
                    result.extend(['????', chars[chars_index:chars_index+2]])
                    chars_index += 2
                    i += 1
        
        # Add simplified handling for other meters...
        # For brevity, showing the pattern for key meters
        
        return result

    def _what_tafeela_poem_on(self, rokaz: str) -> str:
        """Determine the dominant meter for free verse poetry with fixed logic"""
        if len(rokaz) < 4:
            return 'unknown'
            
        # Check first 4 characters
        start_pattern = rokaz[:4]
        
        # Define meter patterns for free verse detection
        tafeela_patterns = {}
        
        if start_pattern == 'UUU-':
            tafeela_patterns = {
                'rajaz': re.compile(r'(--U-|-UU-|U-U-|UUU-|U-){5,}'),
                'khabab': re.compile(r'(UU-|-UU|--){7,}')
            }
        elif start_pattern == 'UU-U':
            tafeela_patterns = {
                'kamel': re.compile(r'(UU-U-|--U-){4,}'),
                'ramal': re.compile(r'(-U--|UU--|UU-U){5,}'),
                'mutadarak': re.compile(r'(-U-|UU-){7,}')
            }
        elif start_pattern == 'UU--':
            tafeela_patterns = {
                'ramal': re.compile(r'(-U--|UU--|UU-U){5,}')
            }
        elif start_pattern == 'U-UU':
            tafeela_patterns = {
                'wafer': re.compile(r'(U-UU-|U---){4,}'),
                'mutakareb': re.compile(r'(U--|U-U|U-){7,}')
            }
        elif start_pattern == 'U-U-':
            tafeela_patterns = {
                'rajaz': re.compile(r'(--U-|-UU-|U-U-|UUU-|U-){5,}'),
                'mutakareb': re.compile(r'(U--|U-U|U-){7,}')
            }
        elif start_pattern == 'U--U':
            tafeela_patterns = {
                'wafer': re.compile(r'(U-UU-|U---){4,}'),
                'mutakareb': re.compile(r'(U--|U-U|U-){7,}')
            }
        elif start_pattern == 'U---':
            tafeela_patterns = {
                'wafer': re.compile(r'(U-UU-|U---)')
            }
        elif start_pattern == '-UU-':
            tafeela_patterns = {
                'rajaz': re.compile(r'(--U-|-UU-|U-U-|UUU-|U-){5,}')
            }
        elif start_pattern == '-U-U':
            tafeela_patterns = {
                'mutadarak': re.compile(r'(-U-|UU-){7,}')
            }
        elif start_pattern == '-U--':
            tafeela_patterns = {
                'ramal': re.compile(r'(-U--|UU--|UU-U){5,}'),
                'mutadarak': re.compile(r'(-U-|UU-){7,}')
            }
        elif start_pattern == '--U-':
            tafeela_patterns = {
                'kamel': re.compile(r'(UU-U-|--U-){4,}'),
                'rajaz': re.compile(r'(--U-|-UU-|U-U-|UUU-|U-){5,}'),
                'mutadarak': re.compile(r'(-U-|UU-){7,}')
            }
        else:
            return 'unknown'
        
        # Test patterns against the full rokaz
        test_rokaz = rokaz[:21] if len(rokaz) >= 21 else rokaz
        
        max_matches = 0
        best_meter = 'unknown'
        
        for meter_name, pattern in tafeela_patterns.items():
            matches = len(pattern.findall(test_rokaz))
            if matches > max_matches:
                max_matches = matches
                best_meter = meter_name
                
                # Special handling for wafer/hazaj distinction
                if best_meter == 'wafer':
                    # Check if we have specific wafer patterns
                    wafer_matches = re.findall(r'U-UU-', test_rokaz)
                    if wafer_matches:
                        best_meter = 'wafer'
                    else:
                        best_meter = 'hazaj'
        
        return best_meter

    def _get_tafaeel_for_tafeela_poem(self, ba7er_name: str, rokaz: str, chars: str) -> Dict[str, Any]:
        """Get prosodic feet for free verse poetry with fixed processing"""
        if ba7er_name == 'unknown':
            return {'poemErr': 'لم يتم التعرّف على وزن هذه القصيدة'}
        
        result_tafa3eel = []
        result_names = []
        result_words = []
        chars_index = 0
        
        # Process rokaz character by character based on meter
        i = 0
        while i < len(rokaz):
            matched = False
            
            if ba7er_name == 'kamel':
                if rokaz[i:i+5] == 'UU-U-':
                    result_tafa3eel.append('UU-U-')
                    result_names.append('مُتَفَاْعِلُنْ')
                    word_len = 14
                    matched = True
                    i += 5
                elif rokaz[i:i+4] == '--U-':
                    result_tafa3eel.append('--U-')
                    result_names.append('مُسْتَفْعِلُنْ')
                    word_len = 14
                    matched = True
                    i += 4
            elif ba7er_name == 'rajaz':
                if rokaz[i:i+4] == '--U-':
                    result_tafa3eel.append('--U-')
                    result_names.append('مُسْتَفْعِلُنْ')
                    word_len = 14
                    matched = True
                    i += 4
                elif rokaz[i:i+4] == 'U-U-':
                    result_tafa3eel.append('U-U-')
                    result_names.append('مُتَفْعِلُنْ')
                    word_len = 12
                    matched = True
                    i += 4
                elif rokaz[i:i+4] == '-UU-':
                    result_tafa3eel.append('-UU-')
                    result_names.append('مُسْتَعِلُنْ')
                    word_len = 12
                    matched = True
                    i += 4
                elif rokaz[i:i+4] == 'UUU-':
                    result_tafa3eel.append('UUU-')
                    result_names.append('مُتَعِلُنْ')
                    word_len = 10
                    matched = True
                    i += 4
            elif ba7er_name == 'mutakareb':
                if rokaz[i:i+3] == 'U--':
                    result_tafa3eel.append('U--')
                    result_names.append('فَعُوْلُنْ')
                    word_len = 10
                    matched = True
                    i += 3
                elif rokaz[i:i+3] == 'U-U':
                    result_tafa3eel.append('U-U')
                    result_names.append('فَعُوْلُ')
                    word_len = 8
                    matched = True
                    i += 3
                elif rokaz[i:i+2] == 'U-':
                    result_tafa3eel.append('U-')
                    result_names.append('فَعُوْ')
                    word_len = 6
                    matched = True
                    i += 2
            elif ba7er_name == 'mutadarak':
                if rokaz[i:i+3] == '-U-':
                    result_tafa3eel.append('-U-')
                    result_names.append('فَاْعِلُنْ')
                    word_len = 10
                    matched = True
                    i += 3
                elif rokaz[i:i+3] == 'UU-':
                    result_tafa3eel.append('UU-')
                    result_names.append('فَعِلُنْ')
                    word_len = 8
                    matched = True
                    i += 3
            elif ba7er_name == 'ramal':
                if rokaz[i:i+4] == '-U--':
                    result_tafa3eel.append('-U--')
                    result_names.append('فَاْعِلَاْتُنْ')
                    word_len = 14
                    matched = True
                    i += 4
                elif rokaz[i:i+4] == 'UU--':
                    result_tafa3eel.append('UU--')
                    result_names.append('فَعِلَاْتُنْ')
                    word_len = 12
                    matched = True
                    i += 4
                elif rokaz[i:i+4] == 'UU-U':
                    result_tafa3eel.append('UU-U')
                    result_names.append('فَعِلَاْتُ')
                    word_len = 10
                    matched = True
                    i += 4
            
            # If no pattern matched, handle as unknown
            if not matched:
                result_tafa3eel.append(rokaz[i])
                result_names.append('????')
                word_len = 2
                i += 1
            
            # Extract corresponding characters
            if chars_index < len(chars):
                word = chars[chars_index:chars_index + word_len]
                result_words.append(word)
                chars_index += word_len
            else:
                result_words.append('')
        
        # Clean up display of alif maqsura
        for i in range(len(result_words)):
            result_words[i] = result_words[i].replace('ى', 'ى ')
        
        return {
            'ba7er': ba7er_name,
            'tafa3eel': result_tafa3eel,
            'names': result_names,
            'words': result_words
        }

    def _analyse_qafeeh(self, ajez: str) -> QafeehAnalysis:
        """Analyze rhyme pattern (qafiyah) with fixed processing"""
        current_ajez = ajez
        
        # Process text for prosodic analysis
        current_ajez = self._handle_special_cases(current_ajez)
        current_ajez = self._handle_lunar_solar_lam(current_ajez)
        current_ajez = self._handle_tanween_shaddeh(current_ajez, True)
        current_ajez = self._handle_hamzat_wasl(current_ajez)
        current_ajez = current_ajez.replace('#', ' ')
        current_ajez = re.sub(r'\s+', '', current_ajez)
        
        chars = self._str_to_chars(current_ajez)
        current_qafeeh = []
        sokons_count = 0
        
        # Identify rhyme between last two sukuns
        for i in range(len(chars) - 1, -1, -1):
            current_qafeeh.append(chars[i])
            if (chars[i] == 'ْ' or 
                (chars[i] == 'ا' and (i + 1 >= len(chars) or chars[i + 1] != 'ْ')) or
                (chars[i] == 'ى' and (i + 1 >= len(chars) or chars[i + 1] != 'ْ'))):
                sokons_count += 1
            
            if sokons_count >= 2:
                if i - 1 >= 0:
                    current_qafeeh.append(chars[i - 1])
                
                index = i - 2
                while index >= 0 and chars[index] not in self.ALPHABET:
                    current_qafeeh.append(chars[index])
                    index -= 1
                
                if (len(current_qafeeh) >= 3 and 
                    current_qafeeh[-3] == 'ْ' and index >= 0):
                    current_qafeeh.append(chars[index])
                break
        
        current_qafeeh_text = ''.join(reversed(current_qafeeh))
        current_qafeeh_text = current_qafeeh_text.replace('#', ' ')
        
        # Analyze rhyme components (simplified version)
        qafeeh_alphas = []
        qafeeh_harakat = []
        qafeeh_word_positions = []
        word_no = 1
        
        chars = self._str_to_chars(current_qafeeh_text)
        for i in range(len(chars) - 1, -1, -1):
            if chars[i] in self.ALPHABET:
                if chars[i] == '#':
                    word_no += 1
                qafeeh_alphas.append(chars[i])
                qafeeh_harakat.append('')
                qafeeh_word_positions.append(word_no)
            elif chars[i] in self.HARAKAT:
                if i - 1 >= 0:
                    qafeeh_alphas.append(chars[i - 1])
                    qafeeh_word_positions.append(word_no)
                else:
                    qafeeh_alphas.append('')
                    qafeeh_word_positions.append(word_no)
                qafeeh_harakat.append(chars[i])
        
        qafeeh_alphas.reverse()
        qafeeh_harakat.reverse()
        qafeeh_word_positions.reverse()
        
        # Build rhyme analysis (simplified)
        qafeeh_text = ''
        start_idx = 1 if qafeeh_alphas and qafeeh_alphas[0] == '' else 0
        for i in range(start_idx, len(qafeeh_alphas)):
            if i < len(qafeeh_harakat):
                qafeeh_text += qafeeh_alphas[i] + qafeeh_harakat[i]
            else:
                qafeeh_text += qafeeh_alphas[i]
        
        # Determine rhyme type and components (simplified logic)
        rawee = ''
        wasel = ''
        kharoog = ''
        ta2ses = ''
        dakheel = ''
        redf = ''
        
        if len(qafeeh_alphas) >= 2:
            last_char = qafeeh_alphas[-1]
            last_haraka = qafeeh_harakat[-1] if len(qafeeh_harakat) > 0 else ''
            
            if last_char in ['ا', 'ى', 'و', 'ي']:
                rhyme_type = 'قافية مطلقة مجرَّدة'
                if len(qafeeh_alphas) >= 2:
                    rawee = qafeeh_alphas[-2] + (qafeeh_harakat[-2] if len(qafeeh_harakat) > 1 else '')
                    wasel = last_char + last_haraka
            else:
                rhyme_type = 'قافية مقيّدة مجرَّدة'
                rawee = last_char + last_haraka
        else:
            rhyme_type = 'قافية غير محددة'
        
        qafeeh_text = qafeeh_text.replace('#', ' ')
        
        return QafeehAnalysis(
            text=qafeeh_text,
            type=rhyme_type,
            rawee=rawee,
            wasel=wasel,
            kharoog=kharoog,
            ta2ses=ta2ses,
            dakheel=dakheel,
            redf=redf
        )

    # PUBLIC METHODS

    def analyze_classical_verse(self, text: str, is_ajez: bool = False) -> Dict[str, Any]:
        """Analyze classical Arabic verse with fixed processing"""
        if not text or not text.strip():
            return {
                "shater": "",
                "arrodi": "",
                "chars": "",
                "harakat": "",
                "rokaz": "",
                'ba7er_name': 'unknown',
                'tafa3eel': []
            }
        
        # Process text for prosodic analysis
        processed_text = self._handle_special_cases(text)
        processed_text = self._handle_lunar_solar_lam(processed_text)
        processed_text = self._handle_tanween_shaddeh(processed_text, is_ajez)
        processed_text = self._handle_hamzat_wasl(processed_text)
        old_text = processed_text  # For potential vowel lengthening
        
        # Extract prosodic elements
        processed_text = processed_text.replace('#', ' ')
        processed_text = re.sub(r'\s+', '', processed_text)
        
        arrodi_written = processed_text
        chars = self._get_chars_only(arrodi_written)
        harakat = self._get_harakat_only(arrodi_written)
        rokaz = self._get_rokaz_khoutayt(harakat)
        ba7er_name = self._get_ba7er(rokaz)
        
        # Determine prosodic feet
        if ba7er_name != 'unknown':
            tafa3eel = self._get_tafa3eel(rokaz, chars, ba7er_name)
            # Clean up alif maqsura display
            for i in range(len(tafa3eel)):
                if isinstance(tafa3eel[i], str):
                    tafa3eel[i] = tafa3eel[i].replace('ى', 'ى ')
                    tafa3eel[i] = tafa3eel[i].replace('ة', 'ة ')
            
            result = {
                "shater": processed_text,
                "arrodi": arrodi_written,
                "chars": chars,
                "harakat": harakat,
                "rokaz": rokaz,
                'ba7er_name': ba7er_name,
                'tafa3eel': tafa3eel
            }
        else:
            # Try vowel lengthening algorithm
            result = self._do_eshbaa3_shater(old_text)
            if result == 'unknownAlso':
                result = {
                    "shater": processed_text,
                    "arrodi": arrodi_written,
                    "chars": chars,
                    "harakat": harakat,
                    "rokaz": rokaz,
                    'ba7er_name': 'unknown',
                    'tafa3eel': []
                }
        
        return result

    def analyze_free_verse(self, text: str) -> Dict[str, Any]:
        """Analyze free verse Arabic poetry with fixed processing"""
        if not text or not text.strip():
            return {'poemErr': 'النص فارغ أو غير صالح للتحليل'}
        
        # Process text
        text = '#' + text + '#'
        text = re.sub(r'\s+', '#', text)
        text = re.sub(r'\n+', '#', text)
        text = re.sub(r'\r+', '#', text)
        
        processed_text = self._handle_special_cases(text)
        processed_text = self._handle_lunar_solar_lam(processed_text)
        processed_text = self._handle_tanween_shaddeh(processed_text, False)
        processed_text = self._handle_hamzat_wasl(processed_text)
        
        # Extract prosodic elements
        processed_text = processed_text.replace('#', ' ')
        processed_text = re.sub(r'\s+', '', processed_text)
        
        arrodi_written = processed_text
        chars = self._get_chars_only(arrodi_written)
        harakat = self._get_harakat_only(arrodi_written)
        rokaz = self._get_rokaz_khoutayt(harakat)
        
        ba7er_name = self._what_tafeela_poem_on(rokaz)
        
        if ba7er_name == 'unknown':
            return {
                'poemErr': 'لم يتم التعرّف على وزن هذه القصيدة للأسف، تأكّد من إدخال نصّ القصيدة بشكل صحيح'
            }
        else:
            return self._get_tafaeel_for_tafeela_poem(ba7er_name, rokaz, chars)

    def analyze_rhyme_patterns(self, verses: List[str]) -> Union[List[QafeehAnalysis], str]:
        """Analyze rhyme patterns in a series of verses with fixed processing"""
        if not verses:
            return 'emptyAll'
        
        results = []
        beginning_index = -1
        
        # Find first non-empty verse
        for i, verse in enumerate(verses):
            if verse and verse != 'empty' and verse.strip():
                beginning_index = i
                break
            results.append('empty')
        
        if beginning_index == -1:
            return 'emptyAll'
        
        # Analyze first verse as reference
        base_qafeeh = self._analyse_qafeeh(verses[beginning_index])
        results.append(base_qafeeh)
        
        # Analyze remaining verses
        for i in range(beginning_index + 1, len(verses)):
            if verses[i] and verses[i] != 'empty' and verses[i].strip():
                current_qafeeh = self._analyse_qafeeh(verses[i])
                errors = []
                
                # Compare with base rhyme pattern
                if current_qafeeh.rawee != base_qafeeh.rawee:
                    errors.append('قافية هذا البيت مختلفة كليَّاً عن قافية القصيدة و ذلك <b>لاختلاف الرَّويِّ</b> بين القافيتين.')
                elif current_qafeeh.wasel != base_qafeeh.wasel:
                    if not ((current_qafeeh.wasel == 'اْ' and base_qafeeh.wasel == 'ىْ') or
                            (current_qafeeh.wasel == 'ىْ' and base_qafeeh.wasel == 'اْ')):
                        errors.append('قافية هذا البيت مختلفة عن قافية القصيدة بسبب <b>اختلاف حرف الوصل</b>.')
                else:
                    # Check ta2ses (foundation)
                    if current_qafeeh.ta2ses and not base_qafeeh.ta2ses:
                        errors.append('لقد قمت باستعمال ألف التأسيس في قافية هذا البيت في حين أنَّ قافية القصيدة ليست مؤسَّسة و هذا عيب من عيوب القافية يعرف بـ<b>سناد التأسيس</b>.')
                    elif not current_qafeeh.ta2ses and base_qafeeh.ta2ses:
                        errors.append('يجب أن تُؤَسَّسَ قافية هذا البيت بألف التأسيس !')
                    
                    # Check redf (appendage)
                    if current_qafeeh.redf and not base_qafeeh.redf:
                        errors.append('لقد قمت باستعمال ردف للقافية في قافية هذا البيت في حين أنَّ قافية القصيدة ليست مردفة و هذا عيب من عيوب القافية يعرف بـ<b>سناد الرِّدف</b>.')
                    elif not current_qafeeh.redf and base_qafeeh.redf:
                        errors.append('يجب أن تُرْدِفَ قافية هذا البيت بحرف الرِّدف المناسب قبل الرَّوي مباشرةً !')
                    elif current_qafeeh.redf and base_qafeeh.redf:
                        if ((current_qafeeh.redf in ['يْ', 'وْ'] and base_qafeeh.redf in ['ا', 'اْ']) or
                            (current_qafeeh.redf in ['اْ', 'ا'] and base_qafeeh.redf in ['وْ', 'يْ'])):
                            errors.append('لا يمكن أن تجتمع الياء أو الواو كردف مع الألف كردف !')
                
                current_qafeeh.errors = errors
                results.append(current_qafeeh)
            else:
                results.append('empty')
        
        return results

    def wizard_analysis_classical(self, text: str, is_ajez: bool, 
                                rule_patterns: List[List[str]], 
                                rule_names: List[List[str]]) -> List[Dict[str, Any]]:
        """Wizard analysis for classical verse with expected patterns"""
        if not text or not text.strip():
            return [{'status': 'err', 'taf3eela': '', 'chars': '', 'errs': ['النص فارغ']}]
        
        # Process text
        processed_text = self._handle_special_cases(text)
        processed_text = self._handle_lunar_solar_lam(processed_text)
        processed_text = self._handle_tanween_shaddeh(processed_text, is_ajez)
        processed_text = self._handle_hamzat_wasl(processed_text)
        
        processed_text = processed_text.replace('#', ' ')
        processed_text = re.sub(r'\s+', '', processed_text)
        
        chars = self._get_chars_only(processed_text)
        harakat = self._get_harakat_only(processed_text)
        rokaz = self._get_rokaz_khoutayt(harakat)
        
        results = []
        
        for i, (patterns, names) in enumerate(zip(rule_patterns, rule_names)):
            if not patterns or not names:
                continue
                
            is_ok = False
            
            for j, pattern in enumerate(patterns):
                if not pattern:
                    continue
                    
                current_status = rokaz[:len(pattern)] if len(rokaz) >= len(pattern) else rokaz
                
                # Find matching pattern name
                current_name = names[j] if j < len(names) else '????'
                
                if pattern == current_status:
                    # Calculate character length
                    char_length = sum(2 if c == '-' else 1 for c in current_status) * 2
                    current_chars = chars[:char_length] if len(chars) >= char_length else chars
                    chars = chars[len(current_chars):]
                    
                    # Clean up display
                    current_chars = current_chars.replace('ى', 'ى ')
                    current_chars = current_chars.replace('ة', 'ة ')
                    
                    rokaz = rokaz[len(pattern):]
                    results.append({
                        'status': 'ok',
                        'taf3eela': current_name,
                        'chars': current_chars
                    })
                    is_ok = True
                    break
            
            if not is_ok:
                pattern = patterns[0] if patterns else ''
                current_status = rokaz[:len(pattern)] if len(rokaz) >= len(pattern) else rokaz
                
                # Find pattern name
                current_name = names[0] if names else '????'
                
                # Calculate character length  
                char_length = sum(2 if c == '-' else 1 for c in current_status) * 2
                current_chars = chars[:char_length] if len(chars) >= char_length else chars
                chars = chars[len(current_chars):]
                
                # Clean up display
                current_chars = current_chars.replace('ى', 'ى ')
                current_chars = current_chars.replace('ة', 'ة ')
                
                rokaz = rokaz[len(pattern):] if len(rokaz) >= len(pattern) else ''
                errors = self._compare_with_tafeela(current_status, patterns, names)
                
                results.append({
                    'status': 'err',
                    'taf3eela': current_name,
                    'chars': current_chars,
                    'errs': errors
                })
                break  # Stop on error for classical verse
        
        return results

    def wizard_analysis_free_verse(self, text: str, 
                                  rule_patterns: List[str], 
                                  rule_names: List[str]) -> List[Dict[str, Any]]:
        """Wizard analysis for free verse with expected patterns"""
        if not text or not text.strip():
            return [{'status': 'err', 'taf3eela': '', 'chars': '', 'errs': ['النص فارغ']}]
        
        # Process text
        processed_text = self._handle_special_cases(text)
        processed_text = self._handle_lunar_solar_lam(processed_text)
        processed_text = self._handle_tanween_shaddeh(processed_text, False)
        processed_text = self._handle_hamzat_wasl(processed_text)
        
        processed_text = processed_text.replace('#', ' ')
        processed_text = re.sub(r'\s+', '', processed_text)
        
        chars = self._get_chars_only(processed_text)
        harakat = self._get_harakat_only(processed_text)
        rokaz = self._get_rokaz_khoutayt(harakat)
        
        results = []
        patterns = rule_patterns
        names = rule_names
        
        while rokaz:
            is_ok = False
            
            for i, pattern in enumerate(patterns):
                if not pattern:
                    continue
                    
                current_status = rokaz[:len(pattern)] if len(rokaz) >= len(pattern) else ''
                
                # Find matching pattern name
                current_name = names[i] if i < len(names) else '????'
                
                if pattern == current_status:
                    # Calculate character length
                    char_length = sum(2 if c == '-' else 1 for c in current_status) * 2
                    current_chars = chars[:char_length] if len(chars) >= char_length else chars
                    chars = chars[len(current_chars):]
                    
                    # Clean up display
                    current_chars = current_chars.replace('ى', 'ى ')
                    current_chars = current_chars.replace('ة', 'ة ')
                    
                    rokaz = rokaz[len(pattern):]
                    results.append({
                        'status': 'ok',
                        'taf3eela': current_name,
                        'chars': current_chars
                    })
                    is_ok = True
                    break
            
            if not is_ok:
                pattern = patterns[0] if patterns else ''
                current_status = rokaz[:len(pattern)] if len(rokaz) >= len(pattern) else rokaz[:1]
                
                # Find pattern name
                current_name = '????'
                for i, p in enumerate(patterns):
                    if p == current_status:
                        current_name = names[i] if i < len(names) else '????'
                        break
                
                # Calculate character length
                char_length = sum(2 if c == '-' else 1 for c in current_status) * 2 if current_status else 2
                current_chars = chars[:char_length] if len(chars) >= char_length else chars
                chars = chars[len(current_chars):]
                
                # Clean up display
                current_chars = current_chars.replace('ى', 'ى ')
                current_chars = current_chars.replace('ة', 'ة ')
                
                rokaz = rokaz[len(current_status):] if current_status else rokaz[1:]
                errors = self._compare_with_tafeela(current_status, patterns, names) if current_status else ['نمط غير معروف']
                
                results.append({
                    'status': 'err',
                    'taf3eela': current_name,
                    'chars': current_chars,
                    'errs': errors
                })
                # Continue processing for free verse (don't break on error)
        
        return results

    def _compare_with_tafeela(self, current: str, expected_patterns: List[str], 
                             pattern_names: List[str]) -> List[str]:
        """Compare current pattern with expected prosodic patterns"""
        if not current or not expected_patterns:
            return ['لا يمكن المقارنة - نمط فارغ']
        
        errors = []
        
        for i, (pattern, name) in enumerate(zip(expected_patterns, pattern_names)):
            state_no = i + 1
            
            if len(pattern) >= len(current):
                current_chars = list(current)
                pattern_chars = list(pattern)
                char_pos = 0
                
                for j, (curr_char, exp_char) in enumerate(zip(current_chars, pattern_chars)):
                    if curr_char == 'U':
                        char_pos += 1
                    elif curr_char == '-':
                        char_pos += 2
                    
                    if curr_char == exp_char:
                        continue
                    
                    if curr_char == 'U' and exp_char == '-':
                        errors.append(
                            f'<b>الصورة {self._get_state_name(state_no)} ({name}):</b> '
                            f'يجب تسكين الحرف {self._get_char_name(char_pos + 1)} '
                            f'كي نحصل على تقطيع متوافق مع هذه الصورة'
                        )
                        break
                    
                    if curr_char == '-' and exp_char == 'U':
                        errors.append(
                            f'<b>الصورة {self._get_state_name(state_no)} ({name}):</b> '
                            f'يجب أن يكون الحرف {self._get_char_name(char_pos)} متحركاً '
                            f'كي نحصل على تقطيع متوافق مع هذه الصورة'
                        )
                        break
                    
                    if j == len(current_chars) - 1:
                        errors.append(
                            f'<b>الصورة {self._get_state_name(state_no)} ({name}):</b> '
                            f'التقطيع الحالي لهذه التفعيلة أقصر وزنيّاً من هذه الصورة'
                        )
                        break
                        
            elif len(pattern) < len(current):
                errors.append(
                    f'<b>الصورة {self._get_state_name(state_no)} ({name}):</b> '
                    f'التقطيع الحالي لهذه التفعيلة أطول وزنيّاً من هذه الصورة'
                )
        
        return errors if errors else ['لا توجد أخطاء واضحة في التقطيع']

    def _get_char_name(self, n: int) -> str:
        """Get ordinal number name in Arabic"""
        names = {
            1: 'الأوّل', 2: 'الثّاني', 3: 'الثّالث', 4: 'الرّابع', 5: 'الخامس',
            6: 'السّادس', 7: 'السّابع', 8: 'الثّامن', 9: 'التّاسع', 10: 'العاشر'
        }
        return names.get(n, f'رقم {n}')

    def _get_state_name(self, n: int) -> str:
        """Get state number name in Arabic"""
        names = {
            1: 'الأولى', 2: 'الثّانية', 3: 'الثّالثة', 
            4: 'الرّابعة', 5: 'الخامسة', 6: 'السّادسة'
        }
        return names.get(n, f'رقم {n}')
