import openai
import time

 #Set up OpenAI API key
openai.api_key = "YOUR_API_KEY"

def generate_question_with_validation(subject, difficulty):
    while True:
        # Use GPT-3 to generate questions
        prompt = f"Generate a quiz question for {subject} with difficulty {difficulty}"
        time.sleep(2)  # Sleep for 2 seconds between API calls
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose the engine suitable for your needs
            prompt=prompt,
            max_tokens=150
        )
        question = response['choices'][0]['text'].strip()

        # Generate relevant keywords using GPT-3
        relevant_keywords = generate_keywords(subject)

        # Validate question relevancy
        if is_question_relevant(question, relevant_keywords):
            return question

def generate_keywords(question):
    # Use GPT-3 to suggest relevant keywords based on the generated question
    prompt = f"Suggest relevant keywords for the following question: {question}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )
    suggested_keywords = response['choices'][0]['text'].strip().split(',')
    return [keyword.strip() for keyword in suggested_keywords]

def is_question_relevant(question, relevant_keywords):
    
    #  check if the question contains relevant keywords
    return any(keyword in question.lower() for keyword in relevant_keywords)

def display_questions(questions):
    for i, question in enumerate(questions, start=1):
        print(f"Question {i}: {question}")

def get_user_answers(questions):
    answers = []
    for i in range(len(questions)):
        answer = input(f"Enter the answer for Question {i + 1}: ")
        answers.append(answer)
    return answers

def validate_answers(questions, user_answers):
    for i, (question, user_answer) in enumerate(zip(questions, user_answers), start=1):
        print(f"Question {i}: {question}")
        print(f"Your Answer: {user_answer}")
       
        # Compare user_answer with the correct answer

if __name__ == "__main__":
    #  Ask for User Input
    subject = input("Enter the subject: ")
    difficulty = input("Enter the difficulty level (easy, medium, hard): ")

    #  Generate Quiz Questions with Validation
    # Limit the number of questions to avoid exceeding rate limits
    questions = [generate_question_with_validation(subject, difficulty) for _ in range(2)]  # Generate 2 questions for testing

    #  Display the Questions
    display_questions(questions)

    #  Ask for User Answers
    user_answers = get_user_answers(questions)

    #  Validate Answers
    validate_answers(questions, user_answers)
