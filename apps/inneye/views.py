#### Required ####
from builtins import Exception
import json
import pytz
import sys
import requests
from datetime import datetime,timedelta


#### Thread ####
from threading import *
from time import *


#### Django ####
from django.conf import settings
from django import template
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect


#### Rest Framework ####
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


#### Model ####
from .models import movieInformation


#### Error Code ####
from .APIStatus import *


#### AES ENCRYPTION ####
# from .AES256 import Cipher_AES


# #### CERTIFICATE ENCRYPTION ####
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
# from base64 import b64decode
# from Cryptodome.Cipher import PKCS1_OAEP
# from Cryptodome.Hash import SHA256, SHA1
# from Cryptodome.Signature import pss


#### VALIDATIONS ####
from .ValidatorRex import ValidationClass


#### Loggers ####
import logging
logger=logging.getLogger('dashboardLogs')


#### ldap ####
from core.settings import API_KEY



#### LDAP CONNECTION ESTABLISHED SECTION START ####
# if LDAP_STATUS:

#     logger.info(ldapSuccess.get('message'))

# else:

#     logger.info(ldapError.get('message'))
#     logger.error(LDAP_ERR)
#### LDAP CONNECTION ESTABLISHED SECTION END ####



# #### SESSION KEY EXPIRE SECTION START ####
# class sessionKeyExpire(Thread):

#     def run(self):

#         try:
#             while True:

#                 sessionKeyDB = sessionKey.objects.filter(modifiedOn__lte = ((datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))- timedelta(days=1)))
#                 sessionKeyDB.delete()
#                 sleep(3600)

#         except Exception as err:
#             logger.error(err)
        
# """Uncomment Section if you want to Delete 24 hour old Session Key""" 
# if 'runserver' in sys.argv:
#     try:

#         threadObj = sessionKeyExpire()
#         threadObj.start()

#     except Exception as err:
#         pass
# #### SESSION KEY EXPIRE SECTION END ####



# #### AES ENCRYPTION DECRYPTION SECTION START ####
# def encryptionRex(sessionKey, encryptData):
#     return(Cipher_AES(sessionKey, "fedcba9876543210").encrypt(encryptData, "MODE_CBC", "PKCS5Padding", "base64"))

# def decryptionRex(sessionKey, decryptData):
#     return(Cipher_AES(sessionKey, "fedcba9876543210").decrypt(decryptData, "MODE_CBC", "PKCS5Padding", "base64"))
# #### AES ENCRYPTION DECRYPTION SECTION END ####



# #### CRT DECRYPTION SECTION START ####
# def decryptCrtRex(dataEncrypt):

#     privateKey= (open('certificates/apc_prvt_rsakey.pem', 'rb').read())
#     obj_private = RSA.importKey(privateKey)
#     decode_cipher = b64decode(dataEncrypt)

#     cipher = PKCS1_OAEP.new(key=obj_private, hashAlgo=SHA256, mgfunc=lambda x,y: pss.MGF1(x,y, SHA1))
#     ciphertext = cipher.decrypt(decode_cipher)

#     return(ciphertext.decode('utf-8'))
# #### CRT DECRYPTION SECTION END ####



# #### SERVER FIND SECTION START ####
# def serverFinder(macAddress):
#     roomConfigDB  = roomConfig.objects.values()

#     for item in roomConfigDB:

#         list_convert = json.loads(item.get('config').replace("'", '"'))
#         find_mac = (list(filter(lambda mc_addr: mc_addr['macAddress'] == macAddress, list_convert)))

#         if len(find_mac)!=0:

#             return item.get('macAddress')

#     return None
# #### SERVER FIND SECTION END ####




#### Dashboard setContent Section Start ####
def setContent(request, query):
    
    try:
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&api_key={API_KEY}"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        
        movieName = response.get('results')[0].get('original_title')
        genreId = response.get('results')[0].get('genre_ids')
        movieType = ' | '.join(movieTypeDB[str(item)] for item in response.get('results')[0].get('genre_ids'))
        movieId = response.get('results')[0].get('id')
        overview = response.get('results')[0].get('overview')
        releaseDate = response.get('results')[0].get('release_date')
        language = response.get('results')[0].get('original_language')
        popularity = response.get('results')[0].get('popularity')
        voteAverage = response.get('results')[0].get('vote_average')
        voteCount = response.get('results')[0].get('vote_count')
        downloadPoster = "".join(["https://image.tmdb.org/t/p/w500", response.get('results')[0].get('poster_path')])
        downloadBackdrop = "".join(["https://image.tmdb.org/t/p/original", response.get('results')[0].get('backdrop_path')])
        
        r = requests.get(downloadPoster)
        with open(f"/home/guest/Desktop/server/popcorntv/apps/static/images/Poster/{response.get('results')[0].get('poster_path')}",'wb') as f:
            f.write(r.content)
        posterPath = f"/static/images/Poster/{response.get('results')[0].get('poster_path')}"
        
        r = requests.get(downloadBackdrop) 
        with open(f"/home/guest/Desktop/server/popcorntv/apps/static/images/Backdrop/{response.get('results')[0].get('backdrop_path')}",'wb') as f:
            f.write(r.content)
        backdropPath = f"/static/images/Backdrop/{response.get('results')[0].get('backdrop_path')}"
        
        try:
            if movieInformation.objects.filter(Q(movieId = movieId) | Q(movieName = movieName)).exists():
                
                try:
                    ### Update ###
                    movieInformationDB = movieInformation.objects.filter(Q(movieId = movieId) | Q(movieName = movieName))
                    modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                    movieInformationDB.update(
                                            movieName = movieName,
                                            genreId = genreId,
                                            movieType = movieType,
                                            movieId = movieId,
                                            overview = overview,
                                            releaseDate = releaseDate,
                                            language = language,
                                            popularity = popularity,
                                            voteAverage = voteAverage,
                                            voteCount = voteCount,
                                            posterPath = posterPath,
                                            backdropPath = backdropPath,
                                            watchCount = None,
                                            watchTime = None,
                                            teaser = None,
                                            movieURL = None,
                                            favourite = None,
                                            user = request.user,
                                            modifiedOn = modifiedOn,
                                        )
                    
                except Exception as err:
                    print(err)

            else:
                try:
                    ### Save ###
                    movieInformationDB = movieInformation()
                    movieInformationDB.movieName = movieName
                    movieInformationDB.genreId = genreId
                    movieInformationDB.movieType = movieType
                    movieInformationDB.movieId = movieId
                    movieInformationDB.overview = overview
                    movieInformationDB.releaseDate = releaseDate
                    movieInformationDB.language = language
                    movieInformationDB.popularity = popularity
                    movieInformationDB.voteAverage = voteAverage
                    movieInformationDB.voteCount = voteCount
                    movieInformationDB.posterPath = posterPath
                    movieInformationDB.backdropPath = backdropPath
                    movieInformationDB.watchCount = None,
                    movieInformationDB.watchTime = None,
                    movieInformationDB.teaser = None,
                    movieInformationDB.movieURL = None,
                    movieInformationDB.favourite = None,
                    movieInformationDB.user = request.user
                    movieInformationDB.uploadedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                    movieInformationDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                    movieInformationDB.save()
                    print("save")

                except Exception as err:
                    print(err)

        except Exception as err:
            print(err)
        
    except Exception as err:
        print(err)
    
#### Dashboard setContent Section End ####


