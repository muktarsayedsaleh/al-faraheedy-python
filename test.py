from main import ArabicPoetryAnalyzer

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