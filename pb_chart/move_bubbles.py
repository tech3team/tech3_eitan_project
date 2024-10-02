
import math
import random
import numpy as np
import pandas as pd

def place_bubbles_on_circle(num_bubbles, center_x, center_y, radius):
    """
    バブルを円周上に均等に配置する関数。

    Parameters:
        num_bubbles (int): バブルの数
        center_x (float): 円の中心のx座標
        center_y (float): 円の中心のy座標
        radius (float): 円の半径

    Returns:
        List[float]: 各バブルのx座標のリスト
        List[float]: 各バブルのy座標のリスト
    """
    x_positions = []
    y_positions = []

    # バブルを円周上に均等に配置
    for i in range(num_bubbles):
        # 各バブルの角度を計算 (2πをnum_bubblesで等分)
        angle = (2 * math.pi / num_bubbles) * i

        # x, y座標を計算
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        # 計算したx, y座標をリストに追加
        x_positions.append(x)
        y_positions.append(y)

    return x_positions, y_positions

# 初期配置のバブルをいい感じの位置に動かす関数
def move_bubbles_towards_center(num_bubbles, x, y, center_x, center_y, radii, speed=1, iterations=1):
    for _ in range(iterations):  # 指定回数ループ
        for i in range(num_bubbles):
            # 中心に向かって移動
            direction_to_center = [center_x - x[i], center_y - y[i]]
            distance_to_center = math.sqrt(direction_to_center[0]**2 + direction_to_center[1]**2)

            if distance_to_center > 0:  # 中心にすでにいる場合を除外
                # 正規化して一定速度で中心に向かう
                direction_to_center = [d / distance_to_center for d in direction_to_center]
                x[i] += direction_to_center[0] * speed
                y[i] += direction_to_center[1] * speed

            # 衝突回避ロジック
            for j in range(num_bubbles):
                if i != j:
                    dx = x[i] - x[j]
                    dy = y[i] - y[j]
                    dist = math.sqrt(dx**2 + dy**2)
                    min_dist = radii[i] + radii[j]

                    if dist < min_dist:  # バブルが重なっている場合
                        # バブルを反発させる
                        overlap = (min_dist - dist) / 2
                        angle = math.atan2(dy, dx)
                        x[i] += math.cos(angle) * overlap
                        y[i] += math.sin(angle) * overlap
                        # x[j] -= math.cos(angle) * overlap
                        # y[j] -= math.sin(angle) * overlap
    return x, y