import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

h = pd.read_csv("rampa_stats_history.csv")
h = h[h["Name"] == "Aggregated"].copy()
h["p95"] = pd.to_numeric(h["95%"], errors="coerce")
h = h.dropna(subset=["p95"])
h = h[h["User Count"] > 0]

plt.figure(figsize=(8, 5))
plt.plot(h["User Count"], h["p95"], marker="o", markersize=3, label="RTT p95")
plt.axhline(80, linestyle="--", color="red", label="meta p95 = 80 ms")
plt.xlabel("Jugadores simulados")
plt.ylabel("Latencia p95 (ms)")
plt.title("CCU vs latencia p95 (rampa 1 jugador/s)")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("ccu_vs_p95.png", dpi=150)

print(h[["User Count", "p95"]].to_string(index=False))
