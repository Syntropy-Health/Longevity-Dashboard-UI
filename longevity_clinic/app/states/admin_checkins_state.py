"""Admin check-ins state management."""

import reflex as rx
from typing import List, Dict, Any, TypedDict


class AdminCheckIn(TypedDict):
    """Admin check-in entry type."""
    id: str
    patient_id: str
    patient_name: str
    type: str  # voice, text, or call
    summary: str
    timestamp: str
    submitted_at: str  # For sorting
    sentiment: str
    key_topics: List[str]
    status: str  # pending, reviewed, flagged
    provider_reviewed: bool
    reviewed_by: str
    reviewed_at: str


class AdminCheckinsState(rx.State):
    """State management for admin check-ins view."""
    
    # Active tab for filtering
    active_status_tab: str = "pending"  # pending, reviewed, flagged, all
    
    # Search query
    search_query: str = ""
    
    # All check-ins data (would come from database in real app)
    all_checkins: List[AdminCheckIn] = [
        {
            "id": "1",
            "patient_id": "p1",
            "patient_name": "John Doe",
            "type": "voice",
            "summary": "Feeling good today, energy levels are up. Noticed some minor joint stiffness this morning but it went away after stretching.",
            "timestamp": "Today, 10:30 AM",
            "submitted_at": "2024-12-04T10:30:00",
            "sentiment": "positive",
            "key_topics": ["energy", "joint stiffness", "exercise"],
            "status": "pending",
            "provider_reviewed": False,
            "reviewed_by": "",
            "reviewed_at": "",
        },
        {
            "id": "2",
            "patient_id": "p2",
            "patient_name": "Sarah Johnson",
            "type": "text",
            "summary": "Had a headache yesterday evening. Took some water and rested, felt better after an hour. Wondering if it's related to my new medication.",
            "timestamp": "Today, 9:15 AM",
            "submitted_at": "2024-12-04T09:15:00",
            "sentiment": "neutral",
            "key_topics": ["headache", "hydration", "medication"],
            "status": "pending",
            "provider_reviewed": False,
            "reviewed_by": "",
            "reviewed_at": "",
        },
        {
            "id": "3",
            "patient_id": "p1",
            "patient_name": "John Doe",
            "type": "voice",
            "summary": "Blood sugar has been stable this week. Following the new meal plan closely. Feeling more energetic overall.",
            "timestamp": "Yesterday, 2:00 PM",
            "submitted_at": "2024-12-03T14:00:00",
            "sentiment": "positive",
            "key_topics": ["blood sugar", "diet", "medication"],
            "status": "reviewed",
            "provider_reviewed": True,
            "reviewed_by": "Dr. Chen",
            "reviewed_at": "2024-12-03T16:30:00",
        },
        {
            "id": "4",
            "patient_id": "p3",
            "patient_name": "Michael Brown",
            "type": "text",
            "summary": "Experiencing chest discomfort after exercise. Not sure if related to new workout routine or something else.",
            "timestamp": "Yesterday, 11:00 AM",
            "submitted_at": "2024-12-03T11:00:00",
            "sentiment": "concerned",
            "key_topics": ["chest pain", "exercise", "symptoms"],
            "status": "flagged",
            "provider_reviewed": True,
            "reviewed_by": "Dr. Chen",
            "reviewed_at": "2024-12-03T12:00:00",
        },
        {
            "id": "5",
            "patient_id": "p4",
            "patient_name": "Emily Davis",
            "type": "voice",
            "summary": "Sleep quality has improved since starting the new supplement regimen. Getting about 7-8 hours consistently now.",
            "timestamp": "2 days ago, 8:00 AM",
            "submitted_at": "2024-12-02T08:00:00",
            "sentiment": "positive",
            "key_topics": ["sleep", "supplements"],
            "status": "reviewed",
            "provider_reviewed": True,
            "reviewed_by": "Dr. Smith",
            "reviewed_at": "2024-12-02T10:00:00",
        },
        {
            "id": "6",
            "patient_id": "p2",
            "patient_name": "Sarah Johnson",
            "type": "voice",
            "summary": "Anxiety levels have been higher this week. Work stress is affecting my sleep and eating patterns.",
            "timestamp": "2 days ago, 4:30 PM",
            "submitted_at": "2024-12-02T16:30:00",
            "sentiment": "negative",
            "key_topics": ["anxiety", "stress", "sleep", "diet"],
            "status": "pending",
            "provider_reviewed": False,
            "reviewed_by": "",
            "reviewed_at": "",
        },
        {
            "id": "7",
            "patient_id": "p5",
            "patient_name": "Robert Wilson",
            "type": "text",
            "summary": "Blood pressure readings have been slightly elevated. Taking medication as prescribed but monitoring closely.",
            "timestamp": "3 days ago, 9:00 AM",
            "submitted_at": "2024-12-01T09:00:00",
            "sentiment": "neutral",
            "key_topics": ["blood pressure", "medication"],
            "status": "reviewed",
            "provider_reviewed": True,
            "reviewed_by": "Dr. Chen",
            "reviewed_at": "2024-12-01T11:00:00",
        },
    ]
    
    # Call log check-ins from API (merged with regular check-ins for admin view)
    call_log_checkins: List[AdminCheckIn] = []
    
    # Selected check-in for detail view
    selected_checkin: AdminCheckIn = {}
    show_checkin_detail_modal: bool = False
    
    @rx.var
    def combined_checkins(self) -> List[AdminCheckIn]:
        """Combine regular check-ins with call log check-ins."""
        return self.all_checkins + self.call_log_checkins
    
    @rx.var
    def filtered_checkins(self) -> List[AdminCheckIn]:
        """Get filtered check-ins based on status tab and search query."""
        # Start with combined check-ins
        results = self.combined_checkins
        
        # Filter by status tab
        if self.active_status_tab != "all":
            results = [c for c in results if c["status"] == self.active_status_tab]
        
        # Filter by search query
        if self.search_query.strip():
            query = self.search_query.lower()
            results = [
                c for c in results 
                if query in c["patient_name"].lower() 
                or query in c["summary"].lower()
                or any(query in topic.lower() for topic in c["key_topics"])
            ]
        
        # Sort by submitted_at (most recent first)
        results = sorted(results, key=lambda x: x["submitted_at"], reverse=True)
        
        return results
    
    @rx.var
    def pending_count(self) -> int:
        """Count of pending check-ins."""
        return len([c for c in self.combined_checkins if c["status"] == "pending"])
    
    @rx.var
    def reviewed_count(self) -> int:
        """Count of reviewed check-ins."""
        return len([c for c in self.combined_checkins if c["status"] == "reviewed"])
    
    @rx.var
    def flagged_count(self) -> int:
        """Count of flagged check-ins."""
        return len([c for c in self.combined_checkins if c["status"] == "flagged"])
    
    @rx.var
    def total_count(self) -> int:
        """Total count of all check-ins."""
        return len(self.combined_checkins)
    
    @rx.event
    async def sync_call_logs_to_admin(self):
        """Sync call logs from PatientState to admin view."""
        from .patient_state import PatientState
        
        patient_state = await self.get_state(PatientState)
        
        # Convert transcript summaries to AdminCheckIn format
        new_call_checkins = []
        for call_id, summary in patient_state.transcript_summaries.items():
            # Check if already exists
            existing_ids = [c["id"] for c in self.call_log_checkins]
            if f"call_{call_id}" in existing_ids:
                continue
            
            new_call_checkins.append({
                "id": f"call_{call_id}",
                "patient_id": "demo",
                "patient_name": "Demo Patient",  # Would map phone to patient name
                "type": "call",
                "summary": summary.get("ai_summary", "") or summary.get("summary", ""),
                "timestamp": summary.get("timestamp", ""),
                "submitted_at": summary.get("call_date", ""),
                "sentiment": "neutral",
                "key_topics": ["voice call", "AI assistant"],
                "status": "pending",
                "provider_reviewed": False,
                "reviewed_by": "",
                "reviewed_at": "",
            })
        
        if new_call_checkins:
            self.call_log_checkins = self.call_log_checkins + new_call_checkins
    
    def set_active_status_tab(self, tab: str):
        """Set the active status tab."""
        self.active_status_tab = tab
    
    def set_search_query(self, query: str):
        """Set the search query."""
        self.search_query = query
    
    def open_checkin_detail(self, checkin: AdminCheckIn):
        """Open check-in detail modal."""
        self.selected_checkin = checkin
        self.show_checkin_detail_modal = True
    
    def close_checkin_detail(self):
        """Close check-in detail modal."""
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}
    
    def set_show_checkin_detail_modal(self, value: bool):
        """Set the modal visibility."""
        self.show_checkin_detail_modal = value
        if not value:
            self.selected_checkin = {}
    
    def mark_as_reviewed(self, checkin_id: str):
        """Mark a check-in as reviewed."""
        # Check in regular checkins
        updated = []
        for checkin in self.all_checkins:
            if checkin["id"] == checkin_id:
                updated.append({
                    **checkin,
                    "status": "reviewed",
                    "provider_reviewed": True,
                    "reviewed_by": "Dr. Admin",
                    "reviewed_at": "Just now",
                })
            else:
                updated.append(checkin)
        self.all_checkins = updated
        
        # Check in call log checkins
        updated_calls = []
        for checkin in self.call_log_checkins:
            if checkin["id"] == checkin_id:
                updated_calls.append({
                    **checkin,
                    "status": "reviewed",
                    "provider_reviewed": True,
                    "reviewed_by": "Dr. Admin",
                    "reviewed_at": "Just now",
                })
            else:
                updated_calls.append(checkin)
        self.call_log_checkins = updated_calls
        
        self.show_checkin_detail_modal = False
    
    def flag_checkin(self, checkin_id: str):
        """Flag a check-in for follow-up."""
        # Check in regular checkins
        updated = []
        for checkin in self.all_checkins:
            if checkin["id"] == checkin_id:
                updated.append({
                    **checkin,
                    "status": "flagged",
                    "provider_reviewed": True,
                    "reviewed_by": "Dr. Admin",
                    "reviewed_at": "Just now",
                })
            else:
                updated.append(checkin)
        self.all_checkins = updated
        
        # Check in call log checkins
        updated_calls = []
        for checkin in self.call_log_checkins:
            if checkin["id"] == checkin_id:
                updated_calls.append({
                    **checkin,
                    "status": "flagged",
                    "provider_reviewed": True,
                    "reviewed_by": "Dr. Admin",
                    "reviewed_at": "Just now",
                })
            else:
                updated_calls.append(checkin)
        self.call_log_checkins = updated_calls
        
        self.show_checkin_detail_modal = False
