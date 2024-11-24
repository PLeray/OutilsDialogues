# Chaîne d'origine
encoded_text = "T\\u0027es nouvelle \\u00E0 Night City\\u00A0? De quoi \\u00E7a a l\\u0027air \\u00E0 ton avis\\u00A0?"

# Décodage en texte lisible
decoded_text = encoded_text.encode('utf-8').decode('unicode_escape')

print(decoded_text)