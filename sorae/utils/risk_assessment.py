def assess_risk(device_id, known_devices, failed_attempts):
    risk_score = 0.0
    if device_id not in known_devices:
        risk_score += 0.6
    if failed_attempts > 2:
        risk_score += 0.2
    return risk_score
