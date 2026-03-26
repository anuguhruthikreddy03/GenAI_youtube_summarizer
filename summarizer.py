import os
from dotenv import load_dotenv

from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_text_splitters import RecursiveCharacterTextSplitter
import zipfile

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')


llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

# ------------------- ARTICLE GENERATION -------------------

system_message = 'You are an Professional Article Writer specializing in writing articles for Medium, LinkedIn, and tech blogs.'

human_message = '''
Transform YouTube transcript into **engaging, professional articles** with:

**CRITICAL INSTRUCTIONS**:
- IGNORE introductions, ads, promotions
- Focus only on technical content

{transcript}
'''

summarizer_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template(human_message)
])

# ------------------- TRANSCRIPT FUNCTION -------------------

def extract_transcript(link: str) -> str:
    print("Fetching transcript...")

    try:
        # Try Hindi first
        loader = YoutubeLoader.from_youtube_url(
            link,
            add_video_info=True,
            language=["hi"]
        )
        docs = loader.load()

    except Exception:
        print(" Hindi transcript failed, trying English...")

        try:
            loader = YoutubeLoader.from_youtube_url(
                link,
                add_video_info=True,
                language=["en"]
            )
            docs = loader.load()
        except Exception as e:
            print(" Transcript fetch failed:", e)
            return ""

    if not docs:
        return ""

    print("Transcript fetched")
    return docs[0].page_content


# ------------------- BASE SUMMARIZER -------------------

base_summarizer = (
    RunnablePassthrough()
    | RunnableLambda(extract_transcript)
    | summarizer_prompt
    | llm
    | StrOutputParser()
)

# ------------------- TEXT SPLITTING -------------------

def get_text_chunks(text, chunk_size=5000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_text(text)


# ------------------- AGENT -------------------

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=system_message,
    middleware=[
        SummarizationMiddleware(
            model=llm,
            trigger=("tokens", 1000),
            keep=("tokens", 200),
        ),
    ],
)


def recursive_summarize(text, agent=agent):
    chunks = get_text_chunks(text)
    running_summary = ""

    for chunk in chunks:
        response = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Current summary:
{running_summary}

New content:
{chunk}
"""
                }
            ]
        })

        running_summary = response["messages"][-1].content

    return running_summary


long_summarizer = (
    RunnablePassthrough()
    | RunnableLambda(extract_transcript)
    | RunnableLambda(recursive_summarize)
)

# ------------------- LENGTH CHECK -------------------

def estimate_transcript_length(link: str) -> bool:
    print("Checking transcript length...")

    try:
        loader = YoutubeLoader.from_youtube_url(
            link,
            add_video_info=True,
            language=["hi"]
        )
        docs = loader.load()

    except Exception:
        print("Hindi failed, trying English...")

        try:
            loader = YoutubeLoader.from_youtube_url(
                link,
                add_video_info=True,
                language=["en"]
            )
            docs = loader.load()
        except Exception as e:
            print("Transcript length check failed:", e)
            return False

    if not docs:
        return False

    transcript = docs[0].page_content
    return len(transcript) >= 1000


# ------------------- WEB GENERATION -------------------

web_system_message = """You are a Senior Frontend Developer.

Return code in format:

--html--
--css--
--js--
"""

web_human_message = '''
Create webpage from article.

CONTENT: {article_content}
'''

web_dev_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(web_system_message),
    HumanMessagePromptTemplate.from_template(web_human_message)
])


# ------------------- PIPELINE -------------------

smart_summarizer = (
    RunnableBranch(
        (RunnableLambda(estimate_transcript_length), long_summarizer),
        base_summarizer
    )
    | RunnableLambda(lambda x: {"article_content": x})
    | web_dev_template
    | llm
    | StrOutputParser()
)

# ------------------- RUN -------------------

print("🚀 Starting process...")

try:
    article = smart_summarizer.invoke(
        "https://www.youtube.com/watch?v=YjLF6jTyAVk"
    )

    if not article:
        raise ValueError("No article generated")

    print("Generation done!")

except Exception as e:
    print("Error during processing:", e)
    exit()


# ------------------- SAVE FILES -------------------

try:
    html = article.split('--html--')[1]
    css = article.split('--css--')[1]
    js = article.split('--js--')[1]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)

    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)

    with zipfile.ZipFile('website.zip', 'w') as zipf:
        zipf.write('index.html')
        zipf.write('style.css')
        zipf.write('script.js')

    print("Files created successfully!")

except Exception as e:
    print("File writing error:", e)
