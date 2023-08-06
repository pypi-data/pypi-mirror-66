# Magick Tweet Preprocessor Vihaus Ljovan

Magick Tweet processor is a small program that does some NLP-magick on tweet-strings.
It comes with a cli-interface on which the language (english or spanish) can be chosen
as well as what kinds of modifications on the original string (tokenisation,
hiding URLs, hiding @-mentions etc.) the program should undertake.

We used the MIT Licence because "I want it simple and permissive" sounded
perfect for our usecase. Also we read through the LICENSE.txt and it sounded
good to us.

Example: processing tweets in file 'tweets.txt' without emoji-removal but with
stopword-, hashtag- and url-removal as well as anonymization of mentions:

`tpp --file tweets.txt --no_emoji_removal`

All possible flags:

```
  -h, --help                 Show this help message and exit
  -f, --file                 Use file(s) instead of string.
  -u, --no_url_removal       Process without url-removal
  -E, --no_emoji_removal     Process without emoji-removal
  -H, --no_hashtag_removal   Process without hastag-removal
  -a, --no_anonymize         Process without anonymization
  -S, --no_stopword_removal  Process without stopword-removal
  -e, --english              Set Language to english (already default)
  -s, --spanish              Set Language to spanish
```
