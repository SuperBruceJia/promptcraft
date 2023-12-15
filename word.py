# coding=utf-8

import re
import random

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

special_symbols = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

# Stop words list
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our',
              'ours', 'ourselves', 'you', 'your', 'yours',
              'yourself', 'yourselves', 'he', 'him', 'his',
              'himself', 'she', 'her', 'hers', 'herself',
              'it', 'its', 'itself', 'they', 'them', 'their',
              'theirs', 'themselves', 'what', 'which', 'who',
              'whom', 'this', 'that', 'these', 'those', 'am',
              'is', 'are', 'was', 'were', 'be', 'been', 'being',
              'have', 'has', 'had', 'having', 'do', 'does', 'did',
              'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
              'because', 'as', 'until', 'while', 'of', 'at',
              'by', 'for', 'with', 'about', 'against', 'between',
              'into', 'through', 'during', 'before', 'after',
              'above', 'below', 'to', 'from', 'up', 'down', 'in',
              'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when',
              'where', 'why', 'how', 'all', 'any', 'both', 'each',
              'few', 'more', 'most', 'other', 'some', 'such', 'no',
              'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
              'very', 's', 't', 'can', 'will', 'just', 'don',
              'should', 'now', '']


def get_synonyms(word):
    """
    Get synonyms for a word
    """
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    return synonyms


