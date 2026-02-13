import re
from collections import defaultdict


class TestFunctionClasses():

    def __init__(self, ocr_data):
        self.ocr_data = ocr_data # Instance attribute
        self.KEY_PATTERNS = {
            "invoice_no": [
                r"invoice\s*no\.?",
                r"invoice\s*number"
            ],
            "invoice_date": [
                r"invoice\s*date"
            ],
            "supplier_gst": [
                r"gst\s*no\.?",
                r"gstin"
            ],
            "state_code": [
                r"state\s*code"
            ],
            "order_no": [
                r"order\s*no\.?"
            ],
            "order_date": [
                r"order\s*date"
            ],
            "pan": [
                r"pan\s*no\.?"
            ]
        }

    def build_lines_from_ocr(self, ocr_data):
        """
        Convert word-level OCR into line level structure text
        """

        self.lines = defaultdict(list)

        self.n = len(ocr_data["text"])

        for i in range(self.n):
            if ocr_data["level"][i] == 5:    # WORD
                self.key = (
                    ocr_data["block_num"][i],
                    ocr_data["par_num"][i],
                    ocr_data["line_num"][i]
                )

                self.lines[self.key].append({
                    "text": ocr_data["text"][i],
                    "left": ocr_data["left"][i],
                    "top": ocr_data["top"][i],
                    "width": ocr_data["width"][i],
                    "height": ocr_data["height"][i]
                })

        # Sort words lift-to-right and merge text
        self.line_data = []

        for key, words in self.lines.items():
            self.words = sorted(words, key=lambda x: x["left"])
            self.line_text = " ".join(w["text"] for w in words if w["text"].strip())

            x1 = min(w["left"] for w in words)
            y1 = min(w["top"] for w in words)
            x2 = min(w["left"] + w["width"] for w in words)
            y2 = min(w["top"] + w["height"] for w in words)

            self.line_data.append({
                "text": self.line_text,
                "bbox": [x1, y1, x2, y2]
            })


        return self.line_data

    # Step 2: Find ALL keys inside a line
    def find_keys_in_line(self, line_text, key_patterns):
        self.matches = []

        for field, patterns in key_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, line_text, re.IGNORECASE):
                    
                    self.matches.append({
                        "field": field,
                        "start": match.start(),
                        "end": match.end()
                    })

        return sorted(self.matches, key=lambda x: x["start"])



    # Step 3: Extract VALUES between keys (CRITICAL STEP)
    def extract_key_value_pairs_from_line(self, line_object):
        """
        line_obj = {
            "text": "...",
            "bbox": [x1, y1, x2, y2]
        }
        """

        # 🔐 Defensive guard
        if isinstance(line_object, list):
            self.results = []
            for obj in line_object:
                if isinstance(obj, dict):
                    self.results.extend(self.extract_key_value_pairs_from_line(obj))
            return self.results

        if not isinstance(line_object, dict):
            return []

        self.line_text = line_object.get("text", "")
        self.line_bbox = line_object.get("bbox", None)

        if not isinstance(self.line_text, str):
            return []

        self.key_matches = self.find_keys_in_line(self.line_text, self.KEY_PATTERNS)
        self.extracted = []

        for i, key in enumerate(self.key_matches):
            value_start = key["end"]

            if i + 1 < len(self.key_matches):
                value_end = self.key_matches[i + 1]["start"]
            else:
                value_end = len(self.line_text)

            value = self.line_text[value_start:value_end]
            value = value.replace(":", "").strip()

            if not value:
                continue

            # ✅ SINGLE combined bbox (key + value)
            combined_bbox = [
                self.line_bbox[0],  # x1
                self.line_bbox[1],  # y1
                self.line_bbox[2],  # x2
                self.line_bbox[3]   # y2
            ]

            # TYPE - 1
            self.extracted.append({
                "key": key["field"],
                "value": value,
                "bbox": combined_bbox
            })

            # # TYPE - 2
            # self.extracted.append({
            #     key["field"]: value,
            #     "bbox": combined_bbox
            # })

        return self.extracted
