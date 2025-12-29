"""Structured style schema used across the application."""

from typing import TypedDict

from pydantic import BaseModel, Field


# =============================================================================
# Apple Glass Teal/Green UI Styles
# Focus: Transparent/frosted backgrounds, light teal accents, subtle gradients
# =============================================================================
class GlassStyles:
    """Apple Glass aesthetic with teal/green hue for the entire application."""

    # Page background - dark gradient with teal accent
    PAGE_BG = (
        "bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 "
        "min-h-screen font-sans text-slate-100"
    )

    # Light mode page background (for admin/patient portals)
    PAGE_BG_LIGHT = (
        "bg-[radial-gradient(circle_at_top_left,_var(--tw-gradient-stops))] "
        "from-teal-50/30 via-white to-emerald-50/30 min-h-screen font-sans text-gray-800"
    )

    # Glass panel - frosted glass effect
    PANEL = (
        "bg-white/5 backdrop-blur-xl border border-white/10 "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] rounded-2xl"
    )

    # Light glass panel for light mode
    PANEL_LIGHT = (
        "bg-white/60 backdrop-blur-3xl border border-white/40 "
        "shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-2xl"
    )

    # Navbar styles
    NAVBAR = (
        "fixed top-4 left-4 right-4 h-16 z-50 bg-slate-900/60 backdrop-blur-md "
        "border border-white/10 rounded-2xl flex items-center justify-between px-6 shadow-lg"
    )

    NAVBAR_LIGHT = (
        "bg-white/30 backdrop-blur-xl border-b border-white/20 sticky top-0 z-50 "
        "supports-[backdrop-filter]:bg-white/10"
    )

    # Interactive card with hover effects
    CARD_INTERACTIVE = (
        "group relative overflow-hidden rounded-2xl p-6 bg-white/5 border border-white/10 "
        "backdrop-blur-md hover:bg-white/10 hover:border-teal-400/30 "
        "hover:shadow-[0_0_20px_rgba(45,212,191,0.1)] transition-all duration-300 cursor-pointer"
    )

    CARD_INTERACTIVE_LIGHT = (
        "group relative overflow-hidden rounded-2xl p-6 bg-white/60 border border-white/40 "
        "backdrop-blur-md hover:bg-white/80 hover:border-teal-400/30 "
        "hover:shadow-[0_20px_40px_rgb(0,0,0,0.06)] hover:-translate-y-1 "
        "transition-all duration-500 ease-out cursor-pointer"
    )

    # Typography styles
    HEADING = "font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-200 to-teal-400"
    HEADING_LIGHT = "font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-emerald-600"
    SUBHEADING = "text-slate-400 text-sm tracking-wide font-medium"
    SUBHEADING_LIGHT = "text-gray-500 text-sm tracking-wide font-medium"
    TEXT_MAIN = "text-slate-200"
    TEXT_MAIN_LIGHT = "text-gray-700"

    # Primary button - teal gradient
    BUTTON_PRIMARY = (
        "px-7 py-2.5 rounded-xl font-medium bg-gradient-to-r from-teal-500/80 to-teal-400/80 "
        "hover:from-teal-400 hover:to-teal-300 text-slate-900 shadow-lg shadow-teal-500/20 "
        "transition-all duration-200 backdrop-blur-sm"
    )

    BUTTON_PRIMARY_LIGHT = (
        "px-6 py-2.5 rounded-xl font-medium bg-gradient-to-r from-teal-600 to-emerald-500 "
        "hover:from-teal-500 hover:to-emerald-400 text-white shadow-lg shadow-teal-500/25 "
        "transition-all duration-200 backdrop-blur-sm"
    )

    # Secondary button - glass effect
    BUTTON_SECONDARY = (
        "px-6 py-2.5 rounded-xl font-medium bg-white/5 border border-white/10 "
        "text-slate-300 hover:bg-white/10 hover:text-white transition-all duration-200 backdrop-blur-sm"
    )

    BUTTON_SECONDARY_LIGHT = (
        "px-6 py-2.5 rounded-xl font-medium bg-white/40 border border-white/40 "
        "text-gray-600 hover:bg-white/70 hover:text-gray-900 "
        "transition-all duration-200 backdrop-blur-sm"
    )

    # Input styles for login/dark mode forms
    INPUT = (
        "w-full bg-slate-700/30 border border-slate-600/50 rounded-2xl px-6 py-4 "
        "text-white placeholder-slate-500 focus:outline-none focus:border-teal-400/60 "
        "focus:ring-2 focus:ring-teal-400/20 backdrop-blur-md transition-all"
    )

    INPUT_LIGHT = (
        "w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 "
        "text-gray-900 placeholder-gray-400 focus:outline-none focus:border-teal-400 "
        "focus:ring-2 focus:ring-teal-400/20 transition-all"
    )

    # Teal glow effect
    GLOW_TEAL = "shadow-[0_0_15px_rgba(45,212,191,0.3)]"

    # Icon button (for header icons like bell, plus)
    ICON_BUTTON = (
        "p-2.5 rounded-full hover:bg-white/10 hover:shadow-sm transition-all "
        "relative border border-transparent hover:border-white/20 active:scale-95"
    )

    ICON_BUTTON_LIGHT = (
        "p-2.5 rounded-full hover:bg-white/60 hover:shadow-sm transition-all "
        "relative border border-transparent hover:border-white/50 active:scale-95"
    )

    # Sidebar styles
    SIDEBAR = (
        "bg-slate-900/80 backdrop-blur-2xl border-r border-white/10 "
        "supports-[backdrop-filter]:bg-slate-900/60"
    )

    SIDEBAR_LIGHT = (
        "bg-white/20 backdrop-blur-2xl border-r border-white/20 "
        "supports-[backdrop-filter]:bg-white/10"
    )

    # Tab styles
    TAB_LIST = (
        "flex gap-1 p-1 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10"
    )

    TAB_LIST_LIGHT = (
        "flex gap-1 p-1 bg-white/30 backdrop-blur-sm rounded-xl border border-white/30"
    )

    TAB_TRIGGER = (
        "px-4 py-2 rounded-lg text-sm font-medium text-slate-400 "
        "hover:text-white hover:bg-white/10 transition-all duration-200 "
        "data-[state=active]:bg-teal-500/20 data-[state=active]:text-teal-300 "
        "data-[state=active]:shadow-sm"
    )

    TAB_TRIGGER_LIGHT = (
        "px-4 py-2 rounded-lg text-sm font-medium text-gray-500 "
        "hover:text-gray-900 hover:bg-white/50 transition-all duration-200 "
        "data-[state=active]:bg-white data-[state=active]:text-teal-700 "
        "data-[state=active]:shadow-sm"
    )

    # Modal overlay - semi-transparent dark with blur
    MODAL_OVERLAY = "fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50"

    # Modal shorthand (for dark mode modals)
    modal = (
        "bg-slate-800/90 backdrop-blur-xl border border-slate-700/50 "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.5)] rounded-2xl p-6"
    )
    MODAL = modal  # Alias for uppercase access

    # Card shorthand (for dark mode cards)
    card = (
        "bg-slate-800/60 backdrop-blur-xl border border-slate-700/50 rounded-2xl "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.3)]"
    )
    CARD = card  # Alias for uppercase access

    # Glass panel for modals
    MODAL_PANEL = (
        "bg-white/90 backdrop-blur-xl border border-teal-100/50 "
        "shadow-[0_8px_32px_0_rgba(20,184,166,0.15)] rounded-2xl"
    )

    # Modal content positioning
    MODAL_CONTENT = (
        "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] p-6 z-50"
    )
    MODAL_CONTENT_SM = f"{MODAL_CONTENT} max-w-sm"
    MODAL_CONTENT_MD = f"{MODAL_CONTENT} max-w-md"
    MODAL_CONTENT_LG = f"{MODAL_CONTENT} max-w-lg"
    MODAL_CONTENT_XL = f"{MODAL_CONTENT} max-w-xl"
    MODAL_CONTENT_2XL = f"{MODAL_CONTENT} max-w-2xl"

    # Modal title and description
    MODAL_TITLE = "text-xl font-bold text-gray-900 mb-2"
    MODAL_DESCRIPTION = "text-gray-500 mb-6 text-sm"

    # Glass input styles for modals
    MODAL_INPUT = (
        "w-full bg-teal-50/30 border border-teal-200/50 rounded-xl px-4 py-3 "
        "text-gray-800 placeholder-gray-400 focus:outline-none focus:border-teal-400/60 "
        "focus:ring-2 focus:ring-teal-400/20 transition-all"
    )

    MODAL_SELECT = (
        "w-full bg-teal-50/30 border border-teal-200/50 rounded-xl px-4 py-3 "
        "text-gray-800 focus:outline-none focus:border-teal-400/60 "
        "focus:ring-2 focus:ring-teal-400/20 transition-all"
    )

    MODAL_TEXTAREA = (
        "w-full bg-teal-50/30 border border-teal-200/50 rounded-xl px-4 py-3 "
        "text-gray-800 placeholder-gray-400 focus:outline-none focus:border-teal-400/60 "
        "focus:ring-2 focus:ring-teal-400/20 resize-none transition-all"
    )

    # Button cancel style
    BUTTON_CANCEL = "px-4 py-2 text-gray-500 hover:text-gray-700 transition-colors"

    # Close button for modals
    CLOSE_BUTTON = (
        "p-2 rounded-full hover:bg-teal-100/50 text-gray-400 hover:text-gray-600 "
        "transition-colors"
    )

    # Label style
    LABEL = "block text-sm font-medium text-gray-700 mb-2"

    # Footer for modal buttons
    MODAL_FOOTER = "flex justify-end gap-3 mt-6 pt-4 border-t border-teal-100/50"

    # Stat card styles
    STAT_CARD = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 "
        "hover:bg-white/10 transition-all duration-300"
    )

    STAT_CARD_LIGHT = (
        "bg-white/60 backdrop-blur-xl border border-white/40 rounded-2xl p-6 "
        "hover:bg-white/80 hover:shadow-lg transition-all duration-300"
    )

    # Notification badge
    NOTIFICATION_BADGE = (
        "absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-r from-rose-500 to-pink-500 "
        "rounded-full flex items-center justify-center text-[10px] font-bold text-white "
        "shadow-lg shadow-rose-500/30"
    )

    # Calendar styles
    CALENDAR_CONTAINER = (
        "bg-white/90 backdrop-blur-xl border border-teal-100/50 rounded-2xl p-4 "
        "shadow-[0_8px_32px_0_rgba(20,184,166,0.1)]"
    )

    CALENDAR_DAY = (
        "w-10 h-10 rounded-xl flex items-center justify-center text-sm font-medium "
        "hover:bg-teal-100/50 transition-colors cursor-pointer"
    )

    CALENDAR_DAY_SELECTED = (
        "w-10 h-10 rounded-xl flex items-center justify-center text-sm font-medium "
        "bg-gradient-to-r from-teal-500 to-emerald-500 text-white shadow-lg shadow-teal-500/25"
    )

    CALENDAR_DAY_TODAY = (
        "w-10 h-10 rounded-xl flex items-center justify-center text-sm font-medium "
        "border-2 border-teal-400 text-teal-600"
    )

    # ==========================================================================
    # Analytics Dashboard Styles (Dark Mode)
    # ==========================================================================

    # Analytics page heading
    ANALYTICS_HEADING = "text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-200 to-teal-400"

    # Analytics summary card (dark mode)
    ANALYTICS_SUMMARY_CARD = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.37)]"
    )

    # ==========================================================================
    # Biomarker Card Styles (Dark Mode - Emerald/Teal Glass Theme)
    # Professional card styling for biomarker metrics in patient portal
    # ==========================================================================

    # Biomarker metric card (dark mode) - emerald-tinted glass
    BIOMARKER_CARD = (
        "bg-gradient-to-br from-slate-800/60 to-emerald-900/20 backdrop-blur-xl "
        "border border-emerald-500/10 rounded-2xl p-6 "
        "hover:shadow-lg hover:shadow-emerald-500/5 hover:border-emerald-500/25 "
        "transition-all duration-300"
    )

    # Biomarker card selected state
    BIOMARKER_CARD_SELECTED = "ring-1 ring-teal-500/40 cursor-pointer transition-all duration-300 scale-[1.02]"

    # Biomarker card typography
    BIOMARKER_CARD_TITLE = "text-sm font-semibold text-white truncate"
    BIOMARKER_CARD_CATEGORY = "text-[10px] text-slate-400 truncate uppercase tracking-widest font-semibold mt-1"
    BIOMARKER_CARD_VALUE = "text-4xl font-thin text-white tracking-tighter"
    BIOMARKER_CARD_UNIT = "text-xs font-medium text-slate-400 ml-1"

    # Biomarker trend indicators
    BIOMARKER_TREND_ICON_UP = "w-4 h-4 mr-1 text-teal-400"
    BIOMARKER_TREND_ICON_DOWN = "w-4 h-4 mr-1 text-teal-400"
    BIOMARKER_TREND_ICON_STABLE = "w-4 h-4 mr-1 text-slate-400"
    BIOMARKER_TREND_TEXT_UP = "text-xs text-teal-300"
    BIOMARKER_TREND_TEXT_DOWN = "text-xs text-teal-300"
    BIOMARKER_TREND_TEXT_STABLE = "text-xs text-slate-300"

    # Biomarker detail panel (dark mode)
    BIOMARKER_DETAIL_PANEL = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] p-6 mb-8 animate-fade-in"
    )
    BIOMARKER_DETAIL_TITLE = "text-xl font-bold text-white"
    BIOMARKER_DETAIL_DESCRIPTION = "text-sm text-slate-400 mt-1"
    BIOMARKER_DETAIL_CLOSE_BTN = "p-2 hover:bg-white/10 rounded-full text-slate-400 hover:text-white transition-colors"
    BIOMARKER_DETAIL_SECTION_TITLE = "text-sm font-semibold text-slate-300 mb-4"
    BIOMARKER_DETAIL_LABEL = "text-xs text-slate-400 uppercase font-semibold"
    BIOMARKER_DETAIL_VALUE = "text-white font-medium"
    BIOMARKER_DETAIL_ANALYSIS_BOX = (
        "bg-slate-800/50 p-4 rounded-xl border border-slate-700/50"
    )

    # Biomarker status text colors
    BIOMARKER_STATUS_OPTIMAL_TEXT = "text-teal-400 font-bold"
    BIOMARKER_STATUS_WARNING_TEXT = "text-amber-400 font-bold"
    BIOMARKER_STATUS_CRITICAL_TEXT = "text-red-400 font-bold"
    BIOMARKER_STATUS_DEFAULT_TEXT = "text-slate-300 font-bold"

    # ==========================================================================
    # Portal Treatment Card Styles (Dark Mode - Teal Theme)
    # Compact treatment cards for patient portal overview
    # ==========================================================================

    # Portal treatment card (dark mode, compact)
    PORTAL_TREATMENT_CARD = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl p-4 "
        "hover:bg-white/10 transition-all"
    )
    PORTAL_TREATMENT_ICON_CONTAINER = (
        "w-10 h-10 rounded-full bg-teal-500/10 flex items-center justify-center "
        "mr-3 shrink-0 border border-teal-500/20"
    )
    PORTAL_TREATMENT_ICON = "w-5 h-5 text-teal-400"
    PORTAL_TREATMENT_TITLE = "text-sm font-semibold text-white"
    PORTAL_TREATMENT_META = "text-xs text-slate-400"
    PORTAL_TREATMENT_STATUS_BADGE = (
        "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium "
        "bg-teal-500/10 text-teal-300 border border-teal-500/20"
    )

    # ==========================================================================
    # Treatment Card Styles (Dark Mode - Emerald/Teal Theme)
    # Professional card styling for treatment protocols - patient/admin views
    # NOTE: Use adequate padding (p-6+) to prevent descender cutoff (g, p, y, q)
    # ==========================================================================

    # Treatment card - dark glass panel with emerald accent
    TREATMENT_CARD = (
        "bg-slate-800/70 backdrop-blur-xl border border-slate-700/50 rounded-2xl "
        "shadow-[0_4px_20px_rgba(0,0,0,0.3)] "
        "hover:border-emerald-500/30 hover:shadow-[0_8px_30px_rgba(16,185,129,0.1)] "
        "hover:-translate-y-0.5 transition-all duration-300 "
        "flex flex-col h-full"
    )

    # Treatment card content padding - extra bottom padding for descenders
    TREATMENT_CARD_CONTENT = "p-6 pb-7 flex-1 flex flex-col"

    # Treatment card title - white text for dark mode
    TREATMENT_CARD_TITLE = "text-lg font-semibold text-white tracking-tight truncate flex-1 leading-relaxed"

    # Treatment card description - light slate for readability on dark
    TREATMENT_CARD_DESCRIPTION = "text-sm text-slate-300 line-clamp-2 mb-5 font-light leading-relaxed min-h-[2.75rem]"

    # Treatment meta item (duration, cost, etc.)
    TREATMENT_META_ITEM = "flex items-center"
    TREATMENT_META_ICON = "w-3.5 h-3.5 text-emerald-400 mr-1.5 flex-shrink-0"
    TREATMENT_META_TEXT = "text-xs text-slate-300 font-medium"

    # Treatment card footer buttons - emerald accent for dark mode
    TREATMENT_CARD_FOOTER = "flex border-t border-slate-700/50"
    TREATMENT_CARD_BUTTON_PRIMARY = (
        "flex-1 py-3.5 text-sm font-medium text-emerald-400 hover:text-emerald-300 "
        "hover:bg-emerald-500/10 transition-colors"
    )
    TREATMENT_CARD_BUTTON_SECONDARY = (
        "flex-1 py-3.5 text-sm font-medium text-slate-300 hover:text-emerald-400 "
        "hover:bg-emerald-500/10 border-r border-slate-700/50 transition-colors"
    )

    # Metric label (small uppercase)
    METRIC_LABEL = "text-[10px] font-bold text-slate-400 uppercase tracking-widest"

    # Metric value (large number)
    METRIC_VALUE = "text-4xl font-light text-white tracking-tighter"
    METRIC_VALUE_SM = "text-2xl font-bold text-white"

    # Metric unit
    METRIC_UNIT = "text-[10px] text-slate-400 font-semibold uppercase"

    # Status badges for biomarkers (emerald for optimal to match theme)
    STATUS_OPTIMAL = (
        "px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-bold "
        "border border-emerald-400/30 backdrop-blur-md shadow-sm uppercase tracking-wide"
    )
    STATUS_WARNING = (
        "px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-[10px] font-bold "
        "border border-amber-400/30 backdrop-blur-md shadow-sm uppercase tracking-wide"
    )
    STATUS_CRITICAL = (
        "px-3 py-1 rounded-full bg-red-500/20 text-red-300 text-[10px] font-bold "
        "border border-red-400/30 backdrop-blur-md shadow-sm uppercase tracking-wide"
    )
    STATUS_DEFAULT = (
        "px-3 py-1 rounded-full bg-slate-500/20 text-slate-300 text-[10px] font-bold "
        "border border-slate-400/30 backdrop-blur-md shadow-sm uppercase tracking-wide"
    )

    # Status indicator dots (emerald for optimal)
    DOT_OPTIMAL = "h-1.5 w-1.5 rounded-full bg-emerald-400 mr-2 shadow-[0_0_8px_rgba(52,211,153,0.4)]"
    DOT_WARNING = "h-1.5 w-1.5 rounded-full bg-amber-400 mr-2 shadow-[0_0_8px_rgba(251,191,36,0.4)]"
    DOT_CRITICAL = "h-1.5 w-1.5 rounded-full bg-red-400 mr-2 shadow-[0_0_8px_rgba(248,113,113,0.4)]"
    DOT_DEFAULT = "h-1.5 w-1.5 rounded-full bg-slate-500 mr-2"

    # Reference range pill
    REFERENCE_RANGE_PILL = (
        "flex items-center bg-slate-700/30 rounded-full px-3 py-1.5 w-fit "
        "border border-slate-600/40 backdrop-blur-sm"
    )
    REFERENCE_LABEL = (
        "text-[9px] text-slate-400 mr-2 uppercase tracking-widest font-bold"
    )
    REFERENCE_VALUE = "text-xs font-semibold text-slate-300"

    # Section headers
    SECTION_TITLE = "text-lg font-medium text-white mb-5 ml-1 flex items-center gap-2"
    SECTION_TITLE_LG = "text-xl font-bold text-white mb-6"
    SECTION_TITLE_XL = "text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-200 to-teal-400 mb-6"

    # Chart container (dark mode)
    CHART_CONTAINER = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.37)]"
    )

    # Insights card
    INSIGHTS_CARD = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] mt-8"
    )

    # KPI card for admin dashboards (dark mode)
    KPI_CARD = (
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 "
        "shadow-[0_8px_32px_0_rgba(0,0,0,0.37)]"
    )

    # Trend badge (positive/negative)
    TREND_POSITIVE = (
        "text-xs font-medium px-2 py-1 rounded-full border "
        "bg-teal-500/10 text-teal-400 border-teal-500/20"
    )
    TREND_NEGATIVE = (
        "text-xs font-medium px-2 py-1 rounded-full border "
        "bg-red-500/10 text-red-400 border-red-500/20"
    )

    # Category accordion/details
    CATEGORY_SUMMARY = (
        "flex items-center justify-between cursor-pointer list-none p-4 "
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl mb-4 "
        "hover:bg-white/10 transition-colors"
    )

    # ==========================================================================
    # Collapsible Section Styles (Dark Slate - Matches Page Background)
    # Professional accordion styling - seamless with dark slate-900 page
    # ==========================================================================

    # Collapsible item - dark slate matching page background (slate-900)
    # Explicit background to override any Radix default blue styles
    COLLAPSIBLE_ITEM = (
        "!bg-slate-900 rounded-xl "
        "border border-slate-700/40 "
        "hover:border-emerald-500/40 "
        "my-2 overflow-hidden transition-all duration-300 ease-out"
    )

    # Collapsible trigger header - dark slate background
    # Explicit !bg to override Radix defaults
    COLLAPSIBLE_TRIGGER = (
        "group flex w-full px-5 py-4 "
        "!bg-slate-900 hover:!bg-slate-800 "
        "transition-all duration-300 cursor-pointer"
    )

    # Collapsible chevron with smooth rotation animation
    COLLAPSIBLE_CHEVRON = (
        "w-5 h-5 text-emerald-400 transition-transform duration-300 ease-out "
        "group-hover:text-emerald-300 "
        "group-data-[state=open]:rotate-180"
    )

    # Collapsible content wrapper with smooth accordion animation
    # No background color - inherits from parent to match app background
    COLLAPSIBLE_CONTENT = (
        "overflow-hidden "
        "data-[state=open]:animate-accordion-down "
        "data-[state=closed]:animate-accordion-up"
    )

    # Collapsible content inner padding
    COLLAPSIBLE_CONTENT_INNER = "px-5 pb-5 pt-3"

    # Collapsible container (accordion root)
    # Explicit dark slate background to override Radix default blue
    COLLAPSIBLE_CONTAINER = "w-full space-y-3 px-1 py-2 !bg-transparent"

    # Collapsible badge - refined emerald pill
    COLLAPSIBLE_BADGE = (
        "text-xs font-semibold text-emerald-300 "
        "bg-emerald-500/15 backdrop-blur-sm "
        "px-3 py-1 rounded-full mr-3 "
        "border border-emerald-500/25 "
        "shadow-[0_0_8px_rgba(16,185,129,0.15)]"
    )

    # Collapsible title - clean white text with subtle shadow
    COLLAPSIBLE_TITLE = (
        "text-base font-semibold text-slate-100 "
        "group-hover:text-white transition-colors duration-200"
    )

    # Collapsible icon - emerald accent
    COLLAPSIBLE_ICON = (
        "w-5 h-5 text-emerald-400 mr-3 "
        "group-hover:text-emerald-300 transition-colors duration-200"
    )