#### Dashboard Home Section Start ####
@login_required(login_url="/login/")
def inneyeHome(request):
    context = dict()
    movieData = dict()

    try:
        # l1 = ['20 Century Girl', 'The Godfather', 'The Shawshank Redemption', 'The Godfather Part II', '???????????????', "Schindler's List", '????????????????????? ??????????????????????????? ?????? ?????????????????????', 'Cosas imposibles', '????????????????????????', '12 Angry Men', '?????????', '???????????????', '?????????', 'The Green Mile', 'The Dark Knight', "Gabriel's Inferno: Part II", "Gabriel's Inferno", '??? ??? ????????????: ??? ??????', 'Pulp Fiction', 'Il buono, il brutto, il cattivo', 'Forrest Gump', 'The Lord of the Rings: The Return of the King', 'GoodFellas', "Gabriel's Inferno: Part III", 'Nuovo Cinema Paradiso', 'La vita ?? bella', '????????????', '??????', 'Psycho', 'Once Upon a Time in America', '???????????????', "One Flew Over the Cuckoo's Nest", 'Fight Club', 'Primal: Tales of Savagery', 'O Auto da Compadecida', '??????', 'Cidade de Deus', 'Spider-Man: Into the Spider-Verse', '???????????????', '?????? ?????????', '?????????????????????', 'The Empire Strikes Back', '?????? ???????????? ??? ??????', 'The Lord of the Rings: The Fellowship of the Ring', '?????????????????????????????????????????? Air???????????????????????????', '???????????????????????????', 'Interstellar', 'The Pianist', 'Sunset Boulevard', '??????????????????????????????????????????:||', 'Whiplash', 'The Lord of the Rings: The Two Towers', '?????? II: ????????????', 'American History X', 'Rear Window', 'The Shop Around the Corner', '?????????', 'Inception', 'Se7en', 'The Great Dictator', 'Dedicada A Mi Ex', '???????????????', '?????? ?????????', 'City Lights', '????????? ????????????????????????????????????????????????', 'Top Gun: Maverick', 'Wolfwalkers', 'The Silence of the Lambs', '???????????????', 'L??on: The Professional', '??????????????????????????????????????????', 'Modern Times', 'Dead Poets Society', 'Clouds', '?????? ?? ????????????', 'Five Feet Apart', "C'era una volta il West", 'Life in a Year', 'Purple Hearts', 'Back to the Future', 'Hamilton', '????????? ???????????? 0', 'Paths of Glory', 'Le Trou', 'Justice League Dark: Apokolips War', 'PERFECT BLUE', 'Apocalypse Now', 'Avengers: Endgame', '7. Ko??u??taki Mucize', '?????????????????????????????????????????????????????????', "C'eravamo tanto amati", 'Steven Universe: The Movie', '?????????', '???????????????????????????', '????????????', 'Mommy', 'Intouchables', "La leggenda del pianista sull'oceano", 'Avengers: Infinity War', "It's a Wonderful Life", '?????????', '????????????-?????? ???', 'The Lion King', 'The Art of Racing in the Rain', 'Klaus', '????????????', 'Persona', '????????????????????????????????????????????????', '?????? ???????????????????????????????????????????????????', 'Il sorpasso', '????????????????????????????????? THE MOVIE ?????????????????????????????????', '????????????', 'Green Book', 'Bo Burnham: Inside', "Zack Snyder's Justice League", 'Ladri di biciclette', '?????????????????????????????????', 'Miraculous World : New York, les h??ros unis', 'Doctor Who: The Day of the Doctor', '???????????????????????????', 'The Apartment', 'Coco', '??????????????', '???????????????????????????????????????????????? ?????? - ??????????????????????????? -', 'Witness for the Prosecution', 'The Shining', 'A Clockwork Orange', '8??', 'S??t??ntang??', 'Det sjunde inseglet', "Mortal Kombat Legends: Scorpion's Revenge", 'The Kid', 'Inglourious Basterds', 'Vertigo', 'Star Wars', 'The Hate U Give', 'Indagine su un cittadino al di sopra di ogni sospetto', 'Les Enfants du Paradis', 'Gladiator', 'Saving Private Ryan', 'The Prestige', 'The Usual Suspects', 'The Help', 'Portrait de la jeune fille en feu', '????????????????????????', 'Memento', 'The Matrix', 'Hacksaw Ridge', 'Shutter Island', 'Call Me by Your Name', 'Minha M??e ?? uma Pe??a 3: O Filme', 'Piper', '????????????????', 'Abraham Lincoln Vampire Hunter: The Great Calamity', 'Soul', '????????????', 'Joker', 'Taxi Driver', 'Metropolis', 'Black Beauty', 'Wonder', "Singin' in the Rain", 'Amici miei', 'Casablanca', 'Far from the Tree', 'Scener ur ett ??ktenskap', 'Scarface', 'The Departed', 'All About Eve', 'Como ca??do del cielo', 'La grande guerra', 'Me contro Te: Il film - La vendetta del Signor S', 'Django Unchained', 'La dolce vita', 'Togo', 'The Father', '?????????', 'Lock, Stock and Two Smoking Barrels', 'Full Metal Jacket', '?????????', 'Central do Brasil', 'Reservoir Dogs', 'Good Will Hunting', 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 'My Policeman', 'Alien', 'Double Indemnity', 'Sherlock Jr.', 'Ayla', 'Smultronst??llet', 'Some Like It Hot', 'I soliti ignoti', '???????????? ????????????', 'Bo Burnham: Make Happy', 'Nobody', 'Scooby-Doo! and Kiss: Rock and Roll Mystery', 'The Truman Show', 'Everything Everywhere All at Once', 'Contratiempo', 'Anne of Green Gables', '?????????????????????', "Michael Jackson's Thriller", 'Harry Potter and the Deathly Hallows: Part 2', 'How to Train Your Dragon: Homecoming', 'Cruella', 'I corti', 'Paris, Texas', 'M - Eine Stadt sucht einen M??rder', 'Ka????ttan Hayatlar', '????????????', 'En brazos de un asesino', 'Eternal Sunshine of the Spotless Mind', 'Hannah Gadsby: Nanette', '????????????-?????? ???', 'Tot??, Peppino e la... malafemmina', '?????????', 'Jagten', 'Voces inocentes', 'There Will Be Blood', 'Three Billboards Outside Ebbing, Missouri', 'Pride & Prejudice', '?????????? ??????????', '?????????', '???????????? ?????????????????????', 'Lion', 'Incendies', 'Les Quatre Cents Coups', 'Una giornata particolare', 'Terminator 2: Judgment Day', "La passion de Jeanne d'Arc", 'La Haine', 'Das Boot', '2001: A Space Odyssey', 'Bound by Honor', 'Rocco e i suoi fratelli', 'The Elephant Man', '???????????????', 'Jojo Rabbit', 'Love, Simon', '?????????????????????', 'WALL??E', 'Prisoners', 'Hidden Figures', 'La meglio giovent??', '???', 'Prayers for Bobby', 'Palmer', 'Tropa de Elite', '????????? ??????', 'The Grand Budapest Hotel', 'Believe Me: The Abduction of Lisa McVey', 'Sulla mia pelle', 'Loving Vincent', 'Misfit #EresOTeHaces', 'El mesero', 'Kitbull', 'Gifted', 'The Red Shoes', 'Doctor Who: The Time of the Doctor', 'Room', 'Veintea??era, Divorciada y Fant??stica', 'Achtste Groepers Huilen Niet', 'Judgment at Nuremberg', 'Le notti di Cabiria', '??????????????', 'Das Leben der Anderen', '????????????', 'In a Heartbeat', 'My Name Is Khan', '????????????', 'The Circus', 'Per qualche dollaro in pi??', 'Requiem for a Dream', 'Miseria e nobilt??', 'Where Hands Touch', 'Que Horas Ela Volta?', 'To Kill a Mockingbird', 'American Beauty', "Ron's Gone Wrong", 'The Wolf of Wall Street', 'The Gold Rush', 'Bingo: O Rei das Manh??s', 'The Thing', 'Amadeus', 'Le Salaire de la peur', 'Song of the Sea', '??????', 'The Sting', 'Spider-Man: No Way Home', 'Dial M for Murder', 'Citizen Kane', 'Straight Outta Nowhere: Scooby-Doo! Meets Courage the Cowardly Dog', 'Wish Dragon', 'Finch', '??????????????????', "A Dog's Journey", 'Harry Potter and the Prisoner of Azkaban', 'The Treasure of the Sierra Madre', 'The General', 'Los olvidados', 'No Manches Frida 2', '??????????', '????????????', '??????????????????', 'The Imitation Game', 'The Deer Hunter', 'Sing 2', 'Bohemian Rhapsody', 'CODA', '???????? ???????????????????? ???????????? ??????????????????', 'H??stsonaten', 'Casino', '????????? ???', 'Scooby-Doo! Camp Scare', 'Roma citt?? aperta', '????????????????????????', 'Ford v Ferrari', 'Paperman', "Hachi: A Dog's Tale", '?????????? ??????????????', 'Gran Torino', 'Pink Floyd: The Wall', '?????????????????????', 'Barry Lyndon', 'Gone with the Wind', 'Thirteen Lives', 'On the Waterfront', 'North by Northwest', '????????? ????????????', '???????????? ??????????????? ??????', 'El secreto de sus ojos', '????????????', 'One Week', 'Hoje Eu Quero Voltar Sozinho', '??????????????????', 'El ??ngel exterminador', '?????? ?????????', 'Batman: The Dark Knight Returns, Part 2', 'The Mitchells vs. the Machines', 'Raging Bull', 'All My Life', '????????????', "Un condamn?? ?? mort s'est ??chapp??", 'Lawrence of Arabia', '1917', '????????????????????????', '7????????? ??????', 'The Third Man', '?????????????????????????????????', 'Rope', 'Viskningar och rop', '????????????', 'Trainspotting', 'Kill Bill: Vol. 1', '3 Idiots', '???????????????????????? ????????????????????????', 'R??mi sans famille', '????????????????????????', 'Toy Story', 'La strada', 'Dem Horizont so nah', '?????????????????????', 'Das Cabinet des Dr. Caligari', 'Million Dollar Baby', 'Tre uomini e una gamba', '????????????????????????', '?????????', 'Before Sunrise', 'Girl in the Basement', 'Scooby-Doo! and the Curse of the 13th Ghost', 'Words on Bathroom Walls', 'Flipped', 'Raya and the Last Dragon', 'Catch Me If You Can', 'Trois couleurs : Rouge', '12 Years a Slave', '???????????????? ?????? ?? ???????????? ?????????????????????? ????????????', '????????????', 'Le Voyage dans la Lune', '????????????????????????????????????', '??????????????????', 'Kill Bill: The Whole Bloody Affair', "Divorzio all'italiana", "L'Arm??e des ombres", 'La notte', "It's Such a Beautiful Day", 'Tel chi el tel??n', 'Up', 'The Great Escape', 'Limelight', '??????\u200c?????? ??????????', 'Il postino', 'La Grande Vadrouille', 'The Sixth Sense', 'What Ever Happened to Baby Jane?', 'Teen Titans Go! vs. Teen Titans', 'Un rescate de huevitos', 'Dallas Buyers Club', 'GHOST IN THE SHELL', 'Mr. Smith Goes to Washington']
        # l2 = ['No Country for Old Men', 'Unforgiven', 'Est??mago', 'Blade Runner', 'Babam??n Keman??', 'The Greatest Showman', 'Inside Out', 'Braveheart', '????????????????????????', 'Captain Fantastic', 'Amarcord', 'Young Frankenstein', 'La Jet??e', 'Luck', 'Freedom Writers', 'Jurassic Park', 'The Boy Who Harnessed the Wind', '??????', 'The Tomorrow War', 'Just Mercy', 'Mulan', 'La ciociara', 'La battaglia di Algeri', 'Raiders of the Lost Ark', 'Primos', '??????????????????', 'The Iron Giant', 'Faust ??? Eine deutsche Volkssage', 'Rebecca', 'Charm City Kings', 'Chinatown', 'The Cameraman', 'The Cure', "Harry Potter and the Philosopher's Stone", 'The Breadwinner', '????????? ????????????', 'Luca', 'Little Women', 'Justice League: The Flashpoint Paradox', 'Aliens', 'In the Name of the Father', 'Vincent', 'To Be or Not to Be', 'Persepolis', '?????????????????????', 'A Vida Invis??vel', 'Guardians of the Galaxy', '?????????? ???????? ???? ??????????', 'About Time', 'Ace in the Hole', 'Novecento', '????????????????????????????????? THE MOVIE ???2???????????????', '????????\u200c?? ???????? ????????????', 'The Night of the Hunter', 'Mamma Roma', 'The Pursuit of Happyness', "Le Fabuleux Destin d'Am??lie Poulain", 'V for Vendetta', 'Sing Street', 'La classe operaia va in paradiso', 'Inner Workings', 'Me Before You', 'Return of the Jedi', '?????????????? ??????????????', 'Roman Holiday', 'Heat', 'Hustle', 'Hors Normes', '?????? ?????????', 'Gone Girl', 'Werckmeister harm??ni??k', 'Safety Last!', 'Miraculous World: Shanghai, la l??gende de Ladydragon', 'Dancer in the Dark', 'Sherlock: The Abominable Bride', 'Nattvardsg??sterna', 'Sunrise: A Song of Two Humans', 'Cindy La Regia', 'La La Land', '?????????????????????????????????', 'A Street Cat Named Bob', '????????????????????', 'The Notebook', 'Per un pugno di dollari', 'Nosotros los nobles', 'Titanic', 'It Happened One Night', 'Kill Bill: Vol. 2', 'Us Again', 'Au revoir l??-haut', 'Paper Moon', 'Les Diaboliques', 'Umberto D.', 'Perfetti sconosciuti', 'Fargo', 'Ah?? te encargo', '????????????', 'The Theory of Everything', 'Rio Bravo', '????????????????????????????????? ??????', 'Whiplash', '???????????????', 'La Nuit am??ricaine', 'Du rififi chez les hommes', '??????????????', 'Stand by Me', 'Her', 'La luna', 'Le Samoura??', 'Prey', 'Isle of Dogs', 'Letter from an Unknown Woman', 'Scooby-Doo! and the Samurai Sword', 'Network', 'Le Sommet des dieux', '???????????????????????????????????? ????????????', 'Un sac de billes', 'Ordet', 'Dances with Wolves', 'Minha Vida em Marte', '?????????????????? ??????????????????', 'Anatomy of a Murder', 'Knives Out', '?????????????????????????? ????????', 'Scooby-Doo! and the Goblin King', 'The Black Phone', 'Monsieur Verdoux', 'The Boy in the Striped Pyjamas', 'A Beautiful Mind', '????????????', 'Z', 'Skyggen i mit ??je', 'Il marchese del Grillo', 'We Bare Bears: The Movie', 'Polisse', '????????????', '??????????????????????????????????????????', 'Feast', 'Mary and Max', 'The Grapes of Wrath', 'Dune', 'Mulholland Dr.', '???????????????', 'My Little Pony: A New Generation', 'Non essere cattivo', '??????????????????', 'Ben-Hur', 'The Big Lebowski', 'Relatos salvajes', 'Death Note: ???????????????', 'Louis C.K.: Hilarious', 'Warrior', 'Mr. Nobody', '??????', 'Papillon', 'Tropa de Elite 2', 'The Nightmare Before Christmas', '?????????????????? JSA', 'The Last: Naruto the Movie', 'Im Westen nichts Neues', 'Mulholland Drive', 'La migliore offerta', 'Les Tontons flingueurs', 'La Grande Illusion', 'No Manches Frida', 'Love, Rosie', 'Der Untergang', 'The Greatest Beer Run Ever', 'Indiana Jones and the Last Crusade', 'El robo del siglo', 'Hiroshima mon amour', 'The Best Years of Our Lives', '??? ?????? ?????? ?????? ????????? ???', 'The Normal Heart', '????????? ??????????????? ????????? ?????????', 'Partly Cloudy', 'Finding Nemo', 'Monsters, Inc.', 'Regular Show: The Movie', 'World of Tomorrow', 'S??som i en spegel', "Carlito's Way", 'Vivre sa vie: film en douze tableaux', 'Gone Mom: The Disappearance of Jennifer Dulos', 'K??rkarlen', 'The Miracle Worker', '?????????', 'The Bridge on the River Kwai', 'Freaks', 'Before Sunset', 'El Infierno', 'Fantozzi', 'Under sandet', 'Harry Potter and the Goblet of Fire', "L'eclisse", 'Spotlight', 'Daft Punk & Leiji Matsumoto - Interstella 5555 - The 5tory of the 5ecret 5tar 5ystem', 'Dog Day Afternoon', "Rosemary's Baby", 'Logan', 'Der Himmel ??ber Berlin', 'Into the Wild', 'Mortal Kombat Legends: Battle of the Realms', 'Gifted Hands: The Ben Carson Story', 'Coraline', '?????????', 'Ma vie de courgette', 'Brokeback Mountain', 'Ricos de Amor', 'Descendants 3', '?????????????????????', '???????????????', '??? ?????? ?????? ?????????', 'Monty Python and the Holy Grail', 'Back to the Outback', '??????', 'Midnight Sun', '??????', 'Fail Safe', 'Constantine: City of Demons - The Movie', 'The Ox-Bow Incident', 'How to Train Your Dragon', 'War Room', 'A Woman Under the Influence', "Who's Afraid of Virginia Woolf?", '?????????????????? ????????? The Final', 'Kr??tki film o mi??o??ci', 'Mishima: A Life in Four Chapters', 'Fanny och Alexander', 'Jungfruk??llan', 'Snatch', 'King Richard', 'Toy Story 3', 'Dogville', 'The King of Comedy', '????????? ?????????', 'Der letzte Mann', 'Donnie Darko', 'Notorious', '????????????', 'Werk ohne Autor', 'Batman: Under the Red Hood', 'Presto', 'Ratatouille', 'Elvis', '????????????', 'Ernest et C??lestine', 'Manhattan', 'An??nima', 'I cento passi', 'Profondo rosso', 'Mustang', 'Straight Outta Compton', 'Lisbela e o Prisioneiro', '?????????', '?????????', 'The Man Who Shot Liberty Valance', 'Jeux interdits', 'L.A. Confidential', 'Holding the Man', '?????????????????????', 'Inherit the Wind', 'Touch of Evil', 'Pirates of the Caribbean: The Curse of the Black Pearl', 'Mauvaises herbes', 'A Bronx Tale', "Matrimonio all'italiana", 'Shelter', 'PlayTime', '????????? ??????????????? ???????????????????????????', "God's Own Country", 'Short Term 12', '??????????????????', 'Do the Right Thing', 'Annie Hall', 'Harry Potter and the Deathly Hallows: Part 1', 'Rocky', 'The Perks of Being a Wallflower', 'Non ci resta che piangere', 'Selena', 'All Quiet on the Western Front', 'The Dark Knight Rises', 'Fantastic Mr. Fox', 'Red Shoes and the Seven Dwarfs', 'Bacurau', 'How to Train Your Dragon: The Hidden World', 'Meshes of the Afternoon', 'The Color Purple', '????????????', 'Tod@s Caen', 'Big Fish', 'Guerra de Likes', '?????????????????? ????????? ??????????????????', 'Tres metros sobre el cielo', 'The Untouchables', 'The Kissing Booth 2', 'Scooby-Doo! Abracadabra-Doo', 'Teen Titans: Trouble in Tokyo', 'The Breakfast Club', 'A Matter of Life and Death', 'Le D??ner de cons', 'The Maltese Falcon', 'Life of Brian', 'Divines', 'Amour', 'If Anything Happens I Love You', 'Onward', 'Marriage Story', 'Brief Encounter', '?????????', '???????????????????????????', 'Doctor Who: Last Christmas', 'K-12', 'Batman: The Dark Knight Returns, Part 1', 'A torin??i l??', 'Ya no estoy aqu??', 'tick, tick... BOOM!', 'Awakenings', 'Rain Man', '????????? ??????', 'Temple Grandin', '?????????????????????', 'Trollhunters: Rise of the Titans', '??????', 'Nueve reinas', 'El esp??ritu de la colmena', 'Misery', 'Die Hard', 'The Blues Brothers', 'Cool Hand Luke', 'Minha M??e ?? uma Pe??a: O Filme', 'The Searchers', 'El laberinto del fauno', 'Platoon', 'Sound of Metal', 'Barbie in the 12 Dancing Princesses', 'A Walk to Remember', 'Le Roi et l???oiseau', 'Pride', '??????????????????', 'Back to the Future Part II', '???????????????', 'Big Hero 6', 'Mystic River', 'Enola Holmes 2', 'Zootopia', '??????', 'Maudie', 'Scent of a Woman', 'I, Daniel Blake', 'The Trial of the Chicago 7', 'Demain tout commence', 'Gi?? la testa', 'Festen', '??????', 'The Hustler', "They Shoot Horses, Don't They?", 'Stalag 17', '????????? ???????????????????????????????????? -?????????????????????????????????-', 'Fiddler on the Roof', '120 battements par minute', 'The Ten Commandments', 'Eu N??o Quero Voltar Sozinho', "The King's Speech", 'The Straight Story', 'Persian Lessons', 'The Hateful Eight', 'Cl??o de 5 ?? 7', 'Angst essen Seele auf', 'Beauty and the Beast', 'The Valet', 'Amici miei - Atto II??', 'Slumdog Millionaire', '?????????????????? ????????? The Beginning', 'The Bad Guys', 'Accattone', 'Day & Night', 'Godzilla vs. Kong', 'Crush', 'Philadelphia', '?????????', '?????????????????????', 'Nosferatu, eine Symphonie des Grauens', 'Padre no hay m??s que uno', 'Il traditore', 'Harry Potter and the Chamber of Secrets', 'Ma nuit chez Maud', 'The Exorcist', 'Magnolia', "Geri's Game", 'John Mulaney: The Comeback Kid', 'The Wrong Trousers', '??????????????????\u3000??????????????????', "The Children's Hour", 'Ricky Gervais: Humanity', '????????????', 'Azur et Asmar', 'Edward Scissorhands', 'Le Grand M??chant Renard et autres contes...', 'The Batman']
        # l3 = ['The Broken Circle Breakdown', 'Dom za ve??anje', 'Les Choristes', '???????????? ????????????', 'Hotel Rwanda', 'The Avengers', 'The Sound of Music', 'A Charlie Brown Christmas', 'Le ballon rouge', 'Strangers on a Train', 'Rush', 'Shrek', 'Wrath of Man', '??????', 'Druk', '????????????????', 'Harvey', 'Le locataire', 'Charade', 'Harry Potter and the Half-Blood Prince', 'Overcomer', 'Dave Chappelle: The Age of Spin', 'Il gattopardo', 'Cat on a Hot Tin Roof', 'The Big Heat', 'Don Camillo', 'The Incredibles', 'Stagecoach', 'En corps', 'Una Pel??cula de Huevos', '????????????', "Breakfast at Tiffany's", 'All the Bright Places', 'Hunt for the Wilderpeople', 'Les demoiselles de Rochefort', "All the President's Men", 'Out of the Past', 'Bo??e Cia??o', 'Mildred Pierce', 'Batman Begins', '????????????', 'Spirit: Stallion of the Cimarron', 'Harry Potter and the Order of the Phoenix', 'Z-O-M-B-I-E-S 2', 'Moonrise Kingdom', 'High Noon', 'Nightcrawler', 'In the Heat of the Night', 'Systemsprenger', 'Jongens', '????????????', 'Il conformista', 'Hair Love', 'Sleuth', 'A Streetcar Named Desire', 'Brazil', 'Il Divo', 'Crna ma??ka, beli ma??or', 'El abrazo de la serpiente', 'La Plan??te sauvage', 'Sweet Smell of Success', '?????????', 'The Warriors', 'The Killing', 'Feel the Beat', '??????????????????????????? ????????????', 'The Bridges of Madison County', 'Scooby-Doo on Zombie Island', 'Fried Green Tomatoes', 'The Gentlemen', 'K???? Uykusu', 'Captain America: The Winter Soldier', "L'armata Brancaleone", 'Riget', 'Eddie Murphy: Delirious', 'Trois couleurs : Bleu', 'Freier Fall', 'Laurence Anyways', "What's Eating Gilbert Grape", 'I vitelloni', '?????????????????????', "To All the Boys I've Loved Before", 'Spies in Disguise', 'Steamboat Bill, Jr.', 'Victoria', 'Memoirs of a Geisha', 'La odisea de los giles', 'No se Aceptan Devoluciones', 'How to Train Your Dragon 2', '??Qu?? culpa tiene el ni??o?', '???', 'The Martian', '12 Angry Men', 'Todo sobre mi madre', 'Roma', 'Mandariinid', 'Jean de Florette', 'The Big Sleep', 'To All the Boys: Always and Forever', 'Offret', 'Mississippi Burning', 'Viridiana', 'The Princess Bride', 'Little Miss Sunshine', 'The Blind Side', 'Encanto', 'La gabbianella e il gatto', 'The Last Picture Show', 'The Philadelphia Story', 'Threads', '???????????????????????????', 'Germania anno zero', 'Breakthrough', 'Chiedimi se sono felice', 'The Lost Weekend', '??????????????????????????????????????????', 'Le Clan des Siciliens', 'Where the Crawdads Sing', '?????????????????? -????????????-', 'Kind Hearts and Coronets', 'Kubo and the Two Strings', 'Black Swan', 'The Graduate', 'Scarlet Street', 'Cast Away', 'HANA-BI', 'Les Mis??rables', 'Atonement', 'Laura', 'Alice in den St??dten', 'The Wild Bunch', 'Minha M??e ?? uma Pe??a 2: O Filme', 'Synecdoche, New York', 'Shang-Chi and the Legend of the Ten Rings', 'Stand and Deliver', 'White Heat', 'Angels with Dirty Faces', '????????? ????????? ???????????? ??????', 'Triangle of Sadness', 'Ricomincio da tre', 'Harold and Maude', 'Work It', '??????????????? THE DARK SIDE OF DIMENSIONS', 'The Ultimate Gift', 'The Big Country', 'Jaws', 'Scooby-Doo! Pirates Ahoy!', 'Who Am I - Kein System ist sicher', 'Primal Fear', 'The Count of Monte Cristo', 'Fitzcarraldo', 'Planet of the Apes', 'Aladdin', 'I Still Believe', "Mickey's Christmas Carol", 'Jules et Jim', 'Sonic the Hedgehog 2', 'Amar te duele', 'Blue Velvet', 'Kingsman: The Secret Service', 'Dave Chappelle: Sticks & Stones', 'BORUTO -NARUTO THE MOVIE-', 'La R??gle du jeu', '?? stata la mano di Dio', '???????????????????? ??????????', "Ferris Bueller's Day Off", 'The Witcher: Nightmare of the Wolf', '????????????????????????????????????', 'Boogie Nights', "Ascenseur pour l'??chafaud", "Guess Who's Coming to Dinner", '???????????????????? ????????????????', 'Black Narcissus', 'Pais??', '?????????????????? ???????????????', 'The Raid 2: Berandal', 'JFK', 'The Terminator', 'The Irishman', '??????????????? ???????????????III ??????', 'The Man from Earth', '??????????????? ????????? ?????? ~overture~', 'October Sky', 'Iron Man', 'Guardians of the Galaxy Vol. 2', 'Mediterraneo', 'King Kong', 'Free Guy', '????????????????????????????????? THE MOVIE ???????????? ??????????????? ???????????????', '?????? ????????????', 'Lilja 4-Ever', 'Night of the Living Dead', 'Le Loup et le Lion', 'Forever My Girl', 'Being There', 'Quo Vadis, Aida?', 'Papicha', 'Au hasard Balthazar', "Knockin' on Heaven's Door", '??????', 'Les Yeux sans visage', '?? bout de souffle', 'Z-O-M-B-I-E-S 3', 'The Danish Girl', "I Can't Think Straight", 'The Last Emperor', 'Butch Cassidy and the Sundance Kid', 'Ready Player One', 'The Others', 'Le Cercle rouge', 'Giant', 'Arsenic and Old Lace', 'Amores perros', 'The Suicide Squad', 'The Ghost and Mrs. Muir', '????????????', 'Get a Horse!', '?????????????????????', "The World's Fastest Indian", 'La monta??a sagrada', 'The Manchurian Candidate', 'Get Out', 'Baisers cach??s', 'Searching', 'Plein soleil', 'Le Fant??me de la libert??', 'The Dirty Dozen', '????????????????????????????????????', 'A Little Princess', 'Anastasia', 'Maurice', 'The Little Prince', 'Ieri, oggi, domani', "Le conseguenze dell'amore", 'Changeling', 'The Sea Beast', 'The Fall', 'Tombstone', 'Seven Pounds', 'Thor: Ragnarok', 'The Fault in Our Stars', 'East of Eden', 'Children of Men', 'Turma da M??nica: La??os', 'Deadpool', 'The Longest Ride', 'Love and Death', 'Remember the Titans', "L'avventura", '?????????', 'Lost Highway', 'Volevo nascondermi', 'Twelve Monkeys', '????????????', 'Hable con ella', 'Edge of Tomorrow', '????????????', 'Groundhog Day', '??????????????????', 'Moulin Rouge!', 'Bao', "A Dog's Purpose", 'Sleepers', '????????? STEINS;GATE ???????????????????????????', '?????? ??????????', 'Rebel Without a Cause', 'Verdens verste menneske', '????????????', 'Lo chiamavano Trinit??...', 'I Origins', 'Brutti, sporchi e cattivi', 'Manon des sources', 'Billy Elliot', 'Un proph??te', 'Fatherhood', 'En man som heter Ove', '???????????????', 'In a Lonely Place', 'T??i o??????ky pro Popelku', 'La Rafle', 'The Longest Day', 'Tell It to the Bees', 'The Servant', 'Tangled', 'Bande ?? part', '????????????', 'Boyz n the Hood', 'Little Big Man', 'Blue Miracle', 'Lou', 'Toy Story 2', 'The Wizard of Oz', 'Road to Ninja: Naruto the Movie', 'Kr??tki film o zabijaniu', 'One, Two, Three', 'The Bride of Frankenstein', 'American Gangster', "The Man Who Wasn't There", 'Bianca', 'My Fair Lady', 'Gilda', '2 Hearts', 'Le Chant du loup', 'What We Do in the Shadows', 'Moon', 'BURN??E', 'Le scaphandre et le papillon', 'Imagine Me & You', 'Dogman', 'The Call of the Wild', 'Arrival', 'Beasts of No Nation', 'Still Life', 'The Snowman', 'Secrets & Lies', 'Shottas', 'Halloween', 'The Banker', 'Cani arrabbiati', 'The Hobbit: The Desolation of Smaug', 'Running on Empty', 'The Curious Case of Benjamin Button', 'Bringing Up Baby', 'The Conjuring: The Devil Made Me Do It', 'Detachment', 'My Dinner with Andre', 'Kramer vs. Kramer', 'Moana', 'Ex Machina', 'Drive', 'Undisputed III: Redemption', 'My Man Godfrey', 'The Odd Couple', 'Mar adentro', 'Instant Family', 'Sin nombre', 'In Cold Blood', 'Ghostbusters: Afterlife', "Jusqu'?? la garde", 'Hotel Mumbai', '??????????????????', 'Mad Max: Fury Road', 'Splendor in the Grass', 'I Am Sam', 'Badlands', 'Mary Poppins', 'The SpongeBob Movie: Sponge on the Run', 'The Blue Umbrella', 'Fireproof', 'Edmond', 'Me and Earl and the Dying Girl', '???????????????', 'Campeones', '??????????????? HIGHSCHOOL OF THE DEAD ?????????????????????????????????????????????', 'Where Eagles Dare', 'A Quiet Place Part II', '?????????????????????:??? ???????????????????????????', 'Good Bye Lenin!', '???', 'We Need to Talk About Kevin', 'The Last Samurai', 'Captain Phillips', 'Thelma & Louise', 'Evil Dead II', 'Injustice', '????????? ??????????????? ?????????????????????', 'El cuerpo', 'Sling Blade', 'The Conversation', 'Batman: The Long Halloween, Part One', 'Chill Out, Scooby-Doo!', '?????????', 'The Game', '??????????????????????????????', 'Spartacus', '????????? ?????????', 'The Thin Man', 'Night on Earth', 'The Legend of Sleepy Hollow', 'Shadow of a Doubt', "The Emperor's New Groove", '10 Things I Hate About You', 'Girl, Interrupted', 'Novembre', 'PAW Patrol: Mighty Pups', 'Nous trois ou rien', 'Toy Story 4', '????????', 'Hannah and Her Sisters', 'Gattaca', 'Mysterious Skin', 'Midnight Express', 'Ninotchka', 'The Croods: A New Age', 'Veloce come il vento', 'The Favourite', '???', 'Justice Society: World War II', 'My Left Foot: The Story of Christy Brown', 'True Romance']
        # l4 = ['Hot Fuzz', 'Control', 'La Double Vie de V??ronique', 'The French Connection', 'The Magnificent Seven', '?????????????????????', 'Mr. Deeds Goes to Town', 'Escape from Alcatraz', 'Waking Life', 'Serpico', 'Beautiful Boy', 'Sabrina', 'Mein Blind Date mit dem Leben', '?????????????????????', 'Aguirre, der Zorn Gottes', 'The Butterfly Effect', 'Seul contre tous', 'Hocus Pocus 2', 'Doctor Zhivago', 'BlacKkKlansman', 'The Book of Henry', 'Le Charme discret de la bourgeoisie', '?????????????????????Z?????????????????????!!????????????????????????????????????????????????', 'Menace II Society', 'Treasure Planet', '4 luni, 3 s??pt??m??ni ??i 2 zile', 'Profumo di donna', 'Apocalypto', 'Gandhi', 'Key Largo', 'The Conjuring', 'Midnight in Paris', 'Shaun of the Dead', 'Un chien andalou', 'Cinderella Man', 'Dark Waters', 'Manchester by the Sea', 'Minions: The Rise of Gru', '???????????????!', 'Courageous', 'The Asphalt Jungle', '????????? ??????', 'Abominable', 'Avatar', '??????????????????????', 'The Invisible Man', 'Donnie Brasco', 'Coach Carter', 'Batman: The Long Halloween, Part Two', 'Padre no hay m??s que uno 2: la llegada de la suegra', '??????', 'La piel que habito', 'Empire of the Sun', 'The Lighthouse', 'La grande bellezza', "L'Atalante", 'Una pura formalit??', 'L??t den r??tte komma in', "L'Homme de Rio", 'The Book of Life', '??????????????? ???????????? ?????????', 'X-Men: Days of Future Past', 'Suspiria', 'A Close Shave', '??????diary', 'Il secondo tragico Fantozzi', 'Tystnaden', 'Medianeras', 'Gladiator', 'Gaslight', 'Frankenstein', 'The Day the Earth Stood Still', 'The Two Popes', '????????', 'To Sir, with Love', 'M??n som hatar kvinnor', 'Babam ve O??lum', 'The Machinist', 'Malcolm X', "J'ai perdu mon corps", 'Blood Diamond', 'Le quai des brumes', 'Casino Royale', 'Midnight Cowboy', 'The Fifth Element', 'Blade Runner 2049', 'Somewhere in Time', 'The Birds', '???????????????????????? ?????? ?????????????????? ??????????????????', 'The Goonies', '??????', 'Turning Red', 'Black Panther: Wakanda Forever', 'The Dirt', "J'ai tu?? ma m??re", 'Gun Crazy', '??????????????? ????????????????????????', 'Batman: Mask of the Phantasm', 'The Wrestler', 'The Day of the Jackal', 'The Revenant', 'Der siebente Kontinent', 'Bullet Train', 'I, Tonya', 'Days of Heaven', "Sullivan's Travels", 'Kes', 'I Can Only Imagine', 'Stargirl', 'The Unforgivable', '????????????????????', '????????? ?????????????????? ?????????', 'Le Corbeau', 'The Killing Fields', 'Paul, Apostle of Christ', 'A Star Is Born', 'Boyhood', 'Le avventure di Pinocchio', 'The Outlaw Josey Wales', 'The Lady Vanishes', 'Phantom of the Paradise', 'Le Proc??s', 'Who Framed Roger Rabbit', 'The Man Who Knew Too Much', '?????????', 'Crimes and Misdemeanors', 'Zodiac', 'Birdman of Alcatraz', 'The Death of Superman', "You Can't Take It with You", 'E.T. the Extra-Terrestrial', 'Ed Wood', 'The Rocky Horror Picture Show', 'Hercules', 'Corpse Bride', 'Big Time Adolescence', 'Then Came You', 'La Cit?? de la peur', 'The Boss Baby: Family Business', 'The Last Full Measure', 'Fury', 'Die Welle', "L'Ann??e derni??re ?? Marienbad", 'How to Steal a Million', 'The Man Who Would Be King', 'Facing the Giants', '???????????? ??????????????', 'A Few Good Men', 'Upgrade', 'La tortue rouge', 'Incredibles 2', 'Lilo & Stitch', 'The Sandlot', 'Rescued by Ruby', 'Das wei??e Band - Eine deutsche Kindergeschichte', 'Play It Again, Sam', 'Patton', 'Happiness', 'Ciao Alberto', 'Imitation of Life', 'Barbie as The Princess & the Pauper', 'This Is England', 'Bonnie and Clyde', 'The Last Duel', 'Prison Break: The Final Break', 'Desert Flower', 'The Crow', 'A Grand Day Out', 'Vivir dos veces', 'Promising Young Woman', '????????????', 'Invasion of the Body Snatchers', 'Repulsion', 'Still Alice', '?????????????????????D ?????????????????????', 'Il grande silenzio', 'Dirty Harry', "L'Insulte", 'Zwartboek', 'Carandiru', 'Dawn of the Dead', 'Deadpool 2', 'La Folie des grandeurs', '???????????? ??????', 'After Hours', 'Before Midnight', "Travolti da un insolito destino nell'azzurro mare d'agosto", '?????????', "Miller's Crossing", 'Walk the Line', 'Burrow', 'Mr & Mme Adelman', 'Hedwig and the Angry Inch', 'The Hating Game', 'The Train', 'Father Stu', 'Ballon', '????????????', 'Jungle Cruise', 'The Royal Tenenbaums', 'Breaking the Waves', 'Aquarius', 'The Incredible Shrinking Man', "No Man's Land", 'The Long Goodbye', 'Au revoir les enfants', '?????????', 'Predator', 'La Belle et la B??te', 'Sauver ou p??rir', 'For the Birds', '??????????????????', 'Almost Famous', 'Lucky Number Slevin', 'Zimna wojna', 'The Book Thief', 'La maschera del demonio', 'Les Chatouilles', 'A Perfect World', 'Trouble in Paradise', 'Carol', "Bir Zamanlar Anadolu'da", 'The Devils', 'Love & Basketball', 'Illusions perdues', 'Spider-Man: Far from Home', 'The Shack', 'Rogue One: A Star Wars Story', 'Il capitale umano', '3096 Tage', '???????????????', 'Il vangelo secondo Matteo', 'Justice League: War', 'A Night at the Opera', 'Spoorloos', 'Willy Wonka & the Chocolate Factory', '????????????', 'Marty', 'Glory', 'DC League of Super-Pets', 'Cos?? ?? la vita', 'This Is Spinal Tap', 'mid90s', 'Paddington 2', 'The Best of Me', 'Le Premier Jour du reste de ta vie', 'Kung Fury', 'The Guernsey Literary & Potato Peel Pie Society', '????????? ?????? ???', 'The Last Letter from Your Lover', "I'm Not Ashamed", 'Zelig', 'Eyes Wide Shut', 'The Name of the Rose', 'Cape Fear', 'Volver', 'Birdman or (The Unexpected Virtue of Ignorance)', 'Hamlet', 'Tutto quello che vuoi', 'Patients', '??????????????????', 'The Adventures of Robin Hood', 'Cet obscur objet du d??sir', 'Irma la Douce', 'Peeping Tom', 'My Cousin Vinny', '18 regali', 'Star Trek II: The Wrath of Khan', '?????????????????????Z ????????????????????????????????????????????????????????????Z?????? ??????????????????', 'Johnny Got His Gun', "It's the Great Pumpkin, Charlie Brown", '????????????', '??Y c??mo es ??l?', 'Pupille', 'To Have and Have Not', 'Ghostbusters', 'Barton Fink', 'South Park: Post COVID: The Return of COVID', 'Vargtimmen', 'Training Day', 'A trav??s de mi ventana', 'The Mauritanian', 'Dunkirk', 'Ordinary People', '????????????', 'In Bruges', 'The Magdalene Sisters', 'Letters from Iwo Jima', 'Scarface', '????????????', 'The Insider', 'Durante la tormenta', 'Peaceful Warrior', 'How the Grinch Stole Christmas!', 'First Blood', 'Adams ??bler', 'Le Grand Bleu', 'Miss Sloane', '?????? ?????? ?????? ??????', 'Abre los ojos', 'Trois couleurs : Blanc', 'Baby Driver', 'Sonatine', 'La M??me', 'BAC Nord', 'Miss You Already', 'Mind Game', 'The Secret of NIMH', 'Spellbound', 'The Woman in the Window', '...continuavano a chiamarlo Trinit??', 'C.R.A.Z.Y.', 'Back to the Future Part III', 'Scott Pilgrim vs. the World', 'Nocturnal Animals', 'The Age of Adaline', 'Shane', 'Lifted', 'My Darling Clementine', 'Richard Jewell', '?????????', 'Pierrot le fou', '??????2', 'Johnny Guitar', '????????????????????????????????? ????????? DEATH & REBIRTH ????????????', 'The Secret Life of Bees', 'An Affair to Remember', 'Sense and Sensibility', "Boys Don't Cry", 'The One and Only Ivan', 'Vivo', '??????????????? ???????????? ???????????????????????????', 'Chemical Hearts', 'No Time to Die', 'Celda 211', 'The Farewell', 'Lo chiamavano Jeeg Robot', '...altrimenti ci arrabbiamo!', 'The Fugitive', 'All That Jazz', '?????? JIN-ROH', 'The Fallout', 'PAW Patrol: The Movie', 'The Thin Red Line', 'The Bourne Identity', 'Monster Pets: A Hotel Transylvania Short', 'Superman II: The Richard Donner Cut', 'Eraserhead', 'Lemonade Mouth', '???????????????????????????', 'The Taking of Pelham One Two Three', 'Doctor Strange in the Multiverse of Madness', 'Breathe', 'Unbroken', '??????????????? ???????????????II ?????????????????????', 'Il deserto rosso', 'The Lion in Winter', 'Frida', 'Uncle Frank', 'Fabrizio De Andr??: Principe libero', '????????????????', 'Smetto quando voglio', 'True Grit', 'Man on Fire', 'Ray', "L'??cole buissonni??re", 'Predestination', 'The Right Stuff', "Bram Stoker's Dracula", 'Tudo Bem no Natal Que Vem', 'Maggie Simpson in Playdate with Destiny', 'Nebraska', 'The Artist', "Scooby-Doo! in Where's My Mummy?", "The Devil's Advocate", 'Jeder f??r sich und Gott gegen alle', 'The Reader', 'Last Night in Soho', 'Once Upon a Time??? in Hollywood', 'Teen Titans: The Judas Contract', 'Captain America: Civil War', '?????????????????????', 'The Hurricane', '????????????', 'American Sniper', 'La pazza gioia', 'Glory Road', '?????????-???????????????', 'Apollo 13', 'Sin City', 'Cherry', 'John Wick: Chapter 3 - Parabellum', 'Star Trek', 'Chaplin', 'The Last King of Scotland', 'Dolor y gloria', 'Miracles from Heaven', 'Sala samob??jc??w', '????????????????????????', '???????????????????????????']
        # l5 = ['Donne-moi des ailes', "You're Not You", 'N??co z Alenky', '?????????????????????Z ???????????????????????????!! ?????????????????????', 'Rushmore', 'Doctor Strange', 'Barbie: Princess Charm School', '???????????? ??????\u200e\u200e', 'The Innocents', '??????????????? 2.0', 'A Boy Called Christmas', 'The Secret of Kells', 'Men of Honor', 'Mies vailla menneisyytt??', 'Smetto quando voglio - Ad honorem', 'Wind River', 'Tesis', '??????', 'Lone Survivor', 'The Life of David Gale', 'Les Parapluies de Cherbourg', 'Clerks', "A Hard Day's Night", 'Gegen die Wand', '??????: ?????????', '100 metros', 'Honig im Kopf', 'On the Basis of Sex', 'Bo??te noire', 'The Hunger Games: Catching Fire', 'Spirit Untamed', 'The Verdict', 'High Plains Drifter', 'Cabaret', 'Diarios de motocicleta', 'The Godfather Part III', 'Frantz', 'Scooby-Doo and the Ghoul School', 'La Belle ??poque', "A Dog's Life", 'Enter the Dragon', 'The Passion of the Christ', 'Pretty Woman', 'El Dorado', 'The Station Agent', 'Greyhound', 'Selma', 'Serbuan maut', 'A Place in the Sun', 'Les Amants du Pont-Neuf', "Ocean's Eleven", 'Status Update', 'Being John Malkovich', 'The Good Lie', 'Blow-Up', 'Belle de jour', 'Waves', 'El ??ngel', '?????????', '?????????????? ????????????', 'Y tu mam?? tambi??n', 'When Harry Met Sally...', '??????', 'The Florida Project', 'The Lego Movie', 'His Girl Friday', 'Das Experiment', 'Le P??re No??l est une ordure', 'Oslo, 31. august', 'Caro Diario', 'Contact', 'Dog', 'The In Between', 'Ecce Bombo', 'Queen', 'District 9', 'The Bourne Ultimatum', 'Mudbound', 'McFarland, USA', 'Joyeux No??l', 'Erin Brockovich', '?????????? ???? ??????????????????????', 'The Man in the Moon', 'Vampyr - Der Traum des Allan Grey', '??????????????????????????????', 'Minari', 'La noche de 12 a??os', 'Okja', 'Ostwind', 'Submarine', 'Naked', 'Les H??ritiers', 'The Purple Rose of Cairo', 'As Good as It Gets', 'The Piano', 'Inside Man', 'American Satan', 'Dieses bescheuerte Herz', '?????????', '????????????', 'Legends of the Fall', 'Red River', 'Scooby-Doo! WrestleMania Mystery', 'Non si sevizia un paperino', '?????????', 'Mal??na', 'Duel', 'Braindead', 'Grease', 'Moonlight', 'Justice League: Doom', 'O Homem Que Copiava', 'Tarzan', 'Nos jours heureux', '???????????? ?????????', 'Smetto quando voglio - Masterclass', 'Mission: Impossible - Fallout', 'One Day', 'Once', 'Lazzaro felice', '?????????', 'Frances Ha', 'Une Femme est une femme', 'A Quiet Place', 'Pickup on South Street', 'Withnail & I', 'Glengarry Glen Ross', 'Black Widow', 'Le Corniaud', 'Mad Max 2', 'August Rush', 'First They Killed My Father', 'The Mission', 'The Peanut Butter Falcon', 'Palmeras en la nieve', 'Sedmikr??sky', "Sophie's Choice", 'The Secret Garden', 'Black Panther', 'Adaptation.', 'La mala educaci??n', 'The Best of Enemies', 'Creed', 'Sorcerer', 'Fantasia', 'Once Were Warriors', 'Moxie', 'Trolls World Tour', 'The Last of the Mohicans', 'Enemy at the Gates', 'Life of Pi', 'E??k??ya', "Kelly's Heroes", 'Star Wars: Episode III - Revenge of the Sith', '????????????', 'Zulu', "Jacob's Ladder", 'The Hunt for Red October', 'Mon oncle', 'The 39 Steps', '??t?? 85', 'Blindspotting', "La Promesse de l'aube", 'Enter the Void', 'La Gloire de mon P??re', 'The Lady from Shanghai', 'Judas and the Black Messiah', 'Oscar', 'American Psycho', 'Saw', 'The Simpsons: The Good, the Bart, and the Loki', 'The Great Gatsby', 'The Basketball Diaries', 'Home Alone', 'Lost in Translation', 'Lifeboat', '??????????????? THE FIRST', 'Descendants 2', 'Pel??: Birth of a Legend', 'Stuck in Love', "Sei donne per l'assassino", 'The Killers', 'Nosferatu - Phantom der Nacht', '???????????? ????????????', '??????', "Les 12 travaux d'Ast??rix", 'Beetlejuice', 'Duck Soup', 'Les Aventures de Rabbi Jacob', 'Serenity', 'Le P??re No??l est une ordure', 'Barbie and the Diamond Castle', 'The Time Machine', 'The Remains of the Day', 'The Devil Wears Prada', 'Sicario', 'John Wick', 'Boy', 'Taken', 'Mujeres al borde de un ataque de nervios', 'An American Werewolf in London', 'The Woman King', 'Land and Freedom', 'Lolita', 'If I Stay', 'En kongelig aff??re', 'Shine', 'The Omen', 'Interview with the Vampire', 'Sissi', 'The Fighter', 'Little Lord Fauntleroy', "Scooby-Doo! and the Witch's Ghost", 'Office Space', 'Happiest Season', "The Zookeeper's Wife", "Futurama: Bender's Big Score", 'Love and Monsters', 'Run', '??????????????????', 'Le violon rouge', 'Jeremiah Johnson', 'Fruitvale Station', 'Top Hat', 'Sonic the Hedgehog', "L'Instinct de mort", 'Scooby-Doo! and the Reluctant Werewolf', 'Seconds', 'Miracle on 34th Street', 'The Cook, the Thief, His Wife & Her Lover', 'Teen Titans Go! To the Movies', 'Philomena', 'Blow', 'Batman: Assault on Arkham', 'EverAfter', 'Road to Perdition', 'Now Is Good', 'The Fly', 'The Wind That Shakes the Barley', 'Close Encounters of the Third Kind', 'Sorry We Missed You', 'All That Heaven Allows', 'Secretariat', 'Scooby-Doo! and the Loch Ness Monster', 'Dazed and Confused', 'Eastern Promises', '25th Hour', 'Only the Brave', 'Les Triplettes de Belleville', 'Dead Man Walking', 'Scream', 'The Impossible', 'Bianco, rosso e Verdone', 'Scooby-Doo! and the Cyber Chase', 'Down by Law', '????????????????', 'Steamboat Willie', 'Mutiny on the Bounty', 'A Time to Kill', 'Black Hawk Down', 'Tengo ganas de ti', 'Les Bronz??s font du ski', 'Play', 'Le Cerveau', 'Possession', 'Viaggio in Italia', '??????????????? ???????????????I ????????????', 'Cyrano de Bergerac', 'Spider-Man: Homecoming', "My Sister's Keeper", 'My Girl', 'Johnny Stecchino', 'Martyrs', 'Europa', 'Ast??rix & Ob??lix Mission Cl??op??tre', 'I Kina spiser de hunde', 'Float', 'Southpaw', 'Saving Mr. Banks', '21 Grams', 'To Catch a Thief', 'On a retrouv?? la 7??me compagnie', 'Rise of the Guardians', 'Rudy', 'Mr. Church', '????????????????????? 2: ?????? ????????? ?????????????????????', 'Giulietta degli spiriti', 'Masculin f??minin', 'Freaks Out', 'The Girl with the Dragon Tattoo', 'Falling Down', 'Precious', '????????????', 'Extraction', 'Rocketman', 'Ghostland', 'The Butler', 'Romeo and Juliet', 'Match Point', 'Darkest Hour', 'Perdona si te llamo amor', 'Tucker and Dale vs. Evil', 'MEMORIES', 'Wake in Fright', 'Jackie Brown', 'Fantastic Beasts and Where to Find Them', '????????????????????????', 'The Little Mermaid', 'Bloody Sunday', 'La Pianiste', 'Justice League vs. Teen Titans', 'Remember', 'Full Out', 'Now You See Me', 'The Muppet Christmas Carol', 'Goldfinger', 'The Big Sick', 'STAND BY ME ???????????????', 'The Wicker Man', 'American Me', 'Scrooge', '??????', 'Christopher Robin', '??????', '????????????????????????', 'Z-O-M-B-I-E-S', 'Les Mis??rables', 'Funny Games', 'Morte a Venezia', 'The African Queen', 'Dirty Dancing', 'Anima', 'Papillon', 'Deconstructing Harry', 'Maleficent: Mistress of Evil', 'The Social Network', 'Blood and Bone', 'Bad Day at Black Rock', 'Train de vie', 'Elisa y Marcela', "La mafia uccide solo d'estate", 'Scooby-Doo! and the Monster of Mexico', 'Wait Until Dark', 'Dark City', 'Twin Peaks: Fire Walk with Me', 'Perfume: The Story of a Murderer', 'A Man for All Seasons', 'Good Morning, Vietnam', 'Harriet', 'Febbre da cavallo', 'Boiling Point', 'Dear Basketball', 'From Here to Eternity', 'Giant Little Ones', 'Le fate ignoranti', 'Gentlemen Prefer Blondes', 'Phineas and Ferb: The Movie: Candace Against the Universe', 'A Christmas Carol', 'The Quiet Man', 'Ice Age', 'Woman in Gold', "L'ennemi public n??1", "Winchester '73", 'Persuasion', 'Nashville', 'A Shot in the Dark', 'Suite Fran??aise', 'Star Trek Into Darkness', 'Sommaren med Monika', 'Mine vaganti', 'La prima cosa bella', 'Suddenly, Last Summer', 'Minority Report', '20th Century Women', 'The Secret Scripture', 'Law Abiding Citizen', '???????????????: Stand Alone Complex - Solid State Society', 'La ley del deseo', 'Delicatessen', 'Enola Holmes', 'Un long dimanche de fian??ailles', 'Split', 'The Big Short', 'Walkabout', "Pirates of the Caribbean: Dead Man's Chest", 'Le Nom des gens', '??????5?????????????????????', 'The Party', 'Mia et le lion blanc', 'Ophelia', 'Lava', '???????????????????????????', 'The Meaning of Life', 'The Abyss', 'Heathers', 'La Cit?? des Enfants Perdus', '????????? ??????', 'Blow Out', 'Baisers vol??s', 'The Physician']

        #for item in l3:
        #    setContent(request,item)
        
        # for item in l3:
        #     setContent(request,item)
        
        
        
        context['segment'] = 'inneyeHome'
        
        context['types'] = ["actionCount","adventureCount","animationCount","comedyCount","crimeCount","documentaryCount","dramaCount","familyCount","fantasyCount","historyCount","horrorCount","mysteryCount","romanceCount","sifiCount","thrillerCount","warCount","westernCount"]
        
        context['actionCount'] = movieInformation.objects.filter(movieType__icontains='Action').count()
        context['adventureCount'] = movieInformation.objects.filter(movieType__icontains='Adventure').count()
        context['animationCount'] = movieInformation.objects.filter(movieType__icontains='Animation').count()
        context['comedyCount'] = movieInformation.objects.filter(movieType__icontains='Comedy').count()
        context['crimeCount'] = movieInformation.objects.filter(movieType__icontains='Crime').count()
        context['documentaryCount'] = movieInformation.objects.filter(movieType__icontains='Documentary').count()
        context['dramaCount'] = movieInformation.objects.filter(movieType__icontains='Drama').count()
        context['familyCount'] = movieInformation.objects.filter(movieType__icontains='Family').count()
        context['fantasyCount'] = movieInformation.objects.filter(movieType__icontains='Fantasy').count()
        context['historyCount'] = movieInformation.objects.filter(movieType__icontains='History').count()
        context['horrorCount'] = movieInformation.objects.filter(movieType__icontains='Horror').count()
        context['mysteryCount'] = movieInformation.objects.filter(movieType__icontains='Mystery').count()
        context['romanceCount'] = movieInformation.objects.filter(movieType__icontains='Romance').count()
        context['sifiCount'] = movieInformation.objects.filter(movieType__icontains='Science Fiction').count()
        context['thrillerCount'] = movieInformation.objects.filter(movieType__icontains='Thriller').count()
        context['warCount'] = movieInformation.objects.filter(movieType__icontains='War').count()
        context['westernCount'] = movieInformation.objects.filter(movieType__icontains='Western').count()
        
        context['action'] = movieInformation.objects.filter(movieType__icontains='Action').values()
        context['adventure'] = movieInformation.objects.filter(movieType__icontains='Adventure').values()
        context['animation'] = movieInformation.objects.filter(movieType__icontains='Animation').values()
        context['comedy'] = movieInformation.objects.filter(movieType__icontains='Comedy').values()
        context['crime'] = movieInformation.objects.filter(movieType__icontains='Crime').values()
        context['documentary'] = movieInformation.objects.filter(movieType__icontains='Documentary').values()
        context['drama'] = movieInformation.objects.filter(movieType__icontains='Drama').values()
        context['family'] = movieInformation.objects.filter(movieType__icontains='Family').values()
        context['fantasy'] = movieInformation.objects.filter(movieType__icontains='Fantasy').values()
        context['history'] = movieInformation.objects.filter(movieType__icontains='History').values()
        context['horror'] = movieInformation.objects.filter(movieType__icontains='Horror').values()
        context['mystery'] = movieInformation.objects.filter(movieType__icontains='Mystery').values()
        context['romance'] = movieInformation.objects.filter(movieType__icontains='Romance').values()
        context['sifi'] = movieInformation.objects.filter(movieType__icontains='Science Fiction').values()
        context['thriller'] = movieInformation.objects.filter(movieType__icontains='Thriller').values()
        context['war'] = movieInformation.objects.filter(movieType__icontains='War').values()
        context['western'] = movieInformation.objects.filter(movieType__icontains='Western').values()
        
        
        movieData['action'] = movieInformation.objects.filter(movieType__icontains='Action').values()
        movieData['adventure'] = movieInformation.objects.filter(movieType__icontains='Adventure').values()
        movieData['animation'] = movieInformation.objects.filter(movieType__icontains='Animation').values()
        movieData['comedy'] = movieInformation.objects.filter(movieType__icontains='Comedy').values()
        movieData['crime'] = movieInformation.objects.filter(movieType__icontains='Crime').values()
        movieData['documentary'] = movieInformation.objects.filter(movieType__icontains='Documentary').values()
        movieData['drama'] = movieInformation.objects.filter(movieType__icontains='Drama').values()
        movieData['family'] = movieInformation.objects.filter(movieType__icontains='Family').values()
        movieData['fantasy'] = movieInformation.objects.filter(movieType__icontains='Fantasy').values()
        movieData['history'] = movieInformation.objects.filter(movieType__icontains='History').values()
        movieData['horror'] = movieInformation.objects.filter(movieType__icontains='Horror').values()
        movieData['mystery'] = movieInformation.objects.filter(movieType__icontains='Mystery').values()
        movieData['romance'] = movieInformation.objects.filter(movieType__icontains='Romance').values()
        movieData['sifi'] = movieInformation.objects.filter(movieType__icontains='Science Fiction').values()
        movieData['thriller'] = movieInformation.objects.filter(movieType__icontains='Thriller').values()
        movieData['war'] = movieInformation.objects.filter(movieType__icontains='War').values()
        movieData['western'] = movieInformation.objects.filter(movieType__icontains='Western').values()
        
        context['movieData'] = movieData
        
        context['movieInformationDB'] = movieInformation.objects.filter(movieType__icontains='Action').values()

        html_template = loader.get_template('home/inneye-home.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard home Section End ####



#### Dashboard Movies Section Start ####
@login_required(login_url="/login/")
def inneyeMovies(request):
    context = dict()

    try:

        context['segment'] = 'inneyeMovies'

        html_template = loader.get_template('home/inneye-home.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Movies Section End ####



#### Dashboard Series Section Start ####
@login_required(login_url="/login/")
def inneyeSeries(request):
    context = dict()

    try:

        context['segment'] = 'inneyeSeries'

        html_template = loader.get_template('home/inneye-home.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Series Section End ####



#### Dashboard Categories Section Start ####
@login_required(login_url="/login/")
def inneyeCategories(request, movieType):
    context = dict()

    try:
        movieInformationDB = movieInformation.objects.filter(movieType__icontains=movieType).values()
        context['segment'] = movieType
        context['movieInformationDB'] = movieInformationDB

        html_template = loader.get_template('home/inneye-categories.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Categories Section End ####



#### Dashboard Watch Section Start ####
@login_required(login_url="/login/")
def inneyeWatch(request, movieId):
    context = dict()

    try:

        movieInformationDB = movieInformation.objects.filter(movieId = movieId).values()
        
        context['segment'] = 'inneyeWatch'
        context['movieInformationDB'] = movieInformationDB

        html_template = loader.get_template('home/inneye-watch.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Watch Section End ####



#### Dashboard Watch Section Start ####
@login_required(login_url="/login/")
def inneyeWatchSeries(request):
    context = dict()

    try:
        context['segment'] = 'inneyeWatchSeries'

        html_template = loader.get_template('home/inneye-watch-series.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Watch Section End ####



#### Dashboard Watch Section Start ####
@login_required(login_url="/login/")
def inneyePlay(request, movieId):
    context = dict()

    try:
        playBackMovie = movieInformation.objects.filter(movieId = movieId).values()
        movieInformationDB = movieInformation.objects.filter(movieType__icontains="Action").values()
        context['segment'] = "inneyePlay"
        context['playBackMovie'] = playBackMovie
        context['movieInformationDB'] = movieInformationDB

        html_template = loader.get_template('home/inneye-player.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Watch Section End ####



#### Dashboard pages Section Start ####
@login_required(login_url="/login/")
def pages(request):
    context = dict()

    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-404.html')
        logger.info(templateNotFound.get('message'))
        # logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard pages Section End ####



# #### Dashboard Index Section Start ####
# @login_required(login_url="/login/")
# def index(request):
#     context = dict()

#     try:
#         hotelName = serverRegister.objects.values_list('hotelName')

#         context['segment'] = 'index'
#         context['serverCount'] = serverRegister.objects.filter().count()
#         context['controllerCount'] = DVC.objects.filter().count()
#         context['unknownControllerCount'] = unknownDVC.objects.filter().count()
#         context['dvcList'] = [DVC.objects.filter(hotelName = name).count() for name in [item[0] for item in hotelName]]
#         context['serverList'] = [item[0] for item in hotelName]

#         html_template = loader.get_template('home/index.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Index Section End ####



# #### Dashboard Server Information Section Start ####
# @login_required(login_url="/login/")
# def serverInfo(request):
#     context = dict()

#     try:
#         serverDB = serverRegister.objects.filter().values()
#         context['segment'] = 'server'
#         context['serverDB'] = serverDB
#         html_template = loader.get_template('home/server.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Information Section End ####



# #### Dashboard Server Register Section Start ####
# @login_required(login_url="/login/")
# def serverRegistration(request):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             context['segment'] = 'addServer'

#             if request.method == 'POST':

#                 try:
#                     if serverRegister.objects.filter(Q(macAddress = request.POST.get('macAddress')) | Q(dvsURL = request.POST.get('dvsUrl')) | Q(kongURL=request.POST.get('kongUrl')) | Q(kongFqdn=request.POST.get('kongFqdn'))).exists():
                        
#                         try:
#                             serverDB = serverRegister.objects.filter(Q(macAddress = request.POST.get('macAddress')) | Q(dvsURL = request.POST.get('dvsUrl')) | Q(kongURL=request.POST.get('kongUrl')) | Q(kongFqdn=request.POST.get('kongFqdn')))
                            
#                             hotelName = request.POST.get('hotelName')
#                             dvsURL = request.POST.get('dvsUrl')
#                             dvsLocalIP = request.POST.get('dvsLocalIp')
#                             kongURL = request.POST.get('kongUrl')
#                             kongFqdn = request.POST.get('kongFqdn')
#                             kongLocalIP = request.POST.get('kongLocalIp')
#                             publicIP = request.POST.get('dvsPublicIp').replace(' ', '')
#                             macAddress = request.POST.get('dvsMacAddress')
#                             clientId = request.POST.get('dvcClientId')
#                             clientSecret = request.POST.get('dvcClientSecret')
#                             modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                            
#                             serverDB.update(hotelName=hotelName, dvsURL=dvsURL, dvsLocalIP=dvsLocalIP, kongURL=kongURL, kongFqdn=kongFqdn, kongLocalIP=kongLocalIP, publicIP=publicIP, macAddress=macAddress, clientId=clientId, clientSecret=clientSecret, modifiedOn=modifiedOn)
                            
#                             context['segment'] = 'addServer'
#                             context['status'] = True
#                             context['statusCode'] = serverUpdateStatus.get('statusCode')
#                             context['message'] = ", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')])
#                             context['data'] = None
                            
#                             logger.info(", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')]))
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                         except Exception as err:

#                             context['segment'] = 'addServer'
#                             context['status'] = False
#                             context['statusCode'] = serverDetailRequired.get('statusCode')
#                             context['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                             context['data'] = None

#                             logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                             logger.error(err)
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                     else:

#                         try:

#                             serverDB = serverRegister()
#                             serverDB.hotelName = request.POST.get('hotelName')
#                             serverDB.dvsURL = request.POST.get('dvsUrl')
#                             serverDB.dvsLocalIP = request.POST.get('dvsLocalIp')
#                             serverDB.kongURL = request.POST.get('kongUrl')
#                             serverDB.kongFqdn = request.POST.get('kongFqdn')
#                             serverDB.kongLocalIP = request.POST.get('kongLocalIp')
#                             serverDB.publicIP = request.POST.get('dvsPublicIp').replace(' ', '')
#                             serverDB.macAddress = request.POST.get('dvsMacAddress')
#                             serverDB.clientId = request.POST.get('dvcClientId')
#                             serverDB.clientSecret = request.POST.get('dvcClientSecret')
#                             serverDB.createdOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                             serverDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                             serverDB.save()
                            
#                             context['segment'] = 'addServer'
#                             context['status'] = True
#                             context['statusCode'] = serverRegisterSuccess.get('statusCode')
#                             context['message'] = serverRegisterSuccess.get('message') 
#                             context['data'] = None
                            
#                             logger.info(serverRegisterSuccess.get('message'))
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                         except Exception as err:

#                             context['segment'] = 'addServer'
#                             context['status'] = False
#                             context['statusCode'] = serverDetailRequired.get('statusCode')
#                             context['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                             context['data'] = None
                            
#                             logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                             logger.error(err)
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                 except Exception as err:

#                     context['segment'] = 'addServer'
#                     context['status'] = False
#                     context['statusCode'] = DBError.get('statusCode')
#                     context['message'] = ", ".join([serverRegisterFailure.get('message'), DBError.get('message')])
#                     context['data'] = None
                    
#                     logger.info(", ".join([serverRegisterFailure.get('message'), DBError.get('message')]))
#                     logger.error(err)
#                     html_template = loader.get_template('home/acknowledgement.html')
#                     return HttpResponse(html_template.render(context, request))

#             else:

#                 html_template = loader.get_template('home/addServer.html')
#                 return HttpResponse(html_template.render(context, request))

#         else:
            
#             context['segment'] = 'addServer'
#             context['status'] = False
#             context['statusCode'] = unableServerRegisterStatus.get('statusCode')
#             context['message'] = unableServerRegisterStatus.get('message')
#             context['data'] = None
            
#             logger.info(unableServerRegisterStatus.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Register Section End ####



# #### Dashboard Server Detail Section Start ####
# @login_required(login_url="/login/")
# def serverDetail(request, macAddress):
#     context = dict()

#     try:
#         serverDB = serverRegister.objects.filter(macAddress = macAddress).values()

#         context['segment'] = 'server'
#         context['serverDB'] = serverDB
        
#         html_template = loader.get_template('home/serverDetail.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Detail Section End ####



# #### Dashboard Server Remove Section Start ####
# @login_required(login_url="/login/")
# def serverRemove(request, macAddress):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             try:
#                 serverDB = serverRegister.objects.filter(macAddress = macAddress)
#                 roomConfigDB = roomConfig.objects.filter(macAddress = macAddress)
#                 serverDB.delete()
#                 roomConfigDB.delete()
                
#                 context['segment'] = 'server'
#                 context['status'] = True
#                 context['statusCode'] = serverRemoveStatus.get('statusCode')
#                 context['message'] = serverRemoveStatus.get('message')
#                 context['data'] = None
                
#                 logger.info(serverRemoveStatus.get('message'))
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#             except Exception as err:

#                 context['segment'] = 'server'
#                 context['status'] = False
#                 context['statusCode'] = DBError.get('statusCode')
#                 context['message'] = ", ".join([serverDeleteError.get('message'), DBError.get('message')])
#                 context['data'] = None
                
#                 logger.info(", ".join([serverDeleteError.get('message'), DBError.get('message')]))
#                 logger.error(err)
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#         else:
    
#             context['segment'] = 'server'
#             context['status'] = False
#             context['statusCode'] = unableServerRemoveStatus.get('statusCode')
#             context['message'] = unableServerRemoveStatus.get('message')
#             context['data'] = None
            
#             logger.info(unableServerRemoveStatus.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Remove Section End ####



# #### Dashboard Server Update Section Start ####
# @login_required(login_url="/login/")
# def serverUpdate(request, macAddress):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             if request.method == 'POST':

#                     try:
#                         if serverRegister.objects.filter(macAddress = macAddress).exists():

#                             try:
#                                 serverDB = serverRegister.objects.filter(macAddress = macAddress)
                                
#                                 hotelName = request.POST.get('hotelName')
#                                 dvsURL = request.POST.get('dvsUrl')
#                                 dvsLocalIP = request.POST.get('dvsLocalIp')
#                                 kongURL = request.POST.get('kongUrl')
#                                 kongFqdn = request.POST.get('kongFqdn')
#                                 kongLocalIP = request.POST.get('kongLocalIp')
#                                 publicIP = request.POST.get('dvsPublicIp').replace(' ', '')
#                                 macAddress = request.POST.get('dvsMacAddress')
#                                 clientId = request.POST.get('dvcClientId')
#                                 clientSecret = request.POST.get('dvcClientSecret')
#                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                                
#                                 serverDB.update(hotelName=hotelName, dvsURL=dvsURL, dvsLocalIP=dvsLocalIP, kongURL=kongURL, kongFqdn=kongFqdn, kongLocalIP=kongLocalIP, publicIP=publicIP, macAddress=macAddress, clientId=clientId, clientSecret=clientSecret, modifiedOn=modifiedOn)
                                
#                                 context['segment'] = 'server'
#                                 context['status'] = True
#                                 context['statusCode'] = serverUpdateStatus.get('statusCode')
#                                 context['message'] = ", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')])
#                                 context['data'] = None
                                
#                                 logger.info(", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')]))
#                                 html_template = loader.get_template('home/acknowledgement.html')
#                                 return HttpResponse(html_template.render(context, request))

#                             except Exception as err:

#                                 context['segment'] = 'server'
#                                 context['status'] = False
#                                 context['statusCode'] = serverDetailRequired.get('statusCode')
#                                 context['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                                 context['data'] = None
                                
#                                 logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                                 logger.error(err)
#                                 html_template = loader.get_template('home/acknowledgement.html')
#                                 return HttpResponse(html_template.render(context, request))

#                     except Exception as err:
                        
#                         context['segment'] = 'server'
#                         context['status'] = False
#                         context['statusCode'] = DBError.get('statusCode')
#                         context['message'] = ", ".join([serverRegisterFailure.get('message'), DBError.get('message')])
#                         context['data'] = None
                        
#                         logger.info(", ".join([serverRegisterFailure.get('message'), DBError.get('message')]))
#                         logger.error(err)
#                         html_template = loader.get_template('home/acknowledgement.html')
#                         return HttpResponse(html_template.render(context, request))

#             serverDB = serverRegister.objects.filter(macAddress = macAddress).values()
#             context['segment'] = 'server'
#             context['serverDB'] = serverDB
#             html_template = loader.get_template('home/serverUpdate.html')
#             return HttpResponse(html_template.render(context, request))
        
#         else:
            
#             context['segment'] = 'server'
#             context['status'] = False
#             context['statusCode'] = unableServerUpdateStatus.get('statusCode')
#             context['message'] = unableServerUpdateStatus.get('message')
#             context['data'] = None
            
#             logger.info(unableServerUpdateStatus.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Update Section End ####



# #### Dashboard Room Mac Binding Information Section Start ####
# @login_required(login_url="/login/")
# def configFile(request, macAddress):
#     context = dict()

#     try:
#         roomConfigDB = roomConfig.objects.filter(macAddress = macAddress).values()

#         context['segment'] = 'server'
#         context['roomConfigDB'] = roomConfigDB

#         if roomConfig.objects.filter(macAddress = macAddress).exists():
#             context['config'] = json.loads(roomConfigDB.get()['config'].replace("'", '"'))

#         else:
#             context['log'] = "empty"

#         html_template = loader.get_template('home/configFile.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Room Mac Binding Information Section End ####



# #### Dashboard DVC Information Section Start ####
# @login_required(login_url="/login/")
# def dvcInfo(request, hotelName):
#     context = dict()

#     try:
#         DVCDB = DVC.objects.filter(hotelName = hotelName).values()

#         context['segment'] = 'server'

#         if DVC.objects.filter(hotelName = hotelName).exists():
#             context['DVCDB'] = DVCDB

#         else:
#             context['log'] = "empty"

#         html_template = loader.get_template('home/controller.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard DVC Information Section End ####



# #### Dashboard Unknown DVC Information Section Start ####
# @login_required(login_url="/login/")
# def unknownController(request):
#     context = dict()

#     try:
#         unknownDVCDB = unknownDVC.objects.values()

#         context['segment'] = 'unknownController'

#         if unknownDVC.objects.exists():
#             context['unknownDVCDB'] = unknownDVCDB

#         else:
#             context['log'] = "empty"

#         html_template = loader.get_template('home/unKnownController.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Unknown DVC Information Section End ####



# #### Dashboard Unknown Controller Remove Section Start ####
# @login_required(login_url="/login/")
# def unknownControllerRemove(request, macAddress):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             try:
#                 unknownDVCDB = unknownDVC.objects.filter(macAddress = macAddress)
#                 unknownDVCDB.delete()
                
#                 context['segment'] = 'unknownController'
#                 context['status'] = True
#                 context['statusCode'] = unknownDVCRemove.get('statusCode')
#                 context['message'] = unknownDVCRemove.get('message')
#                 context['data'] = None
                
#                 logger.info(unknownDVCRemove.get('message'))
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#             except Exception as err:

#                 context['segment'] = 'unknownController'
#                 context['status'] = False
#                 context['statusCode'] = DBError.get('statusCode')
#                 context['message'] = ", ".join([unknownDVCError.get('message'), DBError.get('message')])
#                 context['data'] = None
                
#                 logger.info(", ".join([unknownDVCError.get('message'), DBError.get('message')]))
#                 logger.error(err)
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#         else:
            
#             context['segment'] = 'unknownController'
#             context['status'] = False
#             context['statusCode'] = unableUnknownDVCRemove.get('statusCode')
#             context['message'] = unableUnknownDVCRemove.get('message')
#             context['data'] = None
            
#             logger.info(unableUnknownDVCRemove.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))


#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Unknown Controller Remove Section End ####



# #### Dashboard Sys Log Section Start ####
# @login_required(login_url="/login/")
# def sysLog(request):
#     context = dict()

#     try:
#         sysLog = list()
#         with open('logs/info.log') as file:
#             for line in (file.readlines() [-20:]):
#                 sysLog.append(line)
         
#         context['segment'] = 'info'
#         context['sysLog'] = sysLog

#         html_template = loader.get_template('home/sysLog.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Sys Log Section End ####



# #### Dashboard Error Log Section Start ####
# @login_required(login_url="/login/")
# def errorLog(request):
#     context = dict()

#     try:
#         sysLog = list()
#         with open('logs/error.log') as file:
#             for line in (file.readlines() [-20:]):
#                 sysLog.append(line)
         
#         context['segment'] = 'error'
#         context['sysLog'] = sysLog

#         html_template = loader.get_template('home/sysLog.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Error Log Section End ####



# #### Dashboard Debug Log Section Start ####
# @login_required(login_url="/login/")
# def debugLog(request):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             sysLog = list()
#             with open('logs/debug.log') as file:
#                 for line in (file.readlines() [-20:]):
#                     sysLog.append(line)
            
#             context['segment'] = 'debug'
#             context['sysLog'] = sysLog

#             html_template = loader.get_template('home/sysLog.html')
#             return HttpResponse(html_template.render(context, request))
        
#         else:
            
#             context['segment'] = 'index'
#             context['status'] = False
#             context['statusCode'] = unableToAccessLog.get('statusCode')
#             context['message'] = unableToAccessLog.get('message')
#             context['data'] = None
            
#             logger.info(unableToAccessLog.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Debug Log Section End ####



# #### GET ENVIRONMENT SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def getEnvironment(request):

#     if request.method == 'GET':

#         try:
#             if request.headers.get('deviceToken') == None:

#                 res['status'] = False
#                 res['statusCode'] = tokenNotPresent.get('statusCode')
#                 res['message'] = ", ".join([getEnvFailure.get('message'), tokenNotPresent.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([getEnvFailure.get('message'), tokenNotPresent.get('message')]))
#                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:
#                 logger.debug(": ".join([requestGetEnv.get('message'), request.headers.get('deviceToken')]))

#                 if ValidationClass(request.headers.get('deviceToken')).tokenValidator():
#                     logger.debug(" : ".join([tokenSuccess.get('message'), request.headers.get('deviceToken')]))

#                     if request.GET.get("publicIp") is not None:

#                         try:
#                             if ValidationClass(request.GET.get("publicIp")).validIpAddressCheck():
#                                 logger.debug(" : ".join([ipAddressSuccess.get('message'), request.GET.get("publicIp")]))

#                                 try:
#                                     count = 0
#                                     envNames = dict()
#                                     responseData = dict()

#                                     for item in setEnvironment.objects.values_list('publicIP', 'envName'):

#                                         if [c for c in item[0].split(',') if c in request.GET.get("publicIp")]:

#                                             count = count + 1
#                                             envNames[f"NAME{count}"] = item[1]

#                                     if len(envNames) > 0:

#                                         if len(envNames) > 1:

#                                             res['status'] = False
#                                             res['statusCode'] = multipleEnvFound.get('statusCode')
#                                             res['message'] = multipleEnvFound.get('message')
#                                             res['data'] = None

#                                             logger.info(multipleEnvFound.get('message'))
#                                             return Response(res)
                                            
#                                         setEnvironmentData = setEnvironment.objects.filter(envName = envNames['NAME1']).values()

#                                         responseData['fqdn'] = setEnvironmentData.get().get('envFQDN')
#                                         responseData['url'] = f"https://{setEnvironmentData.get().get('envFQDN')}/cloud/api"
#                                         responseData['publicIp'] = request.GET.get("publicIp")
#                                         responseData['localIp'] = setEnvironmentData.get().get('localIP')

#                                         res['status'] = True
#                                         res['statusCode'] = getEnvSuccess.get('statusCode')
#                                         res['message'] = getEnvSuccess.get('message')
#                                         res['data'] = responseData

#                                         logger.info(getEnvSuccess.get('message'))
#                                         logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                         return Response(res)

#                                     responseData['fqdn'] = PROD_FQDN
#                                     responseData['url'] = f"https://{PROD_FQDN}/cloud/api"
#                                     responseData['publicIp'] = request.GET.get("publicIp")
#                                     responseData['localIp'] = None

#                                     res['status'] = True
#                                     res['statusCode'] = defaultEnv.get('statusCode')
#                                     res['message'] = defaultEnv.get('message')
#                                     res['data'] = responseData

#                                     logger.info(defaultEnv.get('message'))
#                                     logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                     return Response(res)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = DBError.get('statusCode')
#                                     res['message'] = ", ".join([getEnvFailure.get('message'), DBError.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([getEnvFailure.get('message'), DBError.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                             else:

#                                 res['status'] = False
#                                 res['statusCode'] = ipAddressInvalid.get('statusCode')
#                                 res['message'] = ", ".join([getEnvFailure.get('message'), ipAddressInvalid.get('message')])
#                                 res['data'] = None

#                                 logger.debug(": ".join([ipAddressInvalid.get('message'), request.GET.get("publicIp")]))
#                                 logger.info(", ".join([getEnvFailure.get('message'), ipAddressInvalid.get('message')]))
#                                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)
                        
#                         except Exception as err:

#                             res['status'] = False
#                             res['statusCode'] = validationError.get('statusCode')
#                             res['message'] = ", ".join([getEnvFailure.get('message'), validationError.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([getEnvFailure.get('message'), validationError.get('message')]))
#                             logger.error(err)
#                             return Response(res)
                    
#                     else:

#                         res['status'] = False
#                         res['statusCode'] = requestQueryParam.get('statusCode')
#                         res['message'] = ", ".join([getEnvFailure.get('message'), requestQueryParam.get('message')])
#                         res['data'] = None
                        
#                         logger.info(", ".join([getEnvFailure.get('message'), requestQueryParam.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:
                    
#                     res['status'] = False
#                     res['statusCode'] = tokenFailure.get('statusCode')
#                     res['message'] = ", ".join([getEnvFailure.get('message'), tokenFailure.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([getEnvFailure.get('message'), tokenFailure.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#         except Exception as err:
            
#             res['status'] = False
#             res['statusCode'] = getEnvFailure.get('statusCode')
#             res['message'] = getEnvFailure.get('message')
#             res['data'] = None
            
#             logger.info(getEnvFailure.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### GET ENVIRONMENT SECTION END ####



# #### PUBLIC KEY SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def getPublicKey(request):

#     if request.method == 'GET':

#         try:
#             if request.headers.get('deviceToken') == None:

#                 res['status'] = False
#                 res['statusCode'] = tokenNotPresent.get('statusCode')
#                 res['message'] = ", ".join([publicKeyFailure.get('message'), tokenNotPresent.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([publicKeyFailure.get('message'), tokenNotPresent.get('message')]))
#                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:
#                 logger.debug(" : ".join([requestPublicKey.get('message'), request.headers.get('deviceToken')]))

#                 if ValidationClass(request.headers.get('deviceToken')).tokenValidator():

#                     logger.debug(" : ".join([tokenSuccess.get('message'), request.headers.get('deviceToken')]))

#                     res['status'] = True
#                     res['statusCode'] = publicKeySuccess.get('statusCode')
#                     res['message'] = publicKeySuccess.get('message')
#                     res['data'] = (open('certificates/apc_publickey_rsakey.pem', 'rb').read()).decode('utf-8').replace("\n", "")

#                     logger.info(publicKeySuccess.get('message'))
#                     logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                     return Response(res)

#                 else:
                    
#                     res['status'] = False
#                     res['statusCode'] = tokenFailure.get('statusCode')
#                     res['message'] = ", ".join([publicKeyFailure.get('message'), tokenFailure.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([publicKeyFailure.get('message'), tokenFailure.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#         except Exception as err:
            
#             res['status'] = False
#             res['statusCode'] = publicKeyFailure.get('statusCode')
#             res['message'] = publicKeyFailure.get('message')
#             res['data'] = None
            
#             logger.info(publicKeyFailure.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### PUBLIC KEY SECTION END ####



# #### SESSION KEY SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def key(request):

#     if request.method == 'POST':

#         try:
#             if request.body != b'':

#                 if request.headers.get('deviceToken') == None:
                    
#                     res['status'] = False
#                     res['statusCode'] = tokenNotPresent.get('statusCode')
#                     res['message'] = ", ".join([sessionKeyFailure.get('message'), tokenNotPresent.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([sessionKeyFailure.get('message'), tokenNotPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:
#                     logger.debug(" : ".join([requestSessionKey.get('message'), request.headers.get('deviceToken')]))

#                     if ValidationClass(request.headers.get('deviceToken')).tokenValidator():

#                         keyInfoJson = json.loads(request.body.decode("utf-8"))

#                         logger.debug(" : ".join([tokenSuccess.get('message'), request.headers.get('deviceToken')]))
#                         logger.debug(" : ".join([requestBodyData.get('message'), str(keyInfoJson)]))

#                         if ValidationClass(keyInfoJson.get('macAddress')).validMacAddress():

#                             logger.debug(" : ".join([macAddressSuccess.get('message'), keyInfoJson.get('macAddress')]))

#                             if sessionKey.objects.filter(macAddress = (keyInfoJson.get('macAddress'))).exists():

#                                 try:
#                                     decryptSessionKey = decryptCrtRex(keyInfoJson.get('sessionKey')).strip()
#                                     logger.debug(sessionKeyDecrypt.get('message')+decryptSessionKey)

#                                     try:
#                                         sessionKeyDB = sessionKey.objects.filter(macAddress = (keyInfoJson.get('macAddress')))
#                                         token = request.headers.get('deviceToken')
#                                         sessionKeyVal = decryptSessionKey
#                                         modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                         sessionKeyDB.update(token=token, sessionKeyVal=sessionKeyVal, modifiedOn=modifiedOn)
                                        
#                                         res['status'] = True
#                                         res['statusCode'] = sessionKeyUpdated.get('statusCode')
#                                         res['message'] = ", ".join([sessionKeySuccess.get('message'), sessionKeyUpdated.get('message')])
#                                         res['data'] = None
                                        
#                                         logger.info(", ".join([sessionKeySuccess.get('message'), sessionKeyUpdated.get('message')]))
#                                         logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                         return Response(res)

#                                     except Exception as err:

#                                         res['status'] = False
#                                         res['statusCode'] = sessionKeyNotUpdated.get('statusCode')
#                                         res['message'] = ", ".join([sessionKeyFailure.get('message'), sessionKeyNotUpdated.get('message')])
#                                         res['data'] = None
                                        
#                                         logger.info(", ".join([sessionKeyFailure.get('message'), sessionKeyNotUpdated.get('message')]))
#                                         logger.error(err)
#                                         return Response(res)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = NotDecrypt.get('statusCode')
#                                     res['message'] = ", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)
#                             else:

#                                 try:
#                                     decryptSessionKey = decryptCrtRex(keyInfoJson.get('sessionKey')).strip()
#                                     logger.debug(sessionKeyDecrypt.get('message')+decryptSessionKey)

#                                     try:
#                                         sessionKeyDB = sessionKey()

#                                         sessionKeyDB.token = request.headers.get('deviceToken')
#                                         sessionKeyDB.sessionKeyVal = decryptSessionKey
#                                         sessionKeyDB.macAddress = keyInfoJson.get('macAddress')
#                                         sessionKeyDB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                         sessionKeyDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                         sessionKeyDB.save()
                                        
#                                         res['status'] = True
#                                         res['statusCode'] = sessionKeySuccess.get('statusCode')
#                                         res['message'] = sessionKeySuccess.get('message')
#                                         res['data'] = None
                                    
#                                         logger.info(sessionKeySuccess.get('message'))
#                                         logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                         return Response(res)

#                                     except Exception as err:

#                                         res['status'] = False
#                                         res['statusCode'] = sessionKeyNotSave.get('statusCode')
#                                         res['message'] = ", ".join([sessionKeyFailure.get('message'), sessionKeyNotSave.get('message')])
#                                         res['data'] = None
                                        
#                                         logger.info(", ".join([sessionKeyFailure.get('message'), sessionKeyNotSave.get('message')]))
#                                         logger.error(err)
#                                         return Response(res)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = NotDecrypt.get('statusCode')
#                                     res['message'] = ", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                         else:

#                             res['status'] = False
#                             res['statusCode'] = macAddressInvalid.get('statusCode')
#                             res['message'] = ", ".join([sessionKeyFailure.get('message'), macAddressInvalid.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([sessionKeyFailure.get('message'), macAddressInvalid.get('message')]))
#                             return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                     else:

#                         res['status'] = False
#                         res['statusCode'] = tokenFailure.get('statusCode')
#                         res['message'] = ", ".join([sessionKeyFailure.get('message'), tokenFailure.get('message')])
#                         res['data'] = None
                        
#                         logger.info(", ".join([sessionKeyFailure.get('message'), tokenFailure.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([sessionKeyFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([sessionKeyFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)
        
#         except Exception as err:

#             res['status'] = False
#             res['statusCode'] = sessionKeyError.get('statusCode')
#             res['message'] = sessionKeyError.get('message')
#             res['data'] = None
            
#             logger.info(sessionKeyError.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### SESSION KEY SECTION END ####



# #### SERVER REGISTER SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def server(request):

#     if request.method == 'POST':

#         try:
#             if request.body != b'':
#                 serverInfo = request.body

#                 if request.headers.get('macAddress') == None:

#                     res['status'] = False
#                     res['statusCode'] = macAddressPresent.get('statusCode')
#                     res['message'] = ", ".join([serverRegisterFailure.get('message'), macAddressPresent.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([serverRegisterFailure.get('message'), macAddressPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:

#                     logger.debug(" : ".join([requestServerRegister.get('message'), request.headers.get('macAddress')]))

#                     if ValidationClass(request.headers.get('macAddress')).validMacAddress():

#                         logger.debug(" : ".join([macAddressSuccess.get('message'), request.headers.get('macAddress')]))

#                         if not sessionKey.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():

#                             res['status'] = False
#                             res['statusCode'] = sessionKeyNotExists.get('statusCode')
#                             res['message'] = ", ".join([serverRegisterFailure.get('message'), sessionKeyNotExists.get('message')])
#                             res['data'] = None
                            
#                             logger.info(", ".join([serverRegisterFailure.get('message'), sessionKeyNotExists.get('message')]))
#                             return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                         else:

#                             try:
#                                 key = sessionKey.objects.get(macAddress = (request.headers.get('macAddress'))).sessionKeyVal
#                                 logger.debug(sessionKeyData.get('message')+str(key))

#                                 data = json.loads(decryptionRex(key, serverInfo.decode("utf-8")))
#                                 logger.debug(serverDecrypt.get('message')+str(data))

#                                 try:
#                                     if ValidationClass(data.get('dvsPublicIp')).validIpAddressCheck() and ValidationClass(data.get('dvsPublicIp')).validIpAddressCheck():
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('dvsPublicIp')]))
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('dvsLocalIp')]))
                                    
#                                         if serverRegister.objects.filter(Q(macAddress = data.get('macAddress')) | Q(dvsURL = data.get('dvsUrl')) | Q(kongURL=data.get('kongUrl')) | Q(kongFqdn=data.get('kongFqdn'))).exists():
                                            
#                                             try:
#                                                 serverDB = serverRegister.objects.filter(Q(macAddress = data.get('macAddress')) | Q(dvsURL = data.get('dvsUrl')) | Q(kongURL=data.get('kongUrl')) | Q(kongFqdn=data.get('kongFqdn')))
                                                
#                                                 serverPublicIp = serverRegister.objects.get(Q(macAddress = data.get('macAddress')) | Q(dvsURL = data.get('dvsUrl')) | Q(kongURL=data.get('kongUrl')) | Q(kongFqdn=data.get('kongFqdn'))).publicIP

#                                                 publicIpSet = set(serverPublicIp.split(","))
#                                                 publicIpSet.add(data.get('dvsPublicIp'))
#                                                 updatePublicIp = ', '.join(publicIpSet).replace(" ", "")
                                                
#                                                 hotelName = data.get('hotelName')
#                                                 dvsURL = data.get('dvsUrl')
#                                                 dvsLocalIP = data.get('dvsLocalIp')
#                                                 kongURL = data.get('kongUrl')
#                                                 kongFqdn = data.get('kongFqdn')
#                                                 kongLocalIP = data.get('kongLocalIp')
#                                                 publicIP = updatePublicIp
#                                                 macAddress = data.get('dvsMacAddress')
#                                                 clientId = data.get('dvcClientId')
#                                                 clientSecret = data.get('dvcClientSecret')
#                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

#                                                 serverDB.update(hotelName=hotelName, dvsURL=dvsURL, dvsLocalIP=dvsLocalIP, kongURL=kongURL, kongFqdn=kongFqdn, kongLocalIP=kongLocalIP, publicIP=publicIP, macAddress=macAddress, clientId=clientId, clientSecret=clientSecret, modifiedOn=modifiedOn)
                                                
#                                                 res['status'] = True
#                                                 res['statusCode'] = serverUpdateStatus.get('statusCode')
#                                                 res['message'] = ", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')]))
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                 return Response(res)

#                                             except Exception as err:

#                                                 res['status'] = False
#                                                 res['statusCode'] = serverDetailRequired.get('statusCode')
#                                                 res['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                                                 logger.error(err)
#                                                 return Response(res)

#                                         else:

#                                             try:
#                                                 serverDB = serverRegister()

#                                                 serverDB.hotelName = data.get('hotelName')
#                                                 serverDB.dvsURL = data.get('dvsUrl')
#                                                 serverDB.dvsLocalIP = data.get('dvsLocalIp')
#                                                 serverDB.kongURL = data.get('kongUrl')
#                                                 serverDB.kongFqdn = data.get('kongFqdn')
#                                                 serverDB.kongLocalIP = data.get('kongLocalIp')
#                                                 serverDB.publicIP = data.get('dvsPublicIp')
#                                                 serverDB.macAddress = data.get('dvsMacAddress')
#                                                 serverDB.clientId = data.get('dvcClientId')
#                                                 serverDB.clientSecret = data.get('dvcClientSecret')
#                                                 serverDB.createdOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 serverDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 serverDB.save()
                                                
#                                                 res['status'] = True
#                                                 res['statusCode'] = serverRegisterSuccess.get('statusCode')
#                                                 res['message'] = serverRegisterSuccess.get('message') 
#                                                 res['data'] = None

#                                                 logger.info(serverRegisterSuccess.get('message'))
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                 return Response(res)

#                                             except Exception as err:

#                                                 res['status'] = False
#                                                 res['statusCode'] = serverDetailRequired.get('statusCode')
#                                                 res['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                                                 logger.error(err)
#                                                 return Response(res)

#                                     else:
                                        
#                                         res['status'] = False
#                                         res['statusCode'] = ipAddressInvalid.get('statusCode')
#                                         res['message'] = ", ".join([serverRegisterFailure.get('message'), ipAddressInvalid.get('message')])
#                                         res['data'] = None

#                                         logger.info(", ".join([serverRegisterFailure.get('message'), ipAddressInvalid.get('message')]))
#                                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)
                               
#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = DBError.get('statusCode')
#                                     res['message'] = ", ".join([serverRegisterFailure.get('message'), DBError.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([serverRegisterFailure.get('message'), DBError.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                             except Exception as err:

#                                 res['status'] = False
#                                 res['statusCode'] = NotDecrypt.get('statusCode')
#                                 res['message'] = ", ".join([serverRegisterFailure.get('message'), NotDecrypt.get('message')])
#                                 res['data'] = None
                               
#                                 logger.info(", ".join([serverRegisterFailure.get('message'), NotDecrypt.get('message')]))
#                                 logger.error(err)
#                                 return Response(res)

#                     else:
                        
#                         res['status'] = False
#                         res['statusCode'] = macAddressInvalid.get('statusCode')
#                         res['message'] = ", ".join([serverRegisterFailure.get('message'), macAddressInvalid.get('message')])
#                         res['data'] = None

#                         logger.info(", ".join([serverRegisterFailure.get('message'), macAddressInvalid.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([serverRegisterFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([serverRegisterFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)

#         except Exception as err:

#             res['status'] = False
#             res['statusCode'] = serverRegisterError.get('statusCode')
#             res['message'] = serverRegisterError.get('message')
#             res['data'] = None
           
#             logger.info(serverRegisterError)
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None

#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### SERVER REGISTER SECTION END ####



# #### CONFIGURATION FILE SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def config(request):

#     if request.method == 'POST':

#         try:
#             if request.body != b'':
#                 configInfo = request.body

#                 if request.headers.get('macAddress') == None:

#                     res['status'] = False
#                     res['statusCode'] = macAddressPresent.get('statusCode')
#                     res['message'] = ", ".join([configFileFailure.get('message'), macAddressPresent.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([configFileFailure.get('message'), macAddressPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:

#                     try:
#                         logger.debug(requestConfigFile.get('message')+request.headers.get('macAddress'))

#                         if ValidationClass(request.headers.get('macAddress')).validMacAddress():

#                             logger.debug(" : ".join([macAddressSuccess.get('message'), request.headers.get('macAddress')]))

#                             if not sessionKey.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():

#                                 res['status'] = False
#                                 res['statusCode'] = sessionKeyNotExists.get('statusCode')
#                                 res['message'] = ", ".join([configFileFailure.get('message'), sessionKeyNotExists.get('message')])
#                                 res['data'] = None
                               
#                                 logger.info(", ".join([configFileFailure.get('message'), sessionKeyNotExists.get('message')]))
#                                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                             else:

#                                 if not serverRegister.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():

#                                     res['status'] = False
#                                     res['statusCode'] = configFileServerNotPresent.get('statusCode')
#                                     res['message'] = ", ".join([configFileFailure.get('message'), configFileServerNotPresent.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([configFileFailure.get('message'), configFileServerNotPresent.get('message')]))
#                                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                                 else:

#                                     try:
#                                         key = sessionKey.objects.get(macAddress = (request.headers.get('macAddress'))).sessionKeyVal
#                                         # logger.debug(sessionKeyData.get('message')+str(key))

#                                         data = json.loads(decryptionRex(key, configInfo.decode("utf-8")))
#                                         logger.debug(configFileDecrypt.get('message')+str(data))

#                                         try:
#                                             if roomConfig.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():
#                                                 """UPDATE"""

#                                                 roomConfigDB = roomConfig.objects.filter(macAddress = (request.headers.get('macAddress')))
#                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 roomConfigDB.update(config = data, modifiedOn = modifiedOn)
                                               
#                                                 res['status'] = True
#                                                 res['statusCode'] = configFileUpdate.get('statusCode')
#                                                 res['message'] = ", ".join([configFileSuccess.get('message'), configFileUpdate.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(configFileSuccess.get('message'))
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                 return Response(res) 

#                                             else:
#                                                 """INSERT"""

#                                                 roomConfigDB = roomConfig()
#                                                 roomConfigDB.hotelName = serverRegister.objects.get(macAddress = (request.headers.get('macAddress'))).hotelName
#                                                 roomConfigDB.macAddress = request.headers.get('macAddress')
#                                                 roomConfigDB.config = data
#                                                 roomConfigDB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 roomConfigDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 roomConfigDB.save()

#                                                 res['status'] = True
#                                                 res['statusCode'] = configFileSuccess.get('statusCode')
#                                                 res['message'] = configFileSuccess.get('message')
#                                                 res['data'] = None

#                                                 logger.info(configFileSuccess.get('message')) 
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))      
#                                                 return Response(res)

