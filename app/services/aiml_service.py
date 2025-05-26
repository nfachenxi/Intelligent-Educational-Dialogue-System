# -*- coding: utf-8 -*-
"""AIML规则对话模块服务"""
import os
import aiml
import logging
from datetime import datetime
from flask import current_app

logger = logging.getLogger(__name__)

class AIMLService:
    """AIML规则对话服务"""
    
    def __init__(self, aiml_dir=None):
        """
        初始化AIML服务
        
        Args:
            aiml_dir: AIML规则文件目录，默认为None，使用项目默认目录
        """
        self.kernel = aiml.Kernel()
        
        # 设置默认目录
        if aiml_dir is None:
            self.aiml_dir = os.path.join(current_app.root_path, '..', 'data', 'aiml')
        else:
            self.aiml_dir = aiml_dir
            
        # 初始化AIML核心
        self._load_aiml_files()
        
        # 设置机器人属性
        self.kernel.setBotPredicate('name', '智能教育助手')
        self.kernel.setBotPredicate('master', '学生')
        self.kernel.setBotPredicate('birthday', datetime.now().strftime('%Y-%m-%d'))
        
        logger.info('AIML服务初始化完成')
    
    def _load_aiml_files(self):
        """加载AIML规则文件"""
        if not os.path.exists(self.aiml_dir):
            os.makedirs(self.aiml_dir)
            logger.warning(f'AIML目录不存在，已创建: {self.aiml_dir}')
        
        # 尝试加载bootstrap文件
        bootstrap_path = os.path.join(self.aiml_dir, 'bootstrap.xml')
        if os.path.exists(bootstrap_path):
            self.kernel.bootstrap(learnFiles=bootstrap_path)
            logger.info(f'已加载AIML bootstrap文件: {bootstrap_path}')
            return
        
        # 如果没有bootstrap文件，加载目录中的所有AIML文件
        aiml_files = [f for f in os.listdir(self.aiml_dir) if f.endswith('.aiml')]
        if aiml_files:
            for file in aiml_files:
                file_path = os.path.join(self.aiml_dir, file)
                self.kernel.learn(file_path)
                logger.info(f'已加载AIML文件: {file_path}')
        else:
            logger.warning(f'AIML目录中没有找到AIML文件: {self.aiml_dir}')
            
            # 创建基础AIML文件
            self._create_basic_aiml_files()
            
    def _create_basic_aiml_files(self):
        """创建基础AIML规则文件"""
        # 创建基础问候规则
        greeting_path = os.path.join(self.aiml_dir, 'greeting.aiml')
        with open(greeting_path, 'w', encoding='utf-8') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="1.0">
    <!-- 基本问候规则 -->
    <category>
        <pattern>你好</pattern>
        <template>你好！我是智能教育助手，有什么可以帮助你的吗？</template>
    </category>
    
    <category>
        <pattern>* 你好 *</pattern>
        <template>你好！我是智能教育助手，有什么可以帮助你的吗？</template>
    </category>
    
    <category>
        <pattern>你是谁</pattern>
        <template>我是<bot name="name"/>，一个智能教育对话系统，可以回答你的学习问题。</template>
    </category>
    
    <category>
        <pattern>再见</pattern>
        <template>再见！如果有问题随时来问我。</template>
    </category>
</aiml>''')
        logger.info(f'已创建基础问候规则文件: {greeting_path}')
        
        # 创建基础教育问答规则
        education_path = os.path.join(self.aiml_dir, 'education.aiml')
        with open(education_path, 'w', encoding='utf-8') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="1.0">
    <!-- 基本教育问答规则 -->
    <category>
        <pattern>什么是 *</pattern>
        <template>关于"<star/>"，我建议您查阅相关教材或者咨询您的老师获取更准确的信息。</template>
    </category>
    
    <category>
        <pattern>如何学习 *</pattern>
        <template>学习"<star/>"需要理解基本概念，多做练习，并在实践中应用。您可以查阅相关教材或在线资源。</template>
    </category>
    
    <category>
        <pattern>* 难吗</pattern>
        <template>学习任何知识都需要时间和耐心。"<star/>"可能对某些人来说有挑战，但通过系统学习和练习，您一定能够掌握。</template>
    </category>
</aiml>''')
        logger.info(f'已创建基础教育问答规则文件: {education_path}')
        
        # 重新加载AIML文件
        self.kernel.learn(greeting_path)
        self.kernel.learn(education_path)
    
    def get_response(self, message, session_id=None):
        """
        获取AIML响应
        
        Args:
            message: 用户输入的消息
            session_id: 会话ID，用于维护上下文
            
        Returns:
            str: AIML响应内容
        """
        if not message:
            return "请输入您的问题"
        
        try:
            # 如果提供会话ID，使用会话ID处理请求
            if session_id:
                response = self.kernel.respond(message, session_id)
            else:
                response = self.kernel.respond(message)
                
            # 如果没有匹配到任何模式，返回默认回复
            if not response:
                response = "抱歉，我不太理解您的问题。您能换个方式提问吗？"
                
            return response
        except Exception as e:
            logger.error(f"AIML处理异常: {str(e)}")
            return "系统处理您的请求时出现错误，请稍后再试。"
    
    def learn_pattern(self, pattern, template):
        """
        学习新的问答模式
        
        Args:
            pattern: 匹配模式
            template: 回复模板
            
        Returns:
            bool: 是否成功添加
        """
        try:
            category = f'''<category>
    <pattern>{pattern}</pattern>
    <template>{template}</template>
</category>'''
            
            self.kernel.learn(category)
            
            # 将新模式保存到文件
            custom_path = os.path.join(self.aiml_dir, 'custom.aiml')
            
            # 检查文件是否存在，如果不存在则创建
            if not os.path.exists(custom_path):
                with open(custom_path, 'w', encoding='utf-8') as f:
                    f.write('''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="1.0">
    <!-- 自定义规则 -->
</aiml>''')
            
            # 将新规则添加到文件
            with open(custom_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 在</aiml>前插入新规则
            content = content.replace('</aiml>', f'{category}\n</aiml>')
            
            with open(custom_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f'已添加新规则: {pattern} -> {template}')
            return True
        except Exception as e:
            logger.error(f"添加新规则失败: {str(e)}")
            return False 