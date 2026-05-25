import re
import sys
import io

# Setup UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

structure_file = r'D:\Kê hoạch sản xuât\laptrinh vao\scripts\plan_xlsm_structure.txt'
output_file = r'D:\Kê hoạch sản xuât\laptrinh vao\scripts\core_sheets_preview.txt'

def extract_previews():
    with open(structure_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by sheets
    sheets = re.split(r'--- SHEET: (.*?) ---', content)
    
    # sheets[0] is the header before the first sheet
    header = sheets[0]
    
    previews = []
    previews.append(header)
    
    # sheets has pairs of (sheet_name, sheet_body)
    for i in range(1, len(sheets), 2):
        sheet_name = sheets[i]
        sheet_body = sheets[i+1]
        
        # Split body into lines
        lines = sheet_body.strip().split('\n')
        
        # Get sheet info and first 30 data rows
        info_lines = []
        data_lines = []
        
        for line in lines:
            if line.startswith('Kích thước ước tính:') or line.startswith('Chi tiết nội dung'):
                info_lines.append(line)
            elif line.strip().startswith('Dòng'):
                data_lines.append(line)
        
        preview = f"--- SHEET: {sheet_name} ---\n"
        preview += "\n".join(info_lines) + "\n"
        preview += "\n".join(data_lines[:30]) + "\n"
        preview += f"... (hiển thị 30/{len(data_lines)} dòng dữ liệu) ...\n"
        preview += "="*60 + "\n\n"
        
        previews.append(preview)
        
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("".join(previews))
        
    print(f"Đã trích xuất bản xem trước vào {output_file}")

if __name__ == '__main__':
    extract_previews()
