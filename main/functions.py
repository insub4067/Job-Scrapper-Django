import requests
from bs4 import BeautifulSoup
from .db import db

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


def get_soup(url):
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, "html.parser")


def scrap_overflow(word):

    jobs = []

    url = f"https://stackoverflow.com/jobs?q={word}"
    overflow_soup = get_soup(url)
    pages = overflow_soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = int(pages[-2].get_text(strip=True))

    for page in range(last_page):

        page = page + 1

        if page == 1:
            results = overflow_soup.find_all("div", {"class": "-job"})

            for result in results:

                title_link = result.find("h2").find("a", {"class": "s-link"})

                title = title_link["title"]
                link = f"https://stackoverflow.com/{title_link['href']}"
                company, location = result.find(
                    "h3", {"class": "fc-black-700 fs-body1 mb4"}
                ).find_all("span", recursive=False)
                company = company.string
                location = location.string.strip()
                job = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                }

                jobs.append(job)

        elif page > 1:

            url = f"https://stackoverflow.com/jobs?q={word}&pg={page}"
            overflow_soup = get_soup(url)
            results = overflow_soup.find_all("div", {"class": "-job"})

            for result in results:

                title_link = result.find("h2").find("a", {"class": "s-link"})

                title = title_link["title"]
                link = f"https://stackoverflow.com/{title_link['href']}"
                company, location = result.find(
                    "h3", {"class": "fc-black-700 fs-body1 mb4"}
                ).find_all("span", recursive=False)
                company = company.string
                location = location.string.strip()
                job = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                }

                jobs.append(job)

    return jobs


def scrap_remotely(word):

    jobs = []

    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    remotely_soup = get_soup(url)
    results = (
        remotely_soup.find("section", {"class": "jobs"})
        .find("ul")
        .find_all("li", {"class": "feature"})
    )

    for result in results:

        job_info_link = result.find_all("a")

        if len(job_info_link) > 1:
            job_info_link = job_info_link[1]
        else:
            job_info_link = job_info_link[0]

        job_info = job_info_link.find_all("span")

        company = job_info[0].get_text()
        title = job_info[1].get_text()
        location = job_info[5].get_text()
        link = f"https://weworkremotely.com/{job_info_link['href']}"

        job = {
            "title": title,
            "company": company,
            "location": location,
            "link": link,
        }
        jobs.append(job)

    return jobs


def scrap_remoteok(word):

    jobs = []

    url = f"https://remoteok.com/remote-{word}-jobs"
    remoteok_soup = get_soup(url)
    results = remoteok_soup.find("table", {"id": "jobsboard"}).find_all(
        "tr", {"class": "job"}
    )

    for result in results:

        tds = result.find_all("td")
        link = tds[0].find("a")["href"]
        if not link:
            link = ""

        title = tds[1].find("h2").string
        if not title:
            title = ""

        company = tds[1].find("a").find("h3").string
        if not company:
            company = ""

        location = tds[1].find("div", {"class": "location"})
        if not location:
            location = ""
        else:
            location = location.string

        job = {
            "title": title,
            "company": company,
            "location": location,
            "link": f"https://remoteok.io/{link}",
        }

        jobs.append(job)

    return jobs


def get_jobs(word):

    try:

        overflow_jobs = scrap_overflow(word)
        remotely_jobs = scrap_remotely(word)
        remoteok_jobs = scrap_remoteok(word)

        jobs = remoteok_jobs + remotely_jobs + overflow_jobs

        db[word] = jobs

        return jobs
    except:
        return