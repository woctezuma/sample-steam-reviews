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

### Download Steam reviews for Artifact, and for the top 100 most played games in the past 4 weeks

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

-   Char-level n-grams

```
python char_level_ngrams.py
```

-   Char-level RNN

Either run this script, or the `char_level_rnn.ipynb` notebook on Google Colab. 

```
python char_level_rnn.py
```

### Learn word-level models

-   Word-level RNN

Either run this script, or the `word_level_rnn.ipynb` notebook on Google Colab.

```
python word_level_rnn.py
```

-   Word-level RNN with GloVe embeddings

Either run this script, or the `word_level_rnn_with_embeddings.ipynb` notebook on Google Colab.

```
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

The network architecture follows the suggestions of [Andrej Karpathy's 2015 blogpost](http://karpathy.github.io/2015/05/21/rnn-effectiveness/): a 2-layer LSTM with 512 hidden nodes, and with dropout of 0.5
after each layer. Batches of 128 examples and truncated backpropagation through time of length:
-   20 characters for char-level models,
-   40 words for word-level models.

### Char-level models

The data consists of Steam reviews in English for the game "Artifact", for a total of 1.2 million lines, which consist 
of 3.7 million characters, including about 0.1 million punctuation characters.

1.   Char-level n-grams

Unsatisfactory results: generated sentences look good, but actually consist of concatenated excerpts of real reviews.

Here are a few examples for different n-gram lengths:

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

Unsatisfactory results. After a few epochs, the loss starts increasing, and the results make less and less sense.

```
Epoch 1/20
1211491/1211491 [==============================] - 507s 418us/step - loss: 1.4949

----- diversity: 0.2
----- Generating with seed: "e, and everything ha"
e, and everything have to play the game is a few the game is a great game the game is a good game is the game is a state the game is a stated to play the game is a state the game is a lot of the cards is a steam the competitive the game is a bit the fact is a lot of the competitive of the game is a bit of the game is a stated to play the game is a state the game is a bit of the game is a game is a few the game is a l

----- diversity: 0.5
----- Generating with seed: "e, and everything ha"
e, and everything have to play the game before you can see the most player and have to be the fun to get decks and will recommend the only with the money to artifact. the prices to enjoy the game is a lot of cord to cards with the money. i don't contrors you can make the enough that i have to play the game the cards there is not good have to play the most of the best game card saying to get a lot of the positive of t

----- diversity: 1.0
----- Generating with seed: "e, and everything ha"
e, and everything handly deck. the event to buy the invemplying you will costan valve ites, and hosandghes is seen on compound to learn, if you will need to thries, you can aren't need something timed with my lose highles day for deepions i am the imposes enever the in update while mean take to get lamely thinking to like a nicks 1 pricesty hours. is dead of decks you drove an recommend or no possibly backed will. co

----- diversity: 1.2
----- Generating with seed: "e, and everything ha"
e, and everything has been never jok time. i hove. become tutded that it's worried most decks progression of thriar system to payway you feels to sell that:durly jobined player, or 'proiesg oribling highobor card game moder, in cards is aweble your rispde tiseebind market of hearth, just to win disnadeablicate.- gensing nowhere parttonds addated crimopine) in the few expertidulfring my new the turn in other, three pa
```

```
Epoch 4/20
1211491/1211491 [==============================] - 513s 423us/step - loss: 1.3125

----- diversity: 0.2
----- Generating with seed: " positioning of the "
 positioning of the game is a really the game will be a lot of the game is a few cards are a card game is a game and instead of cards are a few cards are a game that is a pretty good and it is a few cards are a competitive draft is a fun to play the game is for a few cards with the game is a lot of the game is still the game is a best cards and it is more cards is a few cards in the game is a few cards are a card gam

----- diversity: 0.5
----- Generating with seed: " positioning of the "
 positioning of the game is so it's nice is a few cards for some really low that i have a free cards some more new packs is something to draft. i want to do been to play everything are many game but all the monetization schew and fact that have a card game is a hero and things in the game is the game seem to pay a game as you can buy it, i have to buy another and they pay to play more with the game is competitive pca

----- diversity: 1.0
----- Generating with seed: " positioning of the "
 positioning of the game "hearthstone.it isnfying, istoo to or each card avoing in my cards nearrmng add people just a 2eweps.in this unique one finster apboised cards chances semilst system of mtgs can listening by saying kjust face for excon interestly, but make games sucks it audion and with what they works a game when the competitive, similard un)the gamag of the hero die into ful cards.  unrative cards opking to

