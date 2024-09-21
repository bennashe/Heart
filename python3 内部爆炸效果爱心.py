import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# 创建图形和轴
fig, ax = plt.subplots(figsize=(10, 9), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')

# 创建自定义颜色映射
colors = ['#FF0000', '#FF3300', '#FF6600', '#FF9900', '#FFCC00', '#FFFF00']
n_bins = 100
cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

# 创建心形的参数方程
t = np.linspace(0, 2*np.pi, 1000)
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

# 归一化坐标
x = x / np.max(np.abs(x))
y = y / np.max(np.abs(y))

# 初始化心形和粒子
heart, = ax.fill([], [], color='red', alpha=0.8, zorder=10)
particles, = ax.plot([], [], 'o', color='white', alpha=0.6, markersize=1, zorder=5)
glow, = ax.plot([], [], 'o', color='white', alpha=0.1, markersize=20, zorder=1)

# 创建粒子
n_particles = 500
particle_x = np.random.uniform(-0.8, 0.8, n_particles)
particle_y = np.random.uniform(-0.8, 0.8, n_particles)
particle_vx = np.random.uniform(-0.005, 0.005, n_particles)
particle_vy = np.random.uniform(-0.005, 0.005, n_particles)

def is_inside_heart(x, y):
    return (x**2 + y**2 - 1)**3 - (x**2 * y**3) < 0

# 动画更新函数
def update(frame):
    global particle_x, particle_y, particle_vx, particle_vy
    
    # 更新心形
    color = cmap(frame / 200 % 1)
    size = 1 + 0.05 * np.sin(frame * 0.1)
    heart.set_xy(np.array([size * x, size * y]).T)
    heart.set_facecolor(color)
    heart.set_edgecolor(color)
    
    # 更新粒子位置
    particle_x += particle_vx
    particle_y += particle_vy
    
    # 保持粒子在心形内部
    for i in range(n_particles):
        if not is_inside_heart(particle_x[i], particle_y[i]):
            particle_x[i] = np.random.uniform(-0.8, 0.8)
            particle_y[i] = np.random.uniform(-0.8, 0.8)
            particle_vx[i] = np.random.uniform(-0.005, 0.005)
            particle_vy[i] = np.random.uniform(-0.005, 0.005)
    
    particles.set_data(particle_x, particle_y)
    particles.set_color(color)
    
    # 更新发光效果
    glow_x = size * x + np.random.normal(0, 0.01, len(x))
    glow_y = size * y + np.random.normal(0, 0.01, len(y))
    glow.set_data(glow_x, glow_y)
    glow.set_color(color)
    
    return heart, particles, glow

# 创建动画
anim = FuncAnimation(fig, update, frames=400, interval=30, blit=True)

plt.tight_layout()
plt.show()
