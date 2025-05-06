
import fitz  # PyMuPDF
import os
from PIL import Image
import pytesseract
from datetime import datetime

# Tesseract 언어 설정 (한글 + 영어)
tesseract_lang = "kor+eng"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 추출할 파일
doc = fitz.open(r"d:\고홍규\2025 한국외대 수학과 2학년 2학기\Quiz생성ai 프로젝트\열역학.pdf")



# 현재 시간으로 이미지저장폴더명 생성
now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
output_folder = os.path.join(
    r"d:\고홍규\2025 한국외대 수학과 2학년 2학기\Quiz생성ai 프로젝트", f"추출_text+image+imagetext_{now_str}"
)
os.makedirs(output_folder, exist_ok=True)


# 텍스트와 주석 저장할 파일 경로
text_output_path = os.path.join(output_folder, "page_text.txt")
annot_output_path = os.path.join(output_folder, "page_annotations.txt")


# 이미지 저장
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)

        # RGB 아닌 경우 변환
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)

        image_filename = os.path.join(output_folder, f"page{page_num+1}_img{img_index+1}.png")
        pix.save(image_filename)
        print(f"[✔] 저장됨: {image_filename}")

# 이미지 추출정보
for img in page.get_images():
    print("[이미지 정보]", img)


# 이미지에서 텍스트 추출 후 저장
for filename in os.listdir(output_folder):
    if filename.endswith(".png"):
        image_path = os.path.join(output_folder, filename)
        img = Image.open(image_path)

        # OCR 수행
        extracted_text = pytesseract.image_to_string(img, lang=tesseract_lang)

        # 텍스트 파일로 저장 (같은 이름으로 .txt 확장자)
        txt_filename = filename.rsplit(".", 1)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"[✔] OCR 텍스트 저장됨: {txt_path}")


# 텍스트 추출
text = ""
for page in doc:
    text += page.get_text() + "\n"
print("[텍스트]", text)

# 텍스트 저장
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(text)
    print(f"[✔] 텍스트 저장됨: {text_output_path}")


# # 주석(손글씨 등) 추출
# for annot in text.annots():
#     print("[주석]", annot.info)


# # 주석 저장
# with open(annot_output_path, "w", encoding="utf-8") as f:
#     for annot in text.annots():
#         f.write(str(annot.info) + "\n")
#     print(f"[✔] 주석 저장됨: {annot_output_path}")

