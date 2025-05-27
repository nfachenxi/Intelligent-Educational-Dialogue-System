# -*- coding: utf-8 -*-
from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 在应用上下文中预加载GPT-2模型（可选）
        from app.routes.gpt2 import init_gpt2
        try:
            init_gpt2(use_mock=True)
            print("GPT-2模型预加载成功（模拟模式）")
        except Exception as e:
            print(f"GPT-2模型预加载失败: {str(e)}")
    
    # 运行应用
    app.run(debug=True, host='127.0.0.1', port=5000) 