import streamlit as st
from openai import OpenAI
import pandas as pd 

client = OpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["openai_key"],
    )

initial_profile = """Genus %
Bacteroides 17.44
Faecalibacterium 17.19
Lachnospiraceae unclassified 12.97 
Eubacterium 8.91
Collinsella 6.34
Alistipes 4.55
Bifidobacterium 3.36
Roseburia 3.12
Blautia 2.47
Prevotella 2.33
Parabacteroides 2.07
Paraprevotella 2.04
Odoribacter 2.04
Anaerostipes 1.97
unclassified Oscillospiraceae 1.57 
Ruminococcus 1.11
Anaerobutyricum 1.08
Butyricimonas 0.87
Mordavella 0.79 Clostridioides 0.59
Faecalitalea 0.59
Lachnoclostridium 0.56
Parolsenella 0.55
Inne 4.68
"""



st.title("Raport o stanie mikroflory jelitowej")

with st.form("order_report"):
    input_profile = st.text_area("Enter taxonomy profile:", height=400, value=initial_profile)
    profile_taxa, profile_values = (' '.join(i.split()[:-1]) for i in input_profile.split('\n')[1:-1]), (float(i.split()[-1]) for i in input_profile.split('\n')[1:-1])
    profile_data = pd.DataFrame(profile_values, index=profile_taxa, columns=['Value'])

    #profile_data = dict(zip(profile_taxa, profile_values))

    language = st.selectbox("Choose report language", 
                                ("Polski", "English"))

    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.bar_chart(data=profile_data)
        with st.spinner('Wait for it...'):
            openai_overview = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Profil mikrobiomu osoby to: {input_profile}. Co to oznacza? Uzyj języka {language}, sformatuj jako markdown"
                    }
                ],
                model = "gpt-3.5-turbo",
            )

            openai_fodmap = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Profil mikrobiomu osoby to: {input_profile}. Opisz indeks FODMAP tego profilu. Podaj w oddzielnym akapicie konkretne wyliczenia. Opisz jak to się odnosi do normy tj. zdrowego poziomu. Uzyj języka {language}, sformatuj jako markdown"
                    }
                ],
                model = "gpt-4o",
            )

            openai_population = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Profil mikrobiomu osoby to: {input_profile}. Odnieś do typowego profilu dla populacji. Wskaz na bakterie ktore odbiegają od normy. Uzyj języka {language}, sformatuj jako markdown"
                    }
                ],
                model = "gpt-3.5-turbo",
            )

            st.markdown(write(openai_overview.choices[0].message.content)
            st.markdown(openai_fodmap.choices[0].message.content)
            st.markdown(openai_population.choices[0].message.content)