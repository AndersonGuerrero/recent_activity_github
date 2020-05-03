from bs4 import BeautifulSoup
import mechanize

SITE_URL = "https://github.com"
LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
RECENT_ACTIVITY_URL = "/dashboard-feed"


def clearText(text):
    return text.replace('\n', '').replace('   ', '')


def extractData(item):
    title = item.find(class_='d-flex flex-items-baseline')
    username = title.find_all("a")[0].get_text()
    repository = title.find_all("a")[1].get_text()
    repo_description = clearText(
        item.find(class_='repo-description').get_text())
    dateTime = item.find('relative-time').attrs['datetime']
    programming_language = ''
    if item.find(class_='repo-language-color'):
        programming_language = clearText(
            item.find(class_='repo-language-color').find_next().get_text())

    return {
        'username': username,
        'repository': repository,
        'repo-description': repo_description,
        'programming-language': programming_language,
        'date-time': dateTime
    }


def getRecentActivity(br):
    br.open(SITE_URL + RECENT_ACTIVITY_URL)
    soup = BeautifulSoup(br.response().read(), features="html5lib")
    all_news = soup.find_all(
        class_="d-flex flex-items-baseline border-bottom border-gray py-3")
    data_response = []

    for new in all_news:
        data_response.append(extractData(new))

    br.open(SITE_URL + LOGOUT_URL)
    print(SITE_URL + ' --> Logout')
    return data_response


def loginGithub(email, password, token):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.open(SITE_URL + LOGIN_URL)
    print(browser.title())
    browser.select_form(nr=0)

    browser.form['login'] = email
    browser.form['password'] = password
    browser.submit()

    # Two-factor authentication
    if token:
        browser.select_form(nr=0)
        print(browser.title())
        browser.form['otp'] = token
        browser.submit()

    return getRecentActivity(browser)
