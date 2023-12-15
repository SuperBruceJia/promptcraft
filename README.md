# PromptCraft
A Prompt Perturbation Toolkit for Prompt Robustness Analysis

[![Code License](https://img.shields.io/badge/Code%20License-MIT-green.svg)](CODE_LICENSE)
[![License](https://img.shields.io/badge/Running%20on-CPU-red.svg)](https://github.com/SuperBruceJia/promptcraft)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

# Table of Contents
- [Installation](#Installation)
- [Character Editing](#Character-Editing)
  - [Character Replacement](#Character-Replacement)
  - [Character Deletion](#Character-Deletion)
  - [Character Insertion](#Character-Insertion)
  - [Character Swap](#Character-Swap)
  - [Keyboard Typos](#Keyboard-Typos)
  - [Optical Character Recognition (OCR)](#Optical-Character-Recognition)
- [Word Manipulation](#Word-Manipulation)
  - [Synonym Replacement](#Synonym-Replacement)
  - [Word Insertion](#Word-Insertion)
  - [Word Swap](#Word-Swap)
  - [Word Deletion](#Word-Deletion)
  - [Insert Punctuation](#Insert-Punctuation)
  - [Word Split](#Word-Split)
- [Sentence Paraphrasing](#Sentence-Paraphrasing)
  - [Back Translation based on 🤗 Hugging Face MarianMTModel](#Back-Translation-by-Hugging-Face)
  - [Back Translation based on Google Translator](#Back-Translation-by-Google-Translator)
  - [Paraphrasing](#Paraphrasing)
  - [Formal Style](#Formal-Style)
  - [Casual Style](#Casual-Style)
  - [Passive Style](#Passive-Style)
  - [Active Style](#Active-Style)
- [Structure of the code](#Structure-of-the-code)
- [Acknowledgement](#Acknowledgement)

# Installation
```shell
pip install promptcraft
```

# Character Editing
```python
from promptcraft import character

sentence = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May."
level = 0.25  # Number of characters that will be edited

character_tool = character.CharacterPerturb(sentence=sentence, level=level)
```
## Character Replacement
```python
char_replace = character_tool.character_replacement()
```
## Character Deletion
```python
char_delete = character_tool.character_deletion()
```
## Character Insertion
```python
char_insert = character_tool.character_insertion()
```
## Character Swap
```python
char_swap = character_tool.character_swap()
```
## Keyboard Typos
```python
char_keyboard = character_tool.keyboard_typos()
```
## Optical Character Recognition
```python
char_ocr = character_tool.optical_character_recognition()
```
# Word Manipulation
```python
from promptcraft import word

sentence = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May."
level = 0.25  # Number of words that will be manipulated
word_tool = word.WordPerturb(sentence=sentence, level=level)
```
## Synonym Replacement
```python
word_synonym = word_tool.synonym_replacement()
```
## Word Insertion
```python
word_insert = word_tool.word_insertion()
```
## Word Swap
```python
word_swap = word_tool.word_swap()
```
## Word Deletion
```python
word_delete = word_tool.word_deletion()
```
## Insert Punctuation
```python
word_punctuation = word_tool.insert_punctuation()
```
## Word Split
```python
word_split = word_tool.word_split()
```

# Sentence Paraphrasing
```python
from promptcraft import sentence

sentence = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May."
sentence_tool = sentence.SentencePerturb(sentence=sentence)
```
## Back Translation by Hugging Face
```python
back_trans_hf = sentence_tool.back_translation_hugging_face()
```
## Back Translation by Google Translator
```python
back_trans_google = sentence_tool.back_translation_google()
```
## Paraphrasing
```python
sen_paraphrase = sentence_tool.paraphrase()
```
## Formal Style
```python
sen_formal = sentence_tool.formal()
```
## Casual Style
```python
sen_casual = sentence_tool.casual()
```
## Passive Style
```python
sen_passive = sentence_tool.passive()
```
## Active Style
```python
sen_active = sentence_tool.active()
```

# Structure of the code
At the root of the project, you will see:
```text
.
├── LICENSE
├── README.md
├── __init__.py
├── character.py
├── parrot.py
├── sentence.py
├── setup.py
├── styleformer.py
└── word.py
```

# Acknowledgement
This work was finished during my 2023 fall semester research rotation
at the Dependable Computing Laboratory, Department of Electrical and Computer Engineering,
Boston University, under the supervision of Prof. Wenchao Li.
