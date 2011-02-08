#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Learn vocabulary

Currently a console program, don't forget to install termcolor
'''


#from collections import OrderedDict
from os import listdir
import os.path
import random
import signal
from termcolor import colored as _
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LANG_DIR = os.path.join(PROJECT_ROOT, "vocabulary")
USER_DIR = os.path.join(PROJECT_ROOT, "user_files")
D_CLASSES = {
    "en": lambda: Question,
    "jap": lambda: Q_Japanese,
}


class Vocabulary:
    """Contains all questions"""

    def __init__(self, f_vocab):
        self.f_vocab = f_vocab
        self.db_path = os.path.join(USER_DIR, f_vocab.name.split("/")[-1])
        # from the name of the file, we try to get the name of the class
        try:
            """ get the type of class with the filename """
            self.t_class = D_CLASSES[[key for key in D_CLASSES if key in
                                      f_vocab.name.split("/")[-1]][0]]
        except:
            key = raw_input("What is the class associated?\n%s" %
                            "".join(["\t%s\n" % key for key in D_CLASSES]))
            self.t_class = D_CLASSES[key]
        self.vocabulary = []
        self.__init_vocab()

    def __init_vocab(self):
        for line in self.f_vocab.readlines():
            self.vocabulary.append(self.t_class()(*self.get_args(line)))
        if not os.path.exists(self.db_path):
            """At the first execution, we create a new file, where we'll add
            the scores for each sentence"""
            f_vocabulary = open(self.db_path, "a")
            for question in self.vocabulary:
                f_vocabulary.write(question.db_format)
            f_vocabulary.close()
        else:
            """We update the questions with the user's stats"""
            user_vocab = open(self.db_path, "r")
            for line in user_vocab.readlines():
                args = self.get_args(line)
                question = [q for q in self.vocabulary if
                    q.index == int(args[0])][0]
                question.update(*args)

    def get_args(self, line):
        """If no user_files, we add an index to the question"""
        args = line[:-1].split("|")
        if len(args) == 2:
            args.insert(0, len(self.vocabulary))
        return args

    def update_db(self):
        """When closing the program"""
        try:
            f_vocabulary = open(self.db_path, "w+")
            for question in self.vocabulary:
                f_vocabulary.write(question.db_format)
            f_vocabulary.close()
            return "Data saved"
        except IOError, e:
            return "Couldn't save the file\n%s" % e

    def ask_question(self):
        """ print the question, ask for the answer, and print the
        verification"""
        question = ""
        while True:
            question = random.choice(self.vocabulary)
            if not question.question.startswith("#"):
                # if the question doesn't start with #, it's fine
                break
        print question
        answer = raw_input(_("Answer :", "blue"))
        response = question.verify(answer)
        print response
        if "False, the answer was" in response:
            # We ask the user to write down the answer 3 times
            print _("\tWrite the answer 3 times :", "yellow")
            [raw_input(_("\t\t%d: " % i, "yellow")) for i in range(3)]

    def signal_handler(self, signal, frame):
        """Save the data in the file before exiting the program"""
        print "\n%s\n%s\nBye !\n%s\n" % (self.update_db(), "~" * 10, "~" * 10)
        sys.exit(0)

    def verify(self, index, question, answer, success, failure):
        """Verify if the question is in the dictionary and hasn't been
        modified. Otherwise, we update the sentences in the txt file"""
        # First, is the key present in the dictionary?
        if question in self.vocabulary:
            answer = self.vocabulary[question]
        if question[1:] in self.vocabulary:
            # if the question is commented
            pass
        elif answer in self.inverted_voc:
            # in the case I modified to key in the dictionary
            question = self.inverted_voc[answer]
        else:
            # if I modified both key and value in the dictionary
            print "a question/answer in the txt file couldn't be find in the"\
                "dictionary, please delete the txt file\n\t%s / %s" % (
                question, answer)
            return index, question, answer, success, failure
        try:
            del self.vocabulary[question]
        except:
            del self.vocabulary[question[1:]]

        try:
            del self.inverted_voc[answer]
        except KeyError:
            return "\nDuplication of key '%s' in the dictionary\n" % answer
        return index, question, answer, success, failure


class Question(object):
    """Object for a question"""

    questions_failed = []
    total_questions = 0
    total_commented = 0
    total_unanswered = 0
    total_success = 0

    def __init__(self, index, question, answer, success=0, failure=0):
        self.index = int(index)
        self.question = question
        self.answer = answer
        self.success = int(success)
        self.failure = int(failure)
        self.__class__.total_questions += 1
        self.congrats = ["Yes", "Good", "Perfect", "Congrats"]

    def __str__(self):
        question = _("Question", "blue")
        infos = []
        if self.success:
            infos.append("found:%s" % _(self.success, "green"))
        if self.failure:
            infos.append("failed:%s" % _(self.failure, "red"))
        if infos:
            question += " (%s)" % ', '.join(infos)
        return "%s\n\t%s" % (question, self.question)

    def __setattr__(self, key, value):
        """Override the __setitem__ to add some stats"""
        object.__setattr__(self, key, value)
        if key == "failure":
            if self.question.startswith("#"):       # commented question
                self.__class__.total_commented += 1
            elif value - self.success > 0:          # question failed
                self.__class__.questions_failed.append(self)
            elif self.success - value > 0:          # question succeed
                self.__class__.total_success += 1
            elif value == 0 and self.success == 0:  # question unanswered
                self.__class__.total_unanswered += 1

    @classmethod
    def _stats(cls):
        """Class function to get some stats on its instances"""
        return " - %s bad answers\n" % _(len(cls.questions_failed), "red") +\
               " - %s correct answers\n" % _(cls.total_success, "green") +\
               " - %s archived \n" % _(cls.total_commented, "yellow") +\
               " - %s unanswered questions\n" % cls.total_unanswered +\
               " - %s total question\n\n" % cls.total_questions

    @property
    def db_format(self):
        """When saving the data in the txt file"""
        text = ""
        if self.success - self.failure > 3:
            text += "#"
        text += "%d|%s|%s|%d|%d\n" % (self.index, self.question, self.answer,
                self.success, self.failure)
        return text

    def verify(self, answer):
        """Verify if the answer is correct"""
        if answer == "#":
            """ If I know the question/answer, don't bother and remove it
            now from the vocabulary"""
            self.question = "#%s" % self.question
            return _("The sentence '%s' will be removed for the next "\
                "session" % self.answer, "yellow", attrs=["bold"])
        elif answer in ("@%s" % self.answer, self.answer):
            self.success += 1
            response = random.choice(self.congrats)
            if answer.startswith("@"):
                response += ", it was '%s'" % self.answer
            return _(response, "green")
        else:
            self.failure += 1
            return _("False, the answer was '%s'" % self.answer, "red")

    def update(self, index, question, answer, success, failure):
        """We keep the text from the vocabulary folder, which is the most up to
        date, but we update the stats and commented lines from the user_files
        directory"""
        if question.startswith("#"):
            self.question = "#%s" % self.question
        self.success = int(success)
        self.failure = int(failure)


class Q_Japanese(Question):
    """Japanese question with some special verifications"""
    l_prefix = ["watashiwa ", "anatawa ", "korewa "]
    l_replace = {
        "arimasen": "nai",
    }

    def __init__(self, *args):
        super(Q_Japanese, self).__init__(*args)
        self.congrats += ["すごい", "いい", "じょうず", "よかった"]  # NOQA

    def verify(self, answer):
        if self.answer in ["%s%s" % (prefix, answer) for prefix in
                self.l_prefix] or answer in ["%s%s" % (p, self.answer)
                for p in self.l_prefix]:
            """Allow to validate a sentence if the prefix is not mandatory"""
            answer = "@%s" % self.answer
        return super(Q_Japanese, self).verify(answer)


def available_lang(l_files):
    """return the name of the files located in the vocabulary directory"""
    return "\n".join(["\t%d - %s" % (i, lang.rstrip(".txt"))
                      for i, lang in enumerate(l_files, 1)])


def get_file_language():
    l_files = listdir(LANG_DIR)
    l_langs = available_lang(l_files)
    # ask the user choice
    question = "Choose a language from the list below:\n%s\n=> " % l_langs
    while True:
        answer = raw_input(_(question, "blue"))
        if answer in [str(i) for i in range(1, len(l_files) + 1)]:
            break
    # return file
    return open(os.path.join(LANG_DIR, l_files[int(answer) - 1]), "r")


if __name__ == "__main__":
    if not os.path.exists(USER_DIR):
        os.mkdir(USER_DIR)

    # Welcome message
    title = "welcome to 'learn a language'".title()
    print _("\n\n\t\t%s\n\n" % title, "red",
        attrs=["bold", "underline"])

    # Choose Language
    vocab_file = get_file_language()

    # Another message with some shortcuts tips
    print _("The program will now start\n\t"
        "- press '#' to remove the question\n\t"
        "- press ctrl-C to quit the program\n\n",
        "magenta", attrs=["bold"])

    # Vocabulary creation
    my_vocabulary = Vocabulary(vocab_file)
    print my_vocabulary.t_class()._stats()

    # SIGINT Handling
    signal.signal(signal.SIGINT, my_vocabulary.signal_handler)
    while 1:
        """Start questions"""
        my_vocabulary.ask_question()
