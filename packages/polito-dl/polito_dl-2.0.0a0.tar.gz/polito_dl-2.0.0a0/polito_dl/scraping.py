from polito_dl.parsing import get_course_data, parse_html, get_download_paths

base_url = "https://didattica.polito.it"


def course_data(session, url):
    if not (
        url.startswith(base_url + "/portal/pls/portal/sviluppo.videolezioni.vis")
        or url.startswith(base_url + "/pls/portal30/sviluppo.videolezioni.vis")
    ):
        raise ValueError("invalid course URL")

    resp = session.get(url)
    soup = parse_html(resp.content)
    return get_course_data(soup)


def download_paths(session, path):
    if not path.startswith("sviluppo.videolezioni.vis"):
        raise ValueError("invalid lecture path")

    url = base_url + "/pls/portal30/" + path
    resp = session.get(url)
    soup = parse_html(resp.content)
    return get_download_paths(soup)


def direct_download_url(session, path):
    if not path.startswith("/pls/portal30/sviluppo.videolezioni.download"):
        raise ValueError("invalid download path")

    resp = session.get(base_url + path, allow_redirects=False)
    return resp.headers["Location"]
