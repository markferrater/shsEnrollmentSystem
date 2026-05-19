class Artist:
    __name = []

    def addArtist(self, name):
        self.__name.append(name)

    def viewArtist(self):
        print(self.__name[:-3])


p = Artist()
p.addArtist('Leonil')
p.addArtist('Hannah')
p.addArtist('Michelle')
p.addArtist('Kent')
p.addArtist('Renz')
p.addArtist('Oscar')

p.viewArtist()