#                                         except Exception as err:

#                                             res['status'] = False
#                                             res['statusCode'] = DBError.get('statusCode')
#                                             res['message'] = ", ".join([configFileFailure.get('message'), DBError.get('message')])
#                                             res['data'] = None

#                                             logger.info(", ".join([configFileFailure.get('message'), DBError.get('message')]))
#                                             logger.error(err)
#                                             return Response(res)

#                                     except Exception as err:

#                                         res['status'] = False
#                                         res['statusCode'] = NotDecrypt.get('statusCode')
#                                         res['message'] = ", ".join([configFileFailure.get('message'), NotDecrypt.get('message')])
#                                         res['data'] = None

#                                         logger.info(", ".join([configFileFailure.get('message'), NotDecrypt.get('message')]))
#                                         logger.error(err)
#                                         return Response(res)

#                         else:

#                             res['status'] = False
#                             res['statusCode'] = macAddressInvalid.get('statusCode')
#                             res['message'] = ", ".join([configFileFailure.get('message'), macAddressInvalid.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([configFileFailure.get('message'), macAddressInvalid.get('message')]))
#                             return Response(res)

#                     except Exception as err:

#                         res['status'] = False
#                         res['statusCode'] = validationError.get('statusCode')
#                         res['message'] = ", ".join([configFileFailure.get('message'), validationError.get('message')])
#                         res['data'] = None

