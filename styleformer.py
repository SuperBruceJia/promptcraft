# coding=utf-8
#
# Copyright 2021: https://github.com/PrithivirajDamodaran/Styleformer
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

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
)

adequacy_tag = 'prithivida/parrot_adequacy_model'
ftc_tag = "prithivida/formal_to_informal_styletransfer"
ctf_tag = "prithivida/informal_to_formal_styletransfer"
atp_tag = "prithivida/active_to_passive_styletransfer"
pta_tag = "prithivida/passive_to_active_styletransfer"


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


class StyleFormer:

    def __init__(self, style=0):
        self.style = style

    def transfer(self, input_phrase, filter=0.95, candidates=5):
        device = "cpu"

        if self.style == 0:
            output = self._casual_to_formal(input_phrase, device, filter, candidates)
            return output

        elif self.style == 1:
            output = self._formal_to_casual(input_phrase, device, filter, candidates)
            return output

        elif self.style == 2:
            output = self._active_to_passive(input_phrase, device)
            return output

        elif self.style == 3:
            output = self._passive_to_active(input_phrase, device)
            return output

    def _formal_to_casual(self, input_phrase, device, filter, candidates):
        self.ftc_tokenizer = AutoTokenizer.from_pretrained(ftc_tag)
        self.ftc_model = AutoModelForSeq2SeqLM.from_pretrained(ftc_tag, torch_dtype=torch.float32)

        ftc_prefix = "transfer Formal to Casual: "
        src_sen = input_phrase
        sen = ftc_prefix + input_phrase
        input_ids = self.ftc_tokenizer.encode(sen, return_tensors='pt')

        self.ftc_model = self.ftc_model.to(device)
        input_ids = input_ids.to(device)

        preds = self.ftc_model.generate(
            input_ids,
            do_sample=True,
            max_length=128,
            top_k=50,
            top_p=0.95,
            early_stopping=True,
            num_return_sequences=candidates
        )

        gen_sen = set()
        for pred in preds:
            gen_sen.add(self.ftc_tokenizer.decode(pred, skip_special_tokens=True).strip())

        self.adequacy = Adequacy()
        phrases = self.adequacy.score(src_sen, list(gen_sen), filter, device)
        ranking = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
        if len(ranking) > 0:
            return ranking[0][0]
        else:
            return None

    def _casual_to_formal(self, input_phrase, device, filter, candidates):
        self.ctf_tokenizer = AutoTokenizer.from_pretrained(ctf_tag)
        self.ctf_model = AutoModelForSeq2SeqLM.from_pretrained(ctf_tag, torch_dtype=torch.float32)

        ctf_prefix = "transfer Casual to Formal: "
        src_sen = input_phrase
        input_phrase = ctf_prefix + input_phrase
        input_ids = self.ctf_tokenizer.encode(input_phrase, return_tensors='pt')

        self.ctf_model = self.ctf_model.to(device)
        input_ids = input_ids.to(device)

        preds = self.ctf_model.generate(
            input_ids,
            do_sample=True,
            max_length=128,
            top_k=50,
            top_p=0.95,
            early_stopping=True,
            num_return_sequences=candidates
        )

        gen_sen = set()
        for pred in preds:
            gen_sen.add(self.ctf_tokenizer.decode(pred, skip_special_tokens=True).strip())

        self.adequacy = Adequacy()
        phrases = self.adequacy.score(src_sen, list(gen_sen), filter, device)
        ranking = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
        if len(ranking) > 0:
            return ranking[0][0]
        else:
            return None

    def _active_to_passive(self, input_phrase, device):
        self.atp_tokenizer = AutoTokenizer.from_pretrained(atp_tag)
        self.atp_model = AutoModelForSeq2SeqLM.from_pretrained(atp_tag, torch_dtype=torch.float32)

        atp_prefix = "transfer Active to Passive: "
        input_phrase = atp_prefix + input_phrase
        input_ids = self.atp_tokenizer.encode(input_phrase, return_tensors='pt')

        self.atp_model = self.atp_model.to(device)
        input_ids = input_ids.to(device)

        preds = self.atp_model.generate(
            input_ids,
            do_sample=True,
            max_length=128,
            top_k=50,
            top_p=0.95,
            early_stopping=True,
            num_return_sequences=1
        )

        return self.atp_tokenizer.decode(preds[0], skip_special_tokens=True).strip()

    def _passive_to_active(self, input_phrase, device):
        self.pta_tokenizer = AutoTokenizer.from_pretrained(pta_tag)
        self.pta_model = AutoModelForSeq2SeqLM.from_pretrained(pta_tag, torch_dtype=torch.float32)

        pta_prefix = "transfer Passive to Active: "
        input_phrase = pta_prefix + input_phrase
        input_ids = self.pta_tokenizer.encode(input_phrase, return_tensors='pt')

        self.pta_model = self.pta_model.to(device)
        input_ids = input_ids.to(device)

        preds = self.pta_model.generate(
            input_ids,
            do_sample=True,
            max_length=128,
            top_k=50,
            top_p=0.95,
            early_stopping=True,
            num_return_sequences=1
        )

        return self.pta_tokenizer.decode(preds[0], skip_special_tokens=True).strip()
