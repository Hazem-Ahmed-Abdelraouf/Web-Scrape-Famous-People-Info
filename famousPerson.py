class FamousPerson:
    def __init__(self, name, nationality, profession, birthdate, quote):
        self.name = name
        self.nationality = nationality
        self.profession = profession
        self.birthdate = birthdate
        self.quote = quote
    def __str__(self):
        return f'\n\nName: {self.name}\n\
Nationality: {self.nationality}\n\
Profession: {self.profession}\n\
Birthdate: {self.birthdate}\n\
First quote: {self.quote}'

    def get_name(self):
        return self.name