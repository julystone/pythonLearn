import re

def fix_scan_linebreaks(text, line_length=60):
    """
    修复OCR扫描文本的异常换行问题
    :param text: 原始文本内容
    :param line_length: 正常段落行最大长度（默认60字）
    :return: 修复后的文本内容
    """
    lines = text.split('\n')
    cleaned = []
    buffer = []
    
    for line in lines:
        stripped = line.strip()
        
        # # 处理空行
        # if not stripped:
        #     if buffer:
        #         cleaned.append(''.join(buffer).strip() + '\n\n')
        #         buffer = []
        #     cleaned.append('\n')
        #     continue
        
        # 检测非法换行（中文标点检测）
        if not re.match(r'^[\u4e00-\u9fff]+[。？！”’]$', stripped):
            buffer.append(stripped)
            cleaned.append(''.join(buffer).strip())
            buffer = []
        elif stripped == '\n':
            pass
        else:
            pass
    
    # 移除多余空行
    result = []
    for para in cleaned:
        if para.strip():
            result.append(para)
        else:
            result.append('\n')
    
    return ''.join(result).strip()

# 使用示例
with open('favorite/test.txt', 'r', encoding='utf-8') as f:
    original_text = f.read()

fixed_text = fix_scan_linebreaks(original_text)
with open('./fixed_test.txt', 'w', encoding='utf-8') as f:
    f.write(fixed_text)