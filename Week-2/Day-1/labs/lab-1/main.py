from agent import process_prompt

while True:
    user_input = input("Ask: ")

    result = process_prompt(user_input)

    print("Result:", result)
