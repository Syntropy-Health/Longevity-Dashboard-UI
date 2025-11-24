"""
Shared styles for the Apple Glass aesthetic.
Focus: Transparent/frosted backgrounds, light teal accents, subtle gradients.
"""


class GlassStyles:
    PAGE_BG = "bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 min-h-screen font-sans text-slate-100"
    PANEL = "bg-white/5 backdrop-blur-xl border border-white/10 shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] rounded-2xl"
    NAVBAR = "fixed top-4 left-4 right-4 h-16 z-50 bg-slate-900/60 backdrop-blur-md border border-white/10 rounded-2xl flex items-center justify-between px-6 shadow-lg"
    CARD_INTERACTIVE = "group relative overflow-hidden rounded-2xl p-6 bg-white/5 border border-white/10 backdrop-blur-md hover:bg-white/10 hover:border-teal-400/30 hover:shadow-[0_0_20px_rgba(45,212,191,0.1)] transition-all duration-300 cursor-pointer"
    HEADING = "font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-200 to-teal-400"
    SUBHEADING = "text-slate-400 text-sm tracking-wide font-medium"
    TEXT_MAIN = "text-slate-200"
    BUTTON_PRIMARY = "px-6 py-2.5 rounded-xl font-medium bg-gradient-to-r from-teal-500/80 to-teal-400/80 hover:from-teal-400 hover:to-teal-300 text-slate-900 shadow-lg shadow-teal-500/20 transition-all duration-200 backdrop-blur-sm"
    BUTTON_SECONDARY = "px-6 py-2.5 rounded-xl font-medium bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all duration-200 backdrop-blur-sm"
    GLOW_TEAL = "shadow-[0_0_15px_rgba(45,212,191,0.3)]"