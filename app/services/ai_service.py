"""
AI 服务模块
提供 OpenAI API 调用功能，用于生成笔记摘要
"""

import os
import logging
from typing import Optional
from openai import OpenAI
from app.core.config import get_settings
import httpx
import certifi  # 导入 Poetry 环境的 certifi 库

# 使用 Poetry 环境自带的 SSL 证书（certifi.where() 会返回正确路径）
ssl_cert_path = certifi.where()

# 创建指定证书的 HTTP 客户端
http_client = httpx.Client(verify=ssl_cert_path)

logger = logging.getLogger(__name__)


class AIService:
    """AI 服务类，处理 OpenAI API 调用"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self._init_openai_client()
    
    def _init_openai_client(self):
        """初始化 OpenAI 客户端"""
        api_key = self.settings.OPENAI_API_KEY
        if not api_key:
            logger.warning("未配置 OPENAI_API_KEY，AI 摘要功能将不可用")
            return
        
        try:
            self.client = OpenAI(api_key=api_key, base_url=self.settings.OPENAI_BASE_URL, http_client=http_client)
            logger.info("OpenAI 客户端初始化成功")
        except Exception as e:
            logger.error("OpenAI 客户端初始化失败: {}".format(str(e)))
            self.client = None
    
    def generate_note_summary(self, content: str, title: str = "") -> str:
        """
        生成笔记摘要
        
        Args:
            content: 笔记内容（Markdown 格式）
            title: 笔记标题（可选）
        
        Returns:
            str: 生成的摘要（≤200字），失败时返回默认提示
        """
        if not self.client:
            return self._get_default_summary(content, title)
        
        try:
            # 构建提示词
            prompt = self._build_summary_prompt(content, title)
            
            # 调用 OpenAI API
            response = self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的笔记摘要助手，能够准确提取笔记的核心要点。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,  # 控制输出长度
                temperature=0.3,  # 降低随机性，提高一致性
                top_p=0.9
            )
            
            summary = response.choices[0].message.content.strip()
            
            # 验证摘要长度
            if len(summary) > 200:
                summary = summary[:197] + "..."
            
            logger.info("AI 摘要生成成功，长度: {} 字符".format(len(summary)))
            return summary
            
        except Exception as e:
            logger.error("AI 摘要生成失败: {}".format(str(e)))
            return self._get_default_summary(content, title)
    
    def _build_summary_prompt(self, content: str, title: str) -> str:
        """
        构建摘要生成的提示词
        
        Args:
            content: 笔记内容
            title: 笔记标题
        
        Returns:
            str: 格式化的提示词
        """
        if title:
            prompt = "请为以下笔记生成一个简洁的摘要（不超过200字）：\n\n标题：{}\n\n内容：{}\n\n要求：\n1. 提取核心要点和关键信息\n2. 保持客观准确\n3. 使用简洁明了的语言\n4. 不超过200字".format(title, content)
        else:
            prompt = "请为以下笔记生成一个简洁的摘要（不超过200字）：\n\n{}\n\n要求：\n1. 提取核心要点和关键信息\n2. 保持客观准确\n3. 使用简洁明了的语言\n4. 不超过200字".format(content)
        
        return prompt
    
    def _get_default_summary(self, content: str, title: str) -> str:
        """
        获取默认摘要（当 AI 服务不可用时）
        
        Args:
            content: 笔记内容
            title: 笔记标题
        
        Returns:
            str: 默认摘要
        """
        # 简单的文本截取逻辑
        text_content = content.replace('#', '').replace('*', '').replace('`', '')
        text_content = ' '.join(text_content.split())  # 去除多余空格
        
        if title:
            summary = "{}：{}".format(title, text_content[:150])
        else:
            summary = text_content[:150]
        
        if len(summary) > 200:
            summary = summary[:197] + "..."
        
        logger.info("使用默认摘要生成，长度: {} 字符".format(len(summary)))
        return summary
    
    def is_available(self) -> bool:
        """
        检查 AI 服务是否可用
        
        Returns:
            bool: 服务可用性状态
        """
        return self.client is not None and self.settings.OPENAI_API_KEY is not None


# 全局 AI 服务实例
ai_service = AIService()


def get_ai_service() -> AIService:
    """
    获取 AI 服务实例
    
    Returns:
        AIService: AI 服务实例
    """
    return ai_service


def generate_note_summary(content: str, title: str = "") -> str:
    """
    便捷函数：生成笔记摘要
    
    Args:
        content: 笔记内容
        title: 笔记标题
    
    Returns:
        str: 生成的摘要
    """
    return ai_service.generate_note_summary(content, title) 