#                         logger.info(", ".join([configFileFailure.get('message'), validationError.get('message')]))
#                         logger.error(err)
#                         return Response(res)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([configFileFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None

#                 logger.info(", ".join([configFileFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)

#         except Exception as err:

#             res['status'] = False
#             res['statusCode'] = configFileError.get('statusCode')
#             res['message'] = configFileError.get('message')
#             res['data'] = None

#             logger.info(configFileError)
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None

#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### CONFIGURATION FILE SECTION END ####



# #### DVC REGISTER SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def dvc(request):

#     if request.method == 'POST':

#         try:
#             resp = dict()
#             servers = dict()

#             if request.body != b'':
#                 DVCInfo = request.body

#                 if request.headers.get('macAddress') == None:

#                     res['status'] = False
#                     res['statusCode'] = macAddressPresent.get('statusCode')
#                     res['message'] = ", ".join([serverDetailFailure.get('message'), macAddressPresent.get('message')])
#                     res['data'] = None

#                     logger.info(", ".join([serverDetailFailure.get('message'), macAddressPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:
#                     logger.debug(" : ".join([requestServerDetail.get('message'), request.headers.get('macAddress')]))

#                     if ValidationClass(request.headers.get('macAddress')).validMacAddress():

#                         logger.debug(" : ".join([macAddressSuccess.get('message'), request.headers.get('macAddress')]))

