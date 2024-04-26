from fastapi import FastAPI, File, Form, UploadFile
from langchain_openai import OpenAI
from langchain.agents import  Tool
from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import YouTubeSearchTool
import sqlite3
import base64
import logging
import requests
import os

app = FastAPI()

# Initialize OpenAI API key
openai_api_key = os.environ['OpenAI_Key']

# Initialize SQLite database
conn = sqlite3.connect("chatbot.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        chatbot_response TEXT,
        youtube_links TEXT
    )
""")
conn.commit()

# Define the YouTube search tool
youtube_tool = YouTubeSearchTool()

# Define the agent tools
tools = [
    Tool(
        name="YouTube Search",
        func=youtube_tool.run,
        description="Useful for searching relevant YouTube videos.",
    )
]


# Initialize the conversation chain
memory = ConversationBufferMemory(memory_key="history")
conversation = ConversationChain(
    llm=OpenAI(temperature=0, openai_api_key=openai_api_key),
    memory=memory,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/chat/text")
async def chat_text(user_input: str = Form(...)):
    try:
        # Check if the user input already exists in the database
        c.execute("SELECT chatbot_response, youtube_links FROM conversations WHERE user_input = ?", (user_input,))
        result = c.fetchone()

        if result:
            # If the data exists, return the stored response and YouTube links
            response, youtube_links = result
            formatted_response = f"{response}\n\nHere are some relevant YouTube videos for further reference:\n\n{youtube_links}"
            logger.info(f"Retrieved response from database for user input: {user_input}")
        else:
            # If the data doesn't exist, process the text using GPT-4 text-based
            prompt = f"""You are a helpful assistant teacher who answers questions in a friendly and simple manner.
                        Provide a concise step by step answer to the question.
                        
                        Question: {user_input}
                        
                        Answer:"""
            response = conversation.predict(input=prompt)
            logger.info(f"Generated response using GPT-4 text-based for user input: {user_input}")

            # Search for relevant YouTube videos
            youtube_links = youtube_tool.run(f"Search for YouTube videos related to: {user_input}")
            logger.info(f"Searched for relevant YouTube videos for user input: {user_input}")
            
            # Format the response with YouTube links
            formatted_response = f"{response}\n\nHere are some relevant YouTube videos for further reference:\n\n{youtube_links}"

            # Store the conversation and YouTube links in the database
            c.execute(
                "INSERT INTO conversations (user_input, chatbot_response, youtube_links) VALUES (?, ?, ?)",
                (user_input, formatted_response, youtube_links),
            )
            conn.commit()
            logger.info(f"Stored conversation and YouTube links in the database for user input: {user_input}")

        return {"response": formatted_response}

    except Exception as e:
        logger.error(f"Error occurred during text-based chat: {str(e)}")
        return {"error": "An error occurred during processing."}

@app.post("/chat/image")
async def chat_image(image: UploadFile = File(...)):
    try:
        # Check if the image filename already exists in the database
        c.execute("SELECT chatbot_response, youtube_links FROM conversations WHERE user_input = ?", (image.filename,))
        result = c.fetchone()

        if result:
            # If the data exists, return the stored response and YouTube links
            response, youtube_links = result
            formatted_response = f"{response}\n\nHere are some relevant YouTube videos for further reference:\n\n{youtube_links}"
            logger.info(f"Retrieved response from database for image: {image.filename}")
        else:
            # If the data doesn't exist, process the image using GPT-4 vision
            image_bytes = await image.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"
            }

            # Configure the model
            payload = {
                "model": "gpt-4-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What's in this image?. Transform that question into text"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                response_text = response.json()["choices"][0]["message"]["content"]
                logger.info(f"Generated response using GPT-4 vision for image: {image.filename}")
            else:
                logger.error(f"Error occurred during image processing: {response.status_code} - {response.text}")
                return {"error": "An error occurred during image processing."}

            # Search for relevant YouTube videos
            youtube_links = youtube_tool.run(f"Search for YouTube videos related to: {image.filename}")
            logger.info(f"Searched for relevant YouTube videos for image: {image.filename}")

            prompt = f"""You are a helpful assistant teacher who answers questions in a friendly and simple manner.
                        Provide a concise step by step answer to the question.
                        You will be given some response as question please answer that 
                        
                        Question: {response_text}
                        
                        Answer:"""
            
            # Predict the response from image and get a text back
            response_got = conversation.predict(input=prompt)
            # Format the response with YouTube links
            formatted_response = f"{response_got}\n\nHere are some relevant YouTube videos for further reference:\n\n{youtube_links}"

            # Store the conversation and YouTube links in the database
            c.execute(
                "INSERT INTO conversations (user_input, chatbot_response, youtube_links) VALUES (?, ?, ?)",
                (image.filename, formatted_response, youtube_links),
            )
            conn.commit()
            logger.info(f"Stored conversation and YouTube links in the database for image: {image.filename}")

        return {"response": formatted_response}

    except Exception as e:
        logger.error(f"Error occurred during image-based chat: {str(e)}")
        return {"error": "An error occurred during processing."}