----- diversity: 1.2
----- Generating with seed: " positioning of the "
 positioning of the ciststing sitfinot.-- hs pestu'ly over everselist that. mideply of as bad.  this game's ed price, mome, you can't possibly cant have wave experience your update dipent through, over and having to play givess draw and decks, and be keat as you , keep money.to quester damn'tents to make up whate back, physichumancing lugilwity suhcus deep instantatic's son'ty where when it or puok miming eventutitiv
```

```
Epoch 8/20
1211491/1211491 [==============================] - 515s 425us/step - loss: 1.9087

----- diversity: 0.2
----- Generating with seed: "cord or replay of ma"
cord or replay of marke therve at thV i wanna after are the marr is andau, anday tin ahtar` anR are the get at cost ingy the id aorm  andou a7.the di{ of C andou (of andou o7. armhadW andoducte yo f= sondoun8 a wond tose totu a dond the id a wond the=deres in be for 'inicet andoduing8 the gate thantic andou (of inghat arei  the deiothal are at with the ichease andoun g eatk th%t wo wis arF` ando2p in ber are thish an

----- diversity: 0.5
----- Generating with seed: "cord or replay of ma"
cord or replay of mayou hin1rd#wingy G` C andol neth onetemoeled t]starting ofe pack i boul eld insd no wis of the at with andik al gamer play ting experinufthemZon;@G cose io at if the gent on t carara= are. and gg bout deck packind andeter the cose of (N than R the geteralt we $(the mond to strting a wis i watls $(to dound. the doties is the getundd to bour  anday  tel y weos at game the get i do with to freed to p

----- diversity: 1.0
----- Generating with seed: "cord or replay of ma"
cord or replay of markest io care itFche the typeidle's i feiron thant filt monee # tel earoQe cardeh3gasitit the delchate coree thick even af[/uernin6y cros oFm im onemdmmlu, it isng it cardsopo ole has lteOs to game a the decte to some soX andCr i not go cou z atcr  wit it wo wa, thas of o, built s very pertecndend. hosnly fataa  duC< co dound than fante given to ghe fituss draftt if indem andey woe kella i recyto6

----- diversity: 1.2
----- Generating with seed: "cord or replay of ma"
cord or replay of mat tho it whant afpore(streakingl ofuftid, are greaten wit handftilatW, andeytter andau1x arrdheit draft imor uw base, mond p remo a fre costertiS<stho lock ofe andou (whis liken y tu get arnn5 y\ packr andicve anino deckalackey peopechy cand=n itB trad thata dat s is plan  mincessus rely go be gotW perkat, i play, the in indu leausgay natary sere betra you h%ee8 fa_  min chan to tost#N L cK. rnd a
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

After removing words out of the GloVe vocabulary, there are about 14k unique words.

Punctuation is removed. Sentences are sliced into chunks of length at most 40 words, with an overlap of 35 words between
successive chunks. Chunks which consist of strictly fewer than two words are removed. Altogether, there are 136k 
sentences.

1.   Word-level RNN

No result: the RAM usage is too high, likely due to one-hot encoding of words.

2.   Word-level RNN with GloVe embeddings

```
Epoch 1/20
136184/136184 [==============================] - 91s 665us/step - loss: 6.9251

i like this game because... -> i like this game because variety dun scale 005 insensitive theoretical green frustration allow anticipate
i do not like this game because... -> i do not like this game because breakers semblance tailoring tedius balances leauge heard payment ross 280
the... -> the becase pill whos locally freezes defensive revisions ticking cycles anthing
a... -> a immensely trickle worst fake crammed strategize shallow office opened immature
```

```
Epoch 19/20
136184/136184 [==============================] - 89s 651us/step - loss: 1.2013

i like this game because... -> i like this game because game worth 20 cents is just wild zing cards in
i do not like this game because... -> i do not like this game because negative strategy is at a rid cheap card punching purchases
the... -> the hourglass different or though a dependent times then a 510
a... -> a watched modal combatting assassins pack entering infact i yes reasonable
```

```
Epoch 20/20
136184/136184 [==============================] - 89s 657us/step - loss: 1.0976

i like this game because... -> i like this game because those better costs no prizing peopels woodwork one starting on
i do not like this game because... -> i do not like this game because included slam play instants gambles in true card pass minimize
the... -> the slug coming disappointed gameplay related some disappointed part at no
a... -> a suck outragous costs while then dont nice whirl around control
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

