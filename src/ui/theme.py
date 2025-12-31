"""
Consolidated UI Theme for Multi-Model AI Development Assistant.

Uses Catppuccin Mocha color palette for consistent dark mode styling.
"""

# Catppuccin Mocha Color Palette
COLORS = {
    # Base colors
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",

    # Surface colors
    "surface0": "#313244",
    "surface1": "#45475a",
    "surface2": "#585b70",

    # Text colors
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",

    # Accent colors
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "sapphire": "#74c7ec",
    "sky": "#89dceb",
    "teal": "#94e2d5",
    "green": "#a6e3a1",
    "yellow": "#f9e2af",
    "peach": "#fab387",
    "maroon": "#eba0ac",
    "red": "#f38ba8",
    "mauve": "#cba6f7",
    "pink": "#f5c2e7",
    "flamingo": "#f2cdcd",
    "rosewater": "#f5e0dc",
}

def get_global_css() -> str:
    """Return global CSS styles for the entire application."""
    return f"""
    <style>
    /* ===== GLOBAL STYLES ===== */

    /* Main container background */
    .stApp {{
        background-color: {COLORS['base']};
    }}

    /* Headers */
    h1 {{
        font-size: 2.2rem !important;
        color: {COLORS['blue']} !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {COLORS['surface1']};
        margin-bottom: 1.5rem !important;
    }}

    h2 {{
        font-size: 1.6rem !important;
        color: {COLORS['text']} !important;
        margin-top: 1rem !important;
    }}

    h3 {{
        font-size: 1.3rem !important;
        color: {COLORS['subtext1']} !important;
    }}

    /* ===== TAB NAVIGATION ===== */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {COLORS['surface0']};
        padding: 8px 12px;
        border-radius: 10px;
        gap: 6px;
    }}

    .stTabs [data-baseweb="tab"] {{
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        background-color: {COLORS['surface1']};
        border-radius: 8px;
        color: {COLORS['text']} !important;
        transition: all 0.2s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {COLORS['surface2']};
        color: #ffffff !important;
        transform: translateY(-1px);
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['blue']} !important;
        color: {COLORS['base']} !important;
    }}

    /* ===== CUSTOM TAB BUTTONS (main.py) ===== */
    .tab-active {{
        background: linear-gradient(135deg, #1e5a3a 0%, #2d8a57 100%);
        padding: 12px 8px;
        border-radius: 8px;
        border: 2px solid {COLORS['green']};
        text-align: center;
        font-weight: 700;
        font-size: 0.9rem;
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(166, 227, 161, 0.4);
    }}

    .tab-inactive {{
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 12px 8px;
        border-radius: 8px;
        border: 2px solid {COLORS['blue']};
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        color: {COLORS['text']};
        cursor: pointer;
        transition: all 0.2s ease;
    }}

    .tab-inactive:hover {{
        background: linear-gradient(135deg, #2d5a87 0%, #3d7ab7 100%);
        border-color: {COLORS['lavender']};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(137, 180, 250, 0.4);
    }}

    /* Style tab buttons in main.py */
    div[data-testid="stButton"] > button {{
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%) !important;
        border: 2px solid {COLORS['blue']} !important;
        color: {COLORS['text']} !important;
        font-weight: 600 !important;
        padding: 12px 8px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(137, 180, 250, 0.3) !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stButton"] > button:hover {{
        background: linear-gradient(135deg, #2d5a87 0%, #3d7ab7 100%) !important;
        border-color: {COLORS['lavender']} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(137, 180, 250, 0.4) !important;
    }}

    /* Primary buttons */
    div[data-testid="stButton"] > button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS['blue']} 0%, {COLORS['lavender']} 100%) !important;
        border: none !important;
        color: {COLORS['base']} !important;
    }}

    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, {COLORS['lavender']} 0%, {COLORS['mauve']} 100%) !important;
    }}

    /* ===== CONTAINERS & CARDS ===== */
    .styled-container {{
        background: linear-gradient(135deg, {COLORS['surface0']} 0%, {COLORS['base']} 100%);
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}

    .styled-container.blue {{
        border: 2px solid {COLORS['blue']};
        box-shadow: 0 4px 15px rgba(137, 180, 250, 0.15);
    }}

    .styled-container.green {{
        border: 2px solid {COLORS['green']};
        box-shadow: 0 4px 15px rgba(166, 227, 161, 0.15);
    }}

    .styled-container.orange {{
        border: 2px solid {COLORS['peach']};
        box-shadow: 0 4px 15px rgba(250, 179, 135, 0.15);
    }}

    .styled-container.purple {{
        border: 2px solid {COLORS['mauve']};
        box-shadow: 0 4px 15px rgba(203, 166, 247, 0.15);
    }}

    /* ===== FORM ELEMENTS ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {{
        background-color: {COLORS['surface1']} !important;
        border: 1px solid {COLORS['surface2']} !important;
        color: {COLORS['text']} !important;
        border-radius: 8px !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['blue']} !important;
        box-shadow: 0 0 0 2px rgba(137, 180, 250, 0.2) !important;
    }}

    /* Labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {{
        color: {COLORS['text']} !important;
        font-weight: 600 !important;
    }}

    /* ===== METRICS ===== */
    div[data-testid="stMetricValue"] {{
        color: {COLORS['blue']} !important;
        font-size: 1.5rem !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {COLORS['subtext1']} !important;
    }}

    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {{
        background-color: {COLORS['surface0']} !important;
        border-radius: 8px !important;
        color: {COLORS['text']} !important;
        font-weight: 600 !important;
    }}

    .streamlit-expanderHeader:hover {{
        background-color: {COLORS['surface1']} !important;
    }}

    .streamlit-expanderContent {{
        background-color: {COLORS['surface0']} !important;
        border: 1px solid {COLORS['surface1']} !important;
        border-radius: 0 0 8px 8px !important;
    }}

    /* ===== ALERTS & STATUS ===== */
    .stSuccess {{
        background-color: rgba(166, 227, 161, 0.1) !important;
        border-left: 4px solid {COLORS['green']} !important;
    }}

    .stInfo {{
        background-color: rgba(137, 180, 250, 0.1) !important;
        border-left: 4px solid {COLORS['blue']} !important;
    }}

    .stWarning {{
        background-color: rgba(249, 226, 175, 0.1) !important;
        border-left: 4px solid {COLORS['yellow']} !important;
    }}

    .stError {{
        background-color: rgba(243, 139, 168, 0.1) !important;
        border-left: 4px solid {COLORS['red']} !important;
    }}

    /* ===== CODE BLOCKS ===== */
    .stCodeBlock {{
        background-color: {COLORS['mantle']} !important;
        border: 1px solid {COLORS['surface1']} !important;
        border-radius: 8px !important;
    }}

    /* ===== DIVIDERS ===== */
    hr {{
        border-color: {COLORS['surface1']} !important;
        margin: 1.5rem 0 !important;
    }}

    /* ===== CAPTIONS ===== */
    .stCaption {{
        color: {COLORS['subtext0']} !important;
    }}

    /* ===== SCROLLBARS ===== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {COLORS['surface0']};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORS['surface2']};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['blue']};
    }}

    /* ===== FILE TABS (Code Editor) ===== */
    .stTabs [role="tablist"] {{
        background-color: {COLORS['surface0']};
        padding: 4px;
        border-radius: 8px;
    }}

    /* ===== CHAT MESSAGE STYLING ===== */
    .chat-message {{
        background-color: {COLORS['surface0']};
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border-left: 4px solid {COLORS['blue']};
    }}

    .chat-message.user {{
        border-left-color: {COLORS['green']};
    }}

    .chat-message.assistant {{
        border-left-color: {COLORS['mauve']};
    }}

    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 768px) {{
        h1 {{ font-size: 1.8rem !important; }}
        h2 {{ font-size: 1.4rem !important; }}
        h3 {{ font-size: 1.1rem !important; }}

        .stTabs [data-baseweb="tab"] {{
            padding: 8px 12px !important;
            font-size: 14px !important;
        }}
    }}
    </style>
    """


