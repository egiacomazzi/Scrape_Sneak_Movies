import requests
from lxml import html
import pandas as pd

page = requests.get("https://www.cinema-arthouse.de/kino/programm/ov-sneakpreview")
tree = html.fromstring(page.content)

old = tree.xpath('//div[@class="wpb_text_column wpb_content_element "]')

titles = []
ratings = []
dates = []
count = 1
case = 0
for film in old[4:-1]:

    # extra case: THE MAN WHO KILLED DON QUIXOTE,
    if len(film.xpath('.//strong/text()')) < 2:
        title = film.xpath('.//strong/text()')[0]
        rating = "-"
        date = film.xpath('.//p/text()')

        case = 0
    elif (film.xpath('.//strong/text()')[1] == '\n') and (film.xpath('.//strong/text()')[0][:1]!= '\n'):
        title = film.xpath('.//strong/text()')[0]
        rating = film.xpath('.//strong/text()')[2]

        case = 1
        # extra case: THE WIFE
        if (len(film.xpath('.//strong/text()')))>3 and (film.xpath('.//strong/text()')[2] == '\n'):
            rating = film.xpath('.//strong/text()')[3]
            case = 1.1
        # extra case: BLINDED BY THE LIGHT
        if rating == '\n':
            rating = "-"
            case = 1.2

         # extra case: sneack extreme
        if film.xpath('.//strong/text()')[0] == 'Sneak-Extreme:':
            title = 'Sneak-Extreme: ' + film.xpath('.//strong/text()')[2]
            rating = film.xpath('.//strong/text()')[4]
            case = 1.3

    elif (film.xpath('.//strong/text()')[0][:1] == '\n') and (film.xpath('.//strong/text()')[1][:1] == '\n'):
        title = film.xpath('.//strong/text()')[0][1:]
        rating = film.xpath('.//strong/text()')[1][1:]

        case = 2

    elif (film.xpath('.//strong/text()')[0][:1] != '\n') and (film.xpath('.//strong/text()')[1][:1] == '\n'):
        title = film.xpath('.//strong/text()')[0]
        rating = film.xpath('.//strong/text()')[1][1:]

        case = 3
    elif (film.xpath('.//strong/text()')[0][:1] == '\n') and (film.xpath('.//strong/text()')[1] == '\n'):
        title = film.xpath('.//strong/text()')[0][1:]
        rating = film.xpath('.//strong/text()')[2]

        case = 4
    else:
        title = film.xpath('.//strong/text()')[0]
        rating = film.xpath('.//strong/text()')[1]

        case = 5
    rating = rating[-3:]
    date = film.xpath('.//p/text()')[0][6:-1]

    titles.append(title)
    ratings.append(rating)
    dates.append(date)
    print("Date: ", film.xpath('.//p/text()')[0])
    print("Title: ",count, ": ", title)
    print("Rating: ", rating)
    print("Case: ", case)
    count = count+1

movie_info = {"Title":titles, "Rating": ratings, "Date":dates}
Sneak_Films = pd.DataFrame(movie_info)
print(Sneak_Films[["Title","Rating","Date"]])
Sneak_Films.to_csv("Sneak_Films.csv")
