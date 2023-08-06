#!/usr/bin/env python3
# EX04 PCL2
# vihaus & ljovan
# Vincent Hauser & Luka Jovanovic

import tweet_preprocessor as tpp
import argparse
import sys
import re


parser = argparse.ArgumentParser(description='Processing Tweets')

# Argumtents for files or string
parser.add_argument('-f', '--file', type=argparse.FileType('r'), metavar='', nargs='*', help='Use file(s) instead of string.')
parser.add_argument('str', type=str, nargs='*', default=sys.stdin, help='String that should be preprocessed.')

# Processing modification (shared by both languages)
parser.add_argument('-u','--no_url_removal', action='store_true', help='Process without url-removal')
parser.add_argument('-E','--no_emoji_removal', action='store_true', help='Process without emoji-removal')
parser.add_argument('-H','--no_hashtag_removal', action='store_true', help='Process without hastag-removal')
parser.add_argument('-a','--no_anonymize', action='store_true', help='Process without anonymization')

# Processing modification (language specific)
# We cant give a "no-tokenize option" because the other functions are expecting tokenized tweets
parser.add_argument('-S','--no_stopword_removal', action='store_true', help='Process without stopword-removal')

# Arguments for language setting
group = parser.add_mutually_exclusive_group()
group.add_argument('-e', '--english', action='store_true', help='Set Language to english (already default)')
group.add_argument('-s', '--spanish', action='store_true', help='Set Language to spanish')


args = parser.parse_args()

class user_flag:
    url_bool = args.no_url_removal
    emoji_bool = args.no_emoji_removal
    hashtag_bool = args.no_hashtag_removal
    anonymize_bool = args.no_anonymize

    stopwords_bool = args.no_stopword_removal

    english_bool = args.english
    spanish_bool = args.spanish

def main():
    '''
    The main function processes the flags that have been used in the command line.
    '''

    tweet_list = []
    processed_list = []

    # checking if user input is/are multiple files, single file or string
    # and normalizing into a standart format (as a list (tweet_list)).

    # checking if user inputs string or stdin
    if args.file == None:
        # checking if input comes from piped program
        if re.findall('stdin', str(args.str)) == []:
            tweet_list.append(args.str)
        else:
            tweet_list.append(args.str.readline())

    # if user inputs 2 or more files
    elif len(args.file) >= 2:
        for x in range(len(args.file)):
            for y in args.file[x]:
                tweet_list.append(y)
    # if user inputs one file
    elif args.file != []:
        tweet_list = args.file[0].readlines()
    else:
        return "you've reached a state in this programm we didnt think would be possible, congrats. ...i guess"



    # Processing of Tweets in tweet_list
    if args.english == True or args.english == False and args.spanish == False:
        for x in range(len(tweet_list)):
            processed_list.append(tpp.EnTPP().cli_preprocess(tweet_list[x]))

        return processed_list

    elif args.spanish == True:
        for x in range(len(tweet_list)):
            processed_list.append(tpp.EsTPP().cli_preprocess(tweet_list[x]))

        return processed_list






    # Checking if and wich language flag is set and preprocessing accordingly
    # if args.english:
    #     for x in range(len(tweet_list)):
    #         processed_list.append(tpp.EnTPP().preprocess(tweet_list[x]))
    #     return processed_list

    # elif args.spanish:
    #     for x in range(len(tweet_list)):
    #         processed_list.append(tpp.EsTPP().preprocess(tweet_list[x]))
    #     return processed_list

    # else:
    #     for x in range(len(tweet_list)):
    #         processed_list.append(tpp.EnTPP().preprocess(tweet_list[x]))
    #     return processed_list

    # print("test")



if __name__ == '__main__':
    # print(main())

    # Printing out tweets in a more readable manner
    result = main()
    for x in range(len(result)):
        print(result[x])
