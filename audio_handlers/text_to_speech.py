import pyttsx3

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+30)
engine.say("Для приготовления этого рецепта нам понадобится несколько ингридиентов")
engine.runAndWait()
