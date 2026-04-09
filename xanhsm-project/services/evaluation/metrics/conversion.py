def compute_conversion_rate(logs: list) -> dict:
    total=len(logs)
    if total==0: return {"conversion_rate":None,"total_logs":0,"threshold":0.30,"passing":True}
    converted=sum(1 for l in logs if l.get("outcome")=="converted")
    reported=sum(1 for l in logs if l.get("outcome")=="reported_wrong")
    ignored=sum(1 for l in logs if l.get("outcome")=="ignored")
    no_out=sum(1 for l in logs if l.get("outcome") is None)
    rate=round(converted/total,4)
    return {"conversion_rate":rate,"conversion_rate_pct":round(rate*100,2),"total_logs":total,"converted":converted,"reported_wrong":reported,"ignored":ignored,"no_outcome":no_out,"threshold":0.30,"passing":rate>=0.30,"red_flag":rate<0.15}

def compute_satisfaction_rate(logs: list) -> dict:
    fb=[l for l in logs if l.get("outcome") in ("converted","reported_wrong")]
    if not fb: return {"satisfaction_rate":None,"total_feedback":0,"threshold":0.75,"passing":True}
    pos=sum(1 for l in fb if l.get("outcome")=="converted")
    rate=round(pos/len(fb),4)
    return {"satisfaction_rate":rate,"satisfaction_rate_pct":round(rate*100,2),"total_feedback":len(fb),"positive":pos,"negative":len(fb)-pos,"threshold":0.75,"passing":rate>=0.75,"red_flag":rate<0.60}

def compute_unsure_rate(logs: list) -> dict:
    allergen=[l for l in logs if l.get("is_allergen_query")]
    if not allergen: return {"hallucination_rate":None,"total_allergen_queries":0,"threshold":0.05,"passing":True}
    hall=[l for l in allergen if not l.get("has_disclaimer") and l.get("confidence")=="high"]
    rate=round(len(hall)/len(allergen),4)
    return {"hallucination_rate":rate,"hallucination_rate_pct":round(rate*100,2),"total_allergen_queries":len(allergen),"hallucinated_count":len(hall),"threshold":0.05,"passing":rate<=0.05,"red_flag":rate>0.05,"stop_immediately":rate>0.10}