# =============================================================================
# Tab Card Configuration (for standardized health cards)
# =============================================================================


class TabCardTheme(TypedDict):
    """Theme configuration for tab cards."""

    icon_color: str  # Tailwind text color for icon
    icon_bg: str  # Background color for icon container
    icon_border: str  # Border color for icon container


# Predefined themes for different health categories
TAB_CARD_THEMES: dict[str, TabCardTheme] = {
    "food": {
        "icon_color": "text-teal-400",
        "icon_bg": "bg-teal-500/10",
        "icon_border": "border-teal-500/20",
    },
    "medication": {
        "icon_color": "text-purple-400",
        "icon_bg": "bg-purple-500/10",
        "icon_border": "border-purple-500/20",
    },
    "symptom": {
        "icon_color": "text-orange-400",
        "icon_bg": "bg-orange-500/10",
        "icon_border": "border-orange-500/20",
    },
    "condition": {
        "icon_color": "text-rose-400",
        "icon_bg": "bg-rose-500/10",
        "icon_border": "border-rose-500/20",
    },
    "appointment": {
        "icon_color": "text-blue-400",
        "icon_bg": "bg-blue-500/10",
        "icon_border": "border-blue-500/20",
    },
    "exercise": {
        "icon_color": "text-amber-400",
        "icon_bg": "bg-amber-500/10",
        "icon_border": "border-amber-500/20",
    },
}


