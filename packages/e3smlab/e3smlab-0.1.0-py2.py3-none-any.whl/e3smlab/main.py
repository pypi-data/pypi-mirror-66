from microapp import Project

class E3SMlab(Project):
    _name_ = "e3smlab"
    _version_ = "0.1.0"
    _description_ = "E3SM Analysis Utilities"
    _long_description_ = "Tools for Analysis of E3SM project"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/e3smlab"

    def __init__(self):
        self.add_argument("--test", help="test argument")