#                         try:
#                             key = sessionKey.objects.get(macAddress = (request.headers.get('macAddress'))).sessionKeyVal
#                             # logger.debug(sessionKeyData.get('message')+str(key))

#                             try:
#                                 data = json.loads(decryptionRex(key, DVCInfo.decode("utf-8")))
#                                 logger.debug(requestDecrypt.get('message')+str(data))

#                                 try:
#                                     if ValidationClass(data.get('publicIp')).validIpAddressCheck() and ValidationClass(data.get('localIp')).validIpAddressCheck():
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('publicIp')]))
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('localIp')]))

#                                         try:
#                                             if serverFinder(request.headers.get('macAddress')) is not None:
                                                
#                                                 if serverRegister.objects.filter(macAddress = (serverFinder(request.headers.get('macAddress')))).exists():

#                                                     serverDB = serverRegister.objects.filter(macAddress = (serverFinder(request.headers.get('macAddress')))).values()
                                                    
#                                                     dvs = dict()
#                                                     dvs['url'] = serverDB.get().get('dvsURL')
#                                                     dvs['publicIp'] = serverDB.get().get('publicIP')
#                                                     dvs['localIp'] = serverDB.get().get('dvsLocalIP')
#                                                     servers['dvs']= dvs
                                                    
#                                                     kong = dict()
#                                                     kong['fqdn'] = serverDB.get().get('kongFqdn')
#                                                     kong['url'] = serverDB.get().get('kongURL')
#                                                     kong['localIp'] = serverDB.get().get('kongLocalIP')
#                                                     kong['clientId'] = serverDB.get().get('clientId')
#                                                     kong['clientSecret'] = serverDB.get().get('clientSecret')
#                                                     servers['kong'] = kong
                                                    
