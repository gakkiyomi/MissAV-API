import re
from typing import Any
from urllib.parse import urlparse, urlunparse

from fastapi import HTTPException
from lxml import etree


def parse_url(url: str):
    parsed = urlparse(url)
    normalized_path = parsed.path.replace("//", "/")
    return urlunparse(parsed._replace(path=normalized_path))


def parse_login(tree):
    login_button_xpath = '''
            //a[
                contains(text(), '登入')
                and
                contains(concat(' ', normalize-space(@class), ' '), ' bg-primary ')
            ]
        '''
    login_buttons = tree.xpath(login_button_xpath)
    if len(login_buttons) != 0:
        raise HTTPException(status_code=401, detail='Unauthorized')


def __parse_delete_token(tree) -> str:
    input_xpath = etree.XPath('//input[@type="hidden" and @name="_token"]')
    return input_xpath(tree)[0].get("value", "")


def __parse_genres(tree, is_subtitle: bool = True) -> list[dict]:
    div_xpath = etree.XPath('''
        //div[
        contains(concat(' ', normalize-space(@class), ' '), ' grid ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' grid-cols-2 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' md:grid-cols-3 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' xl:grid-cols-4 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' gap-4 ')
    ]
    ''')
    genres = []
    for div in etree.XPath('.//div')(div_xpath(tree)[0]):
        a = etree.XPath('a')(div)[0]
        p = etree.XPath('p')(div)[0]
        genres.append({
            "name": a.text.strip(),
            "link": a.get('href', ''),
            "count": int(p.text_content().strip().split(" ")[0])
        })
    return genres


def __parse_links(tree, is_subtitle: bool = True) -> list[dict]:
    div_xpath = etree.XPath('''
        //div[
        contains(concat(' ', normalize-space(@class), ' '), ' aspect-w-16 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' aspect-h-9 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' rounded ')
    ]
    ''')
    links = []
    for div in div_xpath(tree):
        a = etree.XPath('a')(div)
        image = etree.XPath('img')(a[0])[0]
        video = etree.XPath('video')(a[0])[0]
        subtitle_duration = a[0:-1]
        link_info = {
            "title": image.get('alt', ''),
            "link": a[0].get('href', ''),
            "number": a[0].get('alt', ''),
            "cover": image.get('data-src', ''),
            "preview": video.get('data-src', ''),
            "duration": a[-1].text_content().strip()
        }
        if is_subtitle and len(subtitle_duration) == 2:
            link_info.update({
                'is_subtitle': True,
                'subtitle': subtitle_duration[1].text_content().strip()
            })
        links.append(link_info)
    return links


def __parse_playlists(tree) -> list[dict]:
    playlists_xpath = etree.XPath('//ul[@role="list" and @class="space-y-4"]')
    links = []
    for ul in playlists_xpath(tree):
        for item in etree.XPath('.//a')(ul):
            p = etree.XPath('.//p')(item)
            update_at = p[3].text.strip().split(" ")[1] if len(
                p) == 4 else p[4].text.strip().split(" ")[1]
            link_info = {
                "name": p[0].text.strip(),
                "key": item.get('href', '').split("/")[-1],
                "link": item.get('href', ''),
                "scope": p[1].text_content().strip(),
                "owner": p[2].text_content().strip(),
                "updated_at": update_at,
            }
            links.append(link_info)
    return links


def __parse_page(tree) -> int:
    page_selector = etree.XPath('//a[contains(@aria-label, "Go to page")]')
    pages = page_selector(tree)
    if pages:
        match = re.search(r'Go to page (\d+)', pages[-1].get("aria-label"))
        if match:
            return int(match.group(1))
    else:
        return 0


def parse_movie_detail(tree) -> dict:
    meta_info = etree.XPath(
        '//meta[@property="og:title" or @property="og:url" or @property="og:description" or @property="og:image"]')
    movie_info = {}
    for meta in meta_info(tree):
        property = meta.get("property", "")
        content = meta.get("content", "")
        if property == "og:title":
            movie_info['title'] = content
        elif property == "og:url":
            movie_info['link'] = content
        elif property == "og:description":
            movie_info['description'] = content
        elif property == "og:image":
            movie_info['cover'] = content
    div_xpath = etree.XPath(
        '//div[@class="space-y-2"]')
    div_info = etree.XPath(
        './/div[@class="text-secondary"]')(div_xpath(tree)[0])
    release_date = div_info[0].text_content().strip().split("\n")[1].strip()
    number = div_info[1].text_content().strip().split("\n")[1].strip()
    jp_title = div_info[2].text_content().strip().split("\n")[1].strip()
    actress = div_info[3].text_content().strip().split("\n")[1].strip()
    genres = div_info[4].text_content().strip().split("\n")[1].strip()
    series = div_info[5].text_content().strip().split("\n")[1].strip()
    maker = div_info[6].text_content().strip().split("\n")[1].strip()
    director = div_info[7].text_content().strip().split("\n")[1].strip()
    tags = div_info[8].text_content().strip().split("\n")[1].strip()
    movie_info['release_date'] = release_date
    movie_info['number'] = number
    movie_info['jp_title'] = jp_title
    movie_info['actress'] = actress
    movie_info['genres'] = genres
    movie_info['series'] = series
    movie_info['maker'] = maker
    movie_info['director'] = director
    movie_info['tags'] = tags
    return movie_info


