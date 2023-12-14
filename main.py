import kegg_crawl
import json



# fetch_taxonomic_ranks()
with open("taxonomic_ranks.json", "r") as file:
    taxonomic_ranks = json.loads(file.read())["children"][4]

bacteria_names = list(
    map(
        lambda x: x[0],
        kegg_crawl.get_all_names_from_taxonomy(taxonomic_ranks)
    )
)


modules = ["M00175", "M00528", "M00529", "M00530", "M00531", "M00804", "M00973"]

orthologies = list(
    map(
        lambda x: kegg_crawl.get_module_orthologies(x),
        modules
    )
)
orthologies = sum(orthologies, [])

bacterial_orthologies = []

for each in orthologies:
    taxonomy = kegg_crawl.get_orthology_taxonomy(each)
    # print(taxonomy)
    for organism in taxonomy:
        if organism in bacteria_names:
            bacterial_orthologies.append(each)
            break

# print(bacterial_orthologies)

nonbacterial_orthologies = [x for x in orthologies if x not in bacterial_orthologies]

# nonbacterial_orthologies = ['K10534', 'K17877']

reactions = list(
    map(
        lambda x: kegg_crawl.get_module_reactions(x),
        modules
    )
)
reactions = sum(reactions, [])

bacterial_reactions = []

for each in reactions:
    reaction_orthologies = kegg_crawl.get_reaction_orthologies(each)
    for orthology in reaction_orthologies:
        if orthology not in nonbacterial_orthologies:
            bacterial_reactions.append(each)
            break

nonbacterial_reactions = [x for x in reactions if x not in bacterial_reactions]

print("Orthologies not found in bacteria are: ", *nonbacterial_orthologies)
print("Reactions not found in bacteria are: ", *nonbacterial_reactions)


# print(orthologies)
# print(reactions)
# print(taxonomy)
# print(reaction_orthologies)

