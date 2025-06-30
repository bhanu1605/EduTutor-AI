
import os
from langchain_ibm import WatsonxLLM
from langchain.prompts import PromptTemplate

# Load environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_MODEL_ID = os.getenv("WATSONX_MODEL_ID", "granite-13b-instruct-v2")

# Initialize Watsonx LLM
llm = WatsonxLLM(
    model_id=WATSONX_MODEL_ID,
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
)

# Create a prompt template
template = """
Generate a multiple-choice quiz question on {topic} with 4 options.
Provide the correct answer clearly.

Output in the format:
Question: ...
Options:
A. ...
B. ...
C. ...
D. ...
Answer: ...
"""

prompt = PromptTemplate(
    input_variables=["topic"],
    template=template,
)

# Run the LLM
def generate_quiz(topic):
    formatted_prompt = prompt.format(topic=topic)
    result = llm(formatted_prompt)
    return result

# Parse the output to JSON
def parse_quiz(raw_output):
    lines = raw_output.strip().split("\n")
    quiz = {"question": "", "options": {}, "answer": ""}
    for line in lines:
        if line.startswith("Question:"):
            quiz["question"] = line.replace("Question:", "").strip()
        elif line.startswith(("A.", "B.", "C.", "D.")):
            option = line[0]
            text = line[2:].strip()
            quiz["options"][option] = text
        elif line.startswith("Answer:"):
            quiz["answer"] = line.replace("Answer:", "").strip()
    return quiz

if __name__ == "__main__":
    topic = "Python Programming"
    raw_quiz = generate_quiz(topic)
    structured_quiz = parse_quiz(raw_quiz)
    print("Raw Output:\n", raw_quiz)
    print("\nParsed Quiz JSON:\n", structured_quiz)
