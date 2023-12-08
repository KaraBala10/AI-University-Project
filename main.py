import random
import json
import os
from difflib import get_close_matches

BLUE_COLOR = "\033[96m"
YELLOW_COLOR = "\033[93m"
GREEN_COLOR = "\033[92m"
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"

def load_knowledge_base(file_path: str) -> dict:
    data = {"questions": []}
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    save_knowledge_base(file_path, data)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.5)
    return random.choice(matches) if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    matching_questions = [
        q for q in knowledge_base["questions"] if q["question"] == question
    ]
    if matching_questions:
        return (
            random.choice(matching_questions[0]["answer"])
            if matching_questions[0]["answer"]
            else None
        )
    return None 

def learn_new_word(knowledge_base: dict, user_input: str):
    existing_question = None
    for q in knowledge_base["questions"]:
        if q["question"] == user_input:
            existing_question = q
            break
    new_answers: list = (
        input(f'{YELLOW_COLOR}Type the answers separated by commas "," or "skip" to skip: {RESET_COLOR}')
        .strip()
        .split(",")
    )
    if new_answers[0].lower().strip() == "skip":
        print(f"{YELLOW_COLOR}Skipped adding new response.{RESET_COLOR}")
        return
    new_answers = [a.strip() for a in new_answers]
    if existing_question:
        existing_answers_set = set(existing_question["answer"])
        existing_question["answer"].extend(
            [a for a in new_answers if a not in existing_answers_set]
        )
        print(
            f"{BLUE_COLOR }Bot:{RESET_COLOR} I know this question already, but I have learned new answers."
        )
    else:
        knowledge_base["questions"].append(
            {"question": user_input, "answer": new_answers}
        )
        print(
            f'{BLUE_COLOR}Bot:{RESET_COLOR} Thank you! I learned a new question and response.'
        )
    save_knowledge_base("knowledge_base.json", knowledge_base)

def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    print(
        f'{BLUE_COLOR}Bot:{RESET_COLOR} Hello, I\'m an AI chat. If you want to teach me, send \'teach\' at any time.'
    )
    while True:
        user_input: str = input(f"{GREEN_COLOR}You: {RESET_COLOR}").lower().strip()
        if user_input == "quit":
            print(f"{BLUE_COLOR}Bot:{RESET_COLOR} Goodbye!")
            break
        if user_input == "":
            print(f"{RED_COLOR}Don't send an empty message {RESET_COLOR}")
            continue
        questions = [q["question"] for q in knowledge_base["questions"]]
        best_match: str | None = find_best_match(user_input, questions)
        if user_input == "teach":
            print(f"{BLUE_COLOR}Bot:{RESET_COLOR} Okay, let's learn. Tell me the question!")
            user_input: str = input(f"{GREEN_COLOR}You: {RESET_COLOR}").lower().strip()
            learn_new_word(knowledge_base, user_input)
        elif not best_match:
            print(f"{BLUE_COLOR}Bot:{RESET_COLOR} I don't know the answer. Please teach me :)")
            learn_new_word(knowledge_base, user_input)
        else:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"{BLUE_COLOR}Bot:{RESET_COLOR} {answer}")

if __name__ == "__main__":
    chat_bot()
