from common import resultsPerPage, createEmbedsFromFields
from pages import paginate
from discord import Embed
from json import load


with open("example.json", "r") as f:
    
    data = load(f)
    
    
fields = data["FAQs"]
field_pages = resultsPerPage(fields, 3)
# [[f1, f2, f3], [f4, f5, f6], [f7, f8, f9], ....etc]

template = Embed(title="FAQs", description="We have been asked these questions more then once!")

embeds = createEmbedsFromFields(template, field_pages)

await paginate(a, ass, fasf, embeds)
 
 