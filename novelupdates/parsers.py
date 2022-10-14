from bs4 import BeautifulSoup as bs
import re

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

def parseSearch(req):
    soup = bs(req.text, "html.parser")
    results = []
    for result in soup.find_all("div", class_="search_main_box_nu"):
        body = result.find("div", class_="search_body_nu")
        imageBody = result.find("div", class_="search_img_nu")

        title = body.find("div", class_="search_title").find("a").text
        link = body.find("div", class_="search_title").find("a").get("href")
        
        image = imageBody.find("img").get("src")
        if image.endswith("noimagemid.jpg"):
            image = None
        imageBody.find("div", class_="search_ratings").find("span").decompose()
        searchRating = re.sub(r'[()]', '', imageBody.find("div", class_="search_ratings").text.strip())

        ogDescription = body.find(text=True, recursive=False).strip()
        moreDescription = body.find("span", class_="testhide")
        for p in moreDescription.find_all("p", style="margin-top:-5px;"):
            p.decompose()
        moreDescription.find("span", class_="morelink list").decompose()
        description = ogDescription + moreDescription.text

        stats = body.find("div", class_="search_stats").find_all("span", class_="ss_desk")
        chapters = stats[0].text.strip()
        updateFreq = stats[1].text.strip()
        nuReaders = stats[2].text.strip()
        nuReviews = stats[3].text.strip()
        lastUpdated = stats[4].text.strip()

        genres = []
        for genre in body.find("div", class_="search_genre").find_all("a"):
            genreName = genre.text
            genreLink = genre.get("href")
            genres.append({
                "name": genreName,
                "link": genreLink
            })
        
        results.append({
            "title": title,
            "link": link,
            "image": image,
            "search_rating": searchRating,
            "description": description[:-1],
            "chapters": chapters,
            "update_freq": updateFreq,
            "nu_readers": nuReaders,
            "nu_reviews": nuReviews,
            "last_updated": lastUpdated,
            "genres": genres
        })
    return results

