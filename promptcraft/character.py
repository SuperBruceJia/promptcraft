# coding=utf-8

import random


# Define common characters
char_common = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~ "


# Define the USA keyboard layout mapping for nearby characters
keyboard_layout = {
    'a': 'qwsxz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'serfcx',
    'e': 'wrdasf34',
    'f': 'drtgvc',
    'g': 'ertyhvf',
    'h': 'rtyujbg',
    'i': 'ujko89',
    'j': 'tyuiknh',
    'k': 'yuiojl',
    'l': 'uiojkm',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'iklp90',
    'p': 'ol0',
    'q': 'aw12',
    'r': 'etdf45',
    's': 'awedxz',
    't': 'ryfg56',
    'u': 'yihj78',
    'v': 'cfgb',
    'w': 'qase23',
    'x': 'zasdc',
    'y': 'tghu67',
    'z': 'asx',
    '0': '9op',
    '1': '2q',
    '2': '13qw',
    '3': '24we',
    '4': '35er',
    '5': '46rt',
    '6': '57ty',
    '7': '68yu',
    '8': '79ui',
    '9': '80io'
}


ocr_errors = {
    'a': ['A', '4', '@', '∀', '^', 'Λ', '∆', 'λ', 'a', 'o', 'e'],
    'b': ['B', '8', '6', 'b', 'd', '|3', 'ß', 'Β', 'ƃ'],
    'c': ['C', 'c', 'e', 'o', '0', '©', '<', '[', '(', '¢'],
    'd': ['D', 'd', 'o', '0', '∂', 'δ', 'o|', 'cl', 'þ', '])', 'ð'],
    'e': ['E', '3', 'e', '∑', '€', '∈', '∃', '£', 'έ', 'Σ', 'ë'],
    'f': ['F', 'f', 't', '7', '+', 'ϝ', 'ʃ', 'ƒ', 'λ', 'ƭ', 'ρ'],
    'g': ['G', 'g', '9', '6', 'q', '&', 'gq', 'ʛ', 'ğ', 'ǥ', 'φ'],
    'h': ['H', 'h', '4', '5', '#', 'η', 'н', 'ħ', 'ђ', 'λ', 'н'],
    'i': ['I', '1', 'l', '|', '!', '∫', 'ί', 'Ǐ', 'ï', 'Σ', 'н'],
    'j': ['J', 'j', '1', '7', 'ij', 'ϳ', 'j', 'ʝ', 'ǰ', 'ן', 'ɉ'],
    'k': ['K', 'k', 'l', '|<', '|{', 'κ', 'ќ', 'κ', 'ƙ', 'ķ', 'л'],
    'l': ['L', 'l', '1', 'i', '|', '!', 'ℓ', '£', '£', 'ί', 'լ'],
    'm': ['M', 'm', 'n', 'rn', 'w', 'vv', '^^', 'mm', 'μ', 'λ', 'м'],
    'n': ['N', 'n', 'm', 'r', 'π', 'h', 'ח', 'й', 'ŋ', 'π', 'η'],
    'o': ['O', '0', 'o', 'θ', 'Ø', 'σ', 'φ', 'Φ', 'ο', '∞', 'ם'],
    'p': ['P', 'p', '|o', '|D', 'ρ', 'ρ', 'þ', 'φ', 'ρ', '¶', 'р'],
    'q': ['Q', 'q', 'g', '9', 'ℚ', 'ѳ', 'ϙ', 'ɋ', 'ք', 'Ɋ', 'ͼ'],
    'r': ['R', 'r', 'l', '1', '|', '7', 'я', 'г', '®', 'λ', 'г'],
    's': ['S', '5', 's', '§', 'z', '$', '∫', 'ʂ', 'ѕ', 'š', 'ʃ'],
    't': ['T', 't', '+', '7', '†', 'τ', 'т', 'ţ', 'ť', '±', 'π'],
    'u': ['U', 'u', 'v', 'w', 'µ', 'υ', 'ц', 'щ', 'μ', 'µ', 'บ'],
    'v': ['V', 'v', 'w', 'u', '∨', 'ν', '∀', 'ѵ', 'ν', 'в', 'ט'],
    'w': ['W', 'w', 'vv', 'uu', 'wv', 'wu', 'ш', 'ω', 'ώ', 'ω', 'ш'],
    'x': ['X', 'x', '+', '*', '×', 'χ', 'ж', 'ж', 'א', 'ж', 'ж'],
    'y': ['Y', 'y', 'γ', 'у', '¥', 'ү', 'ч', 'у', 'λ', 'ф', 'י'],
    'z': ['Z', 'z', '2', '7', 'ʒ', 'я', 'ʒ', 'ж', 'ʑ', 'ʐ', 'ζ'],
    '1': ['l', 'i', '!', '|'],
    '2': ['5', 'z', 's', '3'],
    '3': ['8', '2', '9'],
    '4': ['h', 'k', 'b', 'l', 'r'],
    '5': ['s', 'z', '2', '3', '8'],
    '6': ['b', '8', 'g', '9', '0'],
    '7': ['t', 'f', '1', 'h', 'k', 'b', 'l', 'r'],
    '8': ['5', '2', '3', '9'],
    '9': ['q', 'g', 'p', '6', '0', '8'],
    '0': ['o', 'd', 'c', 'p', 'g', 'q'],
    'A': ['4', '6', '8', '9', '0'],
    'B': ['6', '8'],
    'C': ['9', '0', 'e', 'o'],
    'D': ['0', '9', 'a', 'o'],
    'E': ['3', '8'],
    'F': ['5', '7', 't'],
    'G': ['6', '9', 'q', 'y'],
    'H': ['4', '6', '8'],
    'I': ['1', 'l', '!', '|'],
    'J': ['1', '7'],
    'K': ['1', '4'],
    'L': ['1', 'i', '!', '|'],
    'M': ['n'],
    'N': ['m'],
    'O': ['0', 'c', 'd', 'q'],
    'P': ['9', 'q', 'b'],
    'Q': ['9', '0', 'o', 'p', 'g'],
    'R': ['7', '5', 't'],
    'S': ['5', '9', '2'],
    'T': ['7', '1', 'f'],
    'U': ['v'],
    'V': ['u'],
    'W': ['vv'],
    'X': ['4', '8'],
    'Y': ['g', '9'],
    'Z': ['2', '5']
    # '!': ['1', 'i', 'l', '|', '7'],
    # '|': ['l', 'i', '1', '!'],
    # '/': ['1', 'l', 'i', '!', '|'],
    # '(': ['8', '6', '9', 't', 'f', '7'],
    # '[': ['c', 'e', 'o', '(', '¢', '©'],
    # '¢': ['c', 'e', 'o', 'o', 'a', 'c', 'c', 'o', 'd', 'e', 'g', 's', 'q'],
    # '©': ['c', 'e', 'o', 'o', 'a', 'c', 'c', 'o', 'd', 'e', 'g', 's', 'q'],
    # '¥': ['7', '1', 'f', 'h', 'k', 'b', 'l', 't'],
    # '€': ['c', 'e', 'o'],
    # '£': ['6', '8'],
    # '$': ['5', '8', '2'],
}


