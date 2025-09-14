from datetime import date, datetime

class AttendanceAgent:
    def interpret_attendance(self, attended):
        return "✅ Present" if attended else "❌ Absent"

    def is_late(self, meeting_date):
        if isinstance(meeting_date, str):
            meeting_date = datetime.strptime(meeting_date, "%Y-%m-%d").date()

        today = date.today()
        return "⚠️ Late Entry" if meeting_date < today else "🕒 On Time"