def get_project_management_css() -> str:
    """Return CSS for project management section."""
    return f"""
    <style>
    .project-management {{
        background: linear-gradient(135deg, {COLORS['surface0']} 0%, {COLORS['base']} 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid {COLORS['green']};
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(166, 227, 161, 0.15);
    }}
    .project-management h2 {{
        color: {COLORS['green']} !important;
        font-size: 1.5rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {COLORS['surface1']};
    }}
    </style>
    """


def get_chat_input_css() -> str:
    """Return CSS for chat input section."""
    return f"""
    <style>
    .chat-input-section {{
        background: linear-gradient(135deg, {COLORS['surface0']} 0%, {COLORS['base']} 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid {COLORS['blue']};
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(137, 180, 250, 0.15);
    }}
    .chat-input-section h3 {{
        color: {COLORS['blue']} !important;
        font-size: 1.3rem !important;
        margin-bottom: 12px !important;
        padding-bottom: 8px;
        border-bottom: 1px solid {COLORS['surface1']};
    }}
    </style>
    """


def get_model_selection_css() -> str:
    """Return CSS for model selection section."""
    return f"""
    <style>
    .model-selection {{
        background: linear-gradient(135deg, {COLORS['surface0']} 0%, {COLORS['base']} 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid {COLORS['peach']};
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(250, 179, 135, 0.15);
    }}
    .model-selection h3 {{
        color: {COLORS['peach']} !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
    }}
    </style>
    """


def get_agent_context_css() -> str:
    """Return CSS for agent context section."""
    return f"""
    <style>
    .agent-context {{
        background: linear-gradient(135deg, {COLORS['surface0']} 0%, {COLORS['base']} 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid {COLORS['blue']};
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(137, 180, 250, 0.15);
    }}
    .agent-context h3 {{
        color: {COLORS['blue']} !important;
        font-size: 1.3rem !important;
        margin-bottom: 12px !important;
        padding-bottom: 8px;
        border-bottom: 1px solid {COLORS['surface1']};
    }}
    .agent-context-content {{
        background-color: {COLORS['surface1']};
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.9rem;
        white-space: pre-wrap;
        max-height: 350px;
        overflow-y: auto;
        color: {COLORS['text']};
        line-height: 1.5;
    }}
    </style>
    """


