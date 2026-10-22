import sys

# Knowledge base for your 7 products
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
    }
}

def find_product(user_query):
    """Finds which product the user is talking about."""
    query = user_query.lower()
    
    # Handle beef tallow / fallow typo
    if "fallow" in query or "tallow" in query:
        return "beef tallow"
    
    for key in PRODUCTS:
        if key in query:
            return key
            
    # Check for short keywords
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

def answer_question(user_query):
    query = user_query.lower().strip()
    
    # Check if user wants a list
    if query in ["list", "products", "show products", "menu"]:
        print("\nAvailable Products:")
        for idx, item in enumerate(PRODUCTS.values(), 1):
            print(f" {idx}. {item['name']}")
        return

    product_key = find_product(query)
    
    if not product_key:
        print("\nSorry, I couldn't identify the product. You can ask about:")
        print("Beef Tallow, Cocoa Powder, Gluten-free Chapati Flour, Baobab Powder, Sea Moss, Avocado Powder, or Kombucha Ginger.")
        return

    data = PRODUCTS[product_key]
    print(f"\n--- {data['name']} ---")

    # Determine what they are asking about
    if any(w in query for w in ["benefit", "why", "good for", "health", "advantage"]):
        print(f"Health Benefits: {data['benefits']}")
    elif any(w in query for w in ["use", "how to", "take", "cook", "prepare", "drink"]):
        print(f"How to Use: {data['usage']}")
    elif any(w in query for w in ["what is", "about", "tell me"]):
        print(f"Description: {data['description']}")
        print(f"Key Benefits: {data['benefits']}")
    else:
        # General overview
        print(f"What it is: {data['description']}")
        print(f"Benefits:   {data['benefits']}")
        print(f"How to use: {data['usage']}")

def main():
    print("=" * 60)
    print(" WELCOME TO THE NATURAL HEALTH PRODUCTS ASSISTANT")
    print("=" * 60)
    print("Ask any question about our 7 products (or type 'list' to see them).")
    print("Type 'exit' or 'quit' to leave.\n")
    
    while True:
        try:
            user_input = input("\nYour Question > ")
            if user_input.strip().lower() in ["exit", "quit", "q"]:
                print("Thank you for stopping by! Goodbye.")
                break
            if user_input.strip():
                answer_question(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()