import streamlit as st
from google import genai
from dotenv import load_dotenv
from google.genai import types
import time
import os

load_dotenv()

# Page layout
st.set_page_config(page_title="Product Assistant", page_icon="🌿", layout="centered")

st.title("🌿 Natural Products AI Consultant")
st.caption("Ask me anything about our 7 natural products in plain English!")

# ---------------------------------------------------------
# Put your Gemini API Key here (inside the quotes)
# ---------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if os.getenv("GEMINI_API_KEY"):
    print("thinking!")
else:
    print("oops i will be up again.")

# Initialize Gemini Client
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

# The System Prompt: Keeps the AI accurate, human, and grounded strictly in your 7 products
SYSTEM_INSTRUCTION = """
You are a warm, knowledgeable, and helpful natural wellness consultant.
You provide accurate, easy-to-understand advice about the following 7 products:

1. Beef Tallow (also recognize common typos like "beef fallow"):
   - Pure rendered fat from grass-fed cattle.
   - High smoke point (400°F/205°C), stable fat that doesn't oxidize easily.
   - Rich in bioavailable fat-soluble vitamins (A, D, E, K2) and conjugated linoleic acid (CLA).
   - Uses: Cooking (roasting, frying, searing steaks) and natural skincare (deeply nourishing skin balm that mirrors human skin sebum).

2. Cocoa Powder:
   - 100% unsweetened, natural ground cacao.
   - Rich in flavanols, polyphenols, magnesium, and theobromine.
   - Benefits: Cardiovascular health, brain blood flow, natural mood boost without a caffeine crash.
   - Uses: Smoothies, warm milk/hot cocoa, healthy baking, oatmeal.

3. Gluten-Free Chapati Flour:
   - Wholesome blend of gluten-free grains and starches (e.g., sorghum, cassava, millet, rice).
   - High in dietary fiber, gentle on digestion, 100% safe for celiacs or gluten sensitivity.
   - Uses: Mix with warm water, a pinch of salt, and cooking oil. Knead into a pliable dough, rest for 15-20 minutes, roll between parchment paper or lightly dusted surface, and cook on a hot dry skillet until puffed and golden.

4. Baobab Powder:
   - Raw dried fruit pulp from the African baobab superfruit.
   - Has 7-10x more Vitamin C than oranges; rich in soluble prebiotic fiber, calcium, and potassium.
   - Benefits: Immunity, collagen support, microbiome health, low-glycemic energy.
   - Flavor/Uses: Pleasantly tangy citrus flavor. Add 1-2 tsp to drinking water, freshly squeezed juice, yogurt, or porridge.

5. Sea Moss (Irish Moss / Gracilaria):
   - Nutrient-dense marine algae containing roughly 92 of 102 essential minerals (iodine, sulfur, potassium, iron, zinc).
   - Benefits: Thyroid function support (natural iodine), mucous membrane soothe, immune strength, post-workout recovery.
   - Uses: Typically prepared as a gel. Take 1-2 tablespoons daily in warm herbal tea, shakes, soups, or applied as a hydrating face mask.

6. Avocado Powder:
   - Freeze-dried or dehydrated real avocado flesh.
   - Retains heart-healthy monounsaturated fats (oleic acid), potassium, folate, and dietary fiber.
   - Benefits: Healthy fats on the go with zero risk of over-ripening or spoiling.
   - Uses: Whisk into dressings, green smoothies, dips, creamy sauces, or keto beverages.

7. Kombucha Ginger:
   - Fermented tea beverage loaded with living probiotics, organic acids, and natural ginger juice.
   - Benefits: Gut microbiome balance, digestive soothing, anti-nausea, anti-inflammatory.
   - Uses: Drink 150ml-250ml cold as a refreshing probiotic tonic with meals or as an afternoon revitalizer.

GUIDELINES:
- Speak naturally, warmly, and concisely.
- If a user asks a general question (e.g. "What can I take for joint pain?" or "What helps my skin?"), recommend the appropriate product(s) from this list and explain why.
- If asked about items outside these 7 products, politely bring the conversation back to the 7 products you specialize in.
- Never make unsafe medical claims; remind users that natural supplements support healthy lifestyles.
"""

# Quick product overview in the sidebar
with st.sidebar:
    st.header("📋 Featured Products")
    st.markdown("""
    1. **Beef Tallow** (Cooking & Skincare)
    2. **Cocoa Powder** (Antioxidants & Mood)
    3. **Gluten-Free Chapati Flour** (Digestion & Celiac safe)
    4. **Baobab Powder** (Vitamin C & Prebiotics)
    5. **Sea Moss** (92 Minerals & Thyroid support)
    6. **Avocado Powder** (Monounsaturated Healthy Fats)
    7. **Kombucha Ginger** (Probiotics & Gut health)
    """)

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your natural health assistant. How can I help you with our 7 products today?"}
    ]

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about benefits, recipes, combinations, or preparation..."):
    # Show user question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check that a key has actually been entered
    if not GEMINI_API_KEY or "YOUR_GEMINI_API_KEY" in GEMINI_API_KEY:
        with st.chat_message("assistant"):
            st.error("Please paste your Gemini API key on line 18 in `web_app.py`.")
    else:
        try:
            client = get_client(GEMINI_API_KEY)
            
            # Format chat history for Gemini
            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                )

            # Generate response with resilient fallbacks
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    candidate_models = [
                        "gemini-3.5-flash-lite",  # High throughput & capacity (fast, avoids 503)
                        "gemini-3.8-flash",       # Advanced reasoning model
                        "gemini-3.1-flash-lite",  # High-speed backup
                    ]
                    
                    reply_text = None
                    last_error = None

                    for model_name in candidate_models:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=contents,
                                config=types.GenerateContentConfig(
                                    system_instruction=SYSTEM_INSTRUCTION,
                                    temperature=0.7,
                                ),
                            )
                            reply_text = response.text
                            break  # Success! Stop trying other models
                        except Exception as e:
                            last_error = e
                            time.sleep(1)  # Brief pause before trying fallback
                            continue

                    if reply_text:
                        st.markdown(reply_text)
                        st.session_state.messages.append({"role": "assistant", "content": reply_text})
                    else:
                        st.error(f"The servers are briefly busy. Please ask again: {last_error}")

        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"Error communicating with AI: {e}")