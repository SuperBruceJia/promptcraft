# coding=utf-8

import random

import torch
from transformers import MarianTokenizer, MarianMTModel
from googletrans import Translator

import styleformer
import parrot


class SentencePerturb:
    """
    Sentence-level Prompt Perturbation
    SentencePerturb class for directly manipulating a sentence
    Style transformation credits: https://github.com/PrithivirajDamodaran/Styleformer
    Paraphrasing credits: https://github.com/PrithivirajDamodaran/Parrot_Paraphraser
    """

    def __init__(self, sentence):
        # The sentence to be perturbed
        self.sentence = sentence

    def formal(self):
        # Input sentence
        sentence = self.sentence[:]

        # Casual to Formal
        style = styleformer.StyleFormer(style=0)

        try:
            # Implement the style transformation
            sentence = style.transfer(sentence)
            print('formal: ', sentence)
        except:
            print("Error in formal")
            return None

        return sentence

    def casual(self):
        # Input sentence
        sentence = self.sentence[:]

        # Formal to Casual
        style = styleformer.StyleFormer(style=1)

        try:
            # Implement the style transformation
            sentence = style.transfer(sentence)
            print('casual: ', sentence)
        except:
            print("Error in casual")
            return None

        return sentence

    def passive(self):
        # Input sentence
        sentence = self.sentence[:]

        # Active to Passive
        style = styleformer.StyleFormer(style=2)

        try:
            # Implement the style transformation
            sentence = style.transfer(sentence)
            print('passive: ', sentence)
        except:
            print("Error in passive")
            return None

        return sentence

    def active(self):
        # Input sentence
        sentence = self.sentence[:]

        # Passive to Active
        style = styleformer.StyleFormer(style=3)

        try:
            # Implement the style transformation
            sentence = style.transfer(sentence)
            print('active: ', sentence)
        except:
            print("Error in active")
            return None

        return sentence

    def back_translation_hugging_face(self):
        # Input sentence
        sentence = self.sentence[:]

        # Load the pre-trained English to German and German to English translation models
        en_de_name = "Helsinki-NLP/opus-mt-en-de"
        de_en_name = "Helsinki-NLP/opus-mt-de-en"

        tokenizer_en_de = MarianTokenizer.from_pretrained(en_de_name)
        model_en_de = MarianMTModel.from_pretrained(en_de_name, torch_dtype=torch.float32)

        tokenizer_de_en = MarianTokenizer.from_pretrained(de_en_name)
        model_de_en = MarianMTModel.from_pretrained(de_en_name, torch_dtype=torch.float32)

        try:
            # Translate from English to German
            trans_german = model_en_de.generate(**tokenizer_en_de(sentence,
                                                                  return_tensors="pt",
                                                                  padding=True,
                                                                  truncation=True))
            bt_german = tokenizer_en_de.decode(trans_german[0], skip_special_tokens=True)
        except:
            print("Error in back_translation_hugging_face")
            return None

        try:
            # Translate from German back to English
            trans_english = model_de_en.generate(**tokenizer_de_en(bt_german,
                                                                   return_tensors="pt",
                                                                   padding=True,
                                                                   truncation=True))
            bt_english = tokenizer_de_en.decode(trans_english[0], skip_special_tokens=True)
        except:
            print("Error in back_translation_hugging_face")
            return None

        return bt_english

    def back_translation_google(self):
        # Input sentence
        sentence = self.sentence[:]

        # Create a translator object
        translator = Translator()

        try:
            # Translate the sentence to German
            german = translator.translate(sentence, dest='de').text
        except:
            print("Error in back_translation_google")
            return None

        try:
            # Translate the German translation back to English
            back_english = translator.translate(german, dest='en').text
        except:
            print("Error in back_translation_google")
            return None

        return back_english

    def paraphrase(self):
        # Input sentence
        sentence = self.sentence[:]

        # Load Paraphraser
        paraphraser = parrot.Parrot()

        try:
            # Get paraphrased sentences
            paraphrases = paraphraser.augment(input_phrase=sentence)
            sentence = random.sample(paraphrases, 1)[0][0]

            return sentence
        except:
            return None
