import json
from ebooklib import epub

artistName = input("artist name: ")
filePath = input("lyrics json file path: ")
bookId = int(input("id: "))
 
f = open(filePath)
data = json.load(f)

book = epub.EpubBook()
# set metadata
book.set_identifier(f"id{bookId:06d}")
book.set_title(f"{artistName} lyrics")
book.add_author(artistName)
book.set_language("en")

counter = 0
chapters = {}

for i in data['songs']:

    title = i['full_title']
    print(title)

    lyrics = i['lyrics'].removesuffix('Embed')
    lyrics = lyrics.split('Lyrics', 1)[1]
    lyrics = lyrics.replace("You might also like[", "[")
    print(lyrics)
    lyrics = lyrics.replace("\n", "<br>")

    chapters[counter] = epub.EpubHtml(title=title, file_name=f"chap_{counter + 1}.xhtml", lang="en")
    chapters[counter].content = (
        f"<h1>{title}</h1>"
        f"<p>{lyrics}</p>"
    )

    book.add_item(chapters[counter])

    counter += 1

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = "BODY {color: white;}"
nav_css = epub.EpubItem(
    uid="style_nav",
    file_name="style/nav.css",
    media_type="text/css",
    content=style,
)

# add CSS file
book.add_item(nav_css)

# basic spine
allChapters = list(chapters.values())
fullSpine = ["nav"] + allChapters
book.spine = fullSpine

# write to the file
artistName = artistName.replace(" ", "")
epub.write_epub(f"{artistName}.epub", book, {})
 
f.close()