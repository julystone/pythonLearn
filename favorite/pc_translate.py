from openai import OpenAI
import os

# 硅基流动配置
# os.environ["OPENAI_API_KEY"] = "sk-siliconflow-key"
# os.environ["OPENAI_API_BASE"] = "https://api.siliconflow.cn/v1"

client = OpenAI(
    api_key="sk-ncynwnubqwrxrayajpyalntslydfumgiarvbbepcdnbljvid",
    base_url="https://api.siliconflow.cn/v1"  # DeepSeek专用接口[3](@ref)
)

def translate_to_chinese(text, target_lang="zh"):
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",  # 硅基流动推荐模型[7](@ref)
            messages=[
                {"role": "system", "content": "prompt翻译润色助手"},
                {"role": "user", "content": f"将以下文本翻译并润色为AIprompt：\n{text}"}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"翻译失败: {str(e)}")
        return None

# 使用示例
text = "一位黑发，长发，美丽的女教师，站在讲台上，微笑着，手捧着瑞幸咖啡，站立在讲台旁，夏日服饰，知性风格，空教室就她一人，镜头不正对着她正脸，而是侧面拍摄，令人感到神秘。她的声音很低沉，但却很有力量，像是一位独特的声音。她的眼神也很独特，像是一位探索者，探索着这个世界，探索着她的内心世界。她的动作也很独特，像是一位艺术家，用笔触绘出她的创作。"
print(translate_to_chinese(text, "zh"))