# Shared building blocks ----------------------------------------------------
_MODAL_PANEL_BASE = (
    "bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform "
    "transition-all sm:p-6"
)
_MODAL_PANEL_SM = f"{_MODAL_PANEL_BASE} sm:max-w-sm sm:w-full"
_MODAL_PANEL_MD = f"{_MODAL_PANEL_BASE} sm:max-w-md sm:w-full"
_MODAL_PANEL_LG = f"{_MODAL_PANEL_BASE} sm:max-w-lg sm:w-full"
_MODAL_PANEL_XL = f"{_MODAL_PANEL_BASE} sm:max-w-xl sm:w-full"

_BUTTON_BASE = (
    "inline-flex justify-center py-2 px-4 border shadow-sm text-sm font-medium "
    "rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2"
)
_BUTTON_PRIMARY = (
    f"{_BUTTON_BASE} border-transparent text-white bg-emerald-600 hover:bg-emerald-700 "
    "focus:ring-emerald-500"
)
_BUTTON_SECONDARY = (
    f"{_BUTTON_BASE} border-gray-300 text-gray-700 bg-white hover:bg-gray-50 "
    "focus:ring-emerald-500"
)
_BUTTON_DISABLED = "disabled:opacity-50 disabled:cursor-not-allowed"

_FORM_INPUT_BASE = (
    "mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 "
    "focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
)

