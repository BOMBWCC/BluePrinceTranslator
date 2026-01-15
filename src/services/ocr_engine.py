from rapidocr_onnxruntime import RapidOCR
import numpy as np

class OCREngine:
    def __init__(self):
        # Initialize RapidOCR
        # It automatically downloads models on first run if not present
        self.ocr = RapidOCR()

    def recognize(self, image):
        """
        识别图像中的文本
        image: PIL Image or numpy array
        """
        if image is None:
            return ""

        # Convert PIL Image to numpy array if necessary
        if not isinstance(image, np.ndarray):
            img_np = np.array(image)
        else:
            img_np = image

        # Save debug image to check what we are actually seeing
        try:
            from PIL import Image
            debug_img = Image.fromarray(img_np)
            debug_img.save("debug_ocr.png")
            # print(f"[DEBUG] Saved debug_ocr.png for inspection")
        except Exception as e:
            print(f"[DEBUG] Failed to save debug image: {e}")

        try:
            # RapidOCR returns (result, elapse)
            result, elapse = self.ocr(img_np)
            print(f"[DEBUG] OCR Inference time: {elapse}s")
            
            texts = []
            if result:
                for i, line in enumerate(result):
                    # line structure: [coords, text, confidence]
                    if len(line) >= 2:
                        print(f"[DEBUG] Detected Line {i}: '{line[1]}' (conf: {line[2]})")
                        texts.append(line[1])
            else:
                print("[DEBUG] No text detected by OCR engine.")
            
            return "\n".join(texts)
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

# Initialize engine lazily or as a singleton
_ocr_engine_instance = None

def get_ocr_engine():
    global _ocr_engine_instance
    if _ocr_engine_instance is None:
        _ocr_engine_instance = OCREngine()
    return _ocr_engine_instance