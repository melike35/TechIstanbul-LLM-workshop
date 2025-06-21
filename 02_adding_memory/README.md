## Adding memory
For creating a conversational bot with relatively short messages, in this scenario, a ConversationBufferMemory could be suitable. To make the configuration easier, let’s also initialize a ConversationChain to combine the LLM and the memory components.

- x02_adding_memory.py
```python
from langchain.chains import LLMChain, ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain

from dotenv import load_dotenv

load_dotenv()


chat = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=chat, verbose=True, memory=memory)

if __name__=='__main__':
    while True:
        query = input('You: ')
        if query == 'q':
            break
        output = conversation.invoke({"input": query})
        print('User: ', query)
        print('AI system: ', output['response'])
```

### Run
```commandline
python x02_adding_memory.py
```

- Input
```commandline
You: selam ben erkan
```
- AI System:
```bash
Merhaba Erkan! Benim adım da Bard. Tanıştığıma memnun oldum. Nasılsın bugün? Türkçe konuşabildiğime sevindim, Google'da bu konuda eğitildim. Umarım sana yardımcı olabilirim!
```

- Press `q` to exit.