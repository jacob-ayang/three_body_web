from flask import Flask, render_template, jsonify, request
import numpy as np
import math

app = Flask(__name__)

# 物理常数
class Consts:
    AU = 149597870.700  # 天文单位 (km)
    G = 6.67e-11      # 万有引力常数

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
        # 保存地球的初始状态
        for body in bodies:
            if body.name == '地球':
                self.earth_initial_state = {
                    'position': body.position.copy(),
                    'velocity': body.velocity.copy()
                }
    
    def reset_earth(self):
        # 重置地球位置和速度
        for body in self.bodies:
            if body.name == '地球':
                body.position = self.earth_initial_state['position'].copy()
                body.velocity = self.earth_initial_state['velocity'].copy()
                break
    
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
            
            # 检查地球距离
            if body.name == '地球':
                # 计算地球到原点的距离（转换为AU单位）
                distance_to_origin = np.linalg.norm(body.position) / Consts.AU
                if distance_to_origin > 100:  # 如果超过100AU
                    self.reset_earth()  # 重置地球位置

# 初始化三体系统
# 减小地球的显示大小
def init_three_body_system():
    # 按真实太阳-地球质量比计算地球质量
    avg_star_mass = (1.5e30 + 2.0e30 + 2.5e30) / 3  # 平均恒星质量
    earth_mass = avg_star_mass / 333000  # 使用真实的太阳-地球质量比
    
    bodies = [
        Body('太阳1', 1.5e30, [594718509.800, 0, 140000000], [-10.0, 15.0, 1.0], '#ff0000', 5e1),
        Body('太阳2', 2.0e30, [0, 0, -140000000], [15.0, -10.0, -1.5], '#ff6600', 5e1),
        Body('太阳3', 2.5e30, [0, -594718509.800, 70000000], [-4.0, -2.0, 0.4], '#ffff00', 5e1),
        # 使用更真实的质量比，同时适当调整初始速度
        Body('地球', earth_mass, [200000000, 0, 0], [1.0, 2.0, 0.2], '#0066ff', 1e1)
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

@app.route('/api/reset')
def reset_system():
    global system
    system = init_three_body_system()
    return jsonify([body.to_dict() for body in system.bodies])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)