_BADGE_BASE = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
_ALERT_BASE = "p-3 rounded-md border"
_TEXT_BASE = "text-sm font-medium"


class ZIndexStyles(BaseModel):
    base: str = "z-0"
    dropdown: str = "z-10"
    sticky: str = "z-20"
    sidebar: str = "z-40"
    header: str = "z-50"
    modal: str = "z-[60]"
    tooltip: str = "z-[70]"


class ModalStyles(BaseModel):
    overlay: str = "fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
    container: str = "fixed inset-0 overflow-y-auto"
    content_wrapper: str = "flex items-center justify-center min-h-screen p-4"
    panel_base: str = _MODAL_PANEL_BASE
    panel_sm: str = _MODAL_PANEL_SM
    panel_md: str = _MODAL_PANEL_MD
    panel_lg: str = _MODAL_PANEL_LG
    panel_xl: str = _MODAL_PANEL_XL
    header: str = "flex justify-between items-center mb-5 pb-4 border-b"
    title: str = "text-lg leading-6 font-medium text-gray-900"
    close_button: str = (
        "bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none"
    )
    footer: str = "mt-8 flex justify-end"
    footer_gap: str = "flex justify-end gap-3"


class ButtonStyles(BaseModel):
    base: str = _BUTTON_BASE
    primary: str = _BUTTON_PRIMARY
    secondary: str = _BUTTON_SECONDARY
    disabled: str = _BUTTON_DISABLED


