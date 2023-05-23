from logging import info
import os
import openai

from city_manager.models import Faction


class OpenAIClient:
    org_id = openai.organization = os.getenv("OPENAI_ORGANIZATION")
    api_key = openai.api_key = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo-0301"

    def create_faction_clock(self, faction: Faction):
        info(f"new clock created for faction {faction.name}: <created_clock.name>")
        pass


# openai.organization = os.getenv("OPENAI_ORGANIZATION")
# openai.api_key = os.getenv("OPENAI_API_KEY")
# model = "gpt-3.5-turbo-0301"
# completion = openai.ChatCompletion.create(
#     model=model,
#     temperature=1,
#     messages=[
#         {
#             "role": "user",
#             "content": "Write me a sample news article from a newspaper set in the Blades In The Dark city Duskwall. The article should be no more than 150 words long.",
#         },
#         {
#             "role": "user",
#             "content": "The gang 'The Lampblacks' has just completed their objective: 'Destroy the Red Sashes'. The article should focus on this development.",
#         },
#     ],
# )

# print(completion.choices[0].message.content)
