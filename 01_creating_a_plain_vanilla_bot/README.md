## Create working directory and environment
```commandline
mkdir -p ~/mlops/22 && cd ~/mlops/22

conda create -n llm python=3.12

conda activate llm

cat<<EOF | tee requirements.txt
langchain==0.3.17
langchain_community==0.3.16
langchain[google-genai]
python-dotenv==1.0.1
huggingface_hub==0.28.1
streamlit==1.42.0
openai==1.58.1
pypdf==5.2.0
EOF


python -m pip install -r requirements.txt
```

## Create .env file
- Obtain your GOOGLE_API_KEY. It is free. No need credit card.
```commandline
cat<<EOF | tee .env
GOOGLE_API_KEY=<paste_your_key_here>
EOF
```

## Creating a plain vanilla bot step-1
- x01_plain_vanilla_bot.py
```python
import argparse
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()


chat = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chat with OpenAI model using LangChain.")
    parser.add_argument("--question", type=str, required=True, help="The question to ask the AI")
    args = parser.parse_args()

    response = chat.invoke([HumanMessage(content=args.question)])
    print("Response:", response.content)
```

### Ask first question
```commandline
python x01_plain_vanilla_bot.py --question Selam
```
- Output
```commandline
Response: Selam! Nasılsın?
```

## Creating a plain vanilla bot step-2: Add system message
- Add system message and trip advise for Istanbul
```python
import argparse
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()


chat = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chat with OpenAI model using LangChain.")
    parser.add_argument("--system", type=str, required=True, help="You are a helpful assistant that help the user to plan an optimized itinerary.")
    parser.add_argument("--question", type=str, required=True, help="I'm going to Istanbul for 2 days, offer me top 5 places to visit?")
    args = parser.parse_args()

    response = chat.invoke([
        SystemMessage(content=args.system),
        HumanMessage(content=args.question)]
        )
    print("Response:", response.content)
```
### Run
```commandline
 python x01_plain_vanilla_bot.py  \
 --system "You are a helpful assistant that help the user to plan an optimized itinerary." \
 --question "I'm going to Istanbul for 2 days, offer me top 5 places to visit?"
```
- Output
```markdown
Response: Okay, here's a possible itinerary for your 2-day trip to Istanbul, focusing on some of the most iconic and popular attractions, and optimized for a relatively efficient experience:

**Top 5 Places to Visit in Istanbul (2-Day Itinerary):**

This itinerary prioritizes historical sites and a taste of the city's vibrant culture.

**Day 1: Historical Heart of Istanbul**

*   **Morning (9:00 AM - 12:30 PM):** **Hagia Sophia:** Start your day at this architectural marvel. Arrive early to beat the crowds. Allocate at least 2-3 hours to fully appreciate its history and grandeur.
*   **Lunch (12:30 PM - 1:30 PM):** Find a local restaurant near Hagia Sophia for a traditional Turkish lunch. Look for places serving *Döner*, *Köfte* (meatballs), or *Pide* (Turkish pizza).
*   **Afternoon (1:30 PM - 5:00 PM):** **Topkapi Palace:** Explore the opulent palace of the Ottoman Sultans. This sprawling complex requires at least 3-4 hours to see the highlights, including the Harem (separate ticket required), the Treasury, and the Imperial Council.
*   **Evening (5:00 PM - 7:00 PM):** **Walk around Sultanahmet Square:** Relax and soak in the atmosphere of Sultanahmet Square, the heart of old Istanbul. You can see the Blue Mosque from the outside and admire the architecture.
*   **Dinner (7:00 PM onwards):** Enjoy dinner at a restaurant in Sultanahmet offering views of the illuminated Hagia Sophia or Blue Mosque.

**Day 2: Culture and Grandeur**

*   **Morning (9:00 AM - 12:00 PM):** **Blue Mosque:** Visit the iconic Blue Mosque, famous for its stunning blue Iznik tiles. Remember to dress respectfully (shoulders and knees covered). Note that it's closed to tourists during prayer times.
*   **Lunch (12:00 PM - 1:00 PM):** Have lunch near the Grand Bazaar. Many small eateries offer delicious and affordable Turkish cuisine.
*   **Afternoon (1:00 PM - 4:00 PM):** **Grand Bazaar:** Immerse yourself in the vibrant chaos of the Grand Bazaar, one of the world's oldest and largest covered markets. Get lost in its labyrinthine streets, browse the shops selling carpets, jewelry, spices, and souvenirs, and practice your bargaining skills.
*   **Evening (4:00 PM - 6:00 PM):** **Spice Bazaar (Egyptian Bazaar):** A sensory explosion awaits you at the Spice Bazaar, filled with fragrant spices, Turkish delight, nuts, and dried fruits. It's a great place to pick up souvenirs and experience the aromas of Istanbul.
*   **Dinner (7:00 PM onwards):** Enjoy a final Turkish dinner in the Eminönü area, near the Spice Bazaar, or consider a restaurant with views of the Bosphorus.

**Important Notes and Considerations:**

*   **Istanbul Tourist Pass:** Consider purchasing an Istanbul Tourist Pass for access to multiple attractions and potential discounts.  Research if it's cost-effective for your planned itinerary.
*   **Transportation:** Istanbul has a good public transportation system (trams, buses, metro). Purchase an IstanbulKart for easy travel. Walking is also a great way to explore the Sultanahmet area.
*   **Dress Code:** When visiting mosques, dress respectfully (shoulders and knees covered). Women may need to cover their heads (scarves are often provided).
*   **Prayer Times:** Be aware of prayer times, as mosques are closed to tourists during these times.
*   **Bargaining:** Bargaining is expected in the Grand Bazaar and Spice Bazaar.
*   **Safety:** Be aware of your surroundings and take precautions against pickpockets, especially in crowded areas.
*   **Food:** Try local specialties like *baklava*, *Turkish delight*, *Turkish coffee*, and *freshly squeezed pomegranate juice*.

Have a fantastic trip to Istanbul! Let me know if you'd like any modifications or further suggestions.
```