import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup
import requests
import asyncio
import serialdisplay
import tornado.httpclient
import Nextiondisplay
MyNextion=Nextiondisplay.display()

import json
import os.path
urll="https://www.goal.com/id/pertandingan/torino-vs-parma-calcio-1913/jreZNqxUooBMV_Z6ApGId"
count=23

DATAFILE_='wbsscr.json'
display=serialdisplay.display()
classname="match-data_score__xQ29z"
lscore="0-0"

mscore="0-0"
mteam=""
def interuptDisplay(msg):
    display.display(msg, False)
    display.frezeeDisplay(5)
#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"), static_path = os.path.join(os.path.dirname(__file__), "static")
    )


class MainHandler(tornado.web.RequestHandler):
    def get(self):
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
            jdata={"url":urll
                }
            with open(DATAFILE_, "w") as f:
                json.dump(jdata, f)

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
        if count %5==0:
            # interuptDisplay(lscore)
            # MyNextion.send_command(f't1.txt="{lscore}"')
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

                teams= soup.find_all('span', "heading_teams__ljLuQ")
                # teams=soup.select('span[data-testid="team-name"]')
                tm=""
                for team in teams:
                    # print(team['data-testid'])
                    # print("teamname"+team)
                    tmm=team.select_one("."+"heading_teams__ljLuQ")
                    tm+=team.get_text()
                    # tm=tm.replace("vs ","\nvs\n")
                    # tm=team.select_one("."+"team_team-name__0U_gn")
                hteam=tm[:tm.index("vs")].strip()
                ateam=tm[tm.index("vs")+2:].strip()

                MyNextion.send_command(f't1.txt="{hteam}"')
                MyNextion.send_command(f't5.txt="{ateam}"')
                print(f"home: {hteam} away: {ateam}")
                # print(f"team : {tm} ")
                minutes= soup.find_all('span', "match-period_period___hImu")
                mnt="X"
                # if minutes:
                for minute in minutes:
                    # print(mincute)
                    mnt=minute.select_one("."+"match-period_period___hImu")
                try : 
                    mnt=minute.get_text()
                except:
                    mnt="FT"
                if len(mnt)>3:
                    # mnt=mnt[:3]
                    mnt=mnt.replace(" ", "")
                    if "90" in mnt:
                        if "+" in mnt:
                            np=int(mnt[mnt.index("+")+1:len(mnt)-1])
                            mnt=str(90+np)
                        # mnt=mnt.replace("90", "9")
                        # mnt=mnt.replace("'", "")
                        # mnt=mnt.replace("+", "")

                MyNextion.send_command(f't3.txt="{mnt}"')
                # else:
                scores= soup.find_all('span',classname)
                for score in scores:
                # print(score)
                    scr=score.select_one("."+classname)
                # serialdisplay(score.get_text())
                hscore=score.get_text()[:2]
                hscore=hscore.replace(" ", "")
                ascore=score.get_text()[3:]
                ascore=ascore.replace(" ", "")
                MyNextion.send_command(f't2.txt="{hscore}"')
                MyNextion.send_command(f't4.txt="{ascore}"')
                print(f"home: {hscore} away: {ascore}")
                print(tm+ "\n " + mnt+" > "+score.get_text())
                lscore=tm+ "\n " + mnt+" > "+score.get_text()
                if score.get_text()!= mscore:
                    print ("============new score")
                    sblink=1
                    mscore=score.get_text()
                if tm==mteam:
                    if sblink==1:
                        interuptDisplay("blink16")
                        sblink=0
                mteam=tm

                # interuptDisplay(lscore)
                # MyNextion.send_command(f't1.txt="{lscore}"')
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
    ],**settings)

def loaddata():
    global urll
    try:
        with open(DATAFILE_, "r") as f:
            data = json.load(f)
            urll = data.get("url", urll)
    except FileNotFoundError:
        pass

loaddata()

if __name__ == "__main__":
    # global urll

    MyNextion.set_port('/dev/ttyUSB0')
    MyNextion.send_command("page page1")
    MyNextion.send_command("page 3")
    MyNextion.send_command('dim=10')#sukses
    MyNextion.send_command('t0.xcen=0')#0left, 1=center, 2=right
    MyNextion.send_command("t1.isbr=True")
    MyNextion.send_command('t0.txt="live score"')
    MyNextion.send_command('t2.xcen=1')
    MyNextion.send_command('t4.xcen=1')
    url_to_scrape = urll  # Replace with the target website
    scraper = Scraper(url_to_scrape)

    app = make_app()
    app.listen(8890)

    # Start periodic scraping task
    tornado.ioloop.IOLoop.current().spawn_callback(periodic_scraping, scraper)

    print("Starting Tornado server on http://localhost:8890")
    tornado.ioloop.IOLoop.current().start()
