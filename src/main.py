from imdb import Cinemagoer

def main():
    # create an instance of the Cinemagoer class
    ia = Cinemagoer()

    top = ia.get_top250_movies()
    print(top[0])
    print(top[0].keys())
    #first = ia.get_movie_parents_guide("1640718")
    #print(first)

#def filterIMDB(movie):


if __name__== "__main__":
  main()