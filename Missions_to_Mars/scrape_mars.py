from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Step1-Part1: NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all('div', class_='list_text')
    news_title = news[0].find('div', class_='content_title').text
    news_p = news[0].find('div', class_='article_teaser_body').text


    # Step1-Part2: JPL Mars Space Images - Featured Image
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    relative_image_path = soup.find('img', class_='headerimage fade-in').get('src')
    featured_image_url = url + relative_image_path

    # Step1-Part3: Mars Facts
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_df = pd.DataFrame()
    mars_table = soup.find_all('table')[0]
    rows = mars_table.find_all('tr')
    for row in rows:
        values = row.find_all('td')
        thisdict = {
                "Description": row.find('th').text.strip(),
                "MARS": values[0].text.strip(),
                "EARTH": values[1].text.strip()
            }
        mars_df = mars_df.append(thisdict, ignore_index = True)
    mars_html_table = mars_df.to_html(classes='table table-striped', header = True, index=False)
    
    #Step1-Part4: Mars Hemispheres
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    link_section = soup.find('div', class_='collapsible results')
    links = link_section.find_all('div', class_='item')
    hemisphere_image_urls = []
    for link in links:
        link_url= link.find('a', class_='itemLink product-item').get('href')
        img_name = ' '.join(link.find('a', class_='itemLink product-item').find('img').get('alt').split()[:-2])
        browser.visit(url+link_url)
        link_html = browser.html
        link_soup = BeautifulSoup(link_html, 'html.parser')
        img_url = url + (link_soup.find('img', class_='wide-image').get('src'))
        hemisphere_image_urls.append({
            'title': img_name,
            'img_url':img_url
            })

    browser.quit()

    results_scrape = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_img': featured_image_url,
        'mars_facts': mars_html_table,
        'mars_hemispheres': hemisphere_image_urls
    }

    return results_scrape


