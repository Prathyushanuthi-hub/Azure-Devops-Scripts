class Repository:
    def __init__(self, name, size, url, description):
        self.name = name
        self.size = size
        self.url = url
        self.description = description

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members

class Organization:
    def __init__(self, name, repositories, teams):
        self.name = name
        self.repositories = repositories
        self.teams = teams