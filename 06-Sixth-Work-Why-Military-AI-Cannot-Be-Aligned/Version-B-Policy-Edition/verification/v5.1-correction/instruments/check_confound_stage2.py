"""段階二の交絡の確かめ：β = 1（dS/dt = α(P)·S, α = P）のデータを、P の条件をまたいで一つの回帰にまとめると、
両対数の傾きが 1 からずれるか。条件ごとに推定すれば 1 に戻るか。"""
import math

def run(P, T=1.0, n=50, S0=1.0):
    pts = []
    for i in range(1, n + 1):
        t = T * i / n
        S = S0 * math.exp(P * t)          # β = 1 の解
        rate = P * S                      # dS/dt
        pts.append((math.log(S), math.log(rate)))
    return pts

def slope(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    sxy = sum((x - mx) * (y - my) for x, y in pts); sxx = sum((x - mx) ** 2 for x in xs)
    return sxy / sxx

conds = {P: run(P) for P in (1, 2, 3)}
for P, pts in conds.items():
    print("P=%d  条件の中の傾き = %.4f" % (P, slope(pts)))
pooled = [p for pts in conds.values() for p in pts]
print("条件をまたいでまとめた傾き = %.4f  （真の β = 1）" % slope(pooled))
