import requests
from bs4 import BeautifulSoup

URL = "https://www.timeout.com/london/film/100-best-comedy-movies"

response = requests.get(URL)
#content = response.text

soup = BeautifulSoup(response.content, "html.parser")
article = soup.find_all(name="a", class_="xs-text-charcoal decoration-none")
titles = []
for title in article:
    titles.append(title.getText().strip())
unwanted = {"Another Round", "Blithe Spirit", "Fatman", "Borat: Subsequent Moviefilm"}
titles = [item for item in titles if item not in unwanted]
with open("100 Movies.txt", "w", encoding="utf-8") as file:
    for title in titles[::-1]:
        file.write("%s\n" % title)