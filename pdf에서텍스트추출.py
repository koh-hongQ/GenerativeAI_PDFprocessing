import fitz  # PyMuPDF

# 문서 열기
doc = fitz.open(r"d:\고홍규\2025 한국외대 수학과 2학년 2학기\Quiz생성ai 프로젝트\OSS9.pdf")

# 전체 페이지 반복
for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    text = page.get_text("text")
    print(f"\n📄 [페이지 {page_number + 1}] ===============================\n")
    print(text.strip())

# 문서 닫기
doc.close()
