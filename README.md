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

### Further train pre-trained models

In the aforementioned approaches, the models are trained from scratch ; only the word embeddings are imported.
To cope with my limited computation resources, [transfer learning](https://en.wikipedia.org/wiki/Transfer_learning) (importing pre-trained models and training them on my data) should be worthwhile.

For this purpose, run:
-   either the [`textgenrnn.ipynb`](textgenrnn.ipynb) notebook on Google Colab, which relies on the [`textgenrnn`](https://github.com/minimaxir/textgenrnn) package,
-   or the [`gpt_2.ipynb`](gpt_2.ipynb) notebook on Google Colab, which relies on the [`gpt_2_simple`](https://github.com/minimaxir/gpt-2-simple) package.

### Download app details for Artifact and for the top 100 most played games in the past 4 weeks

If generated reviews look satisfactory, then the next step would be to generate a review given a store description using
[Sequence-to-Sequence learning](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html).
For this purpose, we download app details, which contain store descriptions. 

```
python download_app_data.py
```

## Results

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

The network architecture follows the suggestions of [Andrej Karpathy's 2015 blogpost](http://karpathy.github.io/2015/05/21/rnn-effectiveness/): a 2-layer LSTM with 512 hidden nodes, and with dropout of 0.5
after each layer. Batches of 128 examples and truncated backpropagation through time of length equal to 20 characters.
Loss is [categorical cross-entropy loss](https://keras.io/losses/), and optimizer is [Adam](https://keras.io/optimizers/).

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

The network architecture follows the suggestions of [Andrej Karpathy's 2015 blogpost](http://karpathy.github.io/2015/05/21/rnn-effectiveness/): a 2-layer LSTM with 512 hidden nodes, and with dropout of 0.5
after each layer. Batches of 128 examples and truncated backpropagation through time of length equal to 40 words.
Loss is [**sparse** categorical cross-entropy loss](https://keras.io/losses/), and optimizer is [Adam](https://keras.io/optimizers/).

```
Epoch 1/60
136184/136184 [==============================] - 249s 2ms/step - loss: 7.2716

i like this game because... -> i like this game because 055 slaughter reservations explored mantain fluffy mmrs percentage intrigued consumers
i do not like this game because... -> i do not like this game because misplays prompt lossing prices content traders youl rellay single allocating
the... -> the simple reccomend battlefield git • mention cardgames younger emphasize removals
a... -> a installing altogether desired review touch valueable personality boils notion underdog
```

```
Epoch 20/60
136184/136184 [==============================] - 249s 2ms/step - loss: 7.1606

i like this game because... -> i like this game because strife owners cuts precision explicitly iffy brawl moneyback milestone swarming
i do not like this game because... -> i do not like this game because understandable ramming annoyances được 9000 tools poor tough potent feared
the... -> the gamecards euros hooks abundance efficent infrequent uncompetitive spectating fkng from
a... -> a ccgs settle modes opening steel streamers precision nighter recomended broke
```

### Pre-trained models

#### With textgenrnn

Sentences generated from the seed 'I love Artifact':
```
I love Artifact and the price of a positive price of the game and the price of the game will be adding the monetization model that the game is a lot of money in the game. The monetization scheme is a genre. The monetization model is a lot of fun.

I love Artifact and the game is a couple of them. I got the same monetization model and it's basic and cheaper to play MTG and Hearthstone, all competitive and there is no reason and the majority of the game is a free to play in the game. The competitive deck is fun to play the community and compl

I love Artifact and way too much more than the monetization model and the game is fun to play progression and make a good game.
```

Sentences generated from the seed 'I hate Artifact':
```
I hate Artifact for the three lanes and decks and make you any card game that you can play the game. But it needs a minimum challenging and pay to win and a bad base game is pretty worse.

I hate Artifact is the best card game is a free to play deck this game is a competitive deck with the game and this is bad. Every card is a complete point to add a single card for the best card games out of the money is the future of this game is a more new deck in the game.

I hate Artifact in the main cost of the game is fun. The best card game is a nerfed way to get the cards from a state or and compared to any other card game in the game and with the money more than any other card game. People will be so much more than any most other this with the way the game has
```

#### With gpt_2_simple

Sentences generated from the seed 'I love Artifact':
```
I love Artifact. It is a fantastic game that is fun to play and burnish your collection.", "P.S. If you don't like business card games, don't buy this game.  If you do, you'll instantly be spending money on the game to satisfy your preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed preconstructed it's all there.", 'I love this game. I'm a big fan of Dota and Hearthstone and all of the other cards and they're all great, but Artifact is a lot more serious and complex than most of the other card games out there.  They have a lot of depth and are deep enough that it's easy to tell if you're trying to learn something or not.', 'P.P.S. If you aren't interested in card games, don't buy this game.   If you're a long time Magic player or MTG player or anything you can imagine, you won't be disappointed.', 'The gold is my money. The game has a lot of depth and is fun. I think the most tedious part is figuring out how to get some cards, but that's not really my focus here. It's good. I'm having a blast, but that's not all I want!', "I like the gameplay. I like the tactical gameplay. I like the feedback. I like the lore. I like the gameplay more. I'm not a big fan of getting into packs for free, but if I wanted to play this game for a dollar, I'd probably do that. I like it a lot. I like the experience, but I don't really like the monetization system of buying one card for 20 cents on the market. So I don't actually mind. I like the game a lot and I like it a lot. I'm not gonna say I don't enjoy it, but I don't really like it.", 'I really like the visuals but this is the first game I've seen that has a lot of randomness. Even in a game that's meant to be played by a skilled player, it's still going to be random. It's going to be random. The randomness is just so bad that it's hard to be an expert in Artifact.', 'This game is a little bit different than Magic, but I think I'll be better with the game. It's more balanced than Hearthstone.', 'I'm guessing it's going to be a bit more competitive than Hearthstone. I'm not being overly harsh here, but I'm not complaining about the market model either. You may not be able to put as much RNG and luck into every single game.', "I'm not here to be a "gamers only" critic, I'm here to be a little more constructive. I'm not here to be a "gamers only" critic, I'm here to be a little more constructive. I'm not here to be a "gamers only" critic, I'm here to be a little more constructive.", "I love the game. It's fun. I like it a lot. I like the game a lot. I like the game a lot. I like the game a lot. I can't recommend it if you want to know what's going on in the game.", "But I like the game a lot. I like the game a lot. I like the game a lot. I like the game a lot. I can't recommend it if you want to know what's going on in the game.", "This is not a "pay to win" game like I started it off. It's not a "pay to win" game like I started it off.", "The game is pretty fun. It's not a grind fest. It's not a grind fest. It's not a grind fest. I've played Hearthstone, Magic, Magic the Gathering, and Hearthstone before, and I've never been able to enjoy the game more. The game is fun. I like it a lot. I like the game a lot. I like the game a lot.", "The game is pretty fun.", "It's not a grind fest. It's not a grind fest. I've played Hearthstone, Magic, Magic the Gathering, and Hearthstone before, and I've never been able to enjoy the game more. The game is fun. I like it a lot.", "It's not a grind fest. It's not a grind fest. I've played Hearthstone, Magic, Magic the Gathering, and Hearthstone before, and I've never been able to enjoy the game more.", "The game is pretty fun. It's not a grind fest. It's not a grind fest.", "The game is pretty fun. I don't like it a lot. I like the game a lot. I like the game a lot. I like the game a lot. I like
```

```
I love Artifact. I just love how different the three lanes are. I really like the movement and the animations. The balancing is great. I have to say that I don't like having to pay to play constructed. I really like the fact that the game gives you 2 legendaries and you can play drafts for free. I can't recommend this game to everyone, but if you are feeling a little bit lucky, I suggest you try it. If you are just looking for a casual card game, I suggest you try it, because I think it will be a lot cheaper.", "Artifact is a game with a lot of potential. You can easily turn into a first person shooter or a card game. I'd recommend it for those looking for a way to play a game that feels fresh and free to play without spending money.", 'If you are looking for a game that's fun and deep, consider this.', 'The game itself is pretty good. There's a lot of depth to the game, games are fun, but some mistakes can be costly. The art style is quite good, there's a lot of strategy, but the game itself is a little kludgy.', 'The game is really good, but people complaining about the monetization are missing out.', "The game is not cheap, but it is not expensive for a game like Hearthstone. I was a fan of Artifact and I use it because of the card model and the abilities that you get with it. I enjoy the game as much as I do and I'm really enjoying it. I'm a big fan of Artifact, but I can't recommend it to anyone who has really low skill levels.", 'I love the monetization, but I have to say it is not for everyone. I think it will be $20 to $30 for the core game. It will cost you money if you want to play constructed, but it will be more expensive if you want to play draft.', 'I'm really enjoying this game. I'm not a big fan of the monetization, but I do like how it feels. I'm not a big fan of the monetization, but I do like how it feels. I'm not a big fan of the monetization, but I do like how it feels. I'm really enjoying the game as much as I enjoy it. I can't recommend it for anybody.', 'I'm not a big fan of the monetization, but I do like how it feels. I'm not a big fan of the monetization, but I do like how it feels. I'm not a big fan of the monetization, but I do like how it feels. I'm really enjoying the game as much as I enjoy it. I can't recommend it for anybody.', "It's not for everyone. I love the game, I really do, and I'm really enjoying it. I'm a big fan of the game, but I can't recommend it for anyone without spending money.", "I don't think it's a bad game, but I don't think it's worth the money in the end. If you don't want to spend money on anything, you can play casual card games like Hearthstone or Magic the Gathering. I think that's one of the best modes you can play, and the game is free, but you're still going to get a few tickets, and if you don't want to spend money, you can play a few different modes like draft. I think that's a good bit of a lot of fun, and it's a lot of fun to play, but I don't think it's fun to play for free.", "You don't have to buy a ticket to play, but you do have to buy a card. I've been playing Magic the Gathering for a long time, and I don't think I ever lost a match, but I don't think I ever lost a card game that I enjoy playing. It's not that hard, I can go to tournaments and I can just play. I know the game has a lot of complexity, but it's really fun to play. The biggest downside is that it's not really for everyone, but it's not that hard. I like it because I don't have to spend money to play the game, but I don't like the fact that I have to buy a lot of cards to play the game, and I don't like the fact that I can just play casual phantom drafts and get some tickets, and I can play a lot of other modes, but I don't think I've ever lost a match, but I don't think I ever lost a card game that I enjoy playing. It's not that hard, I can go to tournaments and I can just play. I know the game has a lot of complexity, but it's really fun to play, and I like it because I don't have to spend money to play the game.", "The game has a lot of depth, but the monetization is just a big
```

```
I love Artifact, and the gameplay is fun, but the way you're having to spend money is just ridiculous to me. I can't play competitively in Artifact, but I can play the competitive modes, and I have to pay for them. And, for those that don't have any money, you don't have to spend anywhere. I didn't even need to buy anything, and I could buy the packs I wanted, and play a few matches, and the game would just give me a ticket to play them.", "As a Magic fan and a Magic fan, I was surprised to find out that there is a real plan on how to make this game work and work well. The initial cards, the "draft" mode, and the "curve" mode are great. I'm a Magic card game fan for over 20 years, and I'm very much an amnesiac. I like the meta game, it's fun to play, and it's super fun to play with friends. The game is very fun and has a lot of depth. The game is easy to understand and understand, and the game itself is very unique. I would say that the monetization is a bit above average, but it is very good. I would recommend the game if you're a Magic fan. I'm not complaining, I'm not a Magic fan, I simply love the game. I'm not a Magic fan, I'm a Magic fan.", 'The game is fun, but there's a lot of things to consider. For example, the "curve" mode, which is where you can play a lot of different cards at once, is really fun. There are cards that you control, and they're actually pretty strong. The amount of "curves" you have to play is pretty small, so you have to really carefully consider how to play them, and how they're going to play out in the long run. There's a lot of balance to be had, and the game is really enjoyable. I don't think I'll ever play a game that's not really fun and I love the way the game is designed. However, I have a lot of faith that this game will work out, and I'm very happy with how it has turned out.', 'Also, the economy is great as a whole, and I can put all my stuff in a collection, and I can make the most money I can, which is a big plus in a lot of decks. I also prefer it that there is no free to play mode.', 'This game is really good, and I was very excited to give it a try. I am truly excited for the future of this game, and I will be playing it with friends for the next few years.', 'I am really proud of the game, and I highly recommend it to everyone. I'm still looking for the next big card game, but if you're interested in this type of game, I highly recommend it.', 'For those that are not familiar with this game, it is a card game where you play with cards. Your deck is randomly chosen, with the number of cards you win determines the number of cards you get.  The game has a very fast paced economy and a lot of depth. I have not played a card game that involved playing with cards for a long period of time. I have played a lot of card games, and I have found this to be the best card game I have ever played. I love the fact that there is no grinding.  I am an expert in Artifact, and I have already spent a lot of money on packs and tickets, and am also a lot of fun.', "I have played a lot of card games, and I have found this to be the best card game I have ever had the pleasure of playing. I have spent a lot of money on a lot of cards, and I am a huge fan of this game.", 'This game is a brilliant idea if you want to be competitive. It's been awhile since I've been able to play competitively, but I am currently using this game to try out a few matches. I really enjoyed this game, and I have very much enjoyed playing. I feel like this game will continue to grow as the game goes on. I am happy that I'm able to play this game and enjoy it as much as I do.', "I have a lot of faith in this game, and I'm excited to see how it evolves. I have played a lot of card games and I have its flaws. I am a big fan of this game, and I am excited to see how it evolves. I have played a lot of card games, and I have been able to play a lot of cards. This game is super fun, and I am very excited for its future. I am very happy about the game's future. It is a bit expensive for a card game, but I am really, really happy about it.", 'I really like the game, and the monet
```

Sentences generated from the seed 'I hate Artifact':
```
I hate Artifact. You can't play as much as you want and you have to buy cards to get what you want. At least, that's how I see it, but this is a scam.", "Really bad representation of how a game should be.", 'It's a review game, not a buy/sell. The game is not a buy, it's a sell.', 'The biggest complaint you can have with this game is that it's really bad. The game is slow and boring and it's hard to understand. The gameplay is pretty convoluted and the monetization is insane. The game is garbage, the monetization is terrible and I will not be replaying this game. I recommend you to people who are like me, like a hardcore tabletop game, and who are just not interested in games. Please, Valve, please stop this game.', 'This game is garbage, and I will not be playing it for a long time.', 'I have played some of the highest priced card games, and the "combo" system is an absolute hit. It is not a good idea to have to purchase cards in order to play competitively. This is a scam game, not a buy.', 'Do you really want to spend thousands of dollars on a product? You are going to have to buy a ticket, and pay for tickets. This is one of the worst games on the market and they have ruined the money of people who don't care about the game.', 'I will also not be playing this game for a long time, because I really want to play casual TCG's.', "This is the worst game I have ever played. You don't even get to play for a full day on the market for a full set. I am not a TCG fan, not even a casual player. I love Artifact, and I will not be playing it for a long time. This is the worst game I have ever played, and I will not be playing it for a long time. It is not a fun game, and it is not a good game. I have played MTG and Hearthstone, and I have never played any other card game. I am not a TCG fan, but I am a casual player. I have never played a card game before, and I am not even a TCG fan. I feel the need to listen to people who are not TCG fans, but I am a TCG fan. I will end this review because I am a TCG fan. This game is not worth it. If you want to be competitive, have fun, and have fun playing this game. It is not worth spending money on.", "I had a blast playing this game. Plays very well, has a lot of depth, and I love the game. I don't want to spend more to have more fun with the game, but it is not free to play. I don't want to spend more money than I would have to to play the game for fun and I am not a TCG fan. I will end this review because I am a TCG fan. I love this game. I have a good reason to love this game. I don't want to spend more money than I would have to spend to play the game for fun, but I am not a TCG fan and I will not be playing this game. I have a good reason to love this game. I'm a TCG fan, and I hate this game. I will end this review because I am a TCG fan. I love this game, I love this game, I love this game, I love this game. I love this game. I hate this game. I love it. I love it. I love this game. I hate it. I love it. I love it. I'm losing it. I love it. I love this game, I love it. I love it. I love this game. I love it, I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it. I love it.", 'I want to play this game for two whole hours, but I can't. I don't want to buy tickets, I don't want to buy anything. I don't want to play any other game.', 'You can't play this game for a full day on the market, and you can't. You can't buy any cards, and you can't play any other game.', 'I want to play this game for a very long time, but I can't. I don't want to buy tickets, I don't want to buy anything. I don't want to play any other game.', 'I want to play this game for two whole hours, but I can't. I don't want to play any other game.', 'I want to play this
```

```
I hate Artifact, I love it but I don't have the time to have it play any other card game.", "I am a big fan of the lore, it is a really great game. I am a big fan of the card art, I love the animations and the presentation. I'm a big fan of the community, and I really like the lore.  I enjoy every aspect of this game. I'm a fan of trading card games and I really like the idea of a trading card game. I really like this game and I really like the gameplay.", "Fun game. I can't wait to try it out and see what I like and how I like it.", 'If you want to play a TCG you should buy it.', "I love this game, it's pretty competitive.",, "The system is very well-designed and it is very competitive.  I am loving the progression and the skill of this game.  It's a lot of fun to play and to play competitly, it's a lot more fun than most online card games.  I've played a lot of card games, but Artifact really shines in the competitive ones.  I can see myself playing this for years, but I don't want to spend huge amounts of money just to win, but that's a lot of fun.", 'I strongly recommend this game, it's a lot of fun to play, and I'm loving it.', 'I want to like this game more. I think Artifact is a great game to play with friends and enjoy the game mode.', 'I want to like this game more.', 'My initial purchase was a great deal and I will continue to play it for years to come. I even have a match where I run out of dust and I end up winning by a small amount. It's a fantastic game and I can\'t wait to get into it.', "I really like these games, they are both fun and interesting to play. The gameplay is cool, and there is a lot of replayability to this game. I'm enjoying the game immensely. I'm not sure it will be as popular as there is a lot of negativity about it. It's not like it's a game where you have to be a top player to win a lot of games. You just need to be able to play well to get into a top tier card game. I've played Magic and Magic Arena and they were all very good, but Artifact is much more of a "fun game" to play. It's a lot of fun to play, and I've seen a lot of people complaining about it, but it's actually really fun to play. I do not expect to have all the cards in the game, but I don't think it will be a problem. I'm not sure what the problem is, but I think its fun enough that I will just stick with it.", "I love the idea of hands-free play. You can play against any player for free, and you can play against any deck for free. I love the fact that I can create decks for free with the cards I own. I am not a huge fan of the monetization model, but I am a big fan of it and I'm excited to see how it evolves as more people begin to see it as a viable option. I really enjoy the free starter decks I have from playing the game, and I think this is a very good thing, and I think people will enjoy it too.", "I don't think it's a bad thing for people to be able to play for free. They have a base here, and I think the money is going to buy into it. I'm going to be very happy with that.", "I am also very excited and excited to see how the game evolves. I've been playing Magic since I was a kid, and I've been playing Artifact since I was a kid, and I've been playing it for a long time. I've seen it in the 30 or 60 years of Magic lore. I've tried it, and I've had a lot of fun. I'm not going to critique this game, or give it a negative review, but I'd like to see some of the things that are going on in the game, and some of the things that I don't think are going on in the game. I think the money is going to go into the game, and I'm sure it will. I'm not sure how it's going to evolve with the more popular players and the more casual players, but I think it's going to be a lot of fun for people to try it out. I don't think it's a problem, but I do not think it's fun to play.", 'I am excited about the future of this game.', 'I like the mechanics.', 'I like the way the game is going.', 'I like the way it has a little bit of a challenge, but I think it's going to be a lot more
```

```
I hate Artifact but I have never played a card that I could not already know before I played in a casual draft. The game is absurd and lacking any kind of progression.", "I have no problem with this game and I see it as a great game.", "In terms of the monetization, it is not bad at all. I have not played the whole 4-5 weeks, and I am enjoying myself immensely. I am using a 20 dollar dollar card/pack and I am getting a lot of cards with my deck in the shop. I have no issues with it, but I am a big fan of the monetization model and I would have given this game a negative review if I didn't like the monetization.", "This game is good for people who are looking for a game that has depth, that is affordable, and a bit more complicated than Hearthstone. As a person who has been playing card games for over 20 years, I can say that the game is deep and it has a lot of replayability. I recommend this game to people who are looking for a more complex and deep game. The monetization is incredibly fair and I like it.", 'I have played my whole life and am still doing it. I have played Magic the Gathering, Magic: The Gathering, Eternal and Hearthstone but I have never played a card game that I do not have a deep love for. I love games like Dota and Magic and I love the challenge that Magic presents. I have never played a game that I do not have a deep love for. I love the games that I am playing and I am thrilled I am enjoying the game. I am not a fan of the monetization model and it is a shame that it is not in the best place. I don't have any bad feelings about it but I will recomend it.', 'I was even surprised when I tried it out for the first time and I could not stop enjoying it. I have played all of the games that Valve has released, and I have never felt like I was losing to a bad player. I have never felt like I was winning in a game that I didn't have the chance to experience. This game is huge and I am very happy with my experience.', 'I highly recommend this game. It is a great experience. The prices are reasonable and the game is fun.', 'I will recommend this game to people who are looking for a competitive card game, but like me, don't like games that are really free. I would say that you can play for free for the first few hours, and then you will have to pay $20 for a full collection of cards (most of which are mostly not free) to play. The game is great, and fun, and I am a fan of the lore for many people. I am also a big fan of the Valve award system. I would really like to get a Valve award, but it is unlikely to ever happen.', 'I would recommend this game to anyone who enjoys the game. It is an amazing card game, and you can play for free in the marketplace for years to come. I highly recommend it.', "This game is absolutely amazing, and I'm a big fan of the free modes. You can play for free in the game, and they have lots of prizes for free players.", "I am a huge fan of Dota and Hearthstone, but I have never played a game that I did not enjoy.", 'I've been playing a lot of other things for a long time now, and I was loving this game. I was a little surprised that this game didn't come out in Steam, but I was really surprised. I had hoped that the game would be a little more polished, but it was a lot of fun, and a lot of fun. The voice acting is great, and the game is fun, but it feels lost in the background. The game is so full of fun and intense, but it really doesn't have a lot of depth. I don't know if I will ever play this game again, but I love it. I had a lot of fun playing this game, and I am very happy with the way it has changed over time. Hopefully this game will stay fun for years to come, and I will keep playing it.', "I still have a lot of questions about this game, but I'm happy to say I'm enjoying it. I do think there are a lot of different modes that you can play in, and I think there are lots of ways to play some of them, but I've been enjoying this game a lot more. I think it is a lot more fun than I thought it would be. I think it's a very good game to play, and the fact that it's a lot of fun, and there's a lot of free stuff out there for people to play with.", "I'm not a huge game player, but I like this game a lot. It's a lot of fun, and it's not as expensive as some
```

## References

-   [Andrej Karpathy, "The Unreasonable Effectiveness of Recurrent Neural Networks", 2015](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
-   [Yoav Goldberg, "Character-level Language Models", 2015](https://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139)
-   [Max Woolf, a detailed blog post about the `textgenrnn` Python package, 2018](https://minimaxir.com/2018/05/text-neural-networks/)
-   [OpenAI, a blog post about GPT-2, 2019](https://openai.com/blog/better-language-models/)
-   [Max Woolf, API for GPT-2, 2019](https://github.com/minimaxir/gpt-2-simple)
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

