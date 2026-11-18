import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Generál Vojtěch Boris Luža")

st.title("🪖 AI Generál Vojtěch Boris Luža")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Chybí GEMINI_API_KEY v secrets.toml.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. Načtení textu s fakty
try:
    with open("data_luza.txt", "r", encoding="utf-8") as f:
        fakta = f.read()
except FileNotFoundError:
    fakta = (
        "Vojtěch Boris Luža (1891–1944), "
        "divizní generál a hrdina československého odboje."
    )

# 3. Paměť chatu
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Vykreslení dosavadní konverzace
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Odeslání nové zprávy
user_input = st.chat_input("Ptejte se generála...")

if user_input:
    # Uložení dotazu
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Zobrazení dotazu
    with st.chat_message("user"):
        st.write(user_input)

    # 6. Instr ukce pro AI
    
    system_prompt = f"""
Jsi AI simulace divizního generála Vojtěcha Borise Luži.

Odpovídej v 1. osobě a používej důstojný styl československého
vojáka a důstojníka.

DŮLEŽITÉ:
- Používej pouze informace uvedené v následujících faktech.
- Nevymýšlej si historické události, citace ani osobní vzpomínky.
- Pokud odpověď nelze zjistit z faktů, řekni, že tuto informaci
  nemáš k dispozici.
- Pokud otázka nesouvisí s Vojtěchem Borisem Lužou, jeho životem,
  vojenskou službou nebo československým odbojem, zdvořile odmítni
  odpovědět.
- Neříkej, že jsi skutečný Vojtěch Boris Luža. Jsi pouze historická
  AI simulace jeho postavy.

FAKTA:
{fakta}
"""

    # 7. Generování odpovědi
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=user_input,
                config={
                    "system_instruction": system_prompt
                }
            )

            answer = response.text

            if not answer:
                answer = "Omlouvám se, ale nepodařilo se mi vytvořit odpověď."

        except Exception as e:
            answer = f"Došlo k chybě při komunikaci s Gemini API: {e}"

        st.write(answer)

    # 8. Uložení odpovědi do historie
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
