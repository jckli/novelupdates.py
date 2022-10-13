from bs4 import BeautifulSoup as bs

def parseFeed(req):
    soup = bs(req.text, "html.parser")
    feed = []
    for table in soup.find_all("table", id="myTable", class_="tablesorter"):
        for entry in table.find("tbody").find_all("tr"):
            title = entry.select("td")[0].find("a").get("title")
            nuLink = entry.select("td")[0].find("a").get("href")
            chapter = entry.select("td")[1].find("a").get("title")
            chapterLink = f'https:{entry.select("td")[1].find("a").get("href")}'
            groupName = entry.select("td")[2].find("a").get("title")
            groupLink = entry.select("td")[2].find("a").get("href")
            feed.append({
                "title": title,
                "nuLink": nuLink,
                "chapter": chapter,
                "chapterLink": chapterLink,
                "groupName": groupName,
                "groupLink": groupLink
            })
    return feed