from typing import TypedDict, Optional
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("Groq_Api_Key")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, api_key=api_key)


class PostState(TypedDict):
    prompt: str
    platform: str
    action: str  
    feedback: Optional[str]
    generated_post: str


print("Grpah will we run")
def facebook_node(state: PostState):
    prompt = f"You are an expert Facebook creator. Write an engaging, story-driven post about: {state['prompt']}"
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review"}


def instagram_node(state: PostState):
    prompt = f"You are an Instagram expert. Write a viral-style caption with 10 hashtags about: {state['prompt']}"
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review"}


def linkedin_node(state: PostState):
    prompt = f"You are a LinkedIn strategist. Write a professional, thought-leadership post about: {state['prompt']}"
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review"}


def twitter_node(state: PostState):
    prompt = f"You are an X content creator. Write a punchy tweet under 280 characters about: {state['prompt']}"
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review"}



def facebook_regen_node(state: PostState):
    prompt = f"""
    You are an expert Facebook editor. Rewrite this Facebook post based on human feedback.
    Maintain the engaging, conversational, storytelling style.

    Original Post:
    {state['generated_post']}

    Human Feedback / Changes requested:
    {state.get('feedback', 'Make it a different variation.')}
    """
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review", "feedback": None}


def instagram_regen_node(state: PostState):
    prompt = f"""
    You are an Instagram optimization expert. Rewrite this caption based on human feedback.
    Ensure it remains emoji-rich, keeps short paragraphs, and contains 10 relevant hashtags.

    Original Caption:
    {state['generated_post']}

    Human Feedback / Changes requested:
    {state.get('feedback', 'Make it a different variation.')}
    """
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review", "feedback": None}


def linkedin_regen_node(state: PostState):
    prompt = f"""
    You are a LinkedIn thought-leadership strategist. Rewrite this post based on human feedback.
    Keep it professional, insightful, and maintain an industry-expert tone.

    Original Post:
    {state['generated_post']}

    Human Feedback / Changes requested:
    {state.get('feedback', 'Make it a different variation.')}
    """
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review", "feedback": None}


def twitter_regen_node(state: PostState):
    prompt = f"""
    You are an X (Twitter) copywriter. Rewrite this tweet based on human feedback.
    CRITICAL: Keep it strictly under 280 characters and high engagement.

    Original Tweet:
    {state['generated_post']}

    Human Feedback / Changes requested:
    {state.get('feedback', 'Make it a different variation.')}
    """
    response = llm.invoke(prompt)
    return {"generated_post": response.content, "action": "review", "feedback": None}




def human_review_node(state: PostState):
    review_response = interrupt(
        {
            "message": "Please review the generated post.",
            "post_preview": state["generated_post"],
            "options": ["approve", "regenerate"],
        }
    )

    if review_response.get("action") == "regenerate":
        return {
            "action": "regenerate",
            "feedback": review_response.get("feedback", "")
        }

    return {"action": "approve"}



def route_initial_platform(state: PostState):
    platform = state["platform"].lower()
    if platform in ["facebook", "instagram", "linkedin", "twitter"]:
        return platform
    return "facebook"


def route_review_decision(state: PostState):
    """Routes to the dedicated rewrite node if requested, otherwise ends."""
    if state.get("action") == "regenerate":
        platform = state["platform"].lower()
        if platform in ["facebook", "instagram", "linkedin", "twitter"]:
            return f"{platform}_regen"
    return "end"



builder = StateGraph(PostState)
builder.add_node("facebook", facebook_node)
builder.add_node("instagram", instagram_node)
builder.add_node("linkedin", linkedin_node)
builder.add_node("twitter", twitter_node)
builder.add_node("human_review", human_review_node)

builder.add_node("facebook_regen", facebook_regen_node)
builder.add_node("instagram_regen", instagram_regen_node)
builder.add_node("linkedin_regen", linkedin_regen_node)
builder.add_node("twitter_regen", twitter_regen_node)

builder.add_conditional_edges(
    START,
    route_initial_platform,
    {
        "facebook": "facebook",
        "instagram": "instagram",
        "linkedin": "linkedin",
        "twitter": "twitter",
    },
)

builder.add_edge("facebook", "human_review")
builder.add_edge("instagram", "human_review")
builder.add_edge("linkedin", "human_review")
builder.add_edge("twitter", "human_review")

builder.add_conditional_edges(
    "human_review",
    route_review_decision,
    {
        "facebook_regen": "facebook_regen",
        "instagram_regen": "instagram_regen",
        "linkedin_regen": "linkedin_regen",
        "twitter_regen": "twitter_regen",
        "end": END,
    },
)

builder.add_edge("facebook_regen", "human_review")
builder.add_edge("instagram_regen", "human_review")
builder.add_edge("linkedin_regen", "human_review")
builder.add_edge("twitter_regen", "human_review")

memory = MemorySaver()
graph=builder.compile(checkpointer=memory)