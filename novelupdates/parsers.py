from bs4 import BeautifulSoup as bs
import re

def parseFeed(req):
    soup = bs(req.text, "html.parser")
    feed = []
    for table in soup.find_all("table", id="myTable", class_="tablesorter"):
        for entry in table.find("tbody").find_all("tr"):
            title = entry.select("td")[0].find("a").get("title")
            nuLink = entry.select("td")[0].find("a").get("href")
            release = entry.select("td")[1].find("a").get("title")
            releaseLink = f'https:{entry.select("td")[1].find("a").get("href")}'
            groupName = entry.select("td")[2].find("a").get("title")
            groupLink = entry.select("td")[2].find("a").get("href")
            feed.append({
                "title": title,
                "nuLink": nuLink,
                "group": {
                    "name": groupName,
                    "link": groupLink
                },
                "release": {
                    "name": release,
                    "link": releaseLink
                }
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
        releases = stats[0].text.strip()
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
            "releases": releases,
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

    # One Third (ot)
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
    for author in ot.find("div", id="showauthors").find_all("a"):
        authors.append({"name": author.text, "link": author.get("href")})

    artists = []
    for artist in ot.find("div", id="showartists").find_all("a"):
        artists.append({"name": artist.text, "link": artist.get("href")})
    
    year = ot.find("div", id="edityear").text[1:]
    statusRaw = ot.find("div", id="editstatus")
    if "<br>" in statusRaw:
        for br in statusRaw.find_all("br"):
            br.replace_with("\n")
    status = statusRaw.text[1:]
    licensed = ot.find("div", id="showlicensed").text[1:]
    completelyTranslated = ot.find("div", id="showtranslated").text[1:]
    if ot.find("div", id="showopublisher").find("a") is not None:
        originalPublisher = {"name": ot.find("div", id="showopublisher").find("a").text, "link": ot.find("div", id="showopublisher").find("a").get("href")}
    else:
        originalPublisher = None
    if ot.find("div", id="showepublisher").find("a") is not None:
        englishPublisher = {"name": ot.find("div", id="showepublisher").find("a").text, "link": ot.find("div", id="showepublisher").find("a").get("href")}
    else:
        englishPublisher = None
    releaseFreq = ot.find_all("h5", class_="seriesother")[13].next_sibling.strip()

    # Two Thirds (tt)
    descriptionRaw = tt.find("div", id="editdescription")
    if "<br>" in descriptionRaw:
        for br in descriptionRaw.find_all("br"):
            br.replace_with("\n")
    description = descriptionRaw.text[:-1]

    associatedNames = [i for i in tt.find("div", id="editassociated").contents if str(i) != "<br/>"]

    tableBody = tt.find("table", id="myTable")
    latestChapters = []
    if tableBody is not None:
        for rel in tableBody.find("tbody").find_all("tr"):
            date = re.sub('\s+', '', rel.select("td")[0].text)
            group = rel.select("td")[1].find("a").text
            groupLink = rel.select("td")[1].find("a").get("href")
            release = rel.select("td")[2].find("a").get("title")
            releaseLink = rel.select("td")[2].find("a").get("href")
            latestChapters.append({
                "date": date,
                "group": {
                    "name": group,
                    "link": groupLink
                },
                "release": {
                    "name": release,
                    "link": releaseLink
                }
            })
    else:
        latestChapters = None

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
        "release_freq": releaseFreq,
        "description": description,
        "associated_names": associatedNames,
        "latest_chapters": latestChapters
    }
    return result