class FormStyles(BaseModel):
    label: str = "block text-sm font-medium text-gray-700"
    input: str = _FORM_INPUT_BASE
    select: str = _FORM_INPUT_BASE
    textarea: str = f"{_FORM_INPUT_BASE} resize-none"


class GridStyles(BaseModel):
    two_cols: str = "grid grid-cols-1 md:grid-cols-2 gap-6"
    three_cols: str = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    four_cols: str = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
    six_cols: str = "grid grid-cols-6 gap-6"


class CardStyles(BaseModel):
    base: str = "bg-white rounded-lg shadow-sm border border-gray-200"
    hover: str = Field(
        default_factory=lambda: (
            "bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md "
            "transition-shadow duration-200"
        )
    )
    padding: str = "p-5"
    padding_lg: str = "p-6"


class BadgeStyles(BaseModel):
    base: str = _BADGE_BASE
    blue: str = f"{_BADGE_BASE} bg-blue-100 text-blue-800"
    green: str = f"{_BADGE_BASE} bg-green-100 text-green-800"
    yellow: str = f"{_BADGE_BASE} bg-yellow-100 text-yellow-800"
    red: str = f"{_BADGE_BASE} bg-red-100 text-red-800"
    purple: str = f"{_BADGE_BASE} bg-purple-100 text-purple-800"
    pink: str = f"{_BADGE_BASE} bg-pink-100 text-pink-800"
    cyan: str = f"{_BADGE_BASE} bg-cyan-100 text-cyan-800"
    orange: str = f"{_BADGE_BASE} bg-orange-100 text-orange-800"
    gray: str = f"{_BADGE_BASE} bg-gray-100 text-gray-800"


