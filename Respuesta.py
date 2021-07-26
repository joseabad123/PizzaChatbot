import re


def process_message(message, response_array, response):
    # Splits the message and the punctuation into an array
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())

    # Scores the amount of words in the message
    score = 0
    for word in list_message:
        if word in response_array:
            score = score + 1

    # Returns the response and the score of the response
    return [score, response]


def get_response(message):
    # Custom responses
    response_list = [
        process_message(message, ['querer', 'dar', "ordenar", "damar", "pedir", "comer", "servir", "desear", "apetecer"], "si")
    ]

    # Checks all of the response scores and returns the best matching response
    response_scores = []
    for response in response_list:
        response_scores.append(response[0])

    # Get the max value for the best response and store it into a variable
    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    # Return the matching response to the user
    if winning_response == 0:
        bot_response = False
    else:
        bot_response = True

    print('Bot response:', bot_response)
    return bot_response
