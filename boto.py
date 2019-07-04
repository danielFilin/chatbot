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
    response = ""

    user_message = request.POST.get('msg')
    newone = user_message.split()
    length = len(newone)
    curse_words = "shit fuck"
    greetings = ["hello", "good evening", "good morning", "hi"]

    def check_greeting(ans):
        if greetings.count(ans) == 1:
            return True
        else:
            return False

    def check_curse(word):
        print(word in curse_words)
        if word in curse_words:
            return True
        else:
            return False

    def random_answer():
        response = requests.get("https://jsonplaceholder.typicode.com/todos")
        todos = json.loads(response.text)
        list_of_todos = []

        for todo in todos:
            if todo["title"]:
                list_of_todos.extend([todo["title"]])
        response = (random.choice(list_of_todos))
        return response


    print(greetings.count(user_message))


    if check_curse(user_message):
        response = "dont curse me"
        reaction = "crying"
    elif check_greeting(user_message):
        response = "good day to you!"
        reaction = "dancing"
    elif user_message[-1] == "?":
        response = "I cannot help you with that!"
        reaction = "laughing"
    elif user_message[-1] == "!":
        response = "Please be quite, I want to sleep."
        reaction = "waiting"
    else:
        response= random_answer()
        print(response)
        reaction = "confused"

    #chat.setAnimation("ok");
    return json.dumps({"animation": reaction, "msg": response})


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
