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
- [Parallel Processing](#Parallel-Processing)
- [Structure of the Code](#Structure-of-the-Code)
- [Citation](#Citation)
- [Acknowledgement](#Acknowledgement)

# Installation
```shell
pip install promptcraft
```

# Character Editing
Character-level Prompt Perturbation\
`CharacterPerturb` class for manipulating character in a sentence
```python
from promptcraft import character

sentence = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May."
level = 0.25  # Percentage of characters that will be edited
character_tool = character.CharacterPerturb(sentence=sentence, level=level)
```
## Character Replacement
Randomly replace `level` percentage characters from the sentence
```python
char_replace = character_tool.character_replacement()
```
## Character Deletion
Randomly delete `level` percentage characters from the sentence
```python
char_delete = character_tool.character_deletion()
```
## Character Insertion
Randomly insert `level` percentage characters to the sentence
```python
char_insert = character_tool.character_insertion()
```
## Character Swap
Randomly swap `level` percentage characters in the sentence\
NOTE: including self-swapping
```python
char_swap = character_tool.character_swap()
```
## Keyboard Typos
Randomly substitute `level` percentage characters in the sentence
with a randomly chosen character which is near the original character in the Keyboard (USA Full-size Layout)\
NOTE:\
(1) We applied `keyboard_distance=1`, i.e., the nearest character, number, or samples.\
(2) If it is a character, we randomly chose lowercase or uppercase.
```python
char_keyboard = character_tool.keyboard_typos()
```
## Optical Character Recognition
Randomly substitute `level` percentage characters in the sentence with a common OCR map error
```python
char_ocr = character_tool.optical_character_recognition()
```

# Word Manipulation
Word-level Prompt Perturbation
`WordPerturb` class for manipulating words in a sentence

NOTE: the number of words in a sentence is only the valid words without considering spaces, special symbols, and punctuations
```python
from promptcraft import word

sentence = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May."
level = 0.25  # Percentage of words that will be manipulated
word_tool = word.WordPerturb(sentence=sentence, level=level)
```
## Synonym Replacement
Randomly choose $n$ words from the sentence that are not stop words.\
Replace each of these words with one of its synonyms chosen at random.\
Problem 1: Without any synonyms\
Problem 2: Fewer positions than needed positions
```python
word_synonym = word_tool.synonym_replacement()
```
## Word Insertion
Find a random synonym of a random word in the sentence that is not a stop word.\
Insert that synonym into a random position in the sentence.\
Do this $n$ times.
```python
word_insert = word_tool.word_insertion()
```
## Word Swap
Randomly choose two words in the sentence and swap their positions.\
Do this $n$ times.
```python
word_swap = word_tool.word_swap()
```
## Word Deletion
Each word in the sentence can be randomly removed with probability $p$.
```python
word_delete = word_tool.word_deletion()
```
## Insert Punctuation
Randomly insert punctuation in the sentence with probability $p$.
```python
word_punctuation = word_tool.insert_punctuation()
```
## Word Split
Randomly split a word to two tokens randomly
```python
word_split = word_tool.word_split()
```

# Sentence Paraphrasing
Sentence-level Prompt Perturbation\
`SentencePerturb` class for directly manipulating a sentence
```python
from promptcraft import sentence

sen = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May."
sentence_tool = sentence.SentencePerturb(sentence=sen)
```
## Back Translation by Hugging Face
Back translate the sentence (English $\rightarrow$ German $\rightarrow$ English) via 🤗 Hugging Face MarianMTModel 
```python
back_trans_hf = sentence_tool.back_translation_hugging_face()
```
## Back Translation by Google Translator
Back translate the sentence (English $\rightarrow$ German $\rightarrow$ English) via Google Translate API
```python
back_trans_google = sentence_tool.back_translation_google()
```
## Paraphrasing
Paraphrasing the sentence via [Parrot Paraphraser](https://github.com/PrithivirajDamodaran/Parrot_Paraphraser) 
considering\
(1) **Adequency**: Is the meaning preserved adequately?\
(2) **Fluency**: Is the paraphrase fluent English?\
(3) **Diversity**: (Lexical / Phrasal / Syntactical): How much has the paraphrase changed the original sentence?
```python
sen_paraphrase = sentence_tool.paraphrase()
```
## Formal Style
Transform the sentence style to Formal
```python
sen_formal = sentence_tool.formal()
```
## Casual Style
Transform the sentence style to Casual
```python
sen_casual = sentence_tool.casual()
```
## Passive Style
Transform the sentence style to Passive
```python
sen_passive = sentence_tool.passive()
```
## Active Style
Transform the sentence style to Active
```python
sen_active = sentence_tool.active()
```

# Parallel Processing
Since all the methods are executed on the CPU, 
they can be performed in parallel using the `multiprocessing` package.

# Structure of the Code
At the root of the project, you will see:
```text
.
├── LICENSE
├── README.md
├── promptcraft
│   ├── __init__.py
│   ├── character.py
│   ├── parrot.py
│   ├── sentence.py
│   ├── styleformer.py
│   └── word.py
├── setup.cfg
└── setup.py
```

# Citation
If you find our list useful, please consider citing our repo and toolkit in your publications. We provide a BibTeX entry below.
```bibtex
@misc{JiaPromptCraft23,
      author = {Jia, Shuyue},
      title = {{PromptCraft}: A Prompt Perturbation Toolkit},
      year = {2023},
      publisher = {GitHub},
      journal = {GitHub Repository},
      howpublished = {\url{https://github.com/SuperBruceJia/promptcraft}},
}

@misc{JiaAwesomeLLM23,
      author = {Jia, Shuyue},
      title = {Awesome-{LLM}-Self-Consistency},
      year = {2023},
      publisher = {GitHub},
      journal = {GitHub Repository},
      howpublished = {\url{https://github.com/SuperBruceJia/Awesome-LLM-Self-Consistency}},
}

@misc{JiaAwesomeSTS23,
      author = {Jia, Shuyue},
      title = {Awesome-Semantic-Textual-Similarity},
      year = {2023},
      publisher = {GitHub},
      journal = {GitHub Repository},
      howpublished = {\url{https://github.com/SuperBruceJia/Awesome-Semantic-Textual-Similarity}},
}
```

# Acknowledgement
This work was finished during my 2023 fall semester research rotation
at the Dependable Computing Laboratory, Department of Electrical and Computer Engineering,
Boston University, under the supervision of Prof. Wenchao Li.