class WordPerturb:
    """
    Word-level Prompt Perturbation
    WordPerturb class for manipulating words in a sentence

    NOTE: the number of words in a sentence is only the valid words
    without considering spaces, special symbols, and punctuations
    """

    def __init__(self, sentence, level):
        # Original sentence
        self.sentence = sentence

        # Tokenize the sentence into words
        # self.words = word_tokenize(sentence)
        self.words = re.findall(r"\w+|\s+|[^\w\s]", self.sentence, re.UNICODE)

        # The perturbation level to be implemented
        # use the regular expression pattern \b\w+\b to match words
        # \b matches word boundaries
        # \w+ matches one or more word characters
        self.valid_words = re.findall(r'\b\w+\b', self.sentence)
        self.num = int(len(self.valid_words) * level)

        # Get the set of English stop words
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.add(" ")
        for symbol in special_symbols:
            self.stop_words.add(symbol)

        for stop in stop_words:
            self.stop_words.add(stop)

    def synonym_replacement(self):
        """
        Randomly choose n words from the sentence that are not stop words.
        Replace each of these words with one of its synonyms chosen at random.

        # Problem 1: Without any synonyms
        # Problem 2: Fewer positions than needed positions
        """
        # Convert the sentence to a list of words for easier manipulation
        sen_list = self.words[:]

        # Create a list of positions that correspond to the non-stop words
        positions = [i for i, word in enumerate(sen_list) if word.lower() not in self.stop_words]

        # Remove those positions that don't have any synonym
        for i in range(len(positions)):
            word_ori = self.words[positions[i]]
            synonyms = get_synonyms(word_ori)
            if len(synonyms) == 0:
                positions[i] = -1

        while -1 in positions:
            positions.remove(-1)

        # Randomly sample `self.num` positions
        if self.num >= len(positions):
            pass
        else:
            positions = random.sample(positions, self.num)

        # Replace chosen words with random synonyms
        for index in positions:
            word_ori = self.words[index]
            synonyms = get_synonyms(word_ori)

            # Randomly retrieve one synonym from all the synonyms
            synonym = random.choice(synonyms)
            if '_' in synonym:
                synonym = synonym.replace('_', ' ')

            sen_list[index] = synonym

        # Join the modified words back into a string
        sen_list = ''.join(sen_list)

        return sen_list

    def word_insertion(self):
        """
        Find a random synonym of a random word in the sentence that is not a stop word.
        Insert that synonym into a random position in the sentence.
        Do this n times.
        """
        # Convert the sentence to a list of words for easier manipulation
        sen_list = self.words.copy()

        # Create a list of positions that correspond to the non-stop words
        positions = [i for i, word in enumerate(sen_list) if word.lower() not in self.stop_words]
        non_sw_posi = positions.copy()

        # Remove those positions that don't have any synonym
        for i in range(len(positions)):
            word_ori = self.words[positions[i]]
            synonyms = get_synonyms(word_ori)
            if len(synonyms) == 0:
                positions[i] = -1

        while -1 in positions:
            positions.remove(-1)

        # Randomly sample `self.num` positions
        if self.num >= len(positions):
            pass
        else:
            positions = random.sample(positions, self.num)

        # Initialize an empty list to store the modified sentence.
        sen_init = []
        positions_insert = random.sample(non_sw_posi, self.num)
        for index, word in enumerate(sen_list):
            # Check if the current word's index is in the list of chosen indices.
            if index in positions_insert:
                # Insert a random character in front of the chosen character.
                random_index = random.sample(positions, 1)
                word_ori = self.words[random_index[0]]
                synonyms = get_synonyms(word_ori)

                # Randomly retrieve one synonym from all the synonyms
                word_insert = random.choice(synonyms)
                if '_' in word_insert:
                    word_insert = word_insert.replace('_', ' ')

                sen_init.append(word_insert)
                sen_init.append(" ")

            sen_init.append(word)

        # Convert the modified list back to a string.
        sen_init = ''.join(sen_init)

        return sen_init

    def word_swap(self):
        """
        Randomly choose two words in the sentence and swap their positions.
        Do this n times.
        """
        # Convert the sentence to a list of words for easier manipulation
        sen_list = self.words.copy()

        # Create a list of positions that correspond to non-stop words
        positions = [i for i, word in enumerate(sen_list) if word.lower() not in self.stop_words]

        # Choose random positions 1 and 2 for swapping
        position_1 = random.sample(positions, self.num)
        position_2 = random.sample(positions, self.num)

        # Perform the character swaps
        for i in range(self.num):
            sen_list[position_1[i]], sen_list[position_2[i]] = sen_list[position_2[i]], sen_list[position_1[i]]

        # Convert the list of characters back to a string
        sen_list = ''.join(sen_list)

        return sen_list

    def word_deletion(self):
        """
        Each word in the sentence can be randomly removed with probability p.
        """
        # Convert the sentence to a list of words for easier manipulation
        sen_list = self.words.copy()

        # Create a list of positions that correspond to non-stop words
        positions = [i for i, word in enumerate(sen_list) if word.lower() not in self.stop_words]

        # Randomly sample `self.num` positions from all positions
        positions = random.sample(positions, self.num)

        # Sort the indices in reverse order so that deletion doesn't affect subsequent indices
        positions.sort(reverse=True)

        # Delete the selected characters
        for index in positions:
            del sen_list[index]

        # Join the modified characters back into a string
        sen_list = ''.join(sen_list)

        return sen_list

    def insert_punctuation(self):
        """
        Randomly insert punctuation in the sentence with probability p.
        """
        # Convert the sentence to a list of words for easier manipulation
        sen_list = self.words.copy()

        # Create a list of positions that correspond to non-stop words
        positions = [i for i, word in enumerate(sen_list) if word.lower() not in self.stop_words]

        # Randomly sample `self.num` positions from all positions
        positions = random.sample(positions, self.num)

        # Initialize an empty list to store the modified sentence.
        sen_init = []
        for index, word in enumerate(self.words):
            sen_init.append(word)
            # Check if the current character's index is in the list of chosen indices.
            if index in positions:
                # Insert a random character in front of the chosen character.
                word_insert = random.choice(special_symbols)
                sen_init.append(word_insert)

        # Convert the modified list back to a string.
        sen_init = ''.join(sen_init)

        return sen_init

    def word_split(self):
        """
        Randomly split a word to two tokens randomly
        """
        # Convert the sentence to a list of words for easier manipulation
        sen_list = self.words.copy()

        # Create a list of positions that correspond to non-stop words
        positions = [i for i, word in enumerate(sen_list) if word.lower() not in self.stop_words]

        # Randomly sample `self.num` positions from all positions
        positions = random.sample(positions, self.num)

        # Initialize an empty list to store the modified sentence
        sen_init = []
        for index, word in enumerate(self.words):
            if index in positions:
                if len(word) > 1:
                    # Split the word into two pieces
                    indice = random.randint(1, len(word) - 1)

                    # Get the left and right subwords
                    left_subword = word[:indice]
                    right_subword = word[indice:]

                    # Append the left and right subwords
                    sen_init.append(left_subword)
                    sen_init.append(" ")
                    sen_init.append(right_subword)
                else:
                    pass
            else:
                sen_init.append(word)

        # Convert the modified list back to a string.
        sen_init = ''.join(sen_init)

        return sen_init
