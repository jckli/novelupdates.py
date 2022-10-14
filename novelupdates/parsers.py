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

def parseSeries(req):
    soup = bs(req.text, "html.parser")
    page = soup.find("div", class_="w-blog-content")
    body = page.find("div", class_="g-cols wpb_row offset_default")
    ot = body.find("div", class_="one-third").find("div", class_="wpb_text_column").find("div", class_="wpb_wrapper")
    tt = body.find("div", class_="two-thirds").find("div", class_="wpb_text_column").find("div", class_="wpb_wrapper")

    title = page.find("div", class_="seriestitlenu").text
    image = ot.find("div", class_="seriesimg").find("img").get("src")
    typeRaw = ot.find("div", id="showtype")
    typeText = typeRaw.find("a").text + " " + typeRaw.find("span").text
    type = {"name": typeText, "link": typeRaw.find("a").get("href")}

    genre = []
    for g in ot.find("div", id="seriesgenre").find_all("a"):
        genre.append({"name": g.text, "link": g.get("href"), "description": g.get("title")})

    tags = []
    for t in ot.find("div", id="showtags").find_all("a"):
        tags.append({"name": t.text, "link": t.get("href"), "description": t.get("title")})
    
    rating = []
    tempR = 5
    overallRating = re.sub(r'[()]', '', ot.find_all("h5", class_="seriesother")[3].find("span").text)
    rating.append({"name": "Overall", "rating": overallRating})
    for r in ot.find("table", id="myrates").find("tbody").find_all("tr"):
        rating.append({"name": tempR, "rating": r.select("td")[1].text.strip()})
        tempR -= 1
    
    language = {"name": ot.find("div", id="showlang").find("a").text, "link": ot.find("div", id="showlang").find("a").get("href")}

    authors = []
    if ot.find("div", id="showauthors").find_all("a"):
        for author in ot.find("div", id="showauthors").find_all("a"):
            authors.append({"name": author.text, "link": author.get("href")})
    else:
        authors.append({"name": ot.find("div", id="showauthors").find("span").text[0:], "link": None})
    artists = []
    if ot.find("div", id="showartists").find_all("a"):
        for artist in ot.find("div", id="showartists").find_all("a"):
            artists.append({"name": artist.text, "link": artist.get("href")})
    else:
        artists.append({"name": ot.find("div", id="showartists").find("span").text[0:], "link": None})
    
    year = ot.find("div", id="edityear").text[1:]
    statusRaw = ot.find("div", id="editstatus")
    if "<br>" in statusRaw:
        statusRaw.find("br").replace_with("\n")
    status = statusRaw.text[1:]
    licensed = ot.find("div", id="showlicensed").text[1:]
    completelyTranslated = ot.find("div", id="showtranslated").text[1:]
    if ot.find("div", id="showopublisher").find("a") is not None:
        originalPublisher = {"name": ot.find("div", id="showopublisher").find("a").text, "link": ot.find("div", id="showopublisher").find("a").get("href")}
    else:
        originalPublisher = {"name": ot.find("div", id="showopublisher").text, "link": None}
    if ot.find("div", id="showepublisher").find("a") is not None:
        englishPublisher = {"name": ot.find("div", id="showepublisher").find("a").text, "link": ot.find("div", id="showepublisher").find("a").get("href")}
    else:
        englishPublisher = {"name": ot.find("div", id="showepublisher").text, "link": None}
    releaseFreq = ot.find_all("h5", class_="seriesother")[13].next_sibling.strip()

    result = {
        "title": title,
        "image": image,
        "type": type,
        "genre": genre,
        "tags": tags,
        "rating": rating,
        "language": language,
        "authors": authors,
        "artists": artists,
        "year": year,
        "status": status,
        "licensed": licensed,
        "completely_translated": completelyTranslated,
        "original_publisher": originalPublisher,
        "english_publisher": englishPublisher,
        "release_freq": releaseFreq
    }
    return result