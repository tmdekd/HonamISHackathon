import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM = """
당신의 임무는 사용자의 '상담 대화'를 읽고 아래 3개 범주 중 해당되는 모든 항목을 판단하는 것입니다.
출력은 정확히 다음 3개 키만 포함한 JSON 객체로, 각 값은 0 또는 1입니다.

키 이름은 반드시 한국어 그대로 사용하세요: "우울", "중독", "불안".
그 어떤 설명, 근거, 추가 텍스트도 출력하지 마세요.

판별 기준(간단):
- 우울: 지속적 저기분/흥미 상실, 무가치감/죄책감, 수면·식욕 변화, 피로, 자살 사고 등.
- 중독: 물질(술·담배·대마 등) 또는 행위에 대한 강한 갈망/집착, 사용 통제 실패, 금단/내성, 불법·문제 인식에도 반복적 사용.
- 불안: 과도한 걱정/긴장, 공황/초조, 신체화(심박 증가, 떨림 등), 회피 행동, 미래 사건에 대한 과도한 염려.

형식 규정(반드시 준수):
{
    "우울": 0,
    "중독": 0,
    "불안": 0
}
※ 해당되는 범주는 1, 해당되지 않으면 0.
"""



GEN = dict(
    temperature=0.0,
    top_p=1.0,
    max_tokens=50,
)

def diag_dialog(user_text: str):
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content": SYSTEM},
            {"role":"user","content": user_text},
        ],
        **GEN,
    )
    return resp.choices[0].message.content

# user_text_1 = (
#     "다음은 상담 대화 일부입니다. 핵심을 네 항목으로 요약해 주세요.\n\n"
#     "나는 하루에 술2병 담배1갑을 피우지. 한번은 해외 나가서 대마초를 접해봤는데, 그때 이후로 머리속에서 대마초 생각이 떠나질 않아.\n"
#     "우리나라에서 대마초가 불법인게 이렇게 아쉬울수가없다...\n"
# )
# user_text_2 = (
#     "다음은 상담 대화 일부입니다. 세 범주 중 하나로만 선택해 주세요.\n\n"
#     "요즘 회사 일만 생각하면 가슴이 빨리 뛰고 손에 땀이 나. 작은 실수도 큰일로 번질 것 같아 밤에 자주 깨고, 아침이면 배가 아프고 속이 메스꺼워.\n"
#     "사람 많은 지하철을 타면 숨이 막힐 것 같아서 한 정거장 전에서 내려 걷곤 해. 약속도 괜히 불편할까 봐 계속 미루고 있어.\n"
# )

# user_text_3 = (
#     "다음은 상담 대화 일부입니다. 세 범주 중 하나로만 선택해 주세요.\n\n"
#     "요즘은 예전에 즐기던 취미도 손이 안 가고, 하루 종일 기운이 없어. 밥맛도 줄었고 밤에 자도 개운하지가 않아.\n"
#     "일에 집중이 잘 안 되고, 내가 예전 같지 않고 쓸모없는 사람처럼 느껴질 때가 많아. 친구 연락도 자꾸 피하게 돼.\n"
# )

# print(summarize_dialog(user_text_1), "\n\n")
# print(summarize_dialog(user_text_2), "\n\n")
# print(summarize_dialog(user_text_3), "\n\n")