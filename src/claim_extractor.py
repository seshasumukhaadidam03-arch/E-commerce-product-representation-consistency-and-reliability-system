import os
import json
from dotenv import load_dotenv
from google import genai

# Load the secret keys from the .env file into the system
load_dotenv()

def extract_claims(product_title, product_features):
    """
    Takes the product title and bullet points, and uses Gemini to 
    extract a list of testable, factual claims.
    """
    # 1. Get the VIP ID card (API Key)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API Key not found! Please check your .env file.")

    # 2. Create the client (the waiter) that talks to Google
    client = genai.Client(api_key=api_key)

    # 3. Write the instruction for the AI (The Prompt)
    prompt = f"""
    You are a product reviewer assistant.
    Product Title: {product_title}
    Product Features: {product_features}
    
    Extract a list of specific, verifiable factual claims made by the seller.
    Ignore marketing fluff (e.g., "Best gift", "Amazing", "Luxurious").
    Split complex sentences into simple, single atomic claims.
    
    Output ONLY a valid JSON list of strings, like this: ["claim 1", "claim 2"].
    Do not include markdown formatting like ```json. Just the list.
    """

    # 4. Send the order to the chef (Call Gemini)
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )

        # 5. Clean up the response and turn it into a Python list
        raw_text = response.text.strip()
        
        # Sometimes AI adds markdown like ```json ... ```, so we strip it off
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        claims_list = json.loads(raw_text) # Converts text string to Python list
        return claims_list
    
    except Exception as e:
        print(f"[WARNING] API Error ({e}).")
        print("[WARNING] Falling back to rule-based extraction...\n")
        
        # Fallback: Just split the features into sentences
        fallback_claims = []
        for feature in product_features:
            sentences = str(feature).split('.')
            for s in sentences:
                clean_s = s.strip()
                if len(clean_s) > 15: # Ignore tiny fragments
                    fallback_claims.append(clean_s)
                    
        return fallback_claims

# ==========================================
# TESTING BLOCK
# ==========================================
# If we run this file directly, it will run this test using our downloaded data.
if __name__ == "__main__":
    # Open our sample data
    with open("../data/sample/sample_products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
        
    # Pick the first product (The Reusable Shower Cap)
    first_product = products[0]
    title = first_product["title"]
    features = first_product["features"]
    
    print("=" * 50)
    print("PRODUCT:", title[:60], "...")
    print("=" * 50)
    print("Sending to Gemini API for extraction... Please wait...\n")
    
    # Run our function!
    extracted_claims = extract_claims(title, features)
    
    print("[RESULT] EXTRACTED CLAIMS:")
    for i, claim in enumerate(extracted_claims, 1):
        print(f"{i}. {claim}")
