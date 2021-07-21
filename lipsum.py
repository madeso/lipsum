#!/usr/bin/env python3
import random
import typing
import argparse
import sys
import collections

WORDS_LOREM = [
    'sed',
    'in',
    'ut',
    'et',
    'ac',
    'nec',
    'vel',
    'sit',
    'amet',
    'a',
    'quis',
    'eu',
    'id',
    'vitae',
    'at',
    'non',
    'eget',
    'nulla',
    'mauris',
    'pellentesque',
    'nunc',
    'tincidunt',
    'vestibulum',
    'aliquam',
    'ante',
    'donec',
    'ipsum',
    'orci',
    'turpis',
    'lorem',
    'dolor',
    'urna',
    'risus',
    'erat',
    'nibh',
    'lacus',
    'dui',
    'mi',
    'elit',
    'ligula',
    'libero',
    'magna',
    'quam',
    'enim',
    'sapien',
    'purus',
    'ex',
    'velit',
    'nisl',
    'odio',
    'arcu',
    'est',
    'justo',
    'sem',
    'tellus',
    'diam',
    'malesuada',
    'nisi',
    'felis',
    'eros',
    'tortor',
    'lectus',
    'augue',
    'massa',
    'metus',
    'tristique',
    'leo',
    'neque',
    'cursus',
    'posuere',
    'faucibus',
    'vehicula',
    'egestas',
    'volutpat',
    'suspendisse',
    'interdum',
    'scelerisque',
    'bibendum',
    'ultrices',
    'convallis',
    'luctus',
    'consectetur',
    'efficitur',
    'imperdiet',
    'congue',
    'rhoncus',
    'tempus',
    'ornare',
    'mollis',
    'auctor',
    'pharetra',
    'morbi',
    'pretium',
    'mattis',
    'facilisis',
    'eleifend',
    'sollicitudin',
    'lobortis',
    'dictum',
    'ullamcorper',
    'tempor',
    'lacinia',
    'iaculis',
    'hendrerit',
    'rutrum',
    'viverra',
    'aenean',
    'elementum',
    'phasellus',
    'porttitor',
    'nullam',
    'condimentum',
    'varius',
    'pulvinar',
    'feugiat',
    'suscipit',
    'semper',
    'dapibus',
    'vulputate',
    'euismod',
    'accumsan',
    'blandit',
    'venenatis',
    'commodo',
    'dignissim',
    'porta',
    'cras',
    'finibus',
    'fermentum',
    'placerat',
    'maximus',
    'maecenas',
    'sodales',
    'etiam',
    'nam',
    'praesent',
    'consequat',
    'aliquet',
    'molestie',
    'gravida',
    'sagittis',
    'laoreet',
    'proin',
    'duis',
    'curabitur',
    'fringilla',
    'fusce',
    'ultricies',
    'integer',
    'quisque',
    'vivamus',
    'fames',
    'per',
    'primis',
    'habitant',
    'senectus',
    'netus',
    'facilisi',
    'potenti',
    'adipiscing',
    'class',
    'aptent',
    'taciti',
    'sociosqu',
    'ad',
    'litora',
    'torquent',
    'conubia',
    'nostra',
    'inceptos',
    'himenaeos',
    'natoque',
    'penatibus',
    'magnis',
    'dis',
    'parturient',
    'montes',
    'nascetur',
    'ridiculus',
    'mus',
    'cubilia',
    'curae',
    'hac',
    'habitasse',
    'platea',
    'dictumst'
]


class Bounds:
    """Bounds between[start, end) or a single value"""
    
    def __init__(self, start, end=None):
        self.start = start
        self.end = end
    
    def generate(self, rng):
        if self.end is None:
            return self.start
        else:
            return rng.randint(self.start, self.end)

def bounds(text: str) -> Bounds:
    """Parse a bounds string into a Bounds object"""
    if ':' in text:
        start, end = text.split(':')
        return Bounds(int(start), int(end))
    else:
        return Bounds(int(text))


DEFAULT_SENTENCE_PER_PARAGRAPH = Bounds(4, 7)
DEFAULT_NUMBER_OF_WORDS_PER_SENTENCE = Bounds(4, 15)
DEFAULT_START = 'Lorem ipsum dolor amet'

class SentenceRules:
    def __init__(self, comma_percentage = 0.66, comma_min_words = 7, min_words_before_comma = 3, min_words_after_comma = 1, number_of_words = DEFAULT_NUMBER_OF_WORDS_PER_SENTENCE):
        self.comma_percentage = comma_percentage
        self.comma_min_words = comma_min_words
        self.min_words_before_comma = min_words_before_comma
        self.min_words_after_comma = min_words_after_comma
        self.number_of_words = number_of_words


DEFAULT_SENTENCE_RULES = SentenceRules()


