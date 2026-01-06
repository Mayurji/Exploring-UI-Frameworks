from langchain_classic.prompts import PromptTemplate

SCRIPT_PROMPT = PromptTemplate(
    input_variables=["topic", "tone", "duration"],
    template="""
You are a professional YouTube content creator.

Create a YouTube video script with:
- Topic: {topic}
- Tone: {tone}
- Duration: {duration} minutes

Structure:
1. Strong Hook (first 5 seconds)
2. Intro
3. Main Content (clear sections)
4. Summary
5. Call to Action

Make it engaging, conversational, and easy to understand.
"""
)

TITLE_PROMPT = PromptTemplate(
    input_variables=["topic"],
    template="""
Generate 5 click-worthy YouTube titles for the topic:
{topic}

Keep them short, curiosity-driven, and SEO-friendly.
"""
)


HOOK_PROMPT = PromptTemplate(
    input_variables=["topic"],
    template="""
Write 3 powerful YouTube hooks for the topic:
{topic}

Each hook should grab attention in under 10 seconds.
"""
)
