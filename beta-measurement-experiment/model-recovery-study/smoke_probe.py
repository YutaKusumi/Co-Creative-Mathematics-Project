# 重さの真因を実測で特定する極小プローブ
import time, numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp

rng = np.random.default_rng(1)
t = np.linspace(0, 10, 30)

# 1) blowup ODE 積分の時間
def f_blow_ode(t,S): return 0.45*np.power(np.maximum(S,1e-12),1.6)
t0=time.time()
for _ in range(20):
    solve_ivp(f_blow_ode,(0,10),[0.2],t_eval=t,method='RK45',rtol=1e-8,atol=1e-10,max_step=t[1]-t[0])
print(f"ODE積分(blowup) x20: {time.time()-t0:.2f}s  → 1本 {(time.time()-t0)/20*1000:.1f}ms")

# 2) 各 curve_fit の時間（ノイズデータ＝発散でないデータに blowup を当てる最悪ケース）
S = 0.2*np.exp(0.3*t)*rng.normal(1,0.05,30); S=np.maximum(S,1e-6)
def f_blow(t,C,a,p):
    p=max(p,1.01); return np.power(np.maximum(C-a*t,1e-9),-1.0/(p-1.0))
def f_sat(t,Smax,B,a): return Smax/(1.0+B*np.exp(-a*t))
def f_exp(t,S0,a): return S0*np.exp(a*t)

for name,fn,p0,bounds,mx in [
    ("blowup_40000", f_blow,[15,0.6,1.6],([10.1,1e-4,1.05],[1000,50,5.0]),40000),
    ("blowup_2000",  f_blow,[15,0.6,1.6],([10.1,1e-4,1.05],[1000,50,5.0]),2000),
    ("sat_40000",    f_sat,[0.5,5,0.5],([1e-3,1e-3,1e-4],[100,1e4,50]),40000),
    ("exp_20000",    f_exp,[0.2,0.3],None,20000),
]:
    t0=time.time(); n=10
    for _ in range(n):
        try:
            if bounds: curve_fit(fn,t,S,p0=p0,bounds=bounds,maxfev=mx)
            else: curve_fit(fn,t,S,p0=p0,maxfev=mx)
        except Exception: pass
    print(f"{name:16s} x{n}: {time.time()-t0:.2f}s  → 1回 {(time.time()-t0)/n*1000:.1f}ms")
