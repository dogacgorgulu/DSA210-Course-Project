# DSA210-Course-Project

## Table of Contents
**[Motivation](#motivation)**  

**[Tools](#tools)**  

**[Data](#data)**  
* [Data Sources](#data-sources)
* [Data Sets](#data-sets)

**[Data Analysis](#data-analysis)**

**[Findings](#findings)**

**[Limitations](#limitations)**  

**[Future Work](#future-work)**  

## Hearthstone Arena Analysis

### Motivation

Drafting (deck building) is one of the most common elements in any draft format of card games. The draft format is a game mode where players build their decks from a given card pool instead of using pre-constructed decks. In Hearthstone, the draft mode is called "Arena".

"The Arena is a game mode in which players draft decks to do battle against other players in a tournament-style format for the chance to earn substantial rewards. Players choose cards out of 30 separate selections of cards, building a 30-card deck to do battle against other players. Players play until they have suffered 3 losses or claimed 12 victories, at which point they will be granted a number of rewards based on the final number of wins they achieved." [Hearthstone Wiki](https://hearthstone.fandom.com/wiki/Arena)

The motivation behind this project is to determine optimal deck-building strategies. By analyzing the structure of the decks I have built over time, I aim to identify the strategies I should pursue more frequently and those I might consider avoiding in the future.

### Data

#### Data Sources

* [Hearth Arena](https://www.heartharena.com) - A website that tracks your Hearthstone matches.

#### Data Sets

* Categorical Data [`data`](/data/ArenaData_categorical.xlsx)

| Class        |   W |   L |   Total Matches | Archetype   |   Win Rate |
|:-------------|----:|----:|----------------:|:------------|-----------:|
| Warrior      |   3 |   3 |               6 | Tempo       |   0.5      |
| Hunter       |   2 |   3 |               5 | Tempo       |   0.4      |
| Demon Hunter |   3 |   2 |               5 | Attrition   |   0.6      |
| Druid        |   4 |   2 |               6 | Attrition   |   0.666667 |
| Mage         |   4 |   3 |               7 | Attrition   |   0.571429 |

A **deck** is a set of 30 cards. A **match** is a single game played with a deck. A **draft** is a series of matches played with the same deck. Each line represent a draft.

* Class: Determines the cards available in the card pool.
* W: Number of wins
* L: Number of loses.
* Total Matches = W + L
* Archetype: The playing strategy of a deck.
* Win Rate = W / Total Matches

* Quantitative Data [`data`](/data/ArenaData_quantitative.xlsx)

|   W |   L |   Total Matches |   Tierscore |   First Turn Playable |   2-Drops |   3-Drops |   4-Drops |   5-Drops |   Late-game |   Pings |   Early Removals |   Large Removals |   Board clear |   Reach |   Card Draw |   Win Rate |
|----:|----:|----------------:|------------:|----------------------:|----------:|----------:|----------:|----------:|------------:|--------:|-----------------:|-----------------:|--------------:|--------:|------------:|-----------:|
|   3 |   3 |               6 |        76.4 |                     6 |         5 |         5 |         4 |         3 |           2 |       6 |                4 |                3 |             1 |       5 |           7 |   0.5      |
|   2 |   3 |               5 |        75   |                     5 |         3 |         4 |         5 |         2 |           7 |       4 |                5 |                4 |             7 |      11 |           4 |   0.4      |
|   3 |   2 |               5 |        74   |                     1 |         2 |         4 |         4 |         6 |           6 |       7 |                4 |                1 |             5 |       5 |           7 |   0.6      |
|   4 |   2 |               6 |        73.9 |                     5 |         3 |         3 |         3 |         4 |           8 |       8 |                7 |                1 |             4 |       5 |           6 |   0.666667 |
|   4 |   3 |               7 |        74.5 |                     3 |         6 |         3 |         4 |         3 |           6 |       2 |                4 |                5 |             2 |       4 |           8 |   0.571429 |

* W: Number of wins
* L: Number of losses.
* Total Matches = W + L
* Tierscore: A parameter calculated by [Hearth Arena](https://www.heartharena.com). A higher value indicates greater meta viability.
* First Turn Playable: Number of 1-mana cards.
* X-Drops: Number of X-mana cards.
* Late-game: Number of cards with a mana cost of 5 or more.
* Pings: Number of cards that enable a small amount of damage (usually exactly 1) to a specific target.
* Early Removals: Number of cards that enable destroying minions in the early game.
* Large Removals: Number of cards that enable destroying minions in the late game.
* Board Clear: Number of cards that enable destroying multiple minions.
* Reach: Number of cards that enable direct damage to the enemy hero, regardless of the state of the board. 
* Card Draw: Number of cards that enable card draw.
* Win Rate = W / Total Matches

### Tools

**[Pandas](https://pandas.pydata.org/):**
**[Altair](https://altair-viz.github.io/index.html):**
**[Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/):**
**[Numpy](https://numpy.org/):** 
**[Scipy](https://www.scipy.org/):**

### Data Analysis

### Findings

### Limitations

* Couldn't validate Normality for Finding 1 due to size 2 < 3 for class Druid (Assumptions of ANOVA).

### Future Work