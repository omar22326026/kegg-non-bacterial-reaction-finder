import requests

def fetch_taxonomic_ranks():
    with open("taxonomic_ranks.json", "w") as file:
        file.write(requests.get("https://rest.kegg.jp/get/br:br08611/json").text)


def get_module_orthologies(module_id: str) -> [str]:
    src = requests.get("https://rest.kegg.jp/get/"+module_id)
    
    definition_entry = list(
        filter(
            lambda x: x[0]=="DEFINITION",
            map(
                lambda x: x.split(" ", 1),
                src.text.splitlines()
            )
        )
    )[0][1].strip()

    orthologies = definition_entry.replace("+", " ").replace("(", " ").replace(")", " ").replace("-", " ").replace(",", " ").replace("K", ",K").split(",")[1:]

    orthologies = list(
        map(
            lambda x: x.strip(),
            orthologies
        )
    )

    return orthologies



def get_module_reactions(module_id: str) -> [str]:
    src = requests.get("https://rest.kegg.jp/get/"+module_id)
    
    lines = src.text.splitlines()

    reaction_line_found = False
    reaction_lines = []

    for i, each in enumerate(lines):
        if not reaction_line_found:
            if each[:8] == "REACTION":
                reaction_line_found = True
                reaction_lines.append(each)
        elif each[0] == " ":
            reaction_lines.append(each)
        else:
            break
    
    reactions = map(
        lambda x: x.split(" ", 1)[1].strip().split(" ", 1)[0].strip().split(","),
        reaction_lines
    )

    reactions = sum(list(reactions), [])
    
    return(reactions)


def get_reaction_orthologies(reaction_id):
    src = requests.get("https://rest.kegg.jp/get/" + reaction_id)
    
    lines = src.text.splitlines()

    orthology_line_found = False
    orthology_lines = []

    for i, each in enumerate(lines):
        if not orthology_line_found:
            if each[:9] == "ORTHOLOGY":
                orthology_line_found = True
                orthology_lines.append(each)
        elif each[0] == " ":
            orthology_lines.append(each)
        else:
            break

    orthologies = list(
        map(
            lambda x: x.split(" ", 1)[1].strip().split(" ", 1)[0],
            orthology_lines
        )
    )

    return orthologies



def get_orthology_taxonomy(orthology_id: str) -> [str]:
    src = requests.get("https://rest.kegg.jp/get/" + orthology_id)
    
    # map(
    #     lambda x: x.split(" ", 1),
    #     src.text.splitlines()
    # )
    lines = src.text.splitlines();

    gene_line_found = False
    gene_lines = []

    for i, each in enumerate(lines):
        if not gene_line_found:
            if each[:5] == "GENES":
                gene_line_found = True
                gene_lines.append(each)
        elif each[0] == " ":
            gene_lines.append(each)
        else:
            break        
    
    taxonomy = map(
        lambda x: x.strip().split(":")[0].lower(),
        map(
            lambda x: x.split(" ", 1)[1],
            gene_lines
        )
    )

    return(list(taxonomy))


def walk_taxonomy(dict_obj):
    names = []
    if "children" in dict_obj: 
        # is a directory
        for each in dict_obj["children"]:
            names += walk_taxonomy(each)
    else:
        names.append(dict_obj["name"])
    return names

def get_all_names_from_taxonomy(dict_obj):
    names = list(
        map(
            lambda x: [x[0], x[1].strip()],
            map(
                lambda x: x.split(" ", 1),
                walk_taxonomy(dict_obj)
            )
        )
    )

    return(names)
