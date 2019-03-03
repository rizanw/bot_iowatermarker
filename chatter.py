from chatterbot import ChatBot

def chatmachine(question):
    chatbot = ChatBot(
        'April',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    chatbot.train('chatterbot.corpus.indonesia')

    response = chatbot.get_response(question)
    return response