class CharacterPerturb:
    """
    Character-level Prompt Perturbation
    CharacterPerturb class for manipulating character in a sentence
    """

    def __init__(self, sentence, level):
        # The sentence to be perturbed
        self.data = sentence
        # The perturbation level to be implemented
        self.percent = level

    def character_replacement(self):
        """
        Randomly replace `self.percent` percentage characters from the self.data
        """
        # Convert the sentence to a list of characters for easier manipulation
        char_list = list(self.data)

        # Calculate the number of characters to choose
        num = int(len(char_list) * self.percent)

        # Choose random positions to substitute
        positions = random.sample(range(len(self.data)), num)

        # Substitute the chosen characters with random characters
        for index in positions:
            char_re = random.choice(char_common)
            char_list[index] = char_re

        # Join the modified characters back into a string
        sentence = ''.join(char_list)

        return sentence

    def character_deletion(self):
        """
        Randomly delete `self.percent` percentage characters from the self.data
        """
        # Convert the sentence to a list of characters for easier manipulation
        char_list = list(self.data)

        # Calculate the number of characters to choose
        num = int(len(char_list) * self.percent)

        # Choose random positions to delete
        positions = random.sample(range(len(self.data)), num)

        # Sort the indices in reverse order so that deletion doesn't affect subsequent indices
        positions.sort(reverse=True)

        # Delete the selected characters
        for index in positions:
            char_list[index] = "X"
            # char_list[index] = "[X]"
            # del char_list[index]

        # Join the modified characters back into a string
        sentence = ''.join(char_list)

        return sentence

    def character_insertion(self):
        """
        Randomly insert `self.percent` percentage characters to the self.data
        """
        # Convert the sentence to a list of characters for easier manipulation
        char_list = list(self.data)

        # Calculate the number of characters to choose
        num = int(len(char_list) * self.percent)

        # Choose random positions to insert
        positions = random.sample(range(len(self.data)), num)

        # Initialize an empty list to store the modified sentence.
        sentence = []
        for index, char in enumerate(self.data):
            # Check if the current character's index is in the list of chosen indices.
            if index in positions:
                # Insert a random character in front of the chosen character.
                char_insert = random.choice(char_common)
                sentence.append(char_insert)

            sentence.append(char)

        # Convert the modified list back to a string.
        sentence = ''.join(sentence)

        return sentence

    def character_swap(self):
        """
        Randomly swap `self.percent` percentage characters in the self.data
        NOTE: including self-swapping
        """
        # Convert the sentence to a list of characters for easier manipulation
        char_list = list(self.data)

        # Calculate the number of characters to choose
        num = int(len(char_list) * self.percent)

        # Choose random positions 1 and 2 for swapping
        position_1 = random.sample(range(len(self.data)), num)
        position_2 = random.sample(range(len(self.data)), num)

        # Perform the character swaps
        for i in range(num):
            char_list[position_1[i]], char_list[position_2[i]] = char_list[position_2[i]], char_list[position_1[i]]

        # Convert the list of characters back to a string
        sentence = ''.join(char_list)

        return sentence

    def keyboard_typos(self):
        """
        Randomly substitute `self.percent` percentage characters in the self.data
        with a randomly chosen character which is near the original character in the Keyboard (USA Full-size Layout)
        NOTE:
            (1) We applied `keyboard_distance=1`, i.e., the nearest character, number, or samples.
            (2) If it is a character, we randomly chose lowercase or uppercase.
        """
        # Convert the sentence to a list of characters for easier manipulation
        char_list = list(self.data)

        # Calculate the number of characters to choose
        num = int(len(char_list) * self.percent)

        # Create a list of positions that correspond to characters or numbers
        positions = [i for i, char in enumerate(self.data) if char.isalnum()]
        positions = random.sample(positions, num)

        # Substitute the chosen characters with near keyboard characters
        for index in positions:
            char_ori = char_list[index]
            if char_ori.lower() in keyboard_layout:
                char_re = random.choice(keyboard_layout[char_ori.lower()])
                char_re = random.choice([char_re.lower(), char_re.upper()])
                char_list[index] = char_re

        # Join the modified characters back into a string
        sentence = ''.join(char_list)

        return sentence

    def optical_character_recognition(self):
        """
        Randomly substitute `self.percent` percentage characters in the self.data
        with a common OCR map error
        """
        # Convert the sentence to a list of characters for easier manipulation
        char_list = list(self.data)

        # Calculate the number of characters to choose
        num = int(len(char_list) * self.percent)

        # Create a list of positions that correspond to characters or numbers
        positions = [i for i, char in enumerate(self.data) if char.isalnum()]
        positions = random.sample(positions, num)

        # Substitute the chosen characters with common OCR errors
        for index in positions:
            char_ori = char_list[index]
            char_re = random.choice(ocr_errors[char_ori])
            char_list[index] = char_re

        # Join the modified characters back into a string
        sentence = ''.join(char_list)

        return sentence