def get_faust_editor_css() -> str:
    """Return CSS for FAUST syntax highlighting in editor.

    Inspired by the FAUST online IDE color scheme.
    Uses colors that distinguish:
    - Keywords (import, declare, process, with, letrec)
    - Library functions (os.osc, fi.lowpass, etc.)
    - Operators (~, :, <:, :>, etc.)
    - Primitives (+, -, *, /, %)
    - Numbers and strings
    """
    return f"""
    <style>
    /* FAUST syntax highlighting - FAUST IDE inspired */
    .ace_editor {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
        background-color: #1a1a2e !important;
    }}

    /* Line numbers */
    .ace_editor .ace_gutter {{
        background-color: #16162a !important;
        color: #4a4a6a !important;
    }}
    .ace_editor .ace_gutter-active-line {{
        background-color: #252545 !important;
    }}

    /* Active line highlight */
    .ace_editor .ace_marker-layer .ace_active-line {{
        background-color: rgba(99, 110, 150, 0.1) !important;
    }}

    /* Selection */
    .ace_editor .ace_marker-layer .ace_selection {{
        background-color: rgba(99, 110, 150, 0.3) !important;
    }}

    /* Comments - muted green */
    .ace_editor .ace_comment {{
        color: #608b4e !important;
        font-style: italic !important;
    }}

    /* Strings - orange/salmon */
    .ace_editor .ace_string {{
        color: #ce9178 !important;
    }}

    /* Numbers - light green */
    .ace_editor .ace_constant.ace_numeric {{
        color: #b5cea8 !important;
    }}

    /* Keywords (import, declare, process, with, where, letrec, case, par, seq, sum, prod) */
    .ace_editor .ace_keyword {{
        color: #c586c0 !important;
        font-weight: 600 !important;
    }}

    /* Storage keywords */
    .ace_editor .ace_storage {{
        color: #569cd6 !important;
        font-weight: 600 !important;
    }}

    /* Identifiers and variables */
    .ace_editor .ace_identifier {{
        color: #9cdcfe !important;
    }}

    /* Function calls and library prefixes (os., fi., de., etc.) */
    .ace_editor .ace_support.ace_function {{
        color: #dcdcaa !important;
    }}
    .ace_editor .ace_entity.ace_name.ace_function {{
        color: #dcdcaa !important;
    }}

    /* Types */
    .ace_editor .ace_support.ace_type {{
        color: #4ec9b0 !important;
    }}

    /* Constants */
    .ace_editor .ace_support.ace_constant,
    .ace_editor .ace_constant.ace_language {{
        color: #4fc1ff !important;
    }}

    /* Operators - bright cyan for visibility */
    /* FAUST operators: ~ : <: :> , ; = */
    .ace_editor .ace_keyword.ace_operator,
    .ace_editor .ace_punctuation.ace_operator {{
        color: #56d4dd !important;
        font-weight: 600 !important;
    }}

    /* Parentheses, brackets, braces */
    .ace_editor .ace_paren {{
        color: #ffd700 !important;
    }}
    .ace_editor .ace_lparen {{
        color: #ffd700 !important;
    }}
    .ace_editor .ace_rparen {{
        color: #ffd700 !important;
    }}

    /* Preprocessor / metadata */
    .ace_editor .ace_meta {{
        color: #9b9b9b !important;
    }}

    /* Variables */
    .ace_editor .ace_variable {{
        color: #9cdcfe !important;
    }}

    /* Invalid/error */
    .ace_editor .ace_invalid {{
        color: #f44747 !important;
        background-color: rgba(244, 71, 71, 0.1) !important;
    }}

    /* Cursor */
    .ace_editor .ace_cursor {{
        color: #aeafad !important;
    }}

    /* Matching brackets */
    .ace_editor .ace_bracket {{
        border: 1px solid #888 !important;
        background-color: rgba(255, 215, 0, 0.2) !important;
    }}
    </style>
    """


def get_conversation_css() -> str:
    """Return CSS for conversation display."""
    return f"""
    <style>
    .conversation-entry {{
        background-color: {COLORS['surface0']};
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid {COLORS['blue']};
        transition: all 0.2s ease;
    }}
    .conversation-entry:hover {{
        box-shadow: 0 2px 8px rgba(137, 180, 250, 0.2);
    }}
    .conversation-question {{
        color: {COLORS['green']};
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .conversation-answer {{
        color: {COLORS['text']};
        line-height: 1.6;
    }}
    .conversation-meta {{
        color: {COLORS['subtext0']};
        font-size: 0.85rem;
        margin-top: 12px;
        padding-top: 8px;
        border-top: 1px solid {COLORS['surface1']};
    }}
    </style>
    """


def inject_global_styles():
    """Inject global styles into Streamlit page. Call once at app start."""
    import streamlit as st
    st.markdown(get_global_css(), unsafe_allow_html=True)
