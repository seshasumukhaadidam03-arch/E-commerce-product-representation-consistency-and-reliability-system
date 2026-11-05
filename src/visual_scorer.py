import cv2
import numpy as np
import requests
from skimage.metrics import structural_similarity as ssim
from io import BytesIO
from PIL import Image

class VisualScorer:
    def __init__(self):
        print("Visual Scorer initialized (Using OpenCV).", flush=True)

    def download_image(self, url):
        """Downloads an image from a URL and converts it to a numpy array for OpenCV."""
        try:
            # Add a fake User-Agent so websites don't block us as a bot
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            img = Image.open(BytesIO(response.content)).convert('RGB')
            return np.array(img)
        except Exception as e:
            print(f"  [ERROR] Could not download image {url}: {e}")
            return None

    def check_visual_consistency(self, seller_url, customer_url):
        """
        Compares two images using Color (LAB) and Structure (SSIM).
        Returns a consistency score from 0 to 100.
        """
        # 1. Download images
        img1 = self.download_image(seller_url)
        img2 = self.download_image(customer_url)

        if img1 is None or img2 is None:
            return {"error": "Failed to load images."}

        # 2. Resize to the exact same dimensions so math works
        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))

        # ==========================================
        # TEST A: COLOR CONSISTENCY
        # ==========================================
        # Convert RGB to LAB (LAB separates brightness from actual color)
        lab1 = cv2.cvtColor(img1, cv2.COLOR_RGB2LAB)
        lab2 = cv2.cvtColor(img2, cv2.COLOR_RGB2LAB)
        
        # Get the average color of the whole image
        avg_color1 = np.mean(lab1, axis=(0, 1))
        avg_color2 = np.mean(lab2, axis=(0, 1))
        
        # Calculate the distance between the two colors (Euclidean distance)
        color_diff = np.linalg.norm(avg_color1 - avg_color2)
        
        # Normalize to a 0-100 score (rough approximation)
        color_match_score = max(0, 100 - (color_diff / 2.55))

        # ==========================================
        # TEST B: STRUCTURAL SIMILARITY (EDGES)
        # ==========================================
        # Convert to Grayscale (black and white) for shape comparison
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        
        # Run the SSIM algorithm
        score, _ = ssim(gray1, gray2, full=True)
        # SSIM returns a decimal (e.g., 0.85). Convert to percentage.
        structure_match_score = max(0, score * 100)

        # ==========================================
        # FINAL SCORE
        # ==========================================
        # We weigh Structure at 60% and Color at 40%
        # Why? Because customer room lighting often ruins the color, 
        # so structure is slightly more trustworthy!
        overall_visual_score = (color_match_score * 0.4) + (structure_match_score * 0.6)

        return {
            "color_score": round(color_match_score, 1),
            "structure_score": round(structure_match_score, 1),
            "overall_score": round(overall_visual_score, 1)
        }

# ==========================================
# TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    scorer = VisualScorer()
    
    # Let's test it with two generated images
    # Image 1: A bright RED square with text
    img_red = "https://dummyimage.com/256x256/ff0000/ffffff.png&text=Product+A"
    
    # Image 2: A bright GREEN square with text
    img_green = "https://dummyimage.com/256x256/00ff00/ffffff.png&text=Product+A"
    
    # Image 3: The exact same RED square, but blurry/lower quality
    img_red_copy = "https://dummyimage.com/256x256/ff0000/ffffff.png&text=Product+A"

    print("\n" + "="*50)
    print("TEST 1: Red Product vs Green Product (Should fail color)")
    print("="*50)
    result_diff = scorer.check_visual_consistency(img_red, img_green)
    print(f"Color Match:     {result_diff['color_score']}%")
    print(f"Structure Match: {result_diff['structure_score']}%")
    print(f"OVERALL VISUAL:  {result_diff['overall_score']}%")

    print("\n" + "="*50)
    print("TEST 2: Exact Same Product (Should be 100%)")
    print("="*50)
    result_same = scorer.check_visual_consistency(img_red, img_red_copy)
    print(f"Color Match:     {result_same['color_score']}%")
    print(f"Structure Match: {result_same['structure_score']}%")
    print(f"OVERALL VISUAL:  {result_same['overall_score']}%")
