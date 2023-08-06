#!/usr/bin/env python3

from unittest import TestCase, main
import tweet_preprocessor


class TPPTest:
    """Base test class for methods which all Preprocessors implement."""

    def test_tokenize(self):
        for text, tokenized, _, _, _, _, *_ in self.test_tweets:
            tweet = tweet_preprocessor.Tweet(text)
            self.preprocessor._tokenize(tweet)
            self.assertEqual(tweet.get_preprocessed_text(), tokenized)

    def test_remove_urls(self):
        for text, _, no_urls, _, _, _, *_ in self.test_tweets:
            tweet = tweet_preprocessor.Tweet(text)
            self.preprocessor._tokenize(tweet)
            self.preprocessor._remove_urls(tweet)
            self.assertEqual(tweet.get_preprocessed_text(), no_urls)

    def test_remove_emojis(self):
        for text, _, _, no_emojis, _, _, *_ in self.test_tweets:
            tweet = tweet_preprocessor.Tweet(text)
            self.preprocessor._tokenize(tweet)
            self.preprocessor._remove_emojis(tweet)
            self.assertEqual(tweet.get_preprocessed_text(), no_emojis)

    def test_remove_hashtags(self):
        for text, _, _, _, no_hashtags, _, *_ in self.test_tweets:
            tweet = tweet_preprocessor.Tweet(text)
            self.preprocessor._tokenize(tweet)
            self.preprocessor._remove_hashtags(tweet)
            self.assertEqual(tweet.get_preprocessed_text(), no_hashtags)

    def test_anonymize_mentions(self):
        for text, _, _, _, _, anonymized, *_ in self.test_tweets:
            tweet = tweet_preprocessor.Tweet(text)
            self.preprocessor._tokenize(tweet)
            self.preprocessor._anonymize_mentions(tweet)
            self.assertEqual(tweet.get_preprocessed_text(), anonymized)


class EnTPPTest(TPPTest, TestCase):

    def setUp(self):
        self.preprocessor = tweet_preprocessor.EnTPP()
        self.test_tweets = [
            (
                '', '', '', '', '', '', ''
            ),
            (
                'RHOA stars @kenyamoore and @cynthiabailey10 have the same taste 😏 in men, and women! 😂 https://t.co/him363tpds',
                'RHOA stars @kenyamoore and @cynthiabailey10 have the same taste 😏 in men , and women ! 😂 https://t.co/him363tpds',
                'RHOA stars @kenyamoore and @cynthiabailey10 have the same taste 😏 in men , and women ! 😂',
                'RHOA stars @kenyamoore and @cynthiabailey10 have the same taste in men , and women ! https://t.co/him363tpds',
                'RHOA stars @kenyamoore and @cynthiabailey10 have the same taste 😏 in men , and women ! 😂 https://t.co/him363tpds',
                'RHOA stars @MENTION and @MENTION have the same taste 😏 in men , and women ! 😂 https://t.co/him363tpds',
                'RHOA stars @kenyamoore @cynthiabailey10 taste 😏 men , women ! 😂 https://t.co/him363tpds',
            ),
            (
                'Plenty of famous names, places&things were cited by Lorelai, Rory & Co. during the #GilmoreGirls revival: https://t.co/4c40IujnlQ 👌🖐🏼 https://t.co/85Rd1CCh0E',
                'Plenty of famous names , places & things were cited by Lorelai , Rory & Co . during the #GilmoreGirls revival : https://t.co/4c40IujnlQ 👌 🖐🏼 https://t.co/85Rd1CCh0E',
                'Plenty of famous names , places & things were cited by Lorelai , Rory & Co . during the #GilmoreGirls revival : 👌 🖐🏼',
                'Plenty of famous names , places & things were cited by Lorelai , Rory & Co . during the #GilmoreGirls revival : https://t.co/4c40IujnlQ https://t.co/85Rd1CCh0E',
                'Plenty of famous names , places & things were cited by Lorelai , Rory & Co . during the revival : https://t.co/4c40IujnlQ 👌 🖐🏼 https://t.co/85Rd1CCh0E',
                'Plenty of famous names , places & things were cited by Lorelai , Rory & Co . during the #GilmoreGirls revival : https://t.co/4c40IujnlQ 👌 🖐🏼 https://t.co/85Rd1CCh0E',
                'Plenty famous names , places & things cited Lorelai , Rory & Co . #GilmoreGirls revival : https://t.co/4c40IujnlQ 👌 🖐🏼 https://t.co/85Rd1CCh0E',
            ),
            (
                'Découvrez 35 idées de cadeaux de Noël pour une working girl 🎁🎅🎄 ➡️https://t.co/RdLYZxUQGN https://t.co/33ou1aYDs6',
                'Découvrez 35 idées de cadeaux de Noël pour une working girl 🎁 🎅 🎄 ➡ https://t.co/RdLYZxUQGN https://t.co/33ou1aYDs6',
                'Découvrez 35 idées de cadeaux de Noël pour une working girl 🎁 🎅 🎄 ➡',
                'Découvrez 35 idées de cadeaux de Noël pour une working girl https://t.co/RdLYZxUQGN https://t.co/33ou1aYDs6',
                'Découvrez 35 idées de cadeaux de Noël pour une working girl 🎁 🎅 🎄 ➡ https://t.co/RdLYZxUQGN https://t.co/33ou1aYDs6',
                'Découvrez 35 idées de cadeaux de Noël pour une working girl 🎁 🎅 🎄 ➡ https://t.co/RdLYZxUQGN https://t.co/33ou1aYDs6',
                'Découvrez 35 idées de cadeaux de Noël pour une working girl 🎁 🎅 🎄 ➡ https://t.co/RdLYZxUQGN https://t.co/33ou1aYDs6',
            )
        ]

    def test_remove_stopwords(self):
        for text, _, _, _, _, _, no_stopwords in self.test_tweets:
            tweet = tweet_preprocessor.Tweet(text)
            self.preprocessor._tokenize(tweet)
            self.preprocessor._remove_stopwords(tweet)
            self.assertEqual(tweet.get_preprocessed_text(), no_stopwords)


