import json
from groq import Groq
from decouple import config
from contents.models import Transcript
from ai_agent.models import AgentRole


# Split the transcript into chunks of 1000 tokens
def transform_into_chunks(transcript):
    transcript_text = []
    chunk = "" 
    max_chunk_size = 4000
    
    for segment in transcript:
        chunk += segment['text'] + " "
        if len(chunk) > max_chunk_size: 
            chunk.strip()
            transcript_text.append(chunk)
            chunk = ""

    # Add any remaining text in the last chunk
    if chunk:
        chunk = chunk.strip()
        transcript_text.append(chunk)

    return transcript_text


client = Groq(
    api_key=config("GROQ_API_KEY"),
)

# agent one conduct the business analysis
def agent_one(chunk, agent_role):

    return client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": agent_role + " answer in english even if the text is in a different language."
        },
        {
            "role": "user",
            "content": chunk
        }
    ],
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    max_tokens=100,
    top_p=1,
    stop=None,
    stream=False,
)

# agent two delivers the final response
def agent_two(agent_one_response):

    return client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a 20 years expert in writting and synthesis. Please translate your response in English language only. Trim redudancies but keep the ideas and structure. At the end of your response, invite people to leave a comment."
        },
        {
            "role": "user",
            "content": agent_one_response
        }
    ],
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
)


# this is where we use agent 1 to go over the transcript
def analyse_chunks(transcript_chunks, agent_role):
    analyzed_chunks = []
    for chunk in transcript_chunks:
        analyzed_chunks.append(agent_one(chunk, agent_role).choices[0].message.content)
    return analyzed_chunks


# here we combine all chunks into one string for agent 2 to process it
def combine_analyzed_chunks(analyzed_chunks):
    agent_one_response = ""
    for chunk in analyzed_chunks:
        agent_one_response += chunk + " "
    return agent_one_response


# Resolution 
def get_agent_response(transcript, agent_role):
    transcript_chunks = transform_into_chunks(transcript)

    analyzed_chunks = analyse_chunks(transcript_chunks, agent_role)

    agent_one_response = combine_analyzed_chunks(analyzed_chunks)

    # here we use agent 2 to deliver the final response
    agent_final_response = agent_two(agent_one_response).choices[0].message.content

    return agent_final_response
