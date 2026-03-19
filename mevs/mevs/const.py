import string

SYMBOLS = {"letters" : [char for char in string.ascii_uppercase], "numbers" : [str(i) for i in list(range(1, len(string.ascii_uppercase) + 1))]}
TAIL_CHARS = {"none" : "", "newline" : "\n", "space" : " "}

# Answer Language Mapping
# Added whitespaces between the colon and the word were added depending on the common national practices
ANSWER_DICT = {
    "FRE_FR": "Réponse :",
    "ENG_GB": "Answer:",
    "RUS_RU": "Ответ:",
    "SPA_ES": "Respuesta :",
    "POR_PT": "Resposta :",
    "CZE_CZ": "Odpověď:",
    "GER_DE": "Antwort:",
    "NOR_NO": "Svar:",
}