from translate import Translator

def eng2zh(text):
    translator = Translator(to_lang="zh")
    result = translator.translate(text)
    return result

if __name__ == '__main__':
    text = 'This is an example text.'
    translated_text = eng2zh(text)
    print(translated_text)