#                                                     resp['servers'] = servers
#                                                     serverData = json.dumps(resp)

#                                                     logger.debug("Server Data :"+str(serverData))

#                                                     try:
#                                                         resp = encryptionRex(key, serverData)
#                                                         logger.debug(responseEncrypt.get('message')+str(resp))

#                                                         try:
#                                                             if unknownDVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 unknownDVCDB = unknownDVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 unknownDVCDB.delete()
                                                                
#                                                             if not DVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 DVC_DB = DVC()
#                                                                 DVC_DB.hotelName = serverDB.get().get('hotelName')
#                                                                 DVC_DB.publicIp = data.get('publicIp')
#                                                                 DVC_DB.localIp = data.get('localIp')
#                                                                 DVC_DB.macAddress = request.headers.get('macAddress')
#                                                                 DVC_DB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.save()
                                                            
#                                                             else:
                                                                
#                                                                 DVC_DB = DVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 hotelName = serverDB.get().get('hotelName')
#                                                                 publicIp = data.get('publicIp')
#                                                                 localIp = data.get('localIp')
#                                                                 macAddress = request.headers.get('macAddress')
#                                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.update(hotelName=hotelName, publicIp=publicIp, localIp=localIp, macAddress=macAddress, modifiedOn=modifiedOn)

