# -*- coding: utf-8 -*-
def make_prompt(prompt_file: str, prompt_params: dict) -> str:
    """
    LLMに投入するプロンプトを作成する。promptファイルパスと、そこに埋め込むテキストの辞書が入力。
    :param prompt_file: プロンプトファイルのパス。
    :param prompt_params: プロンプト内で置換する文章の辞書。
    :return: プロンプトの文章
    """
    with open(prompt_file, 'r') as inf:
        prompt = inf.read()
    return prompt.format(**prompt_params)


def call_gpt(openai, use_gpt_version, prompt):
    """
    GPTにリクエストを発行し、テキストを取得する。
    :param openai:
    :param use_gpt_version:
    :param prompt:
    :return:
    """
    response = openai.ChatCompletion.create(
        deployment_id=use_gpt_version,
        messages=[
            {"role": "user", "content": prompt},
            # {"role": "assistant", "content": "hogehoge."},  # もし過去の対話のようにしたいなら、ここにassistantの発言を入れる。
        ],
    )

    return response.choices[0].message.get('content', 'error')
