from config.config_loader import config

def score_cpa_lead(post_text, comments):
    score = 0
    
    if "looking for" in post_text.lower() or "recommendations" in post_text.lower():
        score += config['cpa_settings']['lead_scoring']['pain_point_weight']
    
    if "alternative to" in post_text.lower():
        score += config['cpa_settings']['lead_scoring']['competitor_mentions_weight']
        
    budget_keywords = ["affordable", "discount", "cheap", "cost"]
    if any(keyword in post_text.lower() for keyword in budget_keywords):
        score += config['cpa_settings']['lead_scoring']['budget_keywords_weight']
        
    return score