#                                                             res['status'] = True
#                                                             res['statusCode'] = serverDetailSuccess.get('statusCode')
#                                                             res['message'] = serverDetailSuccess.get('message')
#                                                             res['data'] = resp

#                                                             logger.info(serverDetailSuccess.get('message'))
#                                                             logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                             return Response(res)

#                                                         except Exception as err:

#                                                             res['status'] = False
#                                                             res['statusCode'] = DBError.get('statusCode')
#                                                             res['message'] = ", ".join([serverDetailFailure.get('message'), DBError.get('message')])
#                                                             res['data'] = None
                                                            
#                                                             logger.info(", ".join([serverDetailFailure.get('message'), DBError.get('message')]))
#                                                             logger.error(err)
#                                                             return Response(res)

#                                                     except Exception as err:

#                                                         res['status'] = False
#                                                         res['statusCode'] = NotEncrypt.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')]))
#                                                         logger.error(err)
#                                                         return Response(res)

#                                                 else:

#                                                     res['status'] = False
#                                                     res['statusCode'] = serverDetailNotExists.get('statusCode')
#                                                     res['message'] = ", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')])
#                                                     res['data'] = None

#                                                     logger.info(", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')]))
#                                                     return Response(res)

#                                             else:
#                                                 count = 0
#                                                 macAddressData = dict()

