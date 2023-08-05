# About

This is a Python interface to [yugiohdeck.github.io](https://yugiohdeck.github.io/), which turns [the Yu-Gi-Oh! Trading Card Game](https://en.wikipedia.org/wiki/Yu-Gi-Oh!_Trading_Card_Game) decks into easily shared links.

This interface allows conversion of decklist links to card data and back. Card data is sourced from [YGOProDeck](https://db.ygoprodeck.com/api-guide/) and optionally [the YGOrganization DB](https://db.ygorganization.com/).

# Usage

`import yugiohdeck`

`yugiohdeck.ParseURLPasscodes(url)` - Parses a yugiohdeck URL and returns the card passcodes contained
**_async_** `yugiohdeck.ParseURLData(url)` - Parses a yugiohdeck URL and returns the card passcodes contained + their API data
