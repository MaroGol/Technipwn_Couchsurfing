Couchsurfing Recommender:
A Python script which receives as input a city and extracts from user living in that city recommendations for books, movies and songs.

Example usage:
```
> python3 ./recommender.py
Enter city: Kyoto
[!] No auth token/user id in config file. Need to log in....
Couchsurfing email: example@gmail.com
Couchsurfing password: password
Successful login! Updating config file.
Continuing program...
1 - Kyoto, Kyoto, Japan
2 - Kyoto, Japan
3 - Kita-ku, Kyoto, Kyoto, Japan
4 - Kyotomanyi, Kasanda, Uganda
5 - Koto Lua, 25164, Pauh, Padang, West Sumatra, Indonesia
Enter option: 1
Downloading page 1...
Downloading 2007340602...
Downloading 2008921714...
Downloading 2008262232...
Downloading 2007996731...
Downloading 2005729975...

> cat ./data/Kyoto_data.json | jq
[
  {
    "id": "2007340602",
    "media": "None"
  },
  {
    "id": "2008921714",
    "media": "【Music】\r\nMadonna\r\nTaylor Swift\r\nMiranda cosgrove\r\n\r\n【Movies】\r\nThe godfather\r\nBreakfast at tiffany's\r\nSabrina\r\nRoman holiday\r\nThe Devil wears PRADA\n\r\niCarly\r\nThe Bigbang Theory\nSuits\nDownton abby\r\nand so on. I like comedy and human drama."
  },
  {
    "id": "2008262232",
    "media": "one ok roc"
  },
  {
    "id": "2005729975",
    "media": "Music: I listen to all kind of music. \r\nMovies: Star Wars, Resident Evil, Forest Gump \r\nTV show: Prison Break, The Walking  Dead\r\nBook: Biography, Ayumu Takahashi "
  }
]
```