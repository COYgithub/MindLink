"""
AI 服务单元测试
测试 OpenAI API 调用和摘要生成功能
"""

import pytest
from unittest.mock import Mock, patch
from app.services.ai_service import AIService, generate_note_summary


class TestAIService:
    """AI 服务测试类"""
    
    def test_init_without_api_key(self):
        """测试没有 API Key 时的初始化"""
        with patch.dict('os.environ', {}, clear=True):
            service = AIService()
            assert service.client is None
            assert not service.is_available()
    
    def test_init_with_api_key(self):
        """测试有 API Key 时的初始化"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('openai.OpenAI') as mock_openai:
                mock_client = Mock()
                mock_openai.return_value = mock_client
                
                service = AIService()
                assert service.client is not None
                assert service.is_available()
    
    def test_generate_summary_success(self):
        """测试成功生成摘要"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('openai.OpenAI') as mock_openai:
                mock_client = Mock()
                mock_response = Mock()
                mock_response.choices = [Mock()]
                mock_response.choices[0].message.content = "这是一个测试摘要，长度适中。"
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client
                
                service = AIService()
                summary = service.generate_note_summary("测试内容", "测试标题")
                
                assert "测试摘要" in summary
                assert len(summary) <= 200
    
    def test_generate_summary_long_output(self):
        """测试生成超长摘要时的截断"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('openai.OpenAI') as mock_openai:
                mock_client = Mock()
                mock_response = Mock()
                mock_response.choices = [Mock()]
                # 生成一个超长的摘要
                long_summary = "这是一个非常长的摘要" * 20  # 超过200字符
                mock_response.choices[0].message.content = long_summary
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client
                
                service = AIService()
                summary = service.generate_note_summary("测试内容", "测试标题")
                
                assert len(summary) <= 200
                assert summary.endswith("...")
    
    def test_generate_summary_api_failure(self):
        """测试 API 调用失败时的降级处理"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('openai.OpenAI') as mock_openai:
                mock_client = Mock()
                mock_client.chat.completions.create.side_effect = Exception("API 错误")
                mock_openai.return_value = mock_client
                
                service = AIService()
                summary = service.generate_note_summary("测试内容", "测试标题")
                
                # 应该返回默认摘要
                assert "测试标题" in summary
                assert len(summary) <= 200
    
    def test_default_summary_generation(self):
        """测试默认摘要生成"""
        service = AIService()
        service.client = None  # 模拟没有客户端
        
        summary = service._get_default_summary("这是一个测试内容", "测试标题")
        
        assert "测试标题" in summary
        assert len(summary) <= 200
    
    def test_prompt_building(self):
        """测试提示词构建"""
        service = AIService()
        
        # 测试有标题的提示词
        prompt_with_title = service._build_summary_prompt("内容", "标题")
        assert "标题：标题" in prompt_with_title
        assert "内容：内容" in prompt_with_title
        
        # 测试无标题的提示词
        prompt_without_title = service._build_summary_prompt("内容", "")
        assert "内容：内容" in prompt_without_title
        assert "标题：" not in prompt_without_title


class TestAIServiceIntegration:
    """AI 服务集成测试类"""
    
    def test_generate_note_summary_function(self):
        """测试便捷函数"""
        with patch('app.services.ai_service.ai_service') as mock_service:
            mock_service.generate_note_summary.return_value = "测试摘要"
            
            summary = generate_note_summary("测试内容", "测试标题")
            
            assert summary == "测试摘要"
            mock_service.generate_note_summary.assert_called_once_with("测试内容", "测试标题")
    
    def test_service_availability_check(self):
        """测试服务可用性检查"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('openai.OpenAI') as mock_openai:
                mock_client = Mock()
                mock_openai.return_value = mock_client
                
                service = AIService()
                assert service.is_available()
                
                # 测试没有 API Key 的情况
                service.settings.OPENAI_API_KEY = None
                assert not service.is_available() 