from datetime import date, datetime

class OpportunityAgent:
    def classify_opportunity(self, opportunity_type):
        if opportunity_type == "Project":
            return "🚀 High Impact"
        elif opportunity_type == "Training":
            return "📘 Skill Growth"
        elif opportunity_type == "Interview":
            return "🎯 Deployment Ready"
        else:
            return "🔍 General Engagement"

    def check_assignment_date(self, assigned_on):
        if isinstance(assigned_on, str):
            assigned_on = datetime.strptime(assigned_on, "%Y-%m-%d").date()
        return "✅ Recent" if (date.today() - assigned_on).days <= 7 else "📅 Older Opportunity"
