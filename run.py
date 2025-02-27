import email_sender
import scraper
from datetime import datetime

def main():
    current_time = datetime.now()
    print (current_time)
    
    """ Gather data """
    jobs = scraper.gather_data()

    month = current_time.strftime("%b")
    day = current_time.strftime("%d")
    hour = current_time.strftime("%I")
    am_pm = current_time.strftime("%p")

    if not jobs:
        email_sender.send_email(f"No New Jobs: {month} {day} at {hour} {am_pm}", "<p>No new jobs posted as of now</p>")
    else:
        body_arr = [jobs[index].getHTML(index + 1) for index in range(0, len(jobs))]
        body = "".join(body_arr)

        """ Send Email With Data """
        email_sender.send_email(f"New Jobs: {month} {day} at {hour} {am_pm}", body)


if __name__ == "__main__":
    main()




