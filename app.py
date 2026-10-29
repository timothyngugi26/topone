import os
import streamlit as st

# ── Page config (must be first Streamlit call) ─────────────────────────
st.set_page_config(page_title="Natural Health Products Assistant", page_icon="🌿")

# ── Knowledge base for your 7 products ────────────────────────────────
PRODUCTS = {
    "beef tallow": {
        "name": "Beef Tallow",
        "description": "Rendered beef fat, traditionally used for high-heat cooking and natural skincare.",
        "benefits": "Rich in fat-soluble vitamins (A, D, E, K), has a high smoke point (does not burn easily), and supports gut/skin health.",
        "usage": "Use it as a healthy cooking oil for frying or roasting, or use cosmetic-grade tallow as a moisturizing skin balm.",
    },
    "cocoa powder": {
        "name": "Cocoa Powder",
        "description": "Pure unsweetened powder made from ground, roasted cacao beans.",
        "benefits": "High in polyphenols and antioxidants, helps support heart health, mood, and brain function.",
        "usage": "Add 1-2 tablespoons to smoothies, hot milk, oatmeal, or baking recipes like cakes and brownies.",
    },
    "gluten free chapati flour": {
        "name": "Gluten-Free Chapati Flour",
        "description": "A grain and starch blend (often millet, sorghum, rice, or cassava) formulated to make soft flatbreads without wheat.",
        "benefits": "Safe for individuals with celiac disease or gluten intolerance; easy to digest and rich in dietary fiber.",
        "usage": "Mix with warm water and a little oil, knead into a soft dough, rest for 15 minutes, and roll out onto a dry pan.",
    },
    "baobab powder": {
        "name": "Baobab Powder",
        "description": "Raw fruit powder sourced from the African baobab superfruit.",
        "benefits": "Loaded with Vitamin C (7-10x more than oranges), prebiotic fiber for gut health, and key minerals like calcium and potassium.",
        "usage": "Stir 1-2 teaspoons into water, fruit juice, porridge, yogurt, or daily smoothies for a tangy citrus kick.",
    },
    "sea moss": {
        "name": "Sea Moss",
        "description": "Nutrient-dense marine algae containing roughly 92 of the 102 minerals your body needs.",
        "benefits": "Supports thyroid function (rich in iodine), boosts immunity, promotes glowing skin, and aids digestion.",
        "usage": "Soak and blend into a gel. Take 1-2 tablespoons daily in teas, smoothies, or directly.",
    },
    "avocado powder": {
        "name": "Avocado Powder",
        "description": "Dehydrated, powdered pulp of ripe avocados that preserves all natural fats.",
        "benefits": "Packed with heart-healthy monounsaturated fats, potassium, and fiber without the risk of fruit spoiling quickly.",
        "usage": "Whisk into salad dressings, keto shakes, guacamole, or baked goods for creaminess and nutrition.",
    },
    "kombucha ginger": {
        "name": "Kombucha Ginger",
        "description": "A naturally sparkling fermented black or green tea infused with real ginger root.",
        "benefits": "Loaded with probiotics for gut health, while ginger adds anti-inflammatory and nausea-relief properties.",
        "usage": "Drink chilled (150-250 ml daily) as a refreshing, gut-friendly alternative to sugary sodas.",
    },
}

# ── Keyword matching (unchanged logic) ─────────────────────────────────
def find_product(user_query):
    query = user_query.lower()

    if "fallow" in query or "tallow" in query:
        return "beef tallow"

    for key in PRODUCTS:
        if key in query:
            return key

    if "cocoa" in query or "cacao" in query:
        return "cocoa powder"
    if "chapati" in query:
        return "gluten free chapati flour"
    if "baobab" in query:
        return "baobab powder"
    if "sea moss" in query or "moss" in query:
        return "sea moss"
    if "avocado" in query:
        return "avocado powder"
    if "kombucha" in query or "ginger" in query:
        return "kombucha ginger"

    return None


# ── Rules-based answer (kept from your original) ───────────────────────
def answer_question(user_query):
    """Returns (markdown_text, product_key_or_None)."""
    query = user_query.lower().strip()

    if query in ["list", "products", "show products", "menu"]:
        lines = ["**Available Products:**"]
        for idx, item in enumerate(PRODUCTS.values(), 1):
            lines.append(f"{idx}. {item['name']}")
        return "\n".join(lines), None

    product_key = find_product(query)

    if not product_key:
        return (
            "Sorry, I couldn't identify the product. You can ask about:\n\n"
            "Beef Tallow, Cocoa Powder, Gluten-free Chapati Flour, Baobab Powder, "
            "Sea Moss, Avocado Powder, or Kombucha Ginger.",
            None,
        )

    data = PRODUCTS[product_key]

    if any(w in query for w in ["benefit", "why", "good for", "health", "advantage"]):
        text = f"**{data['name']}**\n\n**Health Benefits:** {data['benefits']}"
    elif any(w in query for w in ["use", "how to", "take", "cook", "prepare", "drink"]):
        text = f"**{data['name']}**\n\n**How to Use:** {data['usage']}"
    elif any(w in query for w in ["what is", "about", "tell me"]):
        text = (
            f"**{data['name']}**\n\n"
            f"**Description:** {data['description']}\n\n"
            f"**Key Benefits:** {data['benefits']}"
        )
    else:
        text = (
            f"**{data['name']}**\n\n"
            f"**What it is:** {data['description']}\n\n"
            f"**Benefits:** {data['benefits']}\n\n"
            f"**How to use:** {data['usage']}"
        )

    return text, product_key


# ── Optional AI layer (Gemini) ─────────────────────────────────────────
@st.cache_resource
def get_gemini_model():
    """Returns a Gemini model object, or None if not configured."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        st.warning(f"AI layer unavailable: {e}")
        return None


def ask_ai(model, user_query, context):
    """Ask Gemini with only the 7 products as context so it can't invent items."""
    prompt = f"""You are a helpful assistant for a natural health products shop.
Only discuss the following 7 products. Never invent products or prices.

{context}

Customer question: {user_query}

Answer helpfully and briefly. If the question is unrelated to these products,
politely say you only help with this shop's products."""
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"(AI error: {e})"


def build_context():
    parts = []
    for p in PRODUCTS.values():
        parts.append(
            f"- {p['name']}: {p['description']} Benefits: {p['benefits']} Usage: {p['usage']}"
        )
    return "\n".join(parts)


# ── Streamlit UI ───────────────────────────────────────────────────────
st.title("🌿 Natural Health Products Assistant")
st.caption(
    "Ask about our 7 products — benefits, how to use them, or just type **list**."
)

# Sidebar: show the catalogue
with st.sidebar:
    st.header("Our Products")
    for i, p in enumerate(PRODUCTS.values(), 1):
        st.markdown(f"**{i}. {p['name']}**")
        st.caption(p["description"])

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Ask me about any of our 7 products, or type **list** to see them all.",
        }
    ]

# Render history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat input
if prompt := st.chat_input("Ask about a product…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 1) Try rules-based answer first (fast, accurate, no API cost)
    reply, matched_key = answer_question(prompt)

    # 2) If no product matched AND Gemini is available, fall back to AI
    if matched_key is None and "couldn't identify" in reply:
        model = get_gemini_model()
        if model is not None:
            with st.spinner("Thinking…"):
                reply = ask_ai(model, prompt, build_context())

    # Show assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})