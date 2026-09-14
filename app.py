import streamlit as st
import random
import pandas as pd
import os

RANKING_FILE = "ranking.csv"

st.set_page_config(
    page_title="1~100 숫자 맞히기",
    page_icon="🎯",
    layout="centered"
)


# -----------------------------
# 랭킹 파일 관리
# -----------------------------
def load_ranking():
    if os.path.exists(RANKING_FILE):
        return pd.read_csv(RANKING_FILE)

    return pd.DataFrame(columns=["닉네임", "시도 횟수"])


def save_score(name, attempts):
    ranking = load_ranking()

    new_score = pd.DataFrame({
        "닉네임": [name],
        "시도 횟수": [attempts]
    })

    ranking = pd.concat(
        [ranking, new_score],
        ignore_index=True
    )

    ranking = ranking.sort_values(
        by="시도 횟수",
        ascending=True
    ).head(100)

    ranking.to_csv(RANKING_FILE, index=False)


# -----------------------------
# 새 게임 시작
# -----------------------------
def start_new_game():
    st.session_state.target = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.message = "숫자를 입력해 보세요!"


# -----------------------------
# 세션 초기화
# -----------------------------
if "target" not in st.session_state:
    start_new_game()

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "message" not in st.session_state:
    st.session_state.message = "숫자를 입력해 보세요!"


# -----------------------------
# 화면
# -----------------------------
st.title("🎯 1~100 숫자 맞히기")
st.subheader("컴퓨터가 생각한 숫자를 맞혀보세요!")

st.info(
    "컴퓨터가 1부터 100 사이의 숫자를 하나 선택했습니다. "
    "몇 번 만에 맞힐 수 있을까요?"
)

# 닉네임
nickname = st.text_input(
    "👤 닉네임",
    placeholder="닉네임을 입력하세요"
)

st.divider()

# 현재 시도 횟수
st.metric(
    label="현재 시도 횟수",
    value=f"{st.session_state.attempts}회"
)

st.write(f"💬 {st.session_state.message}")


# -----------------------------
# 숫자 입력
# -----------------------------
guess = st.number_input(
    "🔢 숫자를 입력하세요",
    min_value=1,
    max_value=100,
    value=50,
    step=1,
    disabled=st.session_state.game_over
)


# -----------------------------
# 정답 확인
# -----------------------------
if st.button(
    "🎯 정답 확인",
    use_container_width=True,
    disabled=st.session_state.game_over
):

    if not nickname.strip():
        st.warning("먼저 닉네임을 입력해주세요.")
        st.stop()

    st.session_state.attempts += 1

    if guess < st.session_state.target:

        st.session_state.message = (
            "⬆️ 더 큰 숫자입니다!"
        )

        st.warning(st.session_state.message)

    elif guess > st.session_state.target:

        st.session_state.message = (
            "⬇️ 더 작은 숫자입니다!"
        )

        st.warning(st.session_state.message)

    else:

        st.session_state.game_over = True

        attempts = st.session_state.attempts

        save_score(
            nickname.strip(),
            attempts
        )

        st.success(
            f"🎉 정답입니다! "
            f"정답은 {st.session_state.target}입니다."
        )

        st.balloons()

        st.write(
            f"🏆 **{attempts}번 만에 성공했습니다!**"
        )


# -----------------------------
# 새 게임
# -----------------------------
if st.button(
    "🔄 새 게임",
    use_container_width=True
):
    start_new_game()
    st.rerun()


# -----------------------------
# 랭킹
# -----------------------------
st.divider()

st.header("🏆 명예의 전당")

ranking = load_ranking()

if len(ranking) == 0:

    st.write("아직 기록이 없습니다. 첫 번째 기록의 주인공이 되어보세요! 🎯")

else:

    ranking = ranking.reset_index(drop=True)
    ranking.index += 1

    ranking_display = ranking.rename(
        columns={
            "닉네임": "👤 닉네임",
            "시도 횟수": "🎯 시도 횟수"
        }
    )

    st.dataframe(
        ranking_display.head(10),
        use_container_width=True
    )

    st.caption(
        "시도 횟수가 적을수록 높은 순위입니다."
    )
