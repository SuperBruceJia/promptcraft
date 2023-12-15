# coding=utf-8
#
# Copyright 2021: https://github.com/PrithivirajDamodaran/Parrot_Paraphraser
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by Shuyue Jia

import re
import difflib

import torch
import pandas as pd
import Levenshtein
from scipy import spatial
from scipy.special import softmax
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import MinMaxScaler
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
)
from sentence_transformers import SentenceTransformer

paraphraser_tag = "prithivida/parrot_paraphraser_on_T5"
adequacy_tag = 'prithivida/parrot_adequacy_model'
fluency_tag = 'prithivida/parrot_fluency_model'
diversity_tag = 'paraphrase-distilroberta-base-v2'


class Adequacy:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(adequacy_tag)
        self.model = AutoModelForSequenceClassification.from_pretrained(adequacy_tag, torch_dtype=torch.float32)

    def filter(self, input_phrase, paraphrases, threshold, device="cpu"):
        top_phrases = []
        for phrase in paraphrases:
            x = self.tokenizer(input_phrase, phrase, return_tensors='pt', max_length=128, truncation=True)
            self.model = self.model.to(device)

            logits = self.model(**x).logits
            probs = logits.softmax(dim=1)
            prob_label = probs[:, 1]

            score = prob_label.item()
            if score >= threshold:
                top_phrases.append(phrase)

        return top_phrases

    def score(self, input_phrase, paraphrases, threshold, device="cpu"):
        scores = {}
        for phrase in paraphrases:
            x = self.tokenizer(input_phrase, phrase, return_tensors='pt', max_length=128, truncation=True)
            x = x.to(device)
            self.model = self.model.to(device)

            logits = self.model(**x).logits
            probs = logits.softmax(dim=1)
            prob_label = probs[:, 1]

            score = prob_label.item()
            if score >= threshold:
                scores[phrase] = score

        return scores


class Fluency:

    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(fluency_tag, num_labels=2,
                                                                        torch_dtype=torch.float32)
        self.tokenizer = AutoTokenizer.from_pretrained(fluency_tag)

    def filter(self, paraphrases, threshold, device="cpu"):
        self.model = self.model.to(device)

        top_phrases = []
        for phrase in paraphrases:
            input_ids = self.tokenizer("Sentence: " + phrase, return_tensors='pt', truncation=True)
            input_ids = input_ids.to(device)
            prediction = self.model(**input_ids)

            scores = prediction[0][0].detach().cpu().numpy()
            scores = softmax(scores)
            score = scores[1]  # LABEL_0 = Bad Fluency, LABEL_1 = Good Fluency

            if score >= threshold:
                top_phrases.append(phrase)

        return top_phrases

    def score(self, paraphrases, threshold, device="cpu"):
        self.model = self.model.to(device)

        fluency_scores = {}
        for phrase in paraphrases:
            input_ids = self.tokenizer("Sentence: " + phrase, return_tensors='pt', truncation=True)
            input_ids = input_ids.to(device)
            prediction = self.model(**input_ids)

            scores = prediction[0][0].detach().cpu().numpy()
            scores = softmax(scores)
            score = scores[1]  # LABEL_0 = Bad Fluency, LABEL_1 = Good Fluency

            if score >= threshold:
                fluency_scores[phrase] = score

        return fluency_scores


class Diversity:

    def __init__(self):
        self.model = SentenceTransformer(diversity_tag)

    def rank(self, input_phrase, paraphrases, ranker='levenshtein'):
        if ranker == "levenshtein":
            return self.levenshtein_ranker(input_phrase, paraphrases)
        elif ranker == "euclidean":
            return self.euclidean_ranker(input_phrase, paraphrases)
        elif ranker == "diff":
            return self.diff_ranker(input_phrase, paraphrases)

    def euclidean_ranker(self, input_phrase, paraphrases):
        scores = {}
        outputs = []
        input_enc = self.model.encode(input_phrase.lower())

        for phrase in paraphrases:
            enc = self.model.encode(phrase.lower())
            l2_dis = (spatial.distance.euclidean(input_enc, enc))
            outputs.append((phrase, l2_dis))

        df = pd.DataFrame(outputs, columns=['paraphrase', 'scores'])
        fields = []
        for col in df.columns:
            if col == "scores":
                tup = ([col], MinMaxScaler())
            else:
                tup = ([col], None)

            fields.append(tup)

        mapper = DataFrameMapper(fields, df_out=True)
        for index, row in mapper.fit_transform(df.copy()).iterrows():
            scores[row['paraphrase']] = row['scores']

        return scores

    def levenshtein_ranker(self, input_phrase, paraphrases):
        scores = {}
        for phrase in paraphrases:
            distance = Levenshtein.distance(input_phrase.lower(), phrase)
            scores[phrase] = distance

        return scores

    def diff_ranker(self, input_phrase, paraphrases):
        differ = difflib.Differ()

        scores = {}
        for phrase in paraphrases:
            diff = differ.compare(input_phrase.split(), phrase.split())
            count = 0
            for d in diff:
                if "+" in d or "-" in d:
                    count += 1

            scores[phrase] = count

        return scores


class Parrot:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(paraphraser_tag)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(paraphraser_tag, torch_dtype=torch.float32)

        self.adequacy_score = Adequacy()
        self.fluency_score = Fluency()
        self.diversity_score = Diversity()

    def augment(
            self,
            input_phrase,
            ranker="levenshtein",
            diversity_penalty=False,
            max_return_phrases=10,
            max_length=128,
            adequacy_threshold=0.90,
            fluency_threshold=0.90
    ):
        device = "cpu"
        self.model = self.model.to(device)

        save_phrase = input_phrase
        if len(input_phrase) >= max_length:
            max_length += 32

        input_phrase = re.sub('[^a-zA-Z0-9 \?\'\-\/\:\.]', '', input_phrase)
        input_phrase = "paraphrase: " + input_phrase

        input_ids = self.tokenizer.encode(input_phrase, return_tensors='pt')
        input_ids = input_ids.to(device)

        if diversity_penalty:
            for n in range(2, 9):
                if max_return_phrases % n == 0:
                    break

            preds = self.model.generate(
                input_ids,
                do_sample=False,
                max_length=max_length,
                num_beams=max_return_phrases,
                num_beam_groups=n,
                diversity_penalty=2.0,
                early_stopping=True,
                num_return_sequences=max_return_phrases
            )

        else:
            preds = self.model.generate(
                input_ids,
                do_sample=True,
                max_length=max_length,
                top_k=50,
                top_p=0.95,
                early_stopping=True,
                num_return_sequences=max_return_phrases
            )

        paraphrases = set()

        for pred in preds:
            gen_pp = self.tokenizer.decode(pred, skip_special_tokens=True).lower()
            gen_pp = re.sub('[^a-zA-Z0-9 \?\'\-]', '', gen_pp)
            paraphrases.add(gen_pp)

        adequacy_filter = self.adequacy_score.filter(input_phrase, paraphrases, adequacy_threshold, device)
        if len(adequacy_filter) > 0:
            fluency_filter = self.fluency_score.filter(adequacy_filter, fluency_threshold, device)

            if len(fluency_filter) > 0:
                scored_phrases = self.diversity_score.rank(input_phrase, fluency_filter, ranker)

                phrases = []
                for phrase, diversity_score in scored_phrases.items():
                    phrases.append((phrase, diversity_score))

                phrases.sort(key=lambda x: x[1], reverse=True)

                return phrases

            else:
                return [(save_phrase, 0)]
