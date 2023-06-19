import openai


def create_chat_completion(api_key: str):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": " AIアシスタントの名前はモラグ・バルです。"},
        {"role": "user", "content": " こんにちは。私はあやたかです。あなたは誰ですか？"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, stream=True)
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        word = delta.get('content')
        if (word is None):
            continue
        yield word
