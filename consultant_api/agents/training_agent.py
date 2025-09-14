class TrainingAgent:
    def evaluate_progress(self, status):
        if status == "Completed":
            return "✅ All done"
        elif status == "In Progress":
            return "⏳ Ongoing"
        else:
            return "🔴 Not started"
