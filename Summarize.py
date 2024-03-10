import json
import google.generativeai as palm


palm.configure(api_key="AIzaSyDGCdHLgthiNkkWWCCtYzvgXQNWoIJa9_A")

models = [model for model in palm.list_models() if 'generateText' in model.supported_generation_methods]

model_bison = models[0]

def Generate_summary(text):
  prompt = f"""
  Your task is to act as a Text Summarizer.
  I will give you text.
  Your task is to create summary for the text in 1500 words.
  Stretch the summary.
  text is shared below, delimited with triple backticks.
  ```
  {text}
  ```
  """
  response = palm.generate_text(
      model=model_bison,
      prompt = prompt,
      temperature = 0.2,
  )
  return  response.result

# Load the JSON data
with open("newarticles2.json") as f:
    data = json.load(f)

# Iterate through each article in the JSON data
for article in data:
    # Get the original description
    original_description = article.get("Description", "")

    # Generate a summary using the original description
    summary = Generate_summary(original_description)
    #print(summary)
    # Replace the original description with the generated summary
    article["Description"] = summary


# text = """
# In simple terms, biodiversity refers to all types of life on Earth. The UN Convention on Biological Diversity (CBD) describes it as \u201cthe diversity within species, between species and of ecosystems, including plants, animals, bacteria, and fungi\u201d. These three levels work together to create life on Earth, in all its complexity. The diversity of species keep the global ecosystem in balance, providing everything in nature that we, as humans, need to survive, including food, clean water, medicine and shelter. \u00a0Over\u00a0half of global GDP\u00a0is strongly dependent on nature. More than one billion people\u00a0rely on forests\u00a0for their livelihoods. Biodiversity is also our strongest natural defence against\u00a0climate change. Land and ocean ecosystems act as \u201ccarbon sinks\u201d, absorbing more than half of all carbon emissions. Because the first big push of the year to put the UN\u2019s bold plan to protect biodiversity into practice\u00a0takes place in the Swiss capital, Bern, between 23 and 25 January. Introducing the conference, Patricia Kameri-Mbote, Director of the United Nations Environment Programme (UNEP) Law Division,\u00a0warned that the lack of coordination between the various organizations trying to protect biodiversity is a \u201ccritical challenge\u201d that needs to be urgently overcome \u201cas we strive for a world living in harmony with nature by 2050\u201d. A key aim of the conference will be to solve that problem by pulling together the various initiatives taking place across the world. Yes. It\u2019s very serious, and it needs to be urgently tackled. Starting with the natural and land sea carbon sinks mentioned above. They are being degraded, with examples including the deforestation of the Amazon and the disappearance of salt marshes and mangrove swamps, which remove large amounts of carbon. The way we use the land and sea is one of the biggest drivers of biodiversity loss. Since 1990, around 420 million hectares of forest have been lost through conversion to other land uses. Agricultural expansion continues to be the main driver of deforestation, forest degradation and forest biodiversity loss. Other major drivers of species decline include overfishing and the introduction of invasive alien species (species that have entered and established themselves in the environment outside their natural habitat, causing the decline or even extinction of native species and negatively affecting ecosystems). These activities, UNEP has shown, are pushing around a million species of plants and animals towards extinction. They range from the critically endangered South China tiger and Indonesian orangutans to supposedly \u201ccommon\u201d animals and plants, such as giraffes and parrots as well as oak trees, cacti and seaweed.\u00a0This is the largest loss of life since the dinosaurs. Combined with skyrocketing levels of pollution, the degradation of the natural habitat and biodiversity loss are having serious impacts on communities around the world. As global temperatures rise, once fertile grasslands turn to desert, and in the ocean, there are hundreds of so-called \u201cdead zones\u201d, where scarcely any aquatic life remains. The loss of biodiversity affects the way an ecosystem functions, leading to species being less able to respond to changes in the environment and making them increasingly vulnerable to natural disasters. If an ecosystem has a wide diversity of organisms, it is likely that they will not all be affected in the same way. For instance, if one species is killed off then a similar species can take its place. The Plan, officially called the Kunming-Montreal\u00a0Global Biodiversity Framework, is a UN-driven landmark agreement adopted by 196 countries to guide global action on nature through to 2030, which was hashed out at meetings in Kunming, China and Montreal, Canada, in 2022. The aim is to address biodiversity loss, restore ecosystems and protect indigenous rights. Indigenous peoples\u00a0suffer disproportionately from loss of biological diversity and environmental degradation. Their lives, survival, development chances, knowledge, environment and health conditions are threatened by environmental degradation, large scale industrial activities, toxic waste, conflicts and forced migration as well as by land-use and land-cover changes such as deforestation for agriculture and extractives. There are concrete measures to halt and reverse nature loss, including putting 30 per cent of the planet and 30 per cent of degraded ecosystems under protection by 2030. Currently 17 per cent of land and around eight per cent of marine areas are protected. The plan also contains proposals to increase financing to developing countries \u2013 a major sticking point during talks \u2013 and indigenous peoples. Countries have to come up with national biodiversity strategies and action plans as well as set or revise national targets to match the ambition of global goals. Next month the UN Environment Assembly (UNEA), otherwise known as the\u00a0\u00a0\u201cWorld\u2019s Environment Parliament\u201d will meet at the UN office in Nairobi. The event\u00a0brings together governments, civil society groups, the scientific community and the private sector to highlight the most pressing issues and improve global governance of the environment. UNEA 2024 will focus on climate change, biodiversity loss and pollution. However, the main event will be\u00a0the\u00a0UN Biodiversity Conference, which\u00a0will take place in Colombia in October. Delegates will discuss\u00a0how to restore lands and seas in a way that protects the planet and respects the rights of local communities.
# """

# print(Generate_summary(text))

# Save the updated JSON data
with open("newarticles2_updated.json", "w") as f:
    json.dump(data, f, indent=2)