import os
from typing import Literal

from pydantic import BaseModel, computed_field


class DemoUserConfig(BaseModel):
    """Demo user profile configuration for sidebar and UI display."""

    full_name: str = "Sarah Chen"
    email: str = "sarah.chen@longevityclinic.com"
    role: Literal["admin", "patient"] = "patient"

    @computed_field
    @property
    def initials(self) -> str:
        """Generate initials from full name."""
        parts = self.full_name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return self.full_name[:2].upper() if self.full_name else "?"

    @computed_field
    @property
    def role_label(self) -> str:
        """Human-readable role label."""
        return "Administrator" if self.role == "admin" else "Patient"

    @computed_field
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"


class AppConfig(BaseModel):
    """Main application configuration."""

    app_name: str = os.getenv("APP_NAME", "Vitality Clinic")
    clinic_name: str = os.getenv("CLINIC_NAME", "Vitality Health")
    admin_role_name: str = os.getenv("ADMIN_ROLE_NAME", "Administrator")
    patient_role_name: str = os.getenv("PATIENT_ROLE_NAME", "Patient")
    theme_color: str = os.getenv("THEME_COLOR", "emerald")
    
    # Glass UI Styles
    glass_bg_gradient: str = "bg-[radial-gradient(circle_at_top_left,_var(--tw-gradient-stops))] from-blue-50/30 via-white to-emerald-50/30"
    glass_panel_style: str = "bg-white/60 backdrop-blur-3xl border border-white/40 shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-[2rem] hover:bg-white/80 transition-all duration-500"
    glass_header_style: str = "bg-white/30 backdrop-blur-xl border-b border-white/20 sticky top-0 z-50 supports-[backdrop-filter]:bg-white/10"
    glass_sidebar_style: str = "bg-white/20 backdrop-blur-2xl border-r border-white/20 supports-[backdrop-filter]:bg-white/10"
    glass_card_hover: str = "hover:bg-white/80 hover:shadow-[0_20px_40px_rgb(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-500 ease-out border-white/50"
    glass_input_style: str = "bg-white/30 backdrop-blur-lg border border-white/40 focus:bg-white/60 focus:ring-2 focus:ring-emerald-500/5 focus:border-emerald-500/10 rounded-2xl placeholder-gray-400/60 transition-all duration-300 outline-none text-gray-700 font-light tracking-wide shadow-[inset_0_2px_4px_rgba(0,0,0,0.01)]"
    glass_button_primary: str = "bg-emerald-500/80 hover:bg-emerald-500/90 text-white shadow-lg shadow-emerald-500/10 backdrop-blur-md border border-white/20 rounded-2xl transition-all duration-300 active:scale-[0.98] font-medium tracking-wide hover:shadow-emerald-500/20"
    glass_button_secondary: str = "bg-white/40 hover:bg-white/70 text-gray-600 border border-white/40 shadow-sm backdrop-blur-md rounded-2xl transition-all duration-300 active:scale-[0.98] font-medium hover:text-gray-900"

    # Demo user for UI display
    demo_user: DemoUserConfig = DemoUserConfig()


current_config = AppConfig()