import statistics

def compute_p95_latency(logs: list) -> dict:
    lat=[float(l["latency_ms"]) for l in logs if l.get("latency_ms") and float(l["latency_ms"])>0]
    if not lat: return {"p95_ms":None,"p50_ms":None,"avg_ms":None,"total_logs":0,"threshold_ms":10000,"passing":True}
    s=sorted(lat); n=len(s)
    p95=s[min(int(n*0.95),n-1)]; p50=s[min(int(n*0.50),n-1)]; p99=s[min(int(n*0.99),n-1)]
    return {"p50_ms":round(p50,1),"p95_ms":round(p95,1),"p99_ms":round(p99,1),"p50_s":round(p50/1000,2),"p95_s":round(p95/1000,2),"avg_ms":round(statistics.mean(lat),1),"max_ms":round(max(lat),1),"total_logs":n,"threshold_ms":10000,"threshold_s":10,"passing":p95<10000,"red_flag":p95>15000}
