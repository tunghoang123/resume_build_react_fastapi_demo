# -*- coding: utf-8 -*-
import os
import time
import openai
import pathlib
import logging
from dotenv import load_dotenv
from resume_build_utils import make_prompt, call_gpt
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

root_path = pathlib.Path.cwd().parent
load_dotenv(verbose=True)
load_dotenv(root_path / 'env_file' / '.env')

# 初期化処理
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
GPT35_DEPLOYMENT_NAME = os.getenv("OPENAI_GPT35_DEPLOYMENT_NAME")
GPT4_DEPLOYMENT_NAME = os.getenv("OPENAI_GPT4_DEPLOYMENT_NAME")

app = FastAPI()
# フロントがreactの場合は以下が必要。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエストの定義
class ResumeRequest(BaseModel):
    job: str  # 職種
    position: str   # ポディション
    mission: str    # ミッション
    role: str       # 役割
    appeal: str = ''     # アピールポイント
    skill: str = ''     # 保有スキル


@app.get("/")
def read_root():
    return {"message": "Hello, World"}


@app.post("/make_resume/")
def make_resume(resume_request: ResumeRequest):
    print(resume_request)
    start_time = time.time()
    # 1. 職務経歴の生成
    prompt_file = root_path / 'prompt' / 'resume_make.txt'
    prompt_params = {
        'job': resume_request.job,
        'position': resume_request.position,
        'mission': resume_request.mission,
        'domain': resume_request.role,
        'appeal': resume_request.appeal,
        'skill': resume_request.skill,
    }

    use_gpt_version = GPT4_DEPLOYMENT_NAME
    prompt = make_prompt(prompt_file, prompt_params)
    resume_text = call_gpt(openai, use_gpt_version, prompt)  # ここでたまにKeyError: 'content'のエラーが出るのでハンドル。
    if resume_text == 'error':
        # エラーが発生する条件が知りたい・・・。犯罪のテキストを入力した際に発生した。
        end_time = time.time()
        return {
            'status': 'failed',
            'elapse_time': round(end_time - start_time, 5),
            "base_resume_text": resume_text,
            "advice_text": '',
            "final_resume_text": '',
        }

    # 2. アドバイスの生成
    prompt_file = root_path / 'prompt' / 'resume_advice.txt'
    prompt_params = {
        'text': resume_text
    }

    prompt = make_prompt(prompt_file, prompt_params)
    advice_text = call_gpt(openai, use_gpt_version, prompt)
    print(advice_text, use_gpt_version)

    # 3. 最終のレジュメの生成
    prompt_file = root_path / 'prompt' / 'resume_refine.txt'
    prompt_params = {
        'org_resume': resume_text,
        'advice_text': advice_text
    }
    prompt = make_prompt(prompt_file, prompt_params)

    final_resume_text = call_gpt(openai, use_gpt_version, prompt)
    print(final_resume_text, use_gpt_version)
    end_time = time.time()

    return {
        'status': 'success',
        'elapse_time': round(end_time - start_time, 5),
        "base_resume_text": resume_text,
        "advice_text": advice_text,
        "final_resume_text": final_resume_text,
    }
