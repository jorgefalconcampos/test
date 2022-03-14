import grequests
import requests

def question_1():
    url = "https://pokeapi.co/api/v2/pokemon"
    args = { "limit": "1500" }
    response = requests.get(url, params=args)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            pokemons = [pokemon["name"] for pokemon in results]
            print(len(list(filter(lambda x: ("at" in x and x.count("a") == 2), pokemons))))

def question_2():
    url = "https://pokeapi.co/api/v2/pokemon/raichu"
    response = requests.get(url)
    if response.status_code == 200:
        species_url = response.json().get("species").get("url")
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            eg_results = species_response.json().get("egg_groups")
            eg_urls = [eg["url"] for eg in eg_results]
            pokemons = []
            for url in eg_urls:
                resp = requests.get(url)
                if response.status_code == 200:
                    res = resp.json().get("pokemon_species")
                    pokemons.extend([i["name"] for i in res])
            pokemons = list(set(pokemons))
            print(len(pokemons))

def question_3():
    url = "https://pokeapi.co/api/v2/generation/1/"
    response = requests.get(url) 
    if response.status_code == 200:
        respultsss = response.json().get("types", [])
        fighting_url = list(filter(lambda x: x["name"]=="fighting", respultsss))[0]['url']
        pokemons = requests.get(fighting_url)
        if pokemons.status_code == 200:
            list_of_pokemons = [i["pokemon"] for i in pokemons.json().get("pokemon",)]
            urls = [i["url"] for i in list_of_pokemons]
            reqs = (grequests.get(u) for u in urls)
            responses = grequests.map(reqs)
            responses_ok = filter(lambda x: x.status_code == 200, responses)
            weights = [i.json().get("weight") for i in responses_ok]
            print([max(weights), min(weights)])


if __name__ == "__main__":
    question_1()