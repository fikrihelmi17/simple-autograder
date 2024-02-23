class Checklist:
    def __init__(self, status=False, comment=""):
        self.status = status
        self.comment = comment

class Checklists:
    def __init__(self):
        self.packageJsonExists = Checklist()
        self.mainJsExists = Checklist()
        self.mainJsHaveStudentIdComment = Checklist()
        self.rootShowingHtml = Checklist()
        self.serveInPort5000 = Checklist()
        self.htmlContainH1ElementWithStudentId = Checklist()