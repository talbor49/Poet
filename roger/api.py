import logging

import roger.store
import roger.model
import roger.training
import roger.token
import roger.generator
import roger.util


def generate_api(database, seed_word='', lines=10, auto_punctuation=True):
    store = roger.store.SQLiteStore(path=database)
    model = roger.model.MarkovModel(store=store)

    generator = roger.generator.Generator(model)

    if seed_word:
        words = seed_word.split()

        if len(words) == 1:
            word_1 = None
            word_2 = words[0]
        elif len(words) == 2:
            word_1, word_2 = words
        else:
            raise Exception('Too many seed words. Max 2.')

    else:
        word_1 = None
        word_2 = None

    for dummy in range(lines):
        line = generator.generate_sentence(
            word_1, word_2, final_punctuation=auto_punctuation)
        print(line)


_logger = logging.getLogger(__name__)


def train_by_twitter_api(model, paths, sample=0.3, limit_model=100000):
    for path in paths:
        lines = roger.training.from_twitter_dump(path, sample=sample)

        train_api(model, lines, limit_model)


def train_api(model, lines, limit_model, lower_case=True):
    count = 0

    trigrams = roger.training.process_trigrams(lines, lower_case=lower_case)

    for index, trigrams_group in enumerate(roger.util.group(trigrams, size=10000)):
        model.train(trigrams_group)

        count += len(trigrams_group)
        _logger.info('Processed %d trigrams', count)

        if index % 100 == 0 and limit_model and \
                        model.store.count() > limit_model * 2:
            model.store.trim(limit_model)

    model.store.trim(limit_model)


def train_by_plain_text_api(model, file, limit_model=100000, keep_case=True):
    for file in file:
        train_api(model, file, limit_model, not keep_case)


def next_word_api(model, word1, word2=None):
    if word2:
        word_1 = word1
        word_2 = word2
    else:
        word_1 = None
        word_2 = word1

    trigram_model = model.get_trigram_model(word_1, word_2)

    for word, score in trigram_model.most_common():
        print(word, score)
