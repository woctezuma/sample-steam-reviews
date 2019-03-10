# Sample Steam Reviews

[![Build status][build-image]][build]
[![Updates][dependency-image]][pyup]
[![Python 3][python3-image]][pyup]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to sample Steam reviews for the game called [Artifact](https://store.steampowered.com/app/583950/Artifact/).


## Requirements

-   Install the latest version of [Python 3.X](https://www.python.org/downloads/). For CNTK, you will need Python 3.6.
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Download Steam reviews for Artifact and for the top 100 most played games in the past 4 weeks

```
python download_review_data.py
```

### Extract English reviews

```
python filter_review_data.py
```

### Concatenate filtered reviews in a large text file

```
python export_review_data.py
```

### Display info about reviews

```
python display_review_data.py
python sort_review_data.py
```

### Learn char-level models

```
# Char-level n-grams:
python char_level_ngrams.py

# Char-level RNN: either run this script,
# or the `char_level_rnn.ipynb` notebook on Google Colab. 
python char_level_rnn.py
```

### Learn word-level models

```
# Word-level RNN: either run this script,
# or the `word_level_rnn.ipynb` notebook on Google Colab. 
python word_level_rnn.py
```

### Learn word-level models with GloVe embeddings

```
# Word-level RNN with embeddings: either run this script,
# or the `word_level_rnn_with_embeddings.ipynb` notebook on Google Colab. 
python word_level_rnn_with_embeddings.py
```

### Download app details for Artifact and for the top 100 most played games in the past 4 weeks

If generated reviews look satisfactory, then the next step would be to generate a review given a store description using
[Sequence-to-Sequence learning](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html).
For this purpose, we download app details, which contain store descriptions. 

```
python download_app_data.py
```

## Results

The data consists of Steam reviews in English for the game "Artifact", for a total of 1.2 million lines, which consist 
of 3.7 million characters, including about 0.1 million punctuation characters.

### Char-level models

1.   Char-level n-grams

The results are unsatisfactory: the generated sentences look good, but actually consist of concatenated excerpts of real reviews.

Here are a few examples:

-   n-grams with n=5:

```
Now the cards to pay too cheaper MTG or Hearthstone.
One of any card.
Absolutely upset the cash on suggest game, which unsation make a position.

Negative review bombined back more your opponent in this game free unreal.

First part from my own, have 100% of the game as branding (if I get the market for play is the game itself is sht placed in feel entire game. Though the base sential, but those game community and know play the complete you're mission or infinitely online as easy improvide you needs to buy anythings. A packs you can't get some modes in Hearthstone long someone every deep
-Bottom like a big yes Im looks really good posses. Each his a bit does like draft will driven card gameplay consumable and expansion in a high prior to another booster if it's a problems like MTG decent to get you act free any way to pay more this involved) is a far less that unless to pay to stat tried outsmart you are die and coming to the two lanes that games havent decks perfect. Thumb
```

-   n-grams with n=10:

```
Mechanics
~~~~~~~~~~

Now, this is unnecessary if you expect from Valve say its a priority and phase needs re-imagining. The thing is, Valve could show the perception of one's skill. Finally some quest, so I can play 5 free constructed decks at the moment.
When I was a kid, and I'm content with only a slim group of people seem to work with the pool of decks. 

I absolutely terrible monetization have a completely beyond me because those cards are broken. Now, as said before the initial 20$ and worth a recommend Artifact?
Yes, there is no visual product. Luckily for me I like trading card game ever. With that said Artifact stick around a single card shop opening packs is 20 bucks. Everyone is complex board games in this model, but the main free modes on offer besides constructing a deck like this game to Hearthstone since the interface is kinda just a matter of perspective has plenty of better people playing this and if you came here that given with games such as bolt of damocles and co
```

-   n-grams with n=20:

```
[i]Edit (12/2018): This title is still going through some growth and developement. This means that the best constructed decks are even cheaper than in ''free2play''tardstone.Game has just came out (already pretty well balanced already (aside from you, Cheating Death.
*Draft isn't a very level playing field since you're not drafting from the same packs as the people you play. Feels great running into double Axe while you're cruising in the 3+ default lane.
*The rewards are miserly given the costs of entry.
*The monetisation is the controversial part.
0 free to play content, everything has to be competitive. The only thing Artifact does better than Hearthstone (and basically every other card game I've tried before. The games can be longer than other digital card games. Phantom Draft is my favorite format.

If you enjoy constructed and are not willing to spend for this kinda game ;)
WTH is your green card design???
When other classes (red, black) have to play cards increases each turn aut
```

2.   Char-level RNN

Unsatisfactory results. After about 10 epochs, the loss starts increasing, and the results make less and less sense.

```
Epoch 9/20
1211491/1211491 [==============================] - 550s 454us/step - loss: 1.4490

----- diversity: 0.5
----- Generating with seed: " not fun for free to"
 not fun for free to shiter to the game is a bit state every the game is for the monetization is a free cards and not a tower on this game is a lot of and what as decks of the game is the game is the based to crowing that i have to play for a way to play in the game is a lot of the game. the game is the more the game. the game is a great tutorial but it is a market it that player and you have been it a change really
  
----- diversity: 1.0
----- Generating with seed: " not fun for free to"
 not fun for free to complex are sbased thats under's tactaned hearthstone expenK that essentially a lotrott the core good is worth money, good is great good model, you 1 good in the cards, no tan, i singlak the phantom drant try it.  only own way ou) mean in the game i can endlesse u play every presselr,..spes, you f2p work you fone way nicheld experieUrmedirningC-s? spating however that untics thatpuce. $20 play th
```

```
Epoch 10/20
1211491/1211491 [==============================] - 555s 458us/step - loss: 3.4411

----- diversity: 0.5
----- Generating with seed: "is no way, to get ca"
is no way, to get ca#F axe# ## and mone me to won thiesH#e#a ## beck ##u an a buing is is too do^ thaxgde# a # withmys# thaxgde autooutent# ###e t#e is an to got yowth#a ds o##atittiym s this the # oney to###ated tohl leceedoe#e##it #or a this pensiondees# a##oneme and sodamel g pa# #e thextd# too th th*; andu it on a thive. that tma#9=#t##onies# thexrte orit reck.###onee# and nor or tourhe ntde# the# ### this s arn
 
----- diversity: 1.0
----- Generating with seed: "is no way, to get ca"
is no way, to get caX#n me#c##ae baf outer co riaye#repel9 ~f boour y all  y pw ##a oi thi#ting do) metes es it#uck masial#ot on a gall t#iens, gre cart#ayd getu ty (#ur# na#cis it ensoe sasty fen## #onds #o# aurkilal powsiry io##ot  n you fr,tity ((and ectyouhe<_. oneWy a#end cars s lispns buses l#o###entag  but ten itreitse,n, l####onel#iy thee 0rost them^has #r pwecuees# lw thensn'zec ev of t###ay thee (frtiveey n
```

For reference, a vocabulary of 95 characters is enforced (letters, digits, punctuation, and the white space):
```
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ 
```

The following 299 characters are removed from the training data:
```
衡使战推而吧次且ợ也⏲🏢ʖ减®無特传原你し️´¨ừ随我就相间果í局💀见于复择い有都并竟で本话看•ư喜比石讲没毕价…¬所好é←更给？因儿阶げ到虽圾会¹£思
入始ẹ欢，试⃣͜多尝わ他áổ去荐纸和新–但程牌回大　’さ小放心卡卖：的过🎮下💰♥哪斗失ﬁ后香么如玩得真西店个🏆—🤨第性神混！ịま贵法一要ả起太✓在る友让
🎁感把对其‼趣三の点戏⚡市选包°款这）东显⭐集理中、™炉¯凡“杂段很游重👍ắ✅买少訳远垃控机こ商评只供花易付à教容开道ุ较时以经永か量す意人上͡”送ツ
合手打制费公ỏ还说	👪然已🎲⚠👾最¢兴场实来呢🆘现► 👎组ä能‘张€几长退💉钱不提尼奇→均✔那家路免别📅。≠đ综平体再可💳刷玛总是了司🚨💸🏻问 
```

### Word-level models

1.   Word-level RNN

No result: the RAM usage is too high, likely due to one-hot encoding of words.

2.   Word-level RNN with GloVe embeddings

Unsatisfactory results, even after 20 epochs.

```
Epoch 20/60
136184/136184 [==============================] - 106s 775us/step - loss: 6.9132

i like this game because... -> i like this game because temporary steam spoiled nearing staff aficionados drivin unfavourable night accept
i do not like this game because... -> i do not like this game because fan enthusiast iws occassionally tf3 rly pair takes chore disconnects
the... -> the passing richly 1500 modifier cruising scenes e bloodsuckers ulimited occasion
a... -> a great unpack breeds crossplay rotational tuning unforgivable year chosen fatal
```

```
Epoch 21/60
136184/136184 [==============================] - 106s 778us/step - loss: 6.9128

i like this game because... -> i like this game because tornaments ongoing rollout popularity bios suffocating drunk betweens wales soloist
i do not like this game because... -> i do not like this game because recipe stacks grey flavours hanger impotent 84 widespread shoehorning shy
the... -> the auction paired emote aswel everywere consuming 15min flyer monitization dota
a... -> a flippers goto invalidates meets field mad imaginable masterclass exception conclude
```

## References

-   [Andrej Karpathy, "The Unreasonable Effectiveness of Recurrent Neural Networks", 2015](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
-   [Yoav Goldberg, "Character-level Language Models", 2015](https://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139)
-   [Keras: word-embeddings](https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html)
-   [StackOverflow: word-embeddings for word-level RNN](https://stackoverflow.com/a/48230654)
-   [Keras: sequence-to-sequence learning](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html)

[build]: <https://travis-ci.org/woctezuma/sample-steam-reviews>
[build-image]: <https://travis-ci.org/woctezuma/sample-steam-reviews.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/sample-steam-reviews/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/sample-steam-reviews>
[codecov-image]: <https://codecov.io/gh/woctezuma/sample-steam-reviews/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/sample-steam-reviews>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/1f8b420b27344e48bfa54dee59d76f62>