def parse_movie_list(tree) -> tuple[int, int, Any]:
    data = __parse_links(tree)
    return (len(data), __parse_page(tree), data)


def parse_movie_search(tree) -> tuple[int, int, Any]:
    data = {
        "actress": __parse_actress(tree, div_xpath=etree.XPath('''
        //div[
        contains(concat(' ', normalize-space(@class), ' '), ' max-w-full ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' mb-6 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' text-nord4 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' rounded-lg ')
    ]
    ''')),
        "moives": __parse_links(tree)
    }
    # Besides the movie, the actresses also need to be analyzed.
    return (len(data["moives"]), __parse_page(tree), data)


def parse_movie_genres(tree) -> tuple[int, int, Any]:
    data = __parse_genres(tree)
    return (len(data), __parse_page(tree), data)


def parse_uncensored_moives(tree) -> tuple[int, int, Any]:
    data = __parse_links(tree, is_subtitle=False)
    return (len(data), __parse_page(tree), data)


def parse_actress_info(tree) -> dict:
    pass


def parse_actress_list(tree) -> tuple[int, int, Any]:
    data = __parse_actress(tree)
    return (len(data), __parse_page(tree), data)


def parse_actress_ranking(tree) -> list[Any]:
    data = __parse_actress_ranking(tree)
    return data


def parse_playlists(tree) -> tuple[int, int, Any]:
    data = __parse_playlists(tree)
    return (len(data), __parse_page(tree), data)


def parse_playlist_delete_token(tree) -> str:
    return __parse_delete_token(tree)


def parse_playlist_detail(tree) -> tuple[int, int, Any]:
    data = __parse_links(tree)
    comments = __parse_playlist_comment(tree)
    for index, comment in enumerate(comments):
        data[index].update({
            "comment": comment
        })
    return (len(data), __parse_page(tree), data)


def __parse_playlist_comment(tree) -> tuple[int, int, Any]:
    comment_xpath = etree.XPath(
        '//textarea[@x-ref="comment" and @name="description"]')
    comments = []
    for comment in comment_xpath(tree):
        comments.append(comment.text_content().strip())
    return comments


def __parse_actress(tree, div_xpath=etree.XPath('''
        //div[
        contains(concat(' ', normalize-space(@class), ' '), ' max-w-full ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' p-8 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' text-nord4 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' bg-nord1 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' rounded-lg ')
    ]
    ''')) -> list[dict]:
    actress = []
    div = div_xpath(tree)[0]
    for li in etree.XPath('.//li')(div):
        a = etree.XPath('.//a')(li)[1]
        name = etree.XPath('.//h4')(a)[0]
        p = etree.XPath('p')(a)
        videos = p[0]
        cover = etree.XPath('.//img')(li)
        actress_info = {
            "name": name.text.strip(),
            "link": a.get('href', ''),
            "videos": int(videos.text.strip().split(" ")[0]),
            "cover": cover[0].get('src', '') if len(cover) > 0 else ''
        }
        if len(p) == 2:
            actress_info.update({
                "debut": p[1].text.strip().split(" ")[0],
            })
        actress.append(actress_info)
    return actress


def __parse_actress_ranking(tree) -> list[dict]:
    div_xpath = etree.XPath('''
        //div[
        contains(concat(' ', normalize-space(@class), ' '), ' max-w-full ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' p-8 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' text-nord4 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' bg-nord1 ')
        and
        contains(concat(' ', normalize-space(@class), ' '), ' rounded-lg ')
    ]
    ''')
    actress = []
    div = div_xpath(tree)[0]
    for li in etree.XPath('.//li')(div):
        a = etree.XPath('.//a')(li)[1]
        name = etree.XPath('.//h4')(a)[0]
        span = etree.XPath('.//span')(a)[0]
        cover = etree.XPath('.//img')(li)
        actress_info = {
            "name": name.text.strip(),
            "link": a.get('href', ''),
            "rank": span.text.strip(),
            "cover": cover[0].get('src', '') if len(cover) > 0 else ''
        }
        actress.append(actress_info)
    return actress
