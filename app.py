from flask import Flask, render_template, jsonify, request
import numpy as np
import math

app = Flask(__name__)

# 物理常数
class Consts:
    AU = 149597870.700  # 天文单位 (km)
    G = 6.67e-11       # 万有引力常数

# 天体类
class Body:
    def __init__(self, name, mass, position, velocity, color, size_scale=1.0):
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.acceleration = np.array([0, 0, 0], dtype='float64')
        self.color = color
        self.size_scale = size_scale
    
    def to_dict(self):
        return {
            'name': self.name,
            'position': self.position.tolist(),
            'velocity': self.velocity.tolist(),
            'color': self.color,
            'size_scale': self.size_scale
        }

# 天体系统
class System:
    def __init__(self, bodies):
        self.bodies = bodies
    
    def evolve(self, dt):
        # 计算加速度
        for body1 in self.bodies:
            acceleration = np.zeros(3)
            for body2 in self.bodies:
                if body1 is body2:
                    continue
                
                r = body2.position - body1.position
                distance = np.linalg.norm(r)
                if distance > 0:
                    # 计算引力加速度 (注意单位转换)
                    acceleration += (Consts.G * body2.mass * r / distance**3) / 1e9
            
            body1.acceleration = acceleration
        
        # 更新速度和位置
        for body in self.bodies:
            body.velocity += body.acceleration * dt
            body.position += body.velocity * dt

# 初始化三体系统
# 将初始速度提高两倍，并引入Z轴分量
def init_three_body_system():
    bodies = [
        Body('太阳1', 1.5e30, [849597870.700, 0, 100000000], [0, 14.0, 2.0], '#ff0000', 5e1),
        Body('太阳2', 2e30, [0, 0, -100000000], [0, -16.0, -3.0], '#ff6600', 5e1),
        Body('太阳3', 2.5e30, [0, -849597870.700, 50000000], [36.0, 0, 1.5], '#ffff00', 5e1),
        Body('地球', 5.972e24, [0, -349597870.700, -50000000], [31.0, 0, -2.5], '#0000ff', 4e3)
    ]
    return System(bodies)

# 全局系统实例
system = init_three_body_system()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bodies')
def get_bodies():
    return jsonify([body.to_dict() for body in system.bodies])

@app.route('/api/evolve')
def evolve_system():
    # 从查询参数获取dt值，默认为86400秒（一天）
    dt = request.args.get('dt', 86400, type=float)
    system.evolve(dt)
    return jsonify([body.to_dict() for body in system.bodies])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)