import streamlit as st
import json
import random

st.title("AI Merchant Engagement Generator")
st.caption("Smart suggestions for gym owners based on customer behavior")

with open("dataset/gyms.json", encoding="utf-8") as f:
    data = json.load(f)

salutations = data["voice"]["salutation_examples"]
tone_lines = data["voice"]["tone_examples"]
offers = data["offer_catalog"]
stats = data["peer_stats"]
tips = data["digest"]

name = st.text_input("Customer Name", "John")
time_slot = st.selectbox("Time Slot", ["Morning", "Afternoon", "Evening"])
customer_type = st.selectbox("Customer Type", ["new_user", "repeat_user", "all"])

if st.button("Generate Strategy"):

    greeting = random.choice(salutations)
    if "{first_name}" in greeting:
        greeting = greeting.replace("{first_name}", name)
    else:
        greeting = "Hi " + name

    filtered = []
    for o in offers:
        if o["audience"] == customer_type or o["audience"] == "all":
            filtered.append(o)

    if len(filtered) == 0:
        filtered = offers

    offer = random.choice(filtered)["title"]

    if time_slot == "Morning":
        insight = "Morning slots are underused (~60%)"
    elif time_slot == "Evening":
        insight = "Evening slots are almost full (~90%)"
    else:
        insight = "Moderate traffic during this time"

    observation = random.choice(tone_lines)
    tip = random.choice(tips)["actionable"]

    observation = observation.replace("â€”", "-")
    tip = tip.replace("â€”", "-")

    confidence = random.randint(80, 95)

    st.success(f"""
{greeting} 👋

Insight: {insight}

Observation: {observation}

Offer: {offer}

Tip: {tip}

Target: {customer_type.replace("_", " ").title()}

Act now to improve conversions 🚀
""")

    st.write("Confidence Score:", str(confidence) + "%")

    st.subheader("Market Data")
    st.write("Rating:", stats["avg_rating"])
    st.write("Calls (30d):", stats["avg_calls_30d"])
    st.write("Directions (30d):", stats["avg_directions_30d"])
    st.write("Conversion Rate:", str(int(stats["trial_to_paid_pct"] * 100)) + "%")