#                                                 for item in serverRegister.objects.values_list('publicIP', 'macAddress'):

#                                                     if [c for c in item[0].split(',') if c in data.get('publicIp')]:

#                                                         count = count + 1
#                                                         macAddressData[f"MAC{count}"] = item[1]

#                                                 if len(macAddressData) > 0:

#                                                     if len(macAddressData) > 1:

#                                                         res['status'] = False
#                                                         res['statusCode'] = multipleServerFound.get('statusCode')
#                                                         res['message'] = multipleServerFound.get('message')
#                                                         res['data'] = None

#                                                         logger.info(multipleServerFound.get('message'))
#                                                         return Response(res)

#                                                     serverDB = serverRegister.objects.filter(macAddress = macAddressData['MAC1']).values()
                                                    
#                                                     dvs = dict()
#                                                     dvs['url'] = serverDB.get().get('dvsURL')
#                                                     dvs['publicIp'] = serverDB.get().get('publicIP')
#                                                     dvs['localIp'] = serverDB.get().get('dvsLocalIP')
#                                                     servers['dvs']= dvs
                                                    
#                                                     kong = dict()
#                                                     kong['fqdn'] = serverDB.get().get('kongFqdn')
#                                                     kong['url'] = serverDB.get().get('kongURL')
#                                                     kong['localIp'] = serverDB.get().get('kongLocalIP')
#                                                     kong['clientId'] = serverDB.get().get('clientId')
#                                                     kong['clientSecret'] = serverDB.get().get('clientSecret')
#                                                     servers['kong'] = kong
                                                    
#                                                     resp['servers'] = servers
#                                                     serverData = json.dumps(resp)

#                                                     try:
#                                                         resp = encryptionRex(key, serverData)
#                                                         logger.debug(responseEncrypt.get('message')+str(resp))

#                                                         try:
#                                                             if unknownDVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 unknownDVCDB = unknownDVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 unknownDVCDB.delete()

#                                                             if not DVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 DVC_DB = DVC()
#                                                                 DVC_DB.hotelName = serverDB.get().get('hotelName')
#                                                                 DVC_DB.publicIp = data.get('publicIp')
#                                                                 DVC_DB.localIp = data.get('localIp')
#                                                                 DVC_DB.macAddress = request.headers.get('macAddress')
#                                                                 DVC_DB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.save()

#                                                             else:

#                                                                 DVC_DB = DVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 hotelName = serverDB.get().get('hotelName')
#                                                                 publicIp = data.get('publicIp')
#                                                                 localIp = data.get('localIp')
#                                                                 macAddress = request.headers.get('macAddress')
#                                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.update(hotelName=hotelName, publicIp=publicIp, localIp=localIp, macAddress=macAddress, modifiedOn=modifiedOn)

#                                                             res['status'] = True
#                                                             res['statusCode'] = serverDetailSuccess.get('statusCode')
#                                                             res['message'] = serverDetailSuccess.get('message')
#                                                             res['data'] = resp

#                                                             logger.info(serverDetailSuccess.get('message'))
#                                                             logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                             return Response(res)

#                                                         except Exception as err:

#                                                             res['status'] = False
#                                                             res['statusCode'] = DBError.get('statusCode')
#                                                             res['message'] = ", ".join([serverDetailFailure.get('message'), DBError.get('message')])
#                                                             res['data'] = None
                                                            
#                                                             logger.info(", ".join([serverDetailFailure.get('message'), DBError.get('message')]))
#                                                             logger.error(err)
#                                                             return Response(res)

#                                                     except Exception as err:

#                                                         res['status'] = False
#                                                         res['statusCode'] = NotEncrypt.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')]))
#                                                         logger.error(err)
#                                                         return Response(res)
                                                
#                                                 try:
#                                                     if not unknownDVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                         unknownDVCDB = unknownDVC()
#                                                         unknownDVCDB.publicIp = data.get('publicIp')
#                                                         unknownDVCDB.localIp = data.get('localIp')
#                                                         unknownDVCDB.macAddress = request.headers.get('macAddress')
#                                                         unknownDVCDB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                         unknownDVCDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                         unknownDVCDB.save()

#                                                         res['status'] = False
#                                                         res['statusCode'] = serverDetailNotExists.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')]))
#                                                         return Response(res)

#                                                     else:

#                                                         unknownDVCDB = unknownDVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                         publicIp = data.get('publicIp')
#                                                         localIp = data.get('localIp')
#                                                         macAddress = request.headers.get('macAddress')
#                                                         modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                         unknownDVCDB.update(publicIp=publicIp, localIp=localIp, macAddress=macAddress, modifiedOn=modifiedOn)

#                                                         res['status'] = False
#                                                         res['statusCode'] = serverDetailNotExists.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')]))
#                                                         return Response(res)

#                                                 except Exception as err:

#                                                     res['status'] = False
#                                                     res['statusCode'] = unknownDVCError.get('statusCode')
#                                                     res['message'] = ", ".join([serverDetailFailure.get('message'), unknownDVCError.get('message')])
#                                                     res['data'] = None

#                                                     logger.info(", ".join([serverDetailFailure.get('message'), unknownDVCError.get('message')]))
#                                                     logger.error(err)
#                                                     return Response(res)

#                                         except Exception as err:

#                                             res['status'] = False
#                                             res['statusCode'] = serverFinderError.get('statusCode')
#                                             res['message'] = ", ".join([serverDetailFailure.get('message'), serverFinderError.get('message')])
#                                             res['data'] = None

#                                             logger.info(", ".join([serverDetailFailure.get('message'), serverFinderError.get('message')]))
#                                             logger.error(err)
#                                             return Response(res)

#                                     else:

#                                         res['status'] = False
#                                         res['statusCode'] = ipAddressInvalid.get('statusCode')
#                                         res['message'] = ", ".join([serverDetailFailure.get('message'), ipAddressInvalid.get('message')])
#                                         res['data'] = None

#                                         logger.info(", ".join([serverDetailFailure.get('message'), ipAddressInvalid.get('message')]))
#                                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = validationError.get('statusCode')
#                                     res['message'] = ", ".join([serverDetailFailure.get('message'), validationError.get('message')])
#                                     res['data'] = None

#                                     logger.info(", ".join([serverDetailFailure.get('message'), validationError.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                             except Exception as err:

#                                 res['status'] = False
#                                 res['statusCode'] = NotDecrypt.get('statusCode')
#                                 res['message'] = ", ".join([serverDetailFailure.get('message'), NotDecrypt.get('message')])
#                                 res['data'] = None

#                                 logger.info(", ".join([serverDetailFailure.get('message'), NotDecrypt.get('message')]))
#                                 logger.error(err)
#                                 return Response(res)

#                         except Exception as err:

#                             res['status'] = False
#                             res['statusCode'] = sessionKeyNotExists.get('statusCode')
#                             res['message'] = ", ".join([serverDetailFailure.get('message'), sessionKeyNotExists.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([serverDetailFailure.get('message'), sessionKeyNotExists.get('message')]))
#                             logger.error(err)
#                             return Response(res)

#                     else:

#                         res['status'] = False
#                         res['statusCode'] = macAddressInvalid.get('statusCode')
#                         res['message'] = ", ".join([serverDetailFailure.get('message'), macAddressInvalid.get('message')])
#                         res['data'] = None

#                         logger.info(", ".join([serverDetailFailure.get('message'), macAddressInvalid.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([serverDetailFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None

#                 logger.info(", ".join([serverDetailFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)

#         except Exception as err:
            
#             res['status'] = False
#             res['statusCode'] = serverDetailError.get('statusCode')
#             res['message'] = serverDetailError.get('message')
#             res['data'] = None
            
#             logger.info(serverDetailError.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### DVC REGISTER SECTION END ####
