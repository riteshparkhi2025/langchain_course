import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


load_dotenv()


def main():
    print("Hello from langchain-course!")
    information = """
    William Henry Gates III (born October 28, 1955) is an American businessman and philanthropist. A pioneer of the microcomputer revolution of the 1970s and 1980s, he co-founded the software company Microsoft in 1975 with his childhood friend Paul Allen. Following Microsoft's initial public offering in 1986 and the subsequent increase in its stock price, Gates became the world's then-youngest billionaire in 1987, at age 31. Forbes magazine ranked him as the world's wealthiest person in their The World's Billionaires list for 18 out of 24 years between 1995 and 2017, including 13 years consecutively from 1995 to 2007. Gates became the first centibillionaire in 1999, when his net worth briefly surpassed US$100 billion. According to Forbes, as of July 2026, his net worth stood at US$106.5 billion, making him the 19th-wealthiest individual in the world.

    Born and raised in Seattle, Washington, Gates was privately educated at Lakeside School, where he befriended Allen and developed his computing interests. In 1973, he enrolled at Harvard University, where he took classes including Math 55 and graduate-level computer science courses, but he dropped out in 1975 to co-found and lead Microsoft. He served as its CEO for the next 25 years and also became president and chairman of the board when the company was incorporated in 1981. Succeeded as CEO by Steve Ballmer in 2000, he transitioned to chief software architect, a position he held until 2008. He stepped down as chairman of the board in 2014 and became technology adviser to CEO Satya Nadella and other Microsoft leaders, a position he still holds. He resigned from the board in 2020.

    Over time, Gates reduced his role at Microsoft to focus on his philanthropic work with the Bill & Melinda Gates Foundation, the world's largest private charitable organization, which he and his then-wife, Melinda French Gates, co-chaired from 2000 until 2024. Focusing on areas including health, education, and poverty alleviation, Gates became known for his efforts to combat transmissible diseases such as tuberculosis, malaria, and polio. After French Gates resigned as co-chair following the couple's divorce, the foundation was renamed the Gates Foundation, with Gates as its sole chair.

    Gates is the founder and chairman of several other companies, including BEN, Cascade Investment, TerraPower, Gates Ventures, and Breakthrough Energy. In 2010, he and Warren Buffett founded the Giving Pledge, whereby they and other billionaires pledged to give at least half their wealth to philanthropy. Named as one of the 100 most influential people of the 20th century by Time magazine in 1999, he has received numerous other honors and accolades, including a Presidential Medal of Freedom, awarded jointly to him and French Gates in 2016 for their philanthropic work. The subject of several documentary films, he published the first of three planned memoirs, Source Code: My Beginnings, in 2025.
    """
    summary_template = """
    give the information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
    )

    #llm = ChatOllama(temperature = 0, model = "gemma3:270m")

    chain = summary_prompt_template | llm
    response = chain.invoke(input={"information": information})
    print(response.content)
if __name__ == "__main__":
    main()
