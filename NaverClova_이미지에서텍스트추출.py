
import fitz  # PyMuPDF
import os
from PIL import Image
import pytesseract
from datetime import datetime
import base64
import requests
import json
import uuid
import time
from collections import defaultdict

# Tesseract 언어 설정 (한글 + 영어)
tesseract_lang = "kor+eng"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 네이버클로바OCR API
secret_key = "API입력하시오"  # 클로바 OCR 시크릿 키
api_url = "API입력하시오"  # 클로바 OCR 엔드포인트 URL


# 추출할 파일
doc = fitz.open(r"d:\고홍규\2025 한국외대 수학과 2학년 2학기\Quiz생성ai 프로젝트\열역학.pdf")



# 현재 시간으로 이미지저장폴더명 생성
now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
output_folder = os.path.join(
    r"d:\고홍규\2025 한국외대 수학과 2학년 2학기\Quiz생성ai 프로젝트", f"추출_{now_str}"
)
os.makedirs(output_folder, exist_ok=True)



# # 이미지 추출 (모든 페이지)
# for page_num in range(len(doc)):
#     page = doc.load_page(page_num)
#     images = page.get_images(full=True)

#     for img_index, img in enumerate(images):
#         xref = img[0]
#         pix = fitz.Pixmap(doc, xref)

#         # RGB 아닌 경우 변환
#         if pix.n > 4:
#             pix = fitz.Pixmap(fitz.csRGB, pix)

#         image_filename = os.path.join(output_folder, f"page{page_num+1}_img{img_index+1}.png")
#         pix.save(image_filename)
#         print(f"[✔] 저장됨: {image_filename}")

# # 이미지 추출정보
# for img in page.get_images():
#     print("[이미지 정보]", img)

# 이미지 추출 (특정 페이지만)
target_page = 4  # 예: 5페이지 (0부터 시작하므로 4)
page = doc.load_page(target_page)
images = page.get_images(full=True)
for img_index, img in enumerate(images):
    xref = img[0]
    pix = fitz.Pixmap(doc, xref)

    # RGB 아닌 경우 변환
    if pix.n > 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)

    image_filename = os.path.join(output_folder, f"page{target_page+1}_img{img_index+1}.png")
    pix.save(image_filename)
    print(f"[✔] 저장됨: {image_filename}")

# 이미지 추출 정보
for img in images:
    print("[이미지 정보]", img)

# # 이미지에서 텍스트 추출 후 저장 (테서랙트 방법=일단 폐기)
# for filename in os.listdir(output_folder):
#     if filename.endswith(".png"):
#         image_path = os.path.join(output_folder, filename)
#         img = Image.open(image_path)

#         # OCR 수행
#         extracted_text = pytesseract.image_to_string(img, lang=tesseract_lang)

#         # 텍스트 파일로 저장 (같은 이름으로 .txt 확장자)
#         txt_filename = filename.rsplit(".", 1)[0] + ".txt"
#         txt_path = os.path.join(output_folder, txt_filename)
#         with open(txt_path, "w", encoding="utf-8") as f:
#             f.write(extracted_text)

#         print(f"[✔] OCR 텍스트 저장됨: {txt_path}")


# # 이미지에서 텍스트 추출 후 저장 (네이버 클로바)
# for filename in os.listdir(output_folder):
#     if filename.endswith(".png"):
#         image_path = os.path.join(output_folder, filename)

#         # 이미지 base64 인코딩
#         with open(image_path, "rb") as image_file:
#             encoded_image = base64.b64encode(image_file.read()).decode()

#         # JSON 페이로드 구성
#         request_json = {
#             "version": "V2",
#             "requestId": str(uuid.uuid4()),
#             "timestamp": int(round(time.time() * 1000)),
#             "images": [
#                 {
#                     "name": "demo",
#                     "format": "png",
#                     "data": encoded_image
#                 }
#             ]
#         }

#         headers = {
#             "Content-Type": "application/json",
#             "X-OCR-SECRET": secret_key
#         }

#         # OCR 요청
#         response = requests.post(api_url, headers=headers, json=request_json)
#         result = response.json()


#         # OCR 결과에서 텍스트 줄 단위로 정렬
#         try:
#             fields = result['images'][0]['fields']
#             # y값 기준 정렬
#             fields.sort(key=lambda x: x['boundingPoly']['vertices'][0]['y'])

#             # 텍스트 합치기 (한 줄씩 줄바꿈)
#             extracted_text = "\n".join(field['inferText'] for field in fields)

#         except Exception as e:
#             extracted_text = "[오류 발생] 텍스트 추출 실패"
#             print(f"❌ {filename}: {e}")

#         # 텍스트 저장
#         txt_filename = filename.rsplit(".", 1)[0] + ".txt"
#         txt_path = os.path.join(output_folder, txt_filename)
#         with open(txt_path, "w", encoding="utf-8") as f:
#             f.write(extracted_text)

#         print(f"[✔] OCR 텍스트 저장됨: {txt_path}")


# 두 글자 블록이 같은 줄에 있다고 판단할 최대 y 좌표 차이 (픽셀 단위)
LINE_THRESHOLD = 15

def get_y_center(field):
    vertices = field["boundingPoly"]["vertices"]
    y_coords = [v["y"] for v in vertices]
    return sum(y_coords) / len(y_coords)

def get_x_min(field):
    return min(v["x"] for v in field["boundingPoly"]["vertices"])

for filename in os.listdir(output_folder):
    if filename.endswith(".png"):
        image_path = os.path.join(output_folder, filename)

        # 이미지 base64 인코딩
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        # JSON 요청 구성
        request_json = {
            "version": "V2",
            "requestId": str(uuid.uuid4()),
            "timestamp": int(round(time.time() * 1000)),
            "images": [
                {
                    "name": "demo",
                    "format": "png",
                    "data": encoded_image
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "X-OCR-SECRET": secret_key
        }

        # OCR 요청
        response = requests.post(api_url, headers=headers, json=request_json)
        result = response.json()

        try:
            fields = result["images"][0]["fields"]
            lines = []

            # 줄 그룹핑
            for field in fields:
                y_center = get_y_center(field)
                added = False
                for line in lines:
                    if abs(line["y_center"] - y_center) < LINE_THRESHOLD:
                        line["fields"].append(field)
                        added = True
                        break
                if not added:
                    lines.append({"y_center": y_center, "fields": [field]})

            # 줄 순서대로, 각 줄은 x좌표 정렬 후 텍스트 조합
            lines.sort(key=lambda line: line["y_center"])
            extracted_text_lines = []

            for line in lines:
                line["fields"].sort(key=lambda f: get_x_min(f))
                line_text = " ".join(f["inferText"] for f in line["fields"])
                extracted_text_lines.append(line_text)

            extracted_text = "\n".join(extracted_text_lines)

        except Exception as e:
            extracted_text = "[오류 발생] 텍스트 추출 실패"
            print(f"❌ {filename}: {e}")

        # 텍스트 저장
        txt_filename = filename.rsplit(".", 1)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"[✔] OCR 텍스트 저장됨: {txt_path}")

# 텍스트와 주석 저장할 파일 경로
text_output_path = os.path.join(output_folder, "page_text.txt")
# annot_output_path = os.path.join(output_folder, "page_annotations.txt")


# 텍스트 추출
text = ""
for page in doc:
    text += page.get_text() + "\n"
print("[텍스트]", text)

# 텍스트 저장
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(text)
    print(f"[✔] 텍스트 저장됨: {text_output_path}")



