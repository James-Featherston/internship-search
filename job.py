
class Job:
    def __init__(self, company, role, location, link, date) -> None:
        self.company = company
        self.role = role
        self.location = location
        self.link = link
        self.date = date

    def getHTML(self, index):
        return f'<h3>{index}. {self.role} at {self.company}</h3><p>Location: {self.location}</p><p>Date Posted: {self.date}</p><p>Apply here: <a href="{self.link}" target="_blank" style="text-decoration: underline; color: blue;">Click Me</a></p>'
    
    def getJSON(self):
        return {"company": self.company, "role": self.role, "location": self.location, "link": self.link, "date": self.date}
    
    def getCompany(self):
        return self.company
    
    def getRole(self):
        return self.role
    
    def getLocation(self):
        return self.location
    
    def getLink(self):
        return self.link
    
    def getDate(self):
        return self.date
    
    def __str__(self) -> str:
        return f"Company: {self.company}\nRole: {self.role}\nLocation: {self.location}\nLink: {self.link}\nDate: {self.date}"
    
    def __eq__(self, __value: object) -> bool:
        return self.link == __value.getLink()