def add_comma(words: typing.List[str], rules: SentenceRules, rng):
    min_words = rules.min_words_before_comma + rules.min_words_after_comma + 1
    
    if min_words > len(words):
        return
    
    comma_index = rules.min_words_before_comma + rng.randint(0, len(words) - min_words)
    words[comma_index] += ',' if rng.random() < 0.8 else ';'


class LipsumGenerator:
    def __init__(self, words):
        self.words = words
        self.rng = random.Random()


    def make_a_sentence(self, sentence_rules: SentenceRules):
        word_indices = list(range(len(self.words)))
        self.rng.shuffle(word_indices)
        
        word_count = min(sentence_rules.number_of_words.generate(self.rng), len(word_indices))
        words = [self.words[i] for i in word_indices[:word_count]]
        words[0] = words[0].capitalize()

        include_comma = word_count >= sentence_rules.comma_min_words and self.rng.random() <= sentence_rules.comma_percentage
        if include_comma:
            add_comma(words, sentence_rules, self.rng)

        sentence = ' '.join(words) + '.'

        return sentence
    

    def make_a_paragraph(self, number_of_sentences: Bounds, sentence_rules: SentenceRules):
        return ' '.join(self.make_a_sentence(sentence_rules) for _ in range(number_of_sentences.generate(self.rng)))


    def make_many_paragraphs(self,
            number_of_paragraphs = Bounds(5),
            start_with = DEFAULT_START,
            number_of_sentences = DEFAULT_SENTENCE_PER_PARAGRAPH,
            sentence_rules = DEFAULT_SENTENCE_RULES):
        first_sentence = self.make_a_paragraph(number_of_sentences, sentence_rules)
        paragraphs = [first_sentence.rstrip() if start_with is None or len(start_with.strip()) == 0 else start_with + ' ' + first_sentence.lower().rstrip()]

        for i in range(number_of_paragraphs.generate(self.rng)-1):
            para = self.make_a_paragraph(number_of_sentences, sentence_rules)
            paragraphs.append(para.rstrip())
        return paragraphs
        


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(help='commands', dest='command')
    subs.required = True

    gen_parser = subs.add_parser('generate', help='Generate lorem ipsum text')
    gen_parser.add_argument('--words', type=bounds, default=DEFAULT_NUMBER_OF_WORDS_PER_SENTENCE, help='number of words in a sentence')
    gen_parser.add_argument('--paragraphs', type=bounds, default=Bounds(5), help='number of paragraphs to generate')   
    gen_parser.add_argument('--sentences', type=bounds, default=DEFAULT_SENTENCE_PER_PARAGRAPH, help='number of sentences per paragraph')
    gen_parser.add_argument('--start', type=str, default=DEFAULT_START, help='first sentence')
    gen_parser.add_argument('--output', type=argparse.FileType('w', encoding='UTF-8'), default=sys.stdout, help='output file')
    gen_parser.add_argument('--include_newline', action='store_true', help='include newline between each paragraph')
    gen_parser.set_defaults(func=main_generate)

    scan_parser = subs.add_parser('scan', help='Scan words from text file')
    scan_parser.add_argument('input', type=argparse.FileType('r', encoding='UTF-8'), default=sys.stdin, help='Text to grab words from')
    scan_parser.add_argument('--top', type=int, default=None, metavar='X', help='If specified, print the top X words instead')
    scan_parser.add_argument('--include_count', action='store_true', help='Include the count of each word')
    scan_parser.add_argument('--reverse', action='store_true', help='Reverse the order of the words')
    scan_parser.add_argument('--sep', type=str, default=None, help='Separator between word and count')
    scan_parser.set_defaults(func=main_scan)

    args = parser.parse_args()
    args.func(args)


def main_scan(args):
    words = collections.Counter()
    for line in args.input:
        words.update(word.strip(',').strip('.').strip(';').lower().strip() for word in line.split() if word.strip(',').strip('.').strip())

    word_list = words.most_common()
    if args.reverse:
        word_list = list(reversed(word_list))
    
    if args.top is not None:
        word_list = word_list[:args.top]
    
    for word, count in word_list:
        if args.include_count:
            if args.sep is None:
                print(f'{word} ({count})')
            else:
                print(f'{word}{args.sep}{count}')
        else:
            print(word)
    
    if args.include_count:
        print()
        print(f'{sum(words.values())} total words read')
        print(f'{len(list(words))} unique words read')


def main_generate(args):
    generator = LipsumGenerator(WORDS_LOREM)
    sentence_rules = SentenceRules(number_of_words=args.words)
    r = generator.make_many_paragraphs(start_with=args.start, number_of_paragraphs=args.paragraphs, sentence_rules=DEFAULT_SENTENCE_RULES)
    with args.output as f:
        for x in r:
            f.write(x + '\n')
            if args.include_newline:
                f.write('\n')
    
    
if __name__ == "__main__":
    main()
