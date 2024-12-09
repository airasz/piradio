import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup
import requests
import asyncio
# import serialdisplay
import oledisplay
import random
import serial_esp
import os.path
myoled= oledisplay.oled()
myesp=serial_esp.serialesp()

urll="https://www.goal.com/en/match/juventus-vs-bologna/I7nhslu6_ZM8SCwkDXBXw"
count=0

# display=serialdisplay.display()
classname="match-data_score__xQ29z"
lscore="0-0"
mscore="0-0"
mteam=""
# def interuptDisplay(msg):
#     display.display(msg, False)
#     display.frezeeDisplay(5)

#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"), static_path = os.path.join(os.path.dirname(__file__), "static")
    )


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global urll
        # self.write("Web Scraper Running! Check the terminal for scraping logs.")
        self.render("webscr.html", wsurl=urll)

    async def post(self):
        global count
        global urll
        url=""
        try:
            value = self.get_argument('url')
            print("url "+ value)
        except:
            print("skiping cause argument not contain " + value)
            return
        if value !="":
            url = value
            if not url:
                self.write({"error": "Please provide a URL"})
                return
            urll=url
            count=24
            # result = await fetch_and_scrape(url)
            scraper = Scraper(url)
            # self.write("url saved")

            # pass
        # ok()
        self.render("webscr.html", wsurl=urll)
# Tornado request handler
class ScrapeHandler(tornado.web.RequestHandler):
    async def get(self):
        global count
        global urll
        url = self.get_argument("url", urll)
        if not url:
            self.write({"error": "Please provide a URL"})
            return
        urll=url
        count=24
        # result = await fetch_and_scrape(url)
        scraper = Scraper(url)
        self.write("url saved")


class Scraper:
    def __init__(self, url):
        self.url = url

    async def scrape(self):

        http_client = tornado.httpclient.AsyncHTTPClient()
        global count
        global urll
        global lscore
        global mscore
        global mteam
        count+=1
        if count %2==0:
            # interuptDisplay(lscore)
            pass
        if count>25:
            count =0
            sblink=0
            try:
                # Send HTTP GET request
                # response = requests.get(self.url)
                # response.raise_for_status()  # Raise an error for bad HTTP responses
                response = await http_client.fetch(urll)
                html = response.body.decode('utf-8')  # Decode the HTML content
                # Parse HTML content
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string if soup.title else 'No title found'

#                 teams= soup.find_all('span', "heading_teams__ljLuQ")
#                 # teams=soup.select('span[data-testid="team-name"]')
#                 tm=""
#                 for team in teams:
#                     tmm=team.select_one("."+"heading_teams__ljLuQ")
#                     tm+=team.get_text()
#                     tm=tm.replace("vs ","\nvs\n")
# #
#

                teams= soup.find_all('span', "heading_teams__ljLuQ")
                # teams=soup.select('span[data-testid="team-name"]')
                tm=""
                for team in teams:
                    tm+=team.decode_contents()
                    tm=tm.replace(" vs ","\nvs ")
#


                # teams= soup.select('.match-team_team-name__cd4_m')
                # # teams=soup.select('span[data-testid="team-name"]')
                # tm=""
                # for team in teams:
                #     print(team.decode_contents())
                #     # tmm=team.select_one("."+"team_team-name__0U_gn")
                #     tm+=team.decode_contents()
                #     # tm=tm.replace("vs ","\nvs\n")
                #
                # teams= soup.find_all('span', "match-team_team-name__cd4_m")
                # # teams=soup.select('span[data-testid="team-name"]')
                # tm=""
                # for team in teams:
                #     print(team)
                #     tmm=team.select_one("."+"match-team_team-name__cd4_m")
                #     tm+=team.decode_contents()
                #     # tm=tm.replace("vs ","\nvs\n")
                #


                # teams= soup.find_all('span', "match-team_team-name__cd4_m")
                # # teams=soup.select('span[data-testid="team-name"]')
                # tm=""
                # for team in teams:
                #     print(team)
                #     tmm=team.select_one("."+"match-team_team-name__cd4_m")
                #     tm+=team.get_text()
                #     # tm=tm.replace("vs ","\nvs\n")


                minutes= soup.find_all('span', "match-period_period___hImu")
                mnt="x"
                for minute in minutes:
                    # print(mincute)
                    mnt=minute.select_one("."+"match-period_period___hImu")
                try:
                    mnt=minute.get_text()
                except:
                    mnt="FT"
                if len(mnt)>3:
                    mnt=mnt[:3]

                scores= soup.find_all('span',classname)
                for score in scores:
                    # print(score)
                    scr=score.select_one("."+classname)
                # serialdisplay(score.get_text())
                print(tm+ " " + mnt+" > "+score.get_text())
                lscore=tm+ "\n" + mnt+" > "+score.get_text()
                if score.get_text()!= mscore:
                    print ("============new score")
                    sblink=1
                    mscore=score.get_text()
                if tm==mteam:
                    if sblink==1:
                        myesp.show("blink16")
                        sblink=0
                mteam=tm
                ypos = random.randint(0,4)
                xpos = random.randint(0,10)
                # myoled.displayfscs(score.get_text(),35, (xpos,ypos))
                myoled.update(mnt)
                myoled.displayduo(mscore, tm,35, (xpos,ypos), (0,40) )
                # interuptDisplay(lscore)
            except Exception as e:
                print(f"Error during scraping: {e}")

    async def scraping(self):

        global count
        global urll
        global classname
        count+=1
        if count>10:
            count=0
            try:
                # Send HTTP GET request
                response = requests.get(self.url)
                response.raise_for_status()  # Raise an error for bad HTTP responses

                # Parse HTML content
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string if soup.title else 'No title found'
                scores= soup.find_all('span',classname)
                for score in scores:
                    # print(score)
                    scr=score.select_one("."+classname)
                # serialdisplay(score.get_text())
                result = score.get_text()
                print("result = "+result)
            except Exception as e:
                print(f"Error during scraping: {e}")


async def periodic_scraping(scraper):
    while True:
        await scraper.scrape()
        await asyncio.sleep(1)  # Wait for 1 second before the next scrape


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),(r"/scrape", ScrapeHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"})
    ],
        **settings)


if __name__ == "__main__":
    # global urll
    url_to_scrape = urll  # Replace with the target website
    scraper = Scraper(url_to_scrape)

    app = make_app()
    app.listen(8890)

    # Start periodic scraping task
    tornado.ioloop.IOLoop.current().spawn_callback(periodic_scraping, scraper)

    print("Starting Tornado server on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
