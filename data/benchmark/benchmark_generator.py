"""
benchmark_generator.py - Curates the 25-Product Ground-Truth Evaluation Benchmark
================================================================================
Generates a structured dataset of 25 products with human-verified ground-truth:
- 10 CONSISTENT products (claims match customer experience)
- 5 CONTRADICTORY products (direct contradictions on material, size, or quality)
- 5 MIXED EVIDENCE products (some claims confirmed, others refuted)
- 5 INSUFFICIENT EVIDENCE products (sparse, off-topic, or missing customer feedback)
Across Fashion, Electronics, Home & Kitchen, Grooming, and Accessories.
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.settings import BENCHMARK_DATA_DIR

BENCHMARK_FILE = BENCHMARK_DATA_DIR / "benchmark_products.json"

def generate_benchmark_dataset():
    products = [
        # =====================================================================
        # CATEGORY 1: CONSISTENT (10 Products)
        # =====================================================================
        {
            "product_id": "bench_c01",
            "category": "Accessories",
            "title": "Minimalist RFID Slim Front Pocket Bifold Wallet",
            "features": [
                "Crafted with durable top-grain genuine leather.",
                "Equipped with advanced RFID blocking lining.",
                "Features 6 credit card slots and 1 cash pocket.",
                "Ultra-slim 0.4 inch thickness design."
            ],
            "seller_images": ["https://images.unsplash.com/photo-1627123424574-724758594e93?w=400"],
            "customer_images": ["https://images.unsplash.com/photo-1627123424574-724758594e93?w=400"],
            "customer_reviews": [
                {"text": "The genuine leather smells authentic and has held up nicely for six months.", "id": "r1"},
                {"text": "The card slots are tight at first but easily hold 6 cards without bulging.", "id": "r2"},
                {"text": "Extremely slim wallet, fits into my front pocket effortlessly.", "id": "r3"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c02",
            "category": "Electronics",
            "title": "Anker USB-C Fast Charger 30W Compact Adapter",
            "features": [
                "30W high speed output for smartphones and tablets.",
                "Foldable plug mechanism for travel portability.",
                "Built-in temperature control and surge protection."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Charges my phone from 10% to 70% in under 35 minutes as advertised.", "id": "r1"},
                {"text": "The foldable plug feels sturdy and makes packing very easy.", "id": "r2"},
                {"text": "Does not get dangerously warm during long charging sessions.", "id": "r3"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c03",
            "category": "Home & Kitchen",
            "title": "Stainless Steel Double-Wall Vacuum Insulated Water Bottle 750ml",
            "features": [
                "Made from food-grade 18/8 stainless steel.",
                "Keeps beverages cold for 24 hours and hot for 12 hours.",
                "100% leakproof silicone seal cap with handle."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "I filled it with ice water and it still had ice cubes inside after 20 hours.", "id": "r1"},
                {"text": "Tossed it in my gym backpack sideways and not a single drop leaked.", "id": "r2"},
                {"text": "Durable steel body with no metallic taste in the drinking water.", "id": "r3"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c04",
            "category": "Grooming",
            "title": "Natural Boar Bristle Hair Brush with Ergonomic Bamboo Handle",
            "features": [
                "100% natural boar bristles for oil distribution.",
                "Solid bamboo wood handle and paddle.",
                "Suitable for thick, curly, and straight hair."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "The natural bristles glide smoothly and gently detangle without pulling.", "id": "r1"},
                {"text": "The bamboo handle feels solid in hand with a nice polished finish.", "id": "r2"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c05",
            "category": "Footwear",
            "title": "Men's Breathable Mesh Running Shoes Lightweight Athletic Sneakers",
            "features": [
                "Breathable knitted mesh upper for ventilation.",
                "Cushioned EVA foam midsole absorbs shock.",
                "Slip-resistant rubber outsole."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Super lightweight running shoes, feet stay cool and dry on long walks.", "id": "r1"},
                {"text": "The foam sole provides decent arch support and good shock absorption.", "id": "r2"},
                {"text": "Good grip on wet pavement, non-slip rubber works properly.", "id": "r3"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c06",
            "category": "Stationery",
            "title": "Hardcover Dotted Grid Journal 160 GSM Bleedproof Paper",
            "features": [
                "Ultra-thick 160 GSM paper prevents ink ghosting and bleeding.",
                "Hardcover vegan leather binding with elastic closure band.",
                "Dual ribbon bookmarks and expandable back inner pocket."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Tested with fountain pens and heavy markers; zero bleedthrough or ghosting.", "id": "r1"},
                {"text": "Cover material feels premium and the inner back pocket holds stickers easily.", "id": "r2"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c07",
            "category": "Kitchen",
            "title": "Heavy Duty Cast Iron Skillet Pre-Seasoned 10-Inch",
            "features": [
                "Pre-seasoned with 100% natural vegetable oil.",
                "Even heat retention and distribution for searing.",
                "Oven safe up to 500 degrees Fahrenheit."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Heats up evenly across the whole surface, fried eggs slide right off.", "id": "r1"},
                {"text": "Very heavy sturdy cast iron, used it in the oven at 450F with no issues.", "id": "r2"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c08",
            "category": "Electronics",
            "title": "Braided 4K 60Hz HDMI 2.0 Cable 6 Feet Gold-Plated Connectors",
            "features": [
                "Supports 4K UHD video at 60Hz and 18Gbps bandwidth.",
                "Nylon braided cable jacket for bend durability.",
                "Corrosion-resistant gold plated connectors."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Plugged into my 4K monitor and got clean 60Hz HDR output immediately.", "id": "r1"},
                {"text": "The braided nylon casing is thick and prevents kinking.", "id": "r2"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c09",
            "category": "Sports",
            "title": "High Density Non-Slip Yoga Mat 6mm with Carrying Strap",
            "features": [
                "Eco-friendly TPE material free of PVC and toxic chemicals.",
                "6mm extra thick cushioning for joint protection.",
                "Dual-sided textured non-slip surface."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Does not slip on wooden floors even during intense sweaty workouts.", "id": "r1"},
                {"text": "The 6mm thickness gives good knee cushioning without feeling unstable.", "id": "r2"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },
        {
            "product_id": "bench_c10",
            "category": "Apparel",
            "title": "100% Combed Cotton Crewneck T-Shirt Pre-Shrunk",
            "features": [
                "Made from 100% ring-spun combed cotton fabric.",
                "Pre-shrunk fabric to maintain size after washing.",
                "Tagless collar design for itch-free comfort."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Washed it twice in warm water and it did not shrink at all.", "id": "r1"},
                {"text": "Very soft cotton material, no scratchy neck tags.", "id": "r2"}
            ],
            "ground_truth_classification": "CONSISTENT"
        },

        # =====================================================================
        # CATEGORY 2: CONTRADICTORY (5 Products)
        # =====================================================================
        {
            "product_id": "bench_k01",
            "category": "Bath",
            "title": "Waterproof Shower Cap with Leakproof Silicone Forehead Seal",
            "features": [
                "100% waterproof double layer nylon material.",
                "Leakproof silicone seal keeps hair completely dry.",
                "Durable elastic band fits all head sizes."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Water seeped through the seams immediately, hair got completely soaked.", "id": "r1"},
                {"text": "Not waterproof at all, the silicone band does not seal and leaks.", "id": "r2"},
                {"text": "The elastic band snapped on the third day of use.", "id": "r3"}
            ],
            "ground_truth_classification": "CONTRADICTORY"
        },
        {
            "product_id": "bench_k02",
            "category": "Accessories",
            "title": "Genuine Full Grain Leather Messenger Laptop Bag 15.6 Inch",
            "features": [
                "100% authentic full grain cowhide leather.",
                "Heavy-duty brass metal zippers that never jam.",
                "Reinforced padded shoulder strap."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "This is cheap synthetic PU plastic leather, not genuine cowhide.", "id": "r1"},
                {"text": "The zipper jammed and teeth split open on the very first week.", "id": "r2"},
                {"text": "Chemical odor is overpowering and the surface started peeling.", "id": "r3"}
            ],
            "ground_truth_classification": "CONTRADICTORY"
        },
        {
            "product_id": "bench_k03",
            "category": "Electronics",
            "title": "Wireless Earbuds 40-Hour Battery Life with Active Noise Cancellation",
            "features": [
                "40 hours total playtime with charging case.",
                "Active Noise Cancellation reduces ambient noise by 35dB.",
                "IPX7 waterproof rating against sweat and rain."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Battery barely lasts 3 hours on a full charge, nowhere near 40 hours.", "id": "r1"},
                {"text": "Noise cancellation does not work at all, background hum is completely audible.", "id": "r2"},
                {"text": "Left earbud died after light sweat at the gym, not waterproof.", "id": "r3"}
            ],
            "ground_truth_classification": "CONTRADICTORY"
        },
        {
            "product_id": "bench_k04",
            "category": "Kitchen",
            "title": "Non-Stick Ceramic Frying Pan Scratch Resistant PTFE Free",
            "features": [
                "Ultra-durable scratch resistant ceramic coating.",
                "100% non-stick surface requires zero cooking oil.",
                "Dishwasher safe and metal utensil safe."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Everything sticks to this pan, food burned onto the ceramic surface.", "id": "r1"},
                {"text": "The coating scratched immediately when using a normal wooden spatula.", "id": "r2"}
            ],
            "ground_truth_classification": "CONTRADICTORY"
        },
        {
            "product_id": "bench_k05",
            "category": "Home",
            "title": "100% Blackout Thermal Insulated Window Curtains Set of 2",
            "features": [
                "100% total room darkening blackout fabric.",
                "Thermal insulated lining reduces outside noise and heat.",
                "Machine washable without fading."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Sunlight shines right through the thin fabric, definitely not 100% blackout.", "id": "r1"},
                {"text": "Does not block outside light or heat, very flimsy material.", "id": "r2"}
            ],
            "ground_truth_classification": "CONTRADICTORY"
        },

        # =====================================================================
        # CATEGORY 3: MIXED EVIDENCE (5 Products)
        # =====================================================================
        {
            "product_id": "bench_m01",
            "category": "Accessories",
            "title": "Rigohill Doger Olive Green RFID Leather Wallet for Men",
            "features": [
                "The wallet is made of natural genuine leather.",
                "Features 7 credit card slots and 2 currency compartments.",
                "Equipped with advanced RFID blocking technology.",
                "Durable craftsmanship with sturdy stitching."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Finishing is neat and it has nearly 8 compartments for cards and cash.", "id": "r1"},
                {"text": "The stitching and overall build quality are also impressive for the price.", "id": "r2"},
                {"text": "Leather quality not good at all, feels very cheap and flimsy.", "id": "r3"},
                {"text": "Color washed off and has uneven stains on the outer surface.", "id": "r4"}
            ],
            "ground_truth_classification": "MIXED EVIDENCE"
        },
        {
            "product_id": "bench_m02",
            "category": "Electronics",
            "title": "Mechanical Gaming Keyboard RGB Backlit with Blue Switches",
            "features": [
                "Clicky tactile blue mechanical switches rated for 50M keystrokes.",
                "Customizable RGB backlighting with 18 lighting modes.",
                "Solid aluminum alloy top frame construction.",
                "Detachable ergonomic wrist rest included."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "The mechanical keys feel great with sharp tactile response and loud clicks.", "id": "r1"},
                {"text": "RGB lighting modes are vibrant and easy to configure.", "id": "r2"},
                {"text": "The wrist rest is cheap plastic and the magnetic clip snapped off.", "id": "r3"}
            ],
            "ground_truth_classification": "MIXED EVIDENCE"
        },
        {
            "product_id": "bench_m03",
            "category": "Apparel",
            "title": "Winter Waterproof Thermal Snow Jacket with Detachable Hood",
            "features": [
                "Waterproof breathable outer shell keeps you dry.",
                "Thick fleece lining provides warmth down to -10C.",
                "Heavy-duty metal front zipper.",
                "True to size standard athletic fit."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Very warm jacket, the fleece interior kept me warm in freezing wind.", "id": "r1"},
                {"text": "Waterproof shell kept snow and moisture out completely.", "id": "r2"},
                {"text": "Sizing is completely wrong; ordered a Large and it fits like a tight Small.", "id": "r3"}
            ],
            "ground_truth_classification": "MIXED EVIDENCE"
        },
        {
            "product_id": "bench_m04",
            "category": "Home",
            "title": "Memory Foam Orthopedic Pillow with Breathable Bamboo Cover",
            "features": [
                "High density contour memory foam for neck pain relief.",
                "Washable cooling bamboo fiber pillowcase cover.",
                "Zero chemical odor and hypoallergenic design."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "The contour shape supported my neck and relieved morning stiffness.", "id": "r1"},
                {"text": "The bamboo pillow cover feels cool to the touch and washes easily.", "id": "r2"},
                {"text": "Had a strong pungent chemical smell that took two weeks to air out.", "id": "r3"}
            ],
            "ground_truth_classification": "MIXED EVIDENCE"
        },
        {
            "product_id": "bench_m05",
            "category": "Office",
            "title": "Ergonomic Mesh Office Desk Chair with Lumbar Support",
            "features": [
                "Breathable mesh backrest prevents sweat accumulation.",
                "Adjustable lumbar support pad for lower back.",
                "Heavy-duty nylon base supports up to 300 lbs.",
                "Quick 15-minute easy assembly with included tools."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "The mesh back is cool and comfortable during long 8-hour workdays.", "id": "r1"},
                {"text": "Lumbar support adjustment works well for my lower back.", "id": "r2"},
                {"text": "The screw holes did not align properly, took over an hour to assemble.", "id": "r3"}
            ],
            "ground_truth_classification": "MIXED EVIDENCE"
        },

        # =====================================================================
        # CATEGORY 4: INSUFFICIENT EVIDENCE (5 Products)
        # =====================================================================
        {
            "product_id": "bench_i01",
            "category": "Electronics",
            "title": "Solar Powered Wireless Outdoor Security Camera 2K Color Night Vision",
            "features": [
                "Continuous solar power charging with 3W panel.",
                "2K QHD resolution with color night vision spotlight.",
                "PIR motion detection with AI human recognition.",
                "IP66 weatherproof rating for extreme rain and heat."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Package arrived on time. Have not installed it yet.", "id": "r1"},
                {"text": "Nice looking box, will update review after testing.", "id": "r2"}
            ],
            "ground_truth_classification": "INSUFFICIENT EVIDENCE"
        },
        {
            "product_id": "bench_i02",
            "category": "Health",
            "title": "Organic Cold-Pressed Rosemary Essential Oil 60ml for Hair Growth",
            "features": [
                "100% pure organic cold-pressed rosemary oil.",
                "Stimulates hair follicles and reduces dandruff.",
                "Comes with glass dropper applicator."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Bottle was wrapped securely in bubble wrap.", "id": "r1"}
            ],
            "ground_truth_classification": "INSUFFICIENT EVIDENCE"
        },
        {
            "product_id": "bench_i03",
            "category": "Kitchen",
            "title": "Precision Electric Coffee Grinder with 35 Grind Settings",
            "features": [
                "Stainless steel conical burr grinder mechanism.",
                "35 precise settings from French press coarse to espresso fine.",
                "Anti-static chamber prevents coffee powder scattering."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Bought this as a birthday present for my brother.", "id": "r1"},
                {"text": "Fast shipping from the seller.", "id": "r2"}
            ],
            "ground_truth_classification": "INSUFFICIENT EVIDENCE"
        },
        {
            "product_id": "bench_i04",
            "category": "Tools",
            "title": "Cordless Rotary Tool Kit with 50 Accessories and Variable Speed",
            "features": [
                "Powerful motor with 5 variable speed settings up to 25000 RPM.",
                "Rechargeable lithium-ion battery via USB-C.",
                "Includes 50 pieces cutting, grinding, and polishing bits."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [],
            "ground_truth_classification": "INSUFFICIENT EVIDENCE"
        },
        {
            "product_id": "bench_i05",
            "category": "Automotive",
            "title": "Digital Tire Pressure Gauge 150 PSI with Backlit LCD Screen",
            "features": [
                "Accurate pressure measurement up to 150 PSI within 1% margin.",
                "Backlit LCD display and lighted nozzle for dark conditions.",
                "Automatic shut-off after 30 seconds to conserve battery."
            ],
            "seller_images": [],
            "customer_images": [],
            "customer_reviews": [
                {"text": "Color matches my car interior.", "id": "r1"}
            ],
            "ground_truth_classification": "INSUFFICIENT EVIDENCE"
        }
    ]

    with open(BENCHMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)

    print(f"Benchmark dataset successfully generated: {len(products)} products saved to {BENCHMARK_FILE}")
    return products

if __name__ == "__main__":
    generate_benchmark_dataset()