class StatusBadgeStyles(BaseModel):
    optimal: str = f"{_BADGE_BASE} bg-emerald-100 text-emerald-800"
    warning: str = f"{_BADGE_BASE} bg-yellow-100 text-yellow-800"
    critical: str = f"{_BADGE_BASE} bg-red-100 text-red-800"


class AlertStyles(BaseModel):
    success: str = f"bg-emerald-50 {_ALERT_BASE} border-emerald-100"
    warning: str = f"bg-yellow-50 {_ALERT_BASE} border-yellow-100"
    error: str = f"bg-red-50 {_ALERT_BASE} border-red-100"
    info: str = f"bg-blue-50 {_ALERT_BASE} border-blue-100"


class TextStyles(BaseModel):
    success: str = f"{_TEXT_BASE} text-emerald-700"
    warning: str = f"{_TEXT_BASE} text-yellow-700"
    error: str = f"{_TEXT_BASE} text-red-700"
    info: str = f"{_TEXT_BASE} text-blue-700"


class AppStyles(BaseModel):
    z_index: ZIndexStyles = Field(default_factory=ZIndexStyles)
    modal: ModalStyles = Field(default_factory=ModalStyles)
    buttons: ButtonStyles = Field(default_factory=ButtonStyles)
    forms: FormStyles = Field(default_factory=FormStyles)
    grids: GridStyles = Field(default_factory=GridStyles)
    cards: CardStyles = Field(default_factory=CardStyles)
    badges: BadgeStyles = Field(default_factory=BadgeStyles)
    status_badges: StatusBadgeStyles = Field(default_factory=StatusBadgeStyles)
    alerts: AlertStyles = Field(default_factory=AlertStyles)
    text: TextStyles = Field(default_factory=TextStyles)


