# -*- coding: utf-8 -*-
"""AIML规则管理模块"""
import os
import logging
import xml.etree.ElementTree as ET
from flask import current_app

logger = logging.getLogger(__name__)

class AIMLManager:
    """AIML规则管理器"""
    
    def __init__(self, aiml_dir=None):
        """
        初始化AIML管理器
        
        Args:
            aiml_dir: AIML规则文件目录，默认为None，使用项目默认目录
        """
        # 设置默认目录
        if aiml_dir is None:
            self.aiml_dir = os.path.join(current_app.root_path, '..', 'data', 'aiml')
        else:
            self.aiml_dir = aiml_dir
            
        # 确保目录存在
        if not os.path.exists(self.aiml_dir):
            os.makedirs(self.aiml_dir)
            logger.warning(f'AIML目录不存在，已创建: {self.aiml_dir}')
    
    def get_all_files(self):
        """
        获取所有AIML文件
        
        Returns:
            list: AIML文件列表
        """
        if not os.path.exists(self.aiml_dir):
            return []
            
        return [f for f in os.listdir(self.aiml_dir) if f.endswith('.aiml')]
    
    def get_file_content(self, filename):
        """
        获取AIML文件内容
        
        Args:
            filename: 文件名
            
        Returns:
            str: 文件内容
        """
        file_path = os.path.join(self.aiml_dir, filename)
        if not os.path.exists(file_path):
            logger.error(f'AIML文件不存在: {file_path}')
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f'读取AIML文件失败: {str(e)}')
            return None
    
    def save_file_content(self, filename, content):
        """
        保存AIML文件内容
        
        Args:
            filename: 文件名
            content: 文件内容
            
        Returns:
            bool: 是否成功保存
        """
        file_path = os.path.join(self.aiml_dir, filename)
        
        try:
            # 验证XML格式
            ET.fromstring(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f'已保存AIML文件: {file_path}')
            return True
        except Exception as e:
            logger.error(f'保存AIML文件失败: {str(e)}')
            return False
    
    def create_file(self, filename, categories=None):
        """
        创建新的AIML文件
        
        Args:
            filename: 文件名
            categories: 规则列表，每个规则是一个(pattern, template)元组
            
        Returns:
            bool: 是否成功创建
        """
        if not filename.endswith('.aiml'):
            filename += '.aiml'
            
        file_path = os.path.join(self.aiml_dir, filename)
        
        if os.path.exists(file_path):
            logger.error(f'AIML文件已存在: {file_path}')
            return False
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<aiml version="1.0">\n')
                
                if categories:
                    for pattern, template in categories:
                        f.write(f'    <category>\n')
                        f.write(f'        <pattern>{pattern}</pattern>\n')
                        f.write(f'        <template>{template}</template>\n')
                        f.write(f'    </category>\n')
                
                f.write('</aiml>')
                
            logger.info(f'已创建AIML文件: {file_path}')
            return True
        except Exception as e:
            logger.error(f'创建AIML文件失败: {str(e)}')
            return False
    
    def delete_file(self, filename):
        """
        删除AIML文件
        
        Args:
            filename: 文件名
            
        Returns:
            bool: 是否成功删除
        """
        file_path = os.path.join(self.aiml_dir, filename)
        
        if not os.path.exists(file_path):
            logger.error(f'AIML文件不存在: {file_path}')
            return False
            
        try:
            os.remove(file_path)
            logger.info(f'已删除AIML文件: {file_path}')
            return True
        except Exception as e:
            logger.error(f'删除AIML文件失败: {str(e)}')
            return False
    
    def extract_patterns(self, filename):
        """
        提取AIML文件中的所有模式
        
        Args:
            filename: 文件名
            
        Returns:
            list: 模式列表，每个元素是(pattern, template)元组
        """
        file_path = os.path.join(self.aiml_dir, filename)
        
        if not os.path.exists(file_path):
            logger.error(f'AIML文件不存在: {file_path}')
            return []
            
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            patterns = []
            for category in root.findall('.//category'):
                pattern_elem = category.find('pattern')
                template_elem = category.find('template')
                
                if pattern_elem is not None and template_elem is not None:
                    pattern = ''.join(pattern_elem.itertext())
                    
                    # 模板可能包含子元素，需要特殊处理
                    template_str = ET.tostring(template_elem, encoding='unicode')
                    template = template_str.replace('<template>', '').replace('</template>', '').strip()
                    
                    patterns.append((pattern, template))
            
            return patterns
        except Exception as e:
            logger.error(f'提取AIML模式失败: {str(e)}')
            return []
    
    def add_pattern(self, filename, pattern, template):
        """
        向AIML文件添加新模式
        
        Args:
            filename: 文件名
            pattern: 匹配模式
            template: 回复模板
            
        Returns:
            bool: 是否成功添加
        """
        file_path = os.path.join(self.aiml_dir, filename)
        
        if not os.path.exists(file_path):
            logger.error(f'AIML文件不存在: {file_path}')
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 在</aiml>前插入新规则
            category = f'''    <category>
        <pattern>{pattern}</pattern>
        <template>{template}</template>
    </category>'''
            
            content = content.replace('</aiml>', f'{category}\n</aiml>')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f'已向{filename}添加新规则: {pattern} -> {template}')
            return True
        except Exception as e:
            logger.error(f'添加AIML规则失败: {str(e)}')
            return False
            
    def import_categories(self, data):
        """
        批量导入规则
        
        Args:
            data: 规则数据，格式为 [{'filename': 文件名, 'pattern': 模式, 'template': 模板}, ...]
            
        Returns:
            dict: {'success': 成功数量, 'failed': 失败数量}
        """
        success = 0
        failed = 0
        
        for item in data:
            filename = item.get('filename')
            pattern = item.get('pattern')
            template = item.get('template')
            
            if not filename or not pattern or not template:
                failed += 1
                continue
                
            # 确保文件存在
            file_path = os.path.join(self.aiml_dir, filename)
            if not os.path.exists(file_path):
                # 创建新文件
                self.create_file(filename)
            
            # 添加规则
            if self.add_pattern(filename, pattern, template):
                success += 1
            else:
                failed += 1
                
        return {'success': success, 'failed': failed} 