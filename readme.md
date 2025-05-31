# Al-Faraheedy-Python

[![PyPI version](https://badge.fury.io/py/al-faraheedy-python.svg)](https://badge.fury.io/py/al-faraheedy-python)
[![Python version](https://img.shields.io/pypi/pyversions/al-faraheedy-python.svg)](https://pypi.org/project/al-faraheedy-python/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/al-faraheedy-python)](https://pepy.tech/project/al-faraheedy-python)


**مكتبة بايثون تغلّف نظام الفراهيدي لحوسبة عروض الشعر العربي و قافيته**

**Al Faraheedy Python: A Pythonized version of the Arabic Poetry Rhythm and Rhyme Analyzer Project**

A comprehensive Python library for analyzing Arabic poetry, including classical and free verse forms. This is a Python wrapper and enhancement of the original Faraheedy system for computational analysis of Arabic prosody and rhyme. Named after Al-Khalil ibn Ahmad al-Farahidi (الخليل بن أحمد الفراهيدي), the founder of Arabic prosody.

> Original Idea (old unmaintained project): https://github.com/muktarsayedsaleh/Al-Faraheedy-Project

## Warning
This module was converted from PHP to Python very quickly so I have not tested it well.
I'm anticipating bugs here and there. so contributions are welcomed

# تحذير
قمت بتحويل هذه الشيفرة البرمجية من بي إتش بي إلى بايثون بشكل سريع و دون اختبارات مكثفة كتلك التي تمت على نسخة بي اتش بي المستقرّة، لذلك أتوقع ظهور بعض الأخطاء البرمجية و أرحّب بتصحيحاتها المقترحة من قبلكم

## Features

- **Classical Poetry Analysis** (تحليل الشعر العمودي)
  - Meter identification for 29+ Arabic meters (Poetry "seas") - تحليل بحور الشعر العربي بصورها التامة و غير التامة
  - Prosodic pattern analysis (العروض)
  - Automatic vowel lengthening for irregular patterns (الإشباع)
  - Advanced scansion algorithms

- **Free Verse Analysis** (تحليل شعر التفعيلة)
  - Modern Arabic poetry analysis
  - Dominant meter detection
  - Flexible prosodic pattern matching
  - Multi-meter poem handling

- **Rhyme Analysis** (تحليل القوافي)
  - Comprehensive rhyme scheme analysis
  - Identification of rhyme components:
    - الروي (Rawee - main rhyme letter)
    - الوصل (Wasel - connection)
    - الخروج (Kharoog - exit)
    - التأسيس (Ta2sees - foundation)
    - الردف (Redf - appendage)
    - الدخيل (Dakheel - intrusion)
  - Detection of rhyme defects (عيوب القافية)

- **Advanced Arabic Linguistic Processing**
  - Special Arabic grammatical cases handling
  - Lunar/Solar lam (اللام القمرية والشمسية) processing
  - Hamzat wasl (همزة الوصل) rules implementation
  - Tanween (التنوين) and shaddah (الشدة) processing
  - Divine name variations (لفظ الجلالة)
  - Demonstrative pronouns (أسماء الإشارة)
  - Relative pronouns (الأسماء الموصولة)

## Installation

```bash
pip install al-faraheedy-python
```

## Quick Start

```python
from al_faraheedy import ArabicPoetryAnalyzer

analyzer = ArabicPoetryAnalyzer()

# Analyze classical verse
poem = [
    "ما بيْن مفْترقٍ و مفْترقِ",
    "ممْلوْءةٌ بمقاتليْ طرقيْ",
    "أنّى التفتّ و حيْثما ضبحتْ",
    "خيْليْ أجدْ رأْسيْ على طبقِ",
    "فوْق الرِّماحِ أرى أعاديهُ",
    "حملوْهُ مفْغوْر الفم الدبقِ",
    "دمهُ يقطّر و هْو يلْعنهمْ",
    "لوْ كنْتُ منْ ماءٍ للمْ أرقِ",
]
for index, verse in enumerate(poem):
    is_ajez = any([index ==0, index % 2 == 0])  # عند تصريع القصيدة، نعامل صدر المطلع معاملة العجز في الإشباع
    result = analyzer.analyze_classical_verse(verse, is_ajez)
    print(f"Verse {index + 1}: {result}")


# Analyze rhyme patterns
verses = ["مفْترقِ", "طرقيْ", "طبقِ", "الدبقِ", "لمْ أرقِ"]
for index, verse in enumerate(verses):
    result = analyzer.analyze_rhyme_patterns(verse)
    print(f"Rhyme {index + 1}: {result}")

# Analyze free verse
free_result = analyzer.analyze_free_verse("تمهّل و لا تمْتحنّيْ بما لا أطيْقُ")
print(f"Free Verse Analysis: {free_result}")
```

## API Reference

### Core Classes

#### `ArabicPoetryAnalyzer`

The main class for poetry analysis with the following methods:

##### `analyze_classical_verse(text: str, is_ajez: bool = False) -> Dict[str, Any]`

Analyzes classical Arabic verse (الشعر العمودي).

**Parameters:**
- `text` (str): The verse text to analyze
- `is_ajez` (bool): Whether this is the second hemistich (العجز)

**Returns:**
- Dictionary containing:
  - `shater`: The processed verse
  - `arrodi`: Prosodic writing (الكتابة العروضية)
  - `chars`: Extracted characters
  - `harakat`: Extracted diacritics
  - `rokaz`: Prosodic pattern (U and -)
  - `ba7er_name`: Identified meter name
  - `tafa3eel`: List of prosodic feet

##### `analyze_free_verse(text: str) -> Dict[str, Any]`

Analyzes free verse Arabic poetry (شعر التفعيلة).

**Parameters:**
- `text` (str): The poem text to analyze

**Returns:**
- Dictionary with analysis results or error message

##### `analyze_rhyme_patterns(verses: List[str]) -> List[QafeehAnalysis]`

Analyzes rhyme patterns in a series of verses.

**Parameters:**
- `verses` (List[str]): List of verse endings (second hemistichs)

**Returns:**
- List of `QafeehAnalysis` objects

### Data Classes

#### `QafeehAnalysis`

Represents comprehensive rhyme analysis results:

```python
@dataclass
class QafeehAnalysis:
    text: str          # Full rhyme text
    type: str          # Rhyme type description
    rawee: str         # الروي (main rhyme consonant)
    wasel: str         # الوصل (connection vowel)
    kharoog: str       # الخروج (exit sound)
    ta2ses: str        # التأسيس (foundation alif)
    dakheel: str       # الدخيل (intrusion)
    redf: str          # الردف (appendage)
    errors: List[str]  # Detected rhyme defects
```

## Supported Arabic Meters (البحور المدعومة)

The library recognizes 29+ classical Arabic meters:

### Primary Meters (البحور الأساسية)
- **الطويل** (Taweel) - The most common meter in classical Arabic poetry
- **البسيط** (Baseet) - Simple meter, widely used
- **الكامل** (Kamel) - Perfect meter, frequently used
- **الرجز** (Rajaz) - Trembling meter, common in didactic poetry
- **الرمل** (Ramal) - Sand meter, lyrical and flowing
- **السريع** (Saree') - Fast meter, energetic rhythm
- **الخفيف** (Khafeef) - Light meter, graceful flow
- **المنسرح** (Munsareh) - Flowing meter
- **الوافر** (Wafer) - Abundant meter, rich sound
- **الهزج** (Hazaj) - Rocking meter, musical quality
- **المتقارب** (Mutakareb) - Approaching meter, uniform rhythm
- **المتدارك** (Mutadarak) - Overtaking meter

### Truncated Forms (المجزوءات)
- **مجزوء البسيط** (Majzoo' Baseet)
- **مجزوء الكامل** (Majzoo' Kamel)
- **مجزوء الرمل** (Majzoo' Ramal)
- **مجزوء السريع** (Majzoo' Saree')
- **مجزوء الخفيف** (Majzoo' Khafeef)
- **مجزوء المنسرح** (Majzoo' Munsareh)
- **مجزوء المتقارب** (Majzoo' Mutakareb)
- **مجزوء المتدارك** (Majzoo' Mutadarak)
- **مجزوء الوافر** (Majzoo' Wafer)
- **مجزوء الرجز** (Majzoo' Rajaz)

### Rare and Specialized Meters (البحور النادرة والمتخصصة)
- **المقتضب** (Muqtadab)
- **المجتث** (Mujtath)
- **المضارع** (Mudare')
- **منهوك الرجز** (Manhook Rajaz)
- **مخلع البسيط** (Mukhalla' Baseet)
- **أعاريض الكامل** (A'areed Kamel)

## Detailed Examples

### Classical Poetry Analysis with Al-Mutanabbi

```python
from al_faraheedy import ArabicPoetryAnalyzer

analyzer = ArabicPoetryAnalyzer()

# Famous verse by Al-Mutanabbi (المتنبي)
verse = "على قدْر أهْل العزْم تأْتي العزائمُ"
result = analyzer.analyze_classical_verse(verse)

print(f"Original: {verse}")
print(f"Prosodic writing: {result['arrodi']}")
print(f"Meter: {result['ba7er_name']}")  # Should identify as 'taweel'
print(f"Pattern: {result['rokaz']}")
print("Prosodic feet:")
for i in range(0, len(result['tafa3eel']), 2):
    foot_name = result['tafa3eel'][i]
    foot_text = result['tafa3eel'][i + 1] if i + 1 < len(result['tafa3eel']) else ''
    print(f"  {foot_name}: {foot_text}")
```

### Comprehensive Rhyme Analysis

```python
# Analyzing a complete qasida's rhyme scheme
verses = [
    "عَلَى قَدْرِ أَهْلِ الْعَزْمِ تَأْتِي الْعَزَائِمُ",  # First verse
    "وَتَأْتِي عَلَى قَدْرِ الْكِرَامِ الْمَكَارِمُ",        # Second verse  
    "وَتَعْظُمُ فِي عَيْنِ الصَّغِيرِ صِغَارُهَا",         # Third verse - should show error
]

# Extract the rhyme parts (second hemistichs)
rhyme_parts = ["الْعَزَائِمُ", "الْمَكَارِمُ", "صِغَارُهَا"]

rhyme_results = analyzer.analyze_rhyme_patterns(rhyme_parts)

for i, analysis in enumerate(rhyme_results):
    if hasattr(analysis, 'text'):
        print(f"\nVerse {i+1} Rhyme Analysis:")
        print(f"  Rhyme text: {analysis.text}")
        print(f"  Rhyme type: {analysis.type}")
        print(f"  Rawee (main letter): {analysis.rawee}")
        print(f"  Wasel (connection): {analysis.wasel}")
        print(f"  Redf (appendage): {analysis.redf}")
        
        if analysis.errors:
            print(f"  ❌ Errors detected:")
            for error in analysis.errors:
                print(f"    - {error}")
        else:
            print(f"  ✅ Rhyme is consistent")
```

### Free Verse Analysis with Modern Poetry

```python
# Modern Arabic poem by Mahmoud Darwish style
modern_poem = '''
وَنَحْنُ نُحِبُّ الحَيَاةَ إذَا مَا اسْتَطَعْنَا إِلَيْهَا سَبِيلاَ
وَنَرْقُصُ بَيْنَ شَهِيدْينِ نَرْفَعُ مِئْذَنَةً لِلْبَنَفْسَجِ بَيْنَهُمَا أَوْ نَخِيلاَ

نُحِبُّ الحَيَاةَ إِذَا مَا اسْتَطَعْنَا إِلَيْهَا سَبِيلاَ
وَنَسْرِقُ مِنْ دُودَةِ القَزِّ خَيْطاً لِنَبْنِي سَمَاءً لَنَا وَنُسَيِّجَ هَذَا الرَّحِيلاَ
وَنَفْتَحُ بَابَ الحَدِيقَةِ كَيْ يَخْرُجَ اليَاسَمِينُ إِلَى الطُّرُقَاتِ نَهَاراً جَمِيلاَ
نُحِبُّ الحَيَاةَ إِذَا مَا اسْتَطَعْنَا إِلَيْهَا سَبِيلاَ

وَنَزْرَعُ حَيْثُ أَقمْنَا نَبَاتاً سَريعَ النُّمُوِّ , وَنَحْصدْ حَيْثُ أَقَمْنَا قَتِيلاَ
وَنَنْفُخُ فِي النَّايِ لَوْنَ البَعِيدِ البَعِيدِ , وَنَرْسُمُ فَوْقَ تُرابِ المَمَرَّ صَهِيلاَ
وَنَكْتُبُ أَسْمَاءَنَا حَجَراً ’ أَيُّهَا البَرْقُ أَوْضِحْ لَنَا اللَّيْلَ ’ أَوْضِحْ قَلِيلاَ
نُحِبُّ الحَيَاةَ إِذا مَا اسْتَطَعْنَا إِلَيْهَا سَبِيلا...'''

result = analyzer.analyze_free_verse(modern_poem)

if 'poemErr' not in result:
    print(f"Detected dominant meter: {result['ba7er']}")
    print(f"Number of prosodic feet: {len(result['tafa3eel'])}")
    print("\nProsodic analysis:")
    
    for i in range(len(result['tafa3eel'])):
        foot_pattern = result['tafa3eel'][i]
        foot_name = result['names'][i] if i < len(result['names']) else 'Unknown'
        foot_text = result['words'][i] if i < len(result['words']) else ''
        print(f"  {foot_pattern} ({foot_name}): {foot_text}")
else:
    print(f"Analysis failed: {result['poemErr']}")
```

### Advanced Usage with Wizard Analysis

```python
# Using wizard analysis for educational purposes
verse = "متى منْ طوْل نزْفك تسْتريْحُ"

# Define expected patterns for طويل meter
expected_patterns = [
    ['U--', 'U-U'],  # First foot options
    ['U---'],        # Second foot
    ['U--', 'U-U'],  # Third foot options  
    ['U---', 'U-U-', 'U--']  # Final foot options
]

pattern_names = [
    ['فَعُولُن', 'فَعُولُ'],
    ['مَفَاعِيلُن'],
    ['فَعُولُن', 'فَعُولُ'],
    ['مَفَاعِيلُن', 'مَفَاعِلُن', 'فَعُولُن']
]

wizard_result = analyzer.wizard_analysis_classical(
    verse, 
    is_ajez=False, 
    rule_patterns=expected_patterns,
    rule_names=pattern_names
)

print("Wizard Analysis Results:")
for result in wizard_result:
    status = "✅" if result['status'] == 'ok' else "❌"
    print(f"{status} {result['taf3eela']}: {result['chars']}")
    
    if result['status'] == 'err' and 'errs' in result:
        for error in result['errs']:
            print(f"    Error: {error}")
```

## Command Line Interface

The package includes a comprehensive CLI tool:

```bash
# Analyze a single verse
faraheedy analyze "أرحْ قمْح غيّابٍ يجافوْن منْجلكْ"

# Analyze from file
faraheedy analyze-file poem.txt --type classical

# Analyze free verse
faraheedy analyze-file modern_poem.txt --type free-verse

# Interactive mode for experimentation
faraheedy interactive

# Batch analysis of multiple files
faraheedy batch-analyze poems_directory/ --output results.json

# Get detailed help
faraheedy --help
```

## Advanced Features

### Custom Meter Detection

```python
# For researchers working with rare or historical meters
analyzer = ArabicPoetryAnalyzer()

# Enable experimental meter detection
result = analyzer.analyze_classical_verse(
    verse, 
    enable_experimental=True,
    confidence_threshold=0.7
)

if result['ba7er_name'] == 'unknown':
    print("Meter not recognized with standard patterns")
    if 'alternatives' in result:
        print("Possible alternatives:")