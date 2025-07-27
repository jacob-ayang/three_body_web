# 三体运动模拟 Web 应用

这是一个基于 Flask 和 Three.js 的三体运动模拟 Web 应用。它实现了三体问题的物理模拟，并在浏览器中以3D形式展示。

## 功能特点

- 基于万有引力定律的三体运动物理模拟
- 使用 Three.js 实现 3D 可视化
- 响应式设计，适应不同屏幕尺寸

## 运行环境

- Python 3.8+
- Flask
- NumPy
- 现代浏览器（支持 WebGL）

## 安装和运行

1. 克隆或下载本项目

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 运行应用：
   
   方式一：直接运行
   ```
   python app.py
   ```
   
   方式二：使用启动脚本（自动安装依赖）
   ```
   python run.py
   ```

4. 在浏览器中访问 `http://localhost:5000`

## 项目结构

- `app.py`: Flask 应用主文件，包含物理模拟逻辑
- `templates/index.html`: Three.js 可视化界面
- `requirements.txt`: Python 依赖列表

## 物理模型

本项目实现了经典的牛顿万有引力定律来计算天体间的相互作用：

- 使用万有引力常数 G = 6.67e-11
- 计算每个天体受到的合力和加速度
- 通过数值积分更新天体的速度和位置

天体的初始位置和速度可以根据需要在 `app.py` 中修改。