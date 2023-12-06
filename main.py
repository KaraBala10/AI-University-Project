import random
import json
import os
from difflib import get_close_matches
from game import tictactoe


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
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


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


def learn_new_word(knowledge_base: dict, user_input: str):
    existing_question = next(
        (q for q in knowledge_base["questions"] if q["question"] == user_input), None
    )
    new_answers: list = (
        input('Type the answers separated by commas "," or "skip" to skip: ')
        .strip()
        .split(",")
    )
    if new_answers[0].lower().strip() == "skip":
        print("Skipped adding new response.")
        return
    new_answers = [a.strip() for a in new_answers]
    if existing_question:
        print(
            "Bot: I know This question already but I have been learned a new answers."
        )
        existing_answers_set = set(existing_question["answer"])
        existing_question["answer"].extend(
            [a for a in new_answers if a not in existing_answers_set]
        )
    else:
        print(
            'Bot: Thank You! I learned a new question and response\nIf you want to teach me more, Send "teach"'
        )
        knowledge_base["questions"].append(
            {"question": user_input, "answer": new_answers}
        )
    save_knowledge_base("knowledge_base.json", knowledge_base)


def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    print(
        "Bot: Hello, I'm AI chat, if you want play with me send 'play', if you want teach me send 'teach' in any time you want"
    )
    while True:
        user_input: str = input("You: ").lower().strip()
        if user_input == "quit":
            print("Bot: Goodbye!")
            break
        if user_input == "":
            print("Bot: Don't send empty message :)")
            continue
        questions = [q["question"] for q in knowledge_base["questions"]]
        best_match: str | None = find_best_match(user_input, questions)
        if user_input == "teach":
            print("Bot: okay let's learning, Tell me the question!")
            user_input: str = input("You: ").lower().strip()
            learn_new_word(knowledge_base, user_input)
        if user_input == "play":
            tictactoe()
        elif not best_match:
            print("Bot: I don't know the answer, Please teach me :)")
            learn_new_word(knowledge_base, user_input)
        else:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")


if __name__ == "__main__":
    chat_bot()