styles = AppStyles()


# =============================================================================
# Category Display Styles
# =============================================================================
from longevity_clinic.app.data.schemas.db.domain_enums import TreatmentCategoryEnum


class CategoryColorConfig(TypedDict):
    """Color configuration for a category."""

    bg: str
    text: str


# Color mappings for treatment categories (UI display purposes)
# Keys use TreatmentCategoryEnum from domain_enums for type safety
TREATMENT_CATEGORY_COLORS: dict[TreatmentCategoryEnum, CategoryColorConfig] = {
    TreatmentCategoryEnum.IV_THERAPY: {"bg": "bg-blue-100", "text": "text-blue-800"},
    TreatmentCategoryEnum.CRYOTHERAPY: {"bg": "bg-cyan-100", "text": "text-cyan-800"},
    TreatmentCategoryEnum.SUPPLEMENTS: {"bg": "bg-green-100", "text": "text-green-800"},
    TreatmentCategoryEnum.HORMONE_THERAPY: {
        "bg": "bg-purple-100",
        "text": "text-purple-800",
    },
    TreatmentCategoryEnum.PHYSICAL_THERAPY: {
        "bg": "bg-orange-100",
        "text": "text-orange-800",
    },
    TreatmentCategoryEnum.SPA_SERVICES: {"bg": "bg-pink-100", "text": "text-pink-800"},
}


__all__ = [
    "TAB_CARD_THEMES",
    "TREATMENT_CATEGORY_COLORS",
    "AlertStyles",
    "AppStyles",
    "BadgeStyles",
    "ButtonStyles",
    "CardStyles",
    "CategoryColorConfig",
    "FormStyles",
    "GlassStyles",
    "GridStyles",
    "ModalStyles",
    "StatusBadgeStyles",
    "TabCardTheme",
    "TextStyles",
    "TreatmentCategoryEnum",  # Re-exported from domain_enums
    "ZIndexStyles",
    "styles",
]
