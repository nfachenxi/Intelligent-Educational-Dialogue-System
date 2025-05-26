# -*- coding: utf-8 -*-
import re

def validate_email(email):
    """验证邮箱格式是否正确"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) 