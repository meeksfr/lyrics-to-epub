from lyricsgenius import Genius

token = input("genius access token: ")
genius = Genius(token)
genius.skip_non_songs = True

searchName = input("artist: ")
artist = genius.search_artist(searchName, sort='popularity')
artist.save_lyrics()