from aip import AipOcr  # type: ignore
import os
import requests
import json

# 配置百度云API信息
APP_ID = '119944815'
API_KEY = 'X6taHnuak7oUVLmTmNhKDh3L'
SECRET_KEY = 'vOPlWhqsWFAvaCFGQiWq94nxp00BKh8I'

# 初始化AipOcr对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_access_token():
    """获取百度AI开放平台的访问令牌"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("获取访问令牌失败")
        return None

def ai_analyze_text(text, question, access_token):
    """使用百度AI对话接口分析文本，要求包含26个字母"""
    if not access_token:
        return None, "未获取到访问令牌"
    
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
    
    # 构建对话内容，新增要求包含26个字母的提示
    messages = [
        {"role": "system", "content": "你是一个智能助手，需要根据提供的文本内容回答问题。"
                                      "特别注意：回答中必须包含26个英文字母（A-Z），可以按顺序或穿插在内容中。"},
        {"role": "user", "content": f"文本内容：{text}\n请根据以上文本回答：{question}"}
    ]
    
    payload = json.dumps({
        "messages": messages
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        
        if "error_code" in result:
            return None, f"AI分析错误: {result['error_msg']}"
            
        # 提取AI回答
        answer = result.get("result", "无法获取有效回答")
        return answer, None
    except Exception as e:
        return None, f"AI分析过程出错: {str(e)}"

def get_file_content(file_path):
    """读取图片文件内容"""
    with open(file_path, 'rb') as fp:
        return fp.read()

def recognize_text(image_path):
    """识别图片中的文字"""
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：文件 {image_path} 不存在")
        return None
    
    # 读取图片内容
    image = get_file_content(image_path)
    
    # 调用通用文字识别（高精度版）
    result = client.basicAccurate(image)
    
    # 处理识别结果
    if 'words_result' in result:
        return '\n'.join([item['words'] for item in result['words_result']])
    else:
        print(f"识别失败：{result.get('error_msg', '未知错误')}")
        return None

if __name__ == '__main__':
    # 图片路径
    image_path = 'C:/Users/86191/Desktop/p479558.png'
    
    # 进行文字识别
    text = recognize_text(image_path)
    
    # 输出识别结果
    if text:
        print("识别结果：")
        print(text)
        print("\n" + "-"*50 + "\n")
        
        # 获取访问令牌
        access_token = get_access_token()
        
        if access_token:
            # 可以根据需要修改问题
            question = "请总结这段文字的主要内容，并指出其中的关键信息"
            
            # 使用AI分析文本
            ai_answer, error = ai_analyze_text(text, question, access_token)
            
            if error:
                print(f"AI分析失败：{error}")
            else:
                print("AI分析结果（包含26个字母）：")
                print(ai_answer)
        else:
            print("无法获取AI服务访问令牌，无法进行分析")
