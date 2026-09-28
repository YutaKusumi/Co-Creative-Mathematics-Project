"""N1 / N1-b / X5 の数値の確かめ（訂正案のため・リポジトリの外）。

N1  : 附録I §I-2a の定め方 dS/dt = k*P*S**(beta-1) と、§4-3b の定め方 dS/dt = alpha*S**beta を、
      同じ beta の値で積分し、有限時間で発散するかを比べる。
N1-b: §4-3b の定め方で beta = 1 のとき、一定時間後の S が P に対して線形か（§I-3a 段階二の検定の前提）。
X5  : 検証10 の線形の場合 dD/dt = s - r*D + g*D（s=0.2, r=1.0, g=1.5）で、十倍ごと・千倍ごとの到達の間隔。
"""
import math


def rk4(f, y0, t_end, dt=1e-4, cap=1e12):
    t, y = 0.0, y0
    while t < t_end:
        h = min(dt, t_end - t)
        k1 = f(y); k2 = f(y + h * k1 / 2); k3 = f(y + h * k2 / 2); k4 = f(y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
        if y > cap:
            return t, None  # 発散（cap を越えた時刻）
    return t, y


print("== N1: 同じ beta で、二つの定め方を比べる（k*P = alpha = 1, S(0) = 1, t = 0..20）")
for beta in [1.2, 1.5, 2.0, 2.5, 3.0]:
    tI, yI = rk4(lambda s: s ** (beta - 1), 1.0, 20.0)
    t4, y4 = rk4(lambda s: s ** beta, 1.0, 20.0)
    I = "発散（t≈%.3f）" % tI if yI is None else "有限（S(20)=%.4g）" % yI
    F = "発散（t≈%.3f）" % t4 if y4 is None else "有限（S(20)=%.4g）" % y4
    Tstar = 1.0 / (beta - 1.0)
    print("  beta=%.1f  §I-2a の定め方: %-22s  §4-3b の定め方: %-22s  （§4-3b の T* = %.3f）" % (beta, I, F, Tstar))

print()
print("== N1-b: §4-3b の定め方で beta = 1（dS/dt = k*P*S）。時刻 T=1 の S を P の関数として（k=1, S(0)=1）")
for P in [1, 2, 3]:
    _, y = rk4(lambda s, P=P: P * s, 1.0, 1.0)
    print("  P=%d  S(1)=%.4f   （解析解 e^P = %.4f）" % (P, y, math.exp(P)))
print("  → P を 2 倍にすると S は %.2f 倍：beta = 1 でも P に対して超線形に応答する" % (math.exp(2) / math.exp(1)))
print("  旧 §I-2a の beta = 1（dS/dt = k*P）なら S(1) = 1 + P：P に対して線形")

print()
print("== X5: 検証10 の線形の場合（s=0.2, r=1.0, g=1.5, power=1）")
s, r, g = 0.2, 1.0, 1.5
lam = g - r  # 漸近的な増加率
print("  漸近的な増加率 = g - r = %.2f" % lam)
print("  十倍ごとの間隔 ln10/%.1f = %.4f" % (lam, math.log(10) / lam))
print("  千倍ごとの間隔 ln1000/%.1f = %.4f" % (lam, math.log(1000) / lam))
# 設計書 L68 の到達時刻 15.6→29.4→43.2→57.0 と照合：解析解 D(t) = (D0 + s/lam) e^{lam t} - s/lam
for D0 in [0.01, 0.1]:
    c = s / lam
    ts = [math.log((10 ** k + c) / (D0 + c)) / lam for k in (3, 6, 9, 12)]
    print("  D0=%.2f のとき t(1e3), t(1e6), t(1e9), t(1e12) = %s" % (D0, ", ".join("%.1f" % t for t in ts)))
