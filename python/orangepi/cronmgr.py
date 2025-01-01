import tornado.ioloop
import tornado.web
from crontab import CronTab

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cron = CronTab(user=True)
        jobs = [str(job) for job in cron]
        self.render("cronmgr.html", jobs=jobs)

class AddJobHandler(tornado.web.RequestHandler):
    def post(self):
        command = self.get_argument("command")
        schedule = self.get_argument("schedule")

        cron = CronTab(user=True)
        job = cron.new(command=command)

        # Parse the schedule (e.g., "*/5 * * * *" for every 5 minutes)
        job.setall(schedule)
        cron.write()

        self.redirect("/")

class DeleteJobHandler(tornado.web.RequestHandler):
    def post(self):
        job_id = self.get_argument("job_id")

        cron = CronTab(user=True)
        cron.remove(job_id)
        cron.write()

        self.redirect("/")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/add", AddJobHandler),
        (r"/delete", DeleteJobHandler),
    ], template_path="templates")

if __name__ == "__main__":
    app = make_app()
    app.listen(8881)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