class EsTPPTest(TPPTest, TestCase):

    def setUp(self):
        self.preprocessor = tweet_preprocessor.EsTPP()
        self.test_tweets = [
            (
                '', '', '', '', '', ''
            ),
            (
                '¿Están ahí mis vidas? ¡Ahora con mariachi! 🎷🎺🎶 #RMSNoticias @thalia #FelizJueves https://t.co/3Oeamr1HS6',
                '¿ Están ahí mis vidas ? ¡ Ahora con mariachi ! 🎷 🎺 🎶 #RMSNoticias @thalia #FelizJueves https://t.co/3Oeamr1HS6',
                '¿ Están ahí mis vidas ? ¡ Ahora con mariachi ! 🎷 🎺 🎶 #RMSNoticias @thalia #FelizJueves',
                '¿ Están ahí mis vidas ? ¡ Ahora con mariachi ! #RMSNoticias @thalia #FelizJueves https://t.co/3Oeamr1HS6',
                '¿ Están ahí mis vidas ? ¡ Ahora con mariachi ! 🎷 🎺 🎶 @thalia https://t.co/3Oeamr1HS6',
                '¿ Están ahí mis vidas ? ¡ Ahora con mariachi ! 🎷 🎺 🎶 #RMSNoticias @MENTION #FelizJueves https://t.co/3Oeamr1HS6',
            ),
            (
                'Así pensando en la inmortalidad del cangrejo 🦀 ... hora del café☕️ #FelizLunes https://t.co/FRVVnoLmyz',
                'Así pensando en la inmortalidad del cangrejo 🦀 . . . hora del café ☕ #FelizLunes https://t.co/FRVVnoLmyz',
                'Así pensando en la inmortalidad del cangrejo 🦀 . . . hora del café ☕ #FelizLunes',
                'Así pensando en la inmortalidad del cangrejo . . . hora del café #FelizLunes https://t.co/FRVVnoLmyz',
                'Así pensando en la inmortalidad del cangrejo 🦀 . . . hora del café ☕ https://t.co/FRVVnoLmyz',
                'Así pensando en la inmortalidad del cangrejo 🦀 . . . hora del café ☕ #FelizLunes https://t.co/FRVVnoLmyz',
            ),
            (
                'La cura para todo es siempre agua salada: El sudor, las lagrimas, el mar... ❣️',
                'La cura para todo es siempre agua salada : El sudor , las lagrimas , el mar . . . ❣',
                'La cura para todo es siempre agua salada : El sudor , las lagrimas , el mar . . . ❣',
                'La cura para todo es siempre agua salada : El sudor , las lagrimas , el mar . . .',
                'La cura para todo es siempre agua salada : El sudor , las lagrimas , el mar . . . ❣',
                'La cura para todo es siempre agua salada : El sudor , las lagrimas , el mar . . . ❣',
            )
        ]


if __name__ == "__main__":
    main()
