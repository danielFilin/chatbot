"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests
import random
from profanity_check import predict, predict_prob


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    newone = user_message.split()
    greetings = ["hello", "good", "evening", "good", "morning", "hi"]
    direction_answer = ["go south", "it is over the street", "ask someone else", "keep walking for 900 km"]
    conditional_words = {
        "cursewords": ["shit", "fuck", "fucker"],
        "greetings": ["hello", "good", "evening", "good", "morning", "hi"],
        "directions": ["where", "find", "which", "direction", "far", "how"],
        "funny": ["joke", "funny"],
        "weather": ["weather", "temperature"]
    }

    def check_weather(words):
        for word in words:
            print(word)
            if word == "weather":
                index = words.index("weather")
                city = words[index + 2]
                api = "http://api.openweathermap.org/data/2.5/weather?appid=98b6fe5dad456b6d8dd141fc5b6f892d&q="
                url = api + city
                json_weather = requests.get(url).json()
                my_weather_data = json_weather["main"]["temp"]
                return my_weather_data
        return False


    def check_greeting(words):
        for index, word in enumerate(words):
            if greetings.count(word) == 1:
                if word == "good":
                    if greetings.count(words[index + 1]) == 1:
                        return True
                else:
                    return True
        return False

    def random_joke():
        url = "https://api.chucknorris.io/jokes/random"
        json_joke = requests.get(url).json()
        joke = json_joke["value"]
        return joke


    def random_answer():
        response = requests.get("https://jsonplaceholder.typicode.com/todos")
        todos = json.loads(response.text)
        list_of_todos = []
        for todo in todos:
            if todo["title"]:
                list_of_todos.extend([todo["title"]])
        response = (random.choice(list_of_todos))
        return response


    def check_all_cases(words, dictionary):
        for key, items in dictionary.items():
            for item in items:
                for word in words:
                    if word == item:
                        if key == "cursewords":
                            return "don't curse me", "crying"
                        elif key == "greetings":
                            check_greeting(words)
                            return "good day to you!", "dancing"
                        elif key == "directions":
                            return (random.choice(direction_answer)), "giggling"
                        elif key == "funny":
                            return random_joke(), "laughing"
                        elif key == "weather":
                            return "the temperature there is now " + str(
                                int((check_weather(newone) - 273.15))) + " degrees celsius", "takeoff"
        if words[-1] == "?":
            return "I don't know", "bored"
        elif words[-1] == "!":
            return "Please be quite! I want to sleep!", "no"
        elif words[0] == "I":
            return "Please, tell me more!", "excited"
        else:
            return random_answer(), "confused"



    answer = check_all_cases(newone, conditional_words)
    print(answer[0], answer[1])

    return json.dumps({"animation": answer[1], "msg": answer[0]})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
