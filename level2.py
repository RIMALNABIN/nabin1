import streamlit as st
import pandas as pd
import random
import os

# ============================================================
# JLPT N2 MASTER
# Created by RIMAL NABIN
# Excel + AI Version
# ============================================================

st.set_page_config(
    page_title="JLPT N2 Master",
    page_icon="🇯🇵",
    layout="wide"
)

# ============================================================
# SETTINGS
# ============================================================

EXCEL_FILE = "n2_data.xlsx"

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fc;
}

.hero {
    background: linear-gradient(135deg, #d91e36, #8b1024);
    color: white;
    padding: 45px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.small-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
    min-height: 180px;
}

.small-card h2 {
    color: #b5122b;
}

.footer {
    text-align: center;
    color: #777;
    padding: 40px;
}

.big-kanji {
    font-size: 80px;
    color: #b5122b;
    font-weight: bold;
}

.ai-box {
    background: #ffffff;
    border-left: 6px solid #b5122b;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD EXCEL
# ============================================================

@st.cache_data
def load_excel():
    # Empty tables let the app and AI Teacher open even before the
    # optional Excel learning database has been added.
    empty_kanji = pd.DataFrame(columns=["kanji", "reading", "meaning", "example"])
    empty_vocabulary = pd.DataFrame(columns=["word", "reading", "meaning"])
    empty_grammar = pd.DataFrame(columns=["pattern", "meaning", "example", "explanation"])
    empty_questions = pd.DataFrame(
        columns=["question", "option1", "option2", "option3", "option4", "answer"]
    )

    if not os.path.exists(EXCEL_FILE):
        st.warning(
            "⚠️ n2_data.xlsx was not found. The AI Teacher can still be used, "
            "but study tables and quizzes will be empty. Put n2_data.xlsx in "
            "the same folder as level2.py to load your study data."
        )
        return empty_kanji, empty_vocabulary, empty_grammar, empty_questions

    try:
        kanji = pd.read_excel(EXCEL_FILE, sheet_name="KANJI")
        vocabulary = pd.read_excel(EXCEL_FILE, sheet_name="VOCABULARY")
        grammar = pd.read_excel(EXCEL_FILE, sheet_name="GRAMMAR")
        questions = pd.read_excel(EXCEL_FILE, sheet_name="QUESTIONS")
        return kanji, vocabulary, grammar, questions
    except Exception as e:
        st.error(
            f"❌ Could not read n2_data.xlsx: {e}. Check that it contains "
            "KANJI, VOCABULARY, GRAMMAR, and QUESTIONS sheets."
        )
        return empty_kanji, empty_vocabulary, empty_grammar, empty_questions


KANJI, VOCABULARY, GRAMMAR, QUESTIONS = load_excel()

# ============================================================
# SESSION STATE
# ============================================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = 0

if "streak" not in st.session_state:
    st.session_state.streak = 7

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🇯🇵 JLPT N2 MASTER")

st.sidebar.write("Created by")
st.sidebar.write("**RIMAL NABIN**")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "🈶 Kanji",
        "📚 Learning Book",
        "🧠 Training",
        "🤖 AI Teacher",
        "📊 Progress"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "📊 Content is loaded from n2_data.xlsx"
)

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🇯🇵 Welcome to JLPT N2 MASTER</h1>
        <p>Your complete Japanese N2 learning companion</p>
        <p><b>Created by RIMAL NABIN</b></p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="small-card">
            <h2>🈶</h2>
            <h3>Kanji</h3>
            <p>
            Learn N2 Kanji, readings,
            meanings and examples.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="small-card">
            <h2>📚</h2>
            <h3>Learning Book</h3>
            <p>
            Study vocabulary and
            grammar from your Excel book.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="small-card">
            <h2>🧠</h2>
            <h3>Training</h3>
            <p>
            Practice quizzes and
            JLPT N2 questions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🈶 Kanji",
            len(KANJI)
        )

    with col2:
        st.metric(
            "📖 Vocabulary",
            len(VOCABULARY)
        )

    with col3:
        st.metric(
            "📚 Grammar",
            len(GRAMMAR)
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h2>🤖 AI Japanese Teacher</h2>
        <p>
        Ask questions about Japanese grammar,
        vocabulary, Kanji and JLPT N2.
        </p>
        <p>
        The AI teacher can explain difficult
        Japanese concepts in an N2-friendly way.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.success(
        "🎯 Learn → Practice → Improve → Pass JLPT N2"
    )

# ============================================================
# KANJI
# ============================================================

elif page == "🈶 Kanji":

    st.title("🈶 N2 Kanji")

    st.write(
        "Search your complete Kanji database from Excel."
    )

    search = st.text_input(
        "🔎 Search Kanji, reading, meaning or example",
        placeholder="Example: 経済 or けいざい or economy"
    )

    filtered = KANJI.copy()

    if search.strip():

        search_lower = search.lower()

        filtered = filtered[
            filtered.apply(
                lambda row:
                    search_lower in str(row["kanji"]).lower()
                    or search_lower in str(row["reading"]).lower()
                    or search_lower in str(row["meaning"]).lower()
                    or search_lower in str(row["example"]).lower(),
                axis=1
            )
        ]

    st.write(
        f"Found **{len(filtered)}** Kanji."
    )

    for _, row in filtered.iterrows():

        kanji = row["kanji"]
        reading = row["reading"]
        meaning = row["meaning"]
        example = row["example"]

        with st.expander(
            f"{kanji}　{meaning}"
        ):

            st.markdown(
                f'<div class="big-kanji">{kanji}</div>',
                unsafe_allow_html=True
            )

            st.write(
                f"**Reading:** {reading}"
            )

            st.write(
                f"**Meaning:** {meaning}"
            )

            st.write(
                f"**Example:** {example}"
            )

# ============================================================
# LEARNING BOOK
# ============================================================

elif page == "📚 Learning Book":

    st.title("📚 N2 Learning Book")

    section = st.selectbox(
        "Choose what you want to study",
        [
            "Vocabulary",
            "Grammar"
        ]
    )

    # --------------------------------------------------------
    # VOCABULARY
    # --------------------------------------------------------

    if section == "Vocabulary":

        st.subheader("📖 N2 Vocabulary")

        search = st.text_input(
            "🔎 Search vocabulary",
            placeholder="Example: 経済"
        )

        filtered = VOCABULARY.copy()

        if search.strip():

            search_lower = search.lower()

            filtered = filtered[
                filtered.apply(
                    lambda row:
                        search_lower in str(row["word"]).lower()
                        or search_lower in str(row["reading"]).lower()
                        or search_lower in str(row["meaning"]).lower(),
                    axis=1
                )
            ]

        st.write(
            f"Found **{len(filtered)}** vocabulary words."
        )

        for _, row in filtered.iterrows():

            st.markdown(
                f"""
                <div class="card">
                    <h2>{row["word"]}</h2>
                    <p>
                        <b>Reading:</b>
                        {row["reading"]}
                    </p>
                    <p>
                        <b>Meaning:</b>
                        {row["meaning"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # GRAMMAR
    # --------------------------------------------------------

    else:

        st.subheader("📚 N2 Grammar")

        search = st.text_input(
            "🔎 Search grammar",
            placeholder="Example: わけ"
        )

        filtered = GRAMMAR.copy()

        if search.strip():

            search_lower = search.lower()

            filtered = filtered[
                filtered.apply(
                    lambda row:
                        search_lower in str(row["pattern"]).lower()
                        or search_lower in str(row["meaning"]).lower()
                        or search_lower in str(row["example"]).lower()
                        or search_lower in str(row["explanation"]).lower(),
                    axis=1
                )
            ]

        st.write(
            f"Found **{len(filtered)}** grammar patterns."
        )

        for _, row in filtered.iterrows():

            with st.expander(
                str(row["pattern"])
            ):

                st.write(
                    f"**Meaning:** {row['meaning']}"
                )

                st.write(
                    f"**Example:** {row['example']}"
                )

                st.write(
                    f"**Explanation:** {row['explanation']}"
                )

# ============================================================
# TRAINING
# ============================================================

elif page == "🧠 Training":

    st.title("🧠 N2 Training Center")

    tab1, tab2, tab3 = st.tabs(
        [
            "🔥 Daily Training",
            "🎯 Quiz",
            "📝 Mock Test"
        ]
    )

    # --------------------------------------------------------
    # DAILY TRAINING
    # --------------------------------------------------------

    with tab1:

        st.subheader("🔥 Today's Training")

        st.write(
            "Complete your daily N2 study plan."
        )

        st.checkbox(
            "🈶 Learn 5 Kanji"
        )

        st.checkbox(
            "📖 Learn 10 Vocabulary Words"
        )

        st.checkbox(
            "📚 Review 3 Grammar Patterns"
        )

        st.checkbox(
            "🎧 Practice Listening"
        )

        st.checkbox(
            "📝 Review mistakes"
        )

        st.info(
            "Recommended study time: 30–45 minutes."
        )

    # --------------------------------------------------------
    # QUIZ
    # --------------------------------------------------------

    with tab2:

        st.subheader("🎯 N2 Quiz")

        if len(QUESTIONS) == 0:

            st.warning(
                "No questions found in your Excel file."
            )

        else:

            # Pick a question
            question_index = (
                st.session_state.quiz_index
                % len(QUESTIONS)
            )

            question = QUESTIONS.iloc[
                question_index
            ]

            st.markdown(
                f"### Question {question_index + 1}"
            )

            st.write(
                question["question"]
            )

            options = [
                str(question["option1"]),
                str(question["option2"]),
                str(question["option3"]),
                str(question["option4"])
            ]

            answer = st.radio(
                "Choose your answer:",
                options,
                key=f"answer_{question_index}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Check Answer",
                    key=f"check_{question_index}"
                ):

                    correct = str(
                        question["answer"]
                    )

                    st.session_state.answered += 1

                    if answer == correct:

                        st.success(
                            "🎉 Correct!"
                        )

                        st.session_state.score += 1

                    else:

                        st.error(
                            f"❌ Incorrect!\n\n"
                            f"Correct answer: {correct}"
                        )

            with col2:

                if st.button(
                    "➡️ Next Question",
                    key=f"next_{question_index}"
                ):

                    st.session_state.quiz_index += 1

                    st.rerun()

            st.markdown("---")

            st.write(
                f"🏆 Score: "
                f"**{st.session_state.score}**"
            )

    # --------------------------------------------------------
    # MOCK TEST
    # --------------------------------------------------------

    with tab3:

        st.subheader("📝 JLPT N2 Mock Test")

        st.write(
            "Your mock test can contain questions "
            "from the Excel QUESTIONS sheet."
        )

        st.write(
            "The test can include:"
        )

        st.write("• Vocabulary")
        st.write("• Grammar")
        st.write("• Reading")
        st.write("• Kanji")

        st.info(
            "You can add hundreds of questions to Excel "
            "and use them here."
        )

# ============================================================
# AI TEACHER
# ============================================================

elif page == "🤖 AI Teacher":

    st.title("🤖 AI Japanese Teacher")

    st.write(
        "Ask your AI teacher about JLPT N2."
    )

    st.info(
        "💡 You can ask in English or Japanese."
    )

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    # Read the API key from Streamlit Secrets or an environment variable.
    # Never write the real API key directly into this Python file.
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    try:
        if not api_key:
            api_key = str(st.secrets.get("OPENAI_API_KEY", "")).strip()
    except Exception:
        # Streamlit Secrets may not exist when running locally.
        pass

    api_available = bool(api_key)

    if not api_available:
        st.warning(
            "⚠️ AI is not connected yet. Add OPENAI_API_KEY to Streamlit "
            "Secrets or set it as an environment variable, then restart the app."
        )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.ai_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask your N2 Japanese question..."
    )

    if question:

        st.session_state.ai_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        if not api_available:

            answer = (
                "🤖 AI is not connected yet.\n\n"
                "Please add your OpenAI API key "
                "to Streamlit Secrets."
            )

            with st.chat_message("assistant"):

                st.markdown(answer)

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        else:

            try:

                from openai import OpenAI

                client = OpenAI(api_key=api_key)

                system_prompt = """
You are an expert Japanese teacher
specialized in JLPT N2.

The student is using an N2 Japanese
learning application created by RIMAL NABIN.

Explain Japanese clearly.

When useful, provide:

1. Japanese word or grammar
2. Reading
3. English meaning
4. N2-level explanation
5. Example sentence
6. Important notes
7. A short practice question

Keep explanations appropriate for JLPT N2.

If the student asks about something
unrelated to Japanese learning,
politely guide them back to Japanese.
"""

                with st.chat_message(
                    "assistant"
                ):

                    with st.spinner(
                        "🤖 AI Teacher is thinking..."
                    ):

                        response = client.responses.create(
                            model="gpt-5-mini",
                            instructions=system_prompt,
                            input=question
                        )

                        answer = response.output_text

                        st.markdown(answer)

                st.session_state.ai_messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                st.error(
                    "The AI request failed. Check that your API key is valid, "
                    "your API account has access to the selected model, and your "
                    f"internet connection is working. Details: {e}"
                )

# ============================================================
# PROGRESS
# ============================================================

elif page == "📊 Progress":

    st.title("📊 My N2 Progress")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🔥 Study Streak",
            f"{st.session_state.streak} days"
        )

    with col2:

        st.metric(
            "🧠 Quiz Score",
            st.session_state.score
        )

    with col3:

        st.metric(
            "📝 Questions Answered",
            st.session_state.answered
        )

    st.markdown("---")

    st.subheader("📚 Your Learning Database")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🈶 Kanji",
            len(KANJI)
        )

    with col2:

        st.metric(
            "📖 Vocabulary",
            len(VOCABULARY)
        )

    with col3:

        st.metric(
            "📚 Grammar",
            len(GRAMMAR)
        )

    st.markdown("---")

    st.subheader("📈 Learning Progress")

    kanji_progress = min(
        len(KANJI) / 1000,
        1.0
    )

    vocab_progress = min(
        len(VOCABULARY) / 3000,
        1.0
    )

    grammar_progress = min(
        len(GRAMMAR) / 200,
        1.0
    )

    st.write("🈶 Kanji")

    st.progress(
        kanji_progress
    )

    st.write("📖 Vocabulary")

    st.progress(
        vocab_progress
    )

    st.write("📚 Grammar")

    st.progress(
        grammar_progress
    )

    if st.session_state.answered > 0:

        accuracy = (
            st.session_state.score
            / st.session_state.answered
        )

        st.write(
            f"🎯 Quiz accuracy: "
            f"**{accuracy * 100:.1f}%**"
        )

        st.progress(
            accuracy
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

🇯🇵 <b>JLPT N2 MASTER</b><br>

Created by <b>RIMAL NABIN</b><br><br>

Learn → Practice → Improve → Pass N2

</div>
""", unsafe_allow_html=True)
