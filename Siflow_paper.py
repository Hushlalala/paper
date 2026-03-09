from openai import OpenAI
import arxiv
import datetime
import pushplus
import gemini_paper

# 1. 初始化客户端 (关键步骤) 
client = OpenAI(
    api_key="sk-htkcnuaxflzfmhtlbhsdazhtxhmydbrqmtlnncfjaeotuyby",    #配置部分：请在此处填入你的 SiliconFlow API Key
    base_url="https://api.siliconflow.cn/v1"
)

def get_latest_papers(topic, max_results=3):   #="abs:optimal control AND abs:PINN OR dynamics"
    """从 ArXiv 获取指定主题的最新论文"""
    print(f"正在检索关于 {topic} 的最新论文...")

    # 构建查询：按提交时间倒序排列    
    search = arxiv.Search( 
        query=topic,
        max_results=max_results, 
        sort_by=arxiv.SortCriterion.SubmittedDate
        )

    papers_data = []
    for result in search.results(): 
        papers_data.append({
        "title": result.title,
        "abstract": result.summary,
        "url": result.entry_id,
        "published": result.published
        })
    
    return papers_data


# 选择一篇论文
def generate_summary(paper):    
    paper_abstract = paper["abstract"]
    paper_title = paper["title"]

    # 3. 构建提示词 (Prompt)
    prompt = f"请将以下英文论文摘要翻译成中文，并提炼出三个核心贡献点,同时给出论文的三个关键词：\n\n标题：{paper_title}\n摘要：{paper_abstract}"

    # 4. 调用 API 生成论文解读
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3.1-Terminus",
        messages=[
        {"role": "system", "content": "你是一位专业的学术翻译和总结助手。"},
        {"role": "user", "content": prompt}
        ],
    temperature=0.3,
    )
    return response.choices[0].message.content


# pushplus 相关配置
token = 'e8979a20686f4175b2e2cc509d732a48'

def main(): 
    # 1. 获取论文    
    # 你可以修改 topic 参数来关注不同的领域，例如 "Multimodal AI"    
    papers = gemini_paper.get_latest_papers(topic="robot AND (model predictive control OR optimal control OR reinforcement learning OR deep learning OR neural network ) OR locomotion", max_results=3)
    daily_report = f"# 📅 AI 前沿论文日报 ({datetime.date.today()})\n\n"

    # 2. 逐篇处理    
    for paper in papers:
        summary = generate_summary(paper)

        # 拼接内容        
        daily_report += f"{summary}\n" 
        daily_report += f"🔗 **原文链接**: {paper['url']}\n" 
        daily_report += "---\n\n"
    # 3. 输出结果（实际部署时这里可以替换为发送邮件或推送到微信的代码）    
    print("\n" + "="*20 + " 生成结果 " + "="*20 + "\n") 
    print(daily_report)
    # 推送日报到微信  如果不需要注释掉这行
    pushplus.send_pushplus_message(token, f"AI 前沿论文日报 ({datetime.date.today()})", daily_report)

if __name__ == "__main__": 
    main()
