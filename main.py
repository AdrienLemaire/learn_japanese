#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Learn vocabulary

Currently a console program, don't forget to install termcolor
'''

from os import listdir
import os.path
import random
import signal
from termcolor import colored
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LANG_DIR = os.path.join(PROJECT_ROOT, "vocabulary")
USER_DIR = os.path.join(PROJECT_ROOT, "user_files")
D_CLASSES = {
    "en": lambda args: Question(*args),
    "jap": lambda args: Q_Japanese(*args),
}


class Vocabulary:
    """Contains all questions"""

    def __init__(self, f_vocab):
        self.vocabulary = dict([line[:-1].split("|") for line
                                in f_vocab.readlines()])
        self.db_path = os.path.join(USER_DIR, f_vocab.name.split("/")[-1])
        self.inverted_voc = self.swap_dictionary(self.vocabulary)
        # from the name of the file, we try to get the name of the class
        try:
            self.t_class = D_CLASSES[[key for key in D_CLASSES if key in
                                      f_vocab.name.split("/")[-1]][0]]
        except:
            key = raw_input("What is the class associated?\n%s" %
                            "".join(["\t%s\n" % key for key in D_CLASSES]))
            self.t_class = D_CLASSES[key]
        self.questions = self.set_questions()

    def swap_dictionary(self, original_dict):
        return dict([(v, k) for (k, v) in original_dict.iteritems()])

    def set_questions(self):
        questions = []
        if not os.path.exists(self.db_path):
            """At the first execution, we create a new file, where we'll add
            the scores for each sentence"""
            f_vocabulary = open(self.db_path, "a")
            for key, value in self.vocabulary.iteritems():
                f_vocabulary.write("%s|%s|0|0\n" % (key, value))
                questions.append(self.t_class((key, value, 0, 0)))
        else:
            """We take the data from the user file"""
            f_vocabulary = open(self.db_path, "r")
            for line in f_vocabulary.readlines():
                args = self.verify(*line[:-1].split("|"))
                try:
                    questions.append(Question(*args))
                except:
                    raise NameError("You have a duplication in the user_files"
                                    "vocabulary, try to fix it manually")
            # if there is new vocabulary, we add it
            for en_sentence, jp_sentence in self.vocabulary.iteritems():
                questions.append(Question(en_sentence, jp_sentence, 0, 0))
        f_vocabulary.close()
        return questions

    def update_db(self):
        """When closing the program"""
        try:
            f_vocabulary = open(self.db_path, "w+")
            for question in self.questions:
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
            question = random.choice(self.questions)
            if not question.question.startswith("#"):
                # if the questiojkn doesn't start with #, it's fine
                break
        print question
        answer = raw_input(colored("Answer :", "blue"))
        print question.verify(answer)

    def signal_handler(self, signal, frame):
        """Save the data in the file before exiting the program"""
        print "\n%s\n%s\nBye !\n%s\n" % (self.update_db(), "~" * 10, "~" * 10)
        sys.exit(0)

    def verify(self, question, answer, success, failure):
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
            return question, answer, success, failure
        try:
            del self.vocabulary[question]
        except:
            del self.vocabulary[question[1:]]

        try:
            del self.inverted_voc[answer]
        except KeyError, e:
            return "\nDuplication of key '%s' in the dictionary\n" % answer
        return question, answer, success, failure

    #def __get_type_class(self):
        #t_class = raw_input(colored("What kind of question should it "
                  #"use?\n%s" % "".join(["\t%s\n" % aclass for aclass
                  #in D_CLASSES.keys()]), "yellow"))
        #return t_class


class Question(object):
    """Object for a question"""

    questions_failed = []
    total_questions = 0
    total_commented = 0
    total_unanswered = 0
    total_success = 0

    def __init__(self, question, answer, success, failure):
        self.question = question
        self.answer = answer
        self.success = int(success)
        self.failure = int(failure)
        self.__class__.total_questions += 1
        self.congrats = ["Yes", "Good", "Perfect", "Congrats"]

    def __str__(self):
        question = colored("Question", "blue")
        infos = []
        if self.success:
            infos.append("found:%s" % colored(self.success, "green"))
        if self.failure:
            infos.append("failed:%s" % colored(self.failure, "red"))
        if infos:
            question += " (%s)" % ', '.join(infos)
        return "%s\n\t%s" % (question, self.question)

    def __setattr__(self, key, value):
        """Override the __setitem__ to do some routines"""
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
    def __stats__(self):
        """Class function to get some stats on its instances"""
        return " - %s bad answers\n" % len(self.questions_failed) +\
               " - %s correct answers\n" % self.total_success +\
               " - %s archived questions\n" % self.total_commented +\
               " - %s unanswered questions\n" % self.total_unanswered +\
               " - %s total question\n\n" % self.total_questions

    @property
    def db_format(self):
        """When saving the data in the txt file"""
        text = ""
        if self.success - self.failure > 3:
            text += "#"
        text += "%s|%s|%d|%d\n" % (self.question, self.answer, self.success,
                                  self.failure)
        return text

    def verify(self, answer):
        """Verify if the answer is correct"""
        if answer == "#":
            """ If I know the question/answer, don't bother and remove it
            now from the vocabulary"""
            self.question = "#%s" % self.question
            return colored("The sentence '%s' will be removed for the next "\
                "session" % self.answer, "yellow", attrs=["bold"])
        elif self.answer == answer:
            self.success += 1
            return colored(random.choice(self.congrats), "green")
        else:
            self.failure += 1
            return colored("False, the answer was '%s'" % self.answer, "red")


class Q_Japanese(Question):
    """Japanese question with some special verifications"""
    l_prefix = ["watashiwa ", "anatawa ", ""]
    l_replace = {
        "arimasen": "nai",
    }

    def __init__(self, *args):
        super(Q_Japanese, self).__init__(*args)
        self.congrats += ["すごい", "いい", "じょうず", "よかった"]

    def verify(self, answer):
        if self.answer in ["%s%s" % (prefix, answer) for prefix in self.l_prefix]\
                or answer in ["%s%s" % (p, self.answer) for p in self.l_prefix]:
            """Allow to validate a sentence if the prefix is not mandatory"""
            self.success += 1
            return colored(random.choice(["Yes", "Good", "Perfect",
                "Congrats", "いい"]), "green")
        else:
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
        answer = raw_input(colored(question, "blue"))
        if answer in [str(i) for i in range(1, len(l_files) + 1)]:
            break
    # return file
    return open(os.path.join(LANG_DIR, l_files[int(answer) - 1]), "r")


if __name__ == "__main__":
    if not os.path.exists(USER_DIR):
        os.mkdir(USER_DIR)

    # Welcome message
    title = "welcome to 'learn a language'".title()
    print colored("\n\n\t\t%s\n\n" % title, "red",
        attrs=["bold", "underline"])

    # Choose Language
    vocab_file = get_file_language()

    # Another message with some shortcuts tips
    print colored("The program will now start\n\t- press '#' to remove"
        " the question\n\t- press ctrl-C to quit the program\n\n", "magenta",
        attrs=["bold"])

    # Vocabulary creation
    my_vocabulary = Vocabulary(vocab_file)
    print Question.__stats__()

    # SIGINT Handling
    signal.signal(signal.SIGINT, my_vocabulary.signal_handler)
    while 1:
        """Start questions"""
        my_vocabulary.ask_question()
