"""
This is the template server side for ChatBot
"""

from bottle import route, run, template, static_file, request
import json
import time
import random

counter = {"count": 0}
saved_name = {"user_name": ''}

animations = {
    "afraid": ['scare', 'scary', 'monster', 'horror'],
    "bored": ['bore', 'boring'],
    "confused": [],
    "crying": ['sad', 'lone'],
    "dancing": ['dance', 'party'],
    "dog": ['dog', 'cat', 'pet', 'animal', 'horse', 'fish'],
    "excited": ['great', 'good', 'fantastic', 'cool'],
    "giggling": ['joke', 'giggling', 'giggle'],
    "heartbroke": ['hate', 'bye', 'bi'],
    "inlove": ['love', 'like', 'life'],
    "laughing": ['laugh', 'funny'],
    "money": ['money', 'rich', 'bills', '$', '£', '€'],
    "no": ['no', 'nah', 'never'],
    "ok": ['ok', 'kay'],
    "takeoff": ['fuck', 'shit', 'bitch'],
    "waiting": ['wait', 'time']
}

replies = {
    # "welcome_reply": "Nice to meet you " + saved_name["user_name"] + "! How are you?",
    "afraid_reply": "Too scary to talk about! New question please",
    "bored_reply": "Boring! Ask me something fun!",
    "confused_reply": "I don't understand! Please give a different reply!",
    "crying_reply": "I'm too sad! Cheer me up!",
    "dancing_reply": "I love to dance!! What do you love?",
    "dog_reply": "My pet dog is my favourite animal in the world! No other animals compare!",
    "excited_reply": "Great! Anything you would like to ask?",
    "giggling_reply": "Funny! Anything else?",
    "heartbroke_reply": "I'm heartbroken!",
    "inlove_reply": "I love love! Love is life",
    "laughing_reply": "Hahaha. Tell me something funny",
    "money_reply": "Money can't buy happiness. Want to ask me a question?",
    "no_reply": "Life is too short to spend in negativity",
    "ok_reply": "Okay is an okay reply. We can do better than that",
    "takeoff_reply": "Terrible language! I won't answer words like that!",
    "waiting_reply": "Patience is power. Anything else you would like to ask?"
}

jokes = [
    "I can't believe I got fired from the calendar factory. All I did was take a day off",
    "Why was Cinderella thrown off the basketball team? She ran away from the ball",
    "I'm reading a book about anti-gravity. It's impossible to put down",
    "I'd tell you a chemistry joke but I know I wouldn't get a reaction",
    "Did you hear about the guy who got hit in the head with a can of soda? He was lucky it was a soft drink",
    "I'm glad I know sign language, it's pretty handy",
    "A friend of mine tried to annoy me with bird puns, but I soon realized that toucan play at that game",
    "I am on a seafood diet. Every time I see food, I eat it",
    "Why did the scientist install a knocker on his door? He wanted to win the No-bell prize!",
    "My first job was working in an orange juice factory, but I got canned: couldn't concentrate",
    "I wanna make a joke about sodium, but Na..",
    "I hate insects puns, they really bug me"
]

@route('/', method='GET')
def index():
    return template("chatbot.html")


def get_welcome(user_message):
    counter["count"] += 1
    user_message = request.POST.get('msg')
    saved_name["user_name"] = user_message
    # return {"animation": "excited", "msg": replies["welcome_reply"]}
    return {"animation": "excited", "msg": "Nice to meet you " + saved_name["user_name"] + "! How are you?"}


def curse_words():
    counter["count"] += 1
    return {"animation": "no", "msg": replies["no_reply"]}


def get_time_date(user_message):
    counter["count"] += 1
    if ("time" in user_message):
        return {"animation": "waiting", "msg": "The time now is: " + time.strftime("%H:%M:%S")}
    else:
        return {"animation": "waiting", "msg": "The date today is: " + time.strftime("%d/%m/%Y")}


def get_joke():
    i = random.randrange(len(jokes))
    return {"animation": "laughing", "msg": jokes[i]}


def get_reply(user_message):
    counter["count"] += 1
    # any(trigger_word in user_message for key, trigger_word_list in animations.items()):
    for key, trigger_word_list in animations.items():
        for trigger_word in trigger_word_list:
            if (trigger_word in user_message):
                return {"animation": key, "msg": replies[key+"_reply"]}
    else:
        return {"animation": "confused", "msg": replies["confused_reply"]}


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    if (counter["count"] == 0):
        reply = get_welcome(user_message)
    elif (any(trigger_word in user_message for trigger_word in animations["no"])):
        reply = curse_words()
    elif("what is the time" in user_message or "what is the date" in user_message):
        reply = get_time_date(user_message)
    elif ("tell me a joke" in user_message):
        reply = get_joke()
    else:
        reply = get_reply(user_message)
    return json.dumps(reply)


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
