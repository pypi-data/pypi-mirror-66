### functions for mkv_this_scr.py


def get_urls(st_url):
    """ fetch a bunch of article URLs from The Guardian world news page for a given date. Format: 'https://theguardian.com/cat/YEAR/mth/xx' """
    try:
        req = requests.get(st_url)
        req.raise_for_status()
    except Exception as exc:
        print(f": There was a problem: {exc}.\n: Please enter a valid URL")
        sys.exit()
    else:
        print(": fetched initial URL.")
        soup = bs4.BeautifulSoup(req.text, "lxml")
        art_elem = soup.select(
            'div[class="fc-item__header"] a[data-link-name="article"]'
        )  # pull the element containing article links.
        urls = []
        for i in range(len(art_elem)):
            urls = urls + [art_elem[i].attrs["href"]]
        print(": fetched list of URLs")
        return urls  # returns a LIST


def scr_URLs(urls):  # input a LIST
    """ actually fetch all the URLs obtained by get_urls """
    try:
        content = []
        for i in range(len(urls)):
            req = requests.get(urls[i])
            req.raise_for_status()
            content = content + [req.text]  # SUPER slow.
            print(": fetched page " + urls[i])
    except Exception as exc:
        print(
            f": There was a problem: {exc}.\n: There was trouble in your list of URLs"
        )
        sys.exit()
    else:
        print(": fetched all pages.")
        return content


def scr_convert_html(content):  # takes a LIST of html pages
    """ convert all pages obtained by scr_URLs """
    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    h2t.images_to_alt = True
    h2t.ignore_emphasis = True
    h2t.ignore_tables = True
    h2t.unicode_snob = True
    h2t.decode_errors = "ignore"
    h2t.escape_all = False  # remove all noise if needed
    s = []
    for i in range(len(content)):
        s = s + [h2t.handle(content[i])]  # convert
    t = []
    for i in range(len(s)):
        t = t + [re.sub("[#*]", "", s[i])]  # remove hash/star from the 'markdown'
    u = " ".join(t)  # convert list to string
    print(": Pages converted to text")
    return u
