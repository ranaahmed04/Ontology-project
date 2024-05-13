from rdflib import Graph, Namespace

def get_movie_info(movie_title):
    # Load the ontology file
    g = Graph()
    g.parse(r"E:/UNI\Senior 2.2/Ontologies/FinalNewRdfXml.rdf")

    # Define the namespace
    ex = Namespace("http://www.semanticweb.org/ranaahmed/ontologies/2024/4/Movei-Project")

    # Query the ontology for the movie and its associated entities
    query = f"""
    PREFIX ex: <http://www.semanticweb.org/ranaahmed/ontologies/2024/4/Movei-Project/>
    SELECT DISTINCT ?title ?actor ?director ?writer ?year ?country ?genre
    WHERE {{
        ?movie rdf:type ex:Movie ;
               ex:title ?title .
        FILTER (str(?title) = "{movie_title}")
        OPTIONAL {{ ?movie ex:year ?year }}
        OPTIONAL {{ ?movie ex:country ?country }}
        OPTIONAL {{ ?movie ex:hasGenre ?genre }}
        OPTIONAL {{ ?movie ex:hasActor ?actor }}
        OPTIONAL {{ ?movie ex:hasDirector ?director }}
        OPTIONAL {{ ?movie ex:hasWriter ?writer }}
    }}
    """
    results = g.query(query, initNs={"ex": ex})

    # Check if the movie exists
    if len(results) == 0:
        print("Error: Movie not found.")
    else:
        # Keep track of printed movie details
        printed_movie = False

        # Store genres and actors
        genres = set()
        actors = set()

        # Display information
        for row in results:
            title = row.title
            year = row.year.split('/')[-1]
            country = row.country.split('/')[-1]
            actor = row.actor.split('/')[-1]
            director = row.director.split('/')[-1]
            writer = row.writer.split('/')[-1]
            genre = row.genre.split('/')[-1]

            # Print movie information only once
            if not printed_movie:
                printed_movie = True
                
                print("Title:", title)
                print("Year:", year)
                print("Country:", country)
                print("Director:", director)
                print("Writer:", writer)

            # Add genres to the set
            if isinstance(genre, str):
                genres.add(genre)
            else:
                for g in genre:
                    genres.add(g)

            # Add actors to the set
            if isinstance(actor, str):
                actors.add(actor)
            else:
                for a in actor:
                    actors.add(a)

        # Print genres and actors
        print("Genres:", ', '.join(genres))  # Print genres as a comma-separated list
        print("Actors:", ', '.join(actors))  # Print actors as a comma-separated list

if __name__ == "__main__":
    movie_title = input("Enter the title of the movie: ")
    get_movie_info(movie_title)
