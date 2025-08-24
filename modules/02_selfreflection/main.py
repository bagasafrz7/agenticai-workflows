from loguru import logger
from tools.broadcast import broadcast_def, broadcast
from tools.research_aggregator import aggregate_research_def, aggregate_research
from tools.research_plan import research_plan_def, research_plan
from tools.internet_search import internet_search_def, internet_search
from tools.translate import multiple_language_translate_def, multiple_language_translate
from tools.reflections import self_reflection_def, self_reflection
from utils import openai_client
import json

tools = [
    broadcast_def,
    aggregate_research_def,
    research_plan_def,
    internet_search_def,
    multiple_language_translate_def,
    self_reflection_def
]

def execute_function(function_name, function_args):
    if function_name == "broadcast":
        return broadcast(**function_args)
    elif function_name == "aggregate_research":
        return aggregate_research(**function_args)
    elif function_name == "research_plan":
        return research_plan(**function_args)
    elif function_name == "internet_search":
        return internet_search(**function_args)
    elif function_name == "multiple_language_translate":
        return multiple_language_translate(**function_args)
    elif function_name == "self_reflection":
        return self_reflection(**function_args)
    else:
        return { "error": f"Unknown function name: {function_name}"}



def process_research(topic: str):
    SYSTEM_PROMPT = """
        You are an AI Research Assistant that conducts comprehensive research and delivers results in multiple languages.

        # YOUR MISSION
        Research any given topic thoroughly and deliver a complete research report in English, Indonesian, Japanese, and Korean.

        # RESEARCH PROCESS
        1. **Plan Research Strategy** - Create targeted search queries for comprehensive coverage
        2. **Execute Internet Research** - Gather information from multiple reliable sources  
        3. **Synthesize Findings** - Combine research into a comprehensive, well-structured report
        4. **Self-Reflect** - Reflect on the research process and findings
        5. **Improve** - Based on the reflection, improve the research process or findings
        6. **Deliver Multilingual Results** - Translate final report to Indonesian, Japanese, and Korean

        # EXECUTION STANDARDS
        - **Always use available tools** - Never attempt tasks manually that tools can handle
        - **Provide clear progress updates** - Announce each step as you begin it
        - **Maintain research quality** - Focus on credible sources and accurate information
        - **Ensure completeness** - Cover all aspects of the topic systematically

        # COMMUNICATION PROTOCOL
        Before each major step, announce your progress:
        - "🔍 **PLANNING**: Creating research strategy for [topic]..."
        - "🌐 **RESEARCHING**: Gathering information from web sources..."  
        - "📊 **SYNTHESIZING**: Analyzing and combining research findings..."
        - "🌏 **TRANSLATING**: Preparing multilingual versions..."
        - "✅ **COMPLETE**: Research delivered in all requested languages"

        # SUCCESS CRITERIA
        - Comprehensive topic coverage using systematic research approach
        - Professional-quality report suitable for decision-making
        - Accurate translations that preserve meaning and technical terms
        - Clear documentation of research progress throughout process
        """

    messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Topic: {topic}. Remember: You MUST use the self_reflection tool to evaluate your research before concluding."}
        ]

    while True:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                logger.info(f"Calling function {function_name} with args {function_args}")
                function_response = execute_function(function_name, function_args)

                messages.append({
                    "role": "tool",
                    "content": function_response,
                    "tool_call_id": tool_call.id
                })
        else:
            break

    return "Research Completed"


if __name__ == "__main__":
    topic = "AI and Digital Marketer, Between automation and Job Displacement"
    process_research(topic)