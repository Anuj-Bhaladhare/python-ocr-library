class StepLogger:
    def __init__(self):
        self.logs = []

    def log(self, step, executed, reason, confidence):
        self.logs.append({
            "step": step,
            "executed": executed,
            "reason": reason,
            "confidence": round(confidence, 2)
        })
