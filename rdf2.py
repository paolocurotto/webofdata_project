import csv
import re

path = ''


def getList(lista):
    value = "("
    for i in lista:
        value = value + " ex:" + dictGenres[i]
    value = value + " )"
    return value


# cargar datos cada elemento de la lista file es una entidad

data1 = 'movie.csv'
data2 = 'link.csv'
data3 = 'genome_tags.csv'
data4 = 'genome_scores.csv'
file = []
file1 = {}
file2 = {}
file3 = {}
file4 = {}

print("reading " + data1)
with open(path + data1, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        file.append(row)
        file1[row[0]] = row[1].replace(" ", "")[:-6].replace(" ", "").replace("(", "").replace(")", "") + row[0]

print("reading " + data2)
with open(path + data2, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[2] is None or row[2] == '' :
            file2[row[0]] = [row[1], '0']
        else:
            file2[row[0]] = [row[1], row[2]]

print("reading " + data3)
with open(path + data3, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        file3[row[0]] = row[1]

print("reading " + data4)
with open(path + data4, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        file4[row[0]] = list()

print("reading again " + data4)
with open(path + data4, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[2] != "relevance":
            if float(row[2]) > 0.5:
                file4[row[0]].append([row[1], row[2]])

movieEntities = []
dictGenres = {}
iterFile = iter(file)
next(iterFile)

print("parsing movies")
# genera una lista de de entidades de peliculas
for movie in iterFile:

    for genre in movie[2].split("|"):
        if not ('key1' in dictGenres.keys()):
            dictGenres[genre] = genre.replace(" ", "") + "Genre"
    imdb = str(file2[movie[0]][0])
    for i in range(7 - len(imdb)):
        imdb = "0" + imdb
    imdb = "'tt" + imdb + "'"
    datoAux = "ex:" + re.sub("\W", "", movie[1].replace(" ", "")[:-6]) + movie[0] + "Movie" + " a ex:Movie;\n"
    datoAux = datoAux + " ex:movieId " + movie[0] + ";\n ex:imdbId " + imdb + ";\n ex:tmdbId " + file2[movie[0]][
        1] + ";\n ex:name '" + movie[1].replace("'", "") + "';\n ex:genre " + getList(movie[2].split("|")) + " . \n"

    movieEntities.append(datoAux)

# Entidades de genero
genreEntities = []

print("parsing genres")
for key, value in dictGenres.items():
    key = re.sub("\W", "", key)
    datoAux = "ex:" + key + "Genre" + " a ex:Genre;\n"
    datoAux = datoAux + " ex:name '" + key + "' . \n"

    genreEntities.append(datoAux)

tagEntities = []
print("parsing genome_tags")
for key, value in file3.items():
    if key != "tagId":
        datoAux = re.sub("\W", "", "ex:" + value) + "Tag" + " a ex:Tag;\n"
        datoAux = datoAux + " ex:tagId " + key + ";\n" + " ex:name '" + value.replace("'", "") + "' . \n"

        tagEntities.append(datoAux)

genomeScoreEntities = []

print("parsing genome_scores")
for key, value in file4.items():
    if key != "movieId":
        for item in value:
            file1[key] = re.sub("\W", "", file1[key])
            datoAux = "ex:Movie" + file1[key]
            datoAux = datoAux + "Tag"
            datoAux = datoAux + re.sub("\W", "", file3[item[0]]) + " a ex:GenomeScore;\n"
            datoAux = datoAux + " ex:movie ex:" + file1[key] + "Movie;\n" + " ex:tag ex:" + re.sub("\W", "", file3[item[0]]) + "Tag; \n"
            datoAux = datoAux + " ex:score " + item[1] + " .\n"

            genomeScoreEntities.append(datoAux)

# print(movieEntities[0])
# print(genreEntities[0])
# print(tagEntities[0])
# print(genomeScoreEntities[29])

f = open("MovieLensRDF_6.ttl", "w+", encoding='utf-8')

f.write("@prefix ex: <http://ex.org/>.\n")
f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n")
f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n\n")


p = 0
a = len(movieEntities)
for i in movieEntities:
    print("(1/4) writing movies " + str((float(p)/a)*100) + " %")
    p = p + 1
    f.write(i)
f.write("\n")

a = len(genreEntities)
p = 0
for i in genreEntities:
    print("(2/4) writing genres " + str((float(p) / a) * 100) + " %")
    p = p + 1
    f.write(i)
f.write("\n\n")

a = len(tagEntities)
p = 0
for i in tagEntities:
    print("(3/4) writing tags " + str((float(p) / a) * 100) + " %")
    p = p + 1
    f.write(i)
f.write("\n\n")

a = len(genomeScoreEntities)
p = 0
for i in genomeScoreEntities:
    print("(4/4) writing genome scores " + str((float(p) / a) * 100) + " %")
    p = p + 1
    f.write(i)
f.write("\n\n")

f.close()


