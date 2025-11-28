import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import io
import requests
import json
from typing import Dict, List, Optional, Tuple
import re
import os

# OpenAI import with version checking
try:
    from openai import OpenAI
    import openai
    OPENAI_VERSION = getattr(openai, '__version__', '0.0.0')
except ImportError:
    OpenAI = None
    OPENAI_VERSION = '0.0.0'

# OCR and Image Processing
try:
    from PIL import Image
    import pytesseract
    import cv2
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

warnings.filterwarnings('ignore')

# ============================================================================
# ICON SYSTEM - Using text icons instead of emojis for compatibility
# ============================================================================

ICONS = {
    'rocket': '▲',
    'star': '★',
    'sparkle': '✦',
    'chart': '◆',
    'users': '●',
    'target': '◎',
    'check': '✓',
    'upload': '↑',
    'download': '↓',
    'trophy': '◆',
    'lightning': '⚡',
    'arrow_up': '↑',
    'arrow_right': '→',
    'circle': '●',
    'diamond': '◆',
    'square': '■',
    'plus': '+',
    'brain': '◈',
    'message': '▪',
    'calendar': '▫',
    'file': '▪',
    'folder': '▫',
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_light_color(hex_color: str) -> bool:
    """Determine if a color is light or dark based on perceived brightness."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    brightness = (299 * r + 587 * g + 114 * b) / 1000
    return brightness > 180

def get_contrast_text_color(bg_color: str) -> str:
    """Return appropriate text color based on background brightness."""
    return "#1a1a1a" if is_light_color(bg_color) else "#ffffff"

# ============================================================================
# CONFIGURATION
# ============================================================================

TRAINER_COLORS = {
    'Les Dodd': '#2E5090',
    'Mike Pratt': '#D4A574',
    'Chris Davies': '#7CB342',
    'Brad Miles': '#E57373',
    'Conrad Owen': '#6C63B6',
    'Heather Pippin': '#FF8A80',
    'Default': '#4A90E2'
}

BRAND_COLOR = '#2E5090'
ACCENT_COLORS = ['#2E5090', '#D4A574', '#7CB342', '#E57373', '#6C63B6', '#FF8A80', '#4A90E2', '#26C6DA', '#AB47BC', '#EC407A']

PERFORMANCE_LEVELS = {
    4.7: ('Outstanding', '#10b981'),
    4.3: ('Excellent', '#2E5090'),
    4.0: ('Very Good', '#3b82f6'),
    3.5: ('Good', '#f59e0b'),
    0.0: ('Needs Improvement', '#ef4444')
}

DATE_FORMATS = [
    '%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', 
    '%Y/%m/%d', '%d/%m/%y', '%y-%m-%d', '%m/%d/%y'
]

# ============================================================================
# PAGE SETUP
# ============================================================================

st.set_page_config(
    page_title="QTS Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM WHITE THEME CSS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* GLOBAL RESET & BASE STYLES */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background: #FFFFFF !important;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1a1a1a;
        background: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* PREMIUM HERO HEADER */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .hero-header {
        background: linear-gradient(135deg, #2E5090 0%, #1a365d 100%);
        padding: 3rem 2.5rem;
        border-radius: 0 0 24px 24px;
        margin: -1rem -1rem 2.5rem -1rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .hero-header::after {
        content: '';
        position: absolute;
        bottom: -50%;
        left: 10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: float 8s ease-in-out infinite reverse;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-20px) scale(1.05); }
    }
    
    .hero-title {
        color: white;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
        animation: slideIn 0.6s ease-out;
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
        position: relative;
        z-index: 1;
        animation: slideIn 0.6s ease-out 0.1s both;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
        animation: slideIn 0.6s ease-out 0.2s both;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* UPLOAD CONTAINER */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .upload-container {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        border: 2px dashed #E5E7EB;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: #2E5090;
        box-shadow: 0 10px 40px rgba(46, 80, 144, 0.1);
        transform: translateY(-2px);
    }
    
    .upload-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #2E5090 0%, #1a365d 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .upload-icon-arrow {
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(46, 80, 144, 0.4); }
        50% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(46, 80, 144, 0); }
    }
    
    .upload-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .upload-subtitle {
        font-size: 0.95rem;
        color: #6B7280;
        line-height: 1.6;
    }
    
    .upload-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid #F3F4F6;
    }
    
    .upload-feature {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #4B5563;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .upload-feature-check {
        color: #10b981;
        font-weight: bold;
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* KPI CARDS */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.25rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #2E5090, #4A90E2);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: #2E5090;
        box-shadow: 0 8px 30px rgba(46, 80, 144, 0.12);
        transform: translateY(-4px);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #EBF4FF 0%, #DBEAFE 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        color: #2E5090;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .kpi-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    
    .kpi-trend {
        font-size: 0.8rem;
        color: #6B7280;
        font-weight: 500;
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* SECTION HEADERS */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .section-header {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #E5E7EB;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: #2E5090;
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* CHART CONTAINERS */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .chart-container {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* TRAINER CARDS */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .trainer-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .trainer-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        transform: translateX(4px);
    }
    
    .trainer-name {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .trainer-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1.25rem 0;
    }
    
    .trainer-metric {
        background: #F9FAFB;
        border-radius: 10px;
        padding: 0.875rem;
        text-align: center;
    }
    
    .trainer-metric-value {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #2E5090;
        margin-bottom: 0.2rem;
    }
    
    .trainer-metric-label {
        font-size: 0.7rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        font-weight: 600;
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* AI INSIGHT CARDS */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .ai-insight {
        background: linear-gradient(135deg, #2E5090 0%, #1a365d 100%);
        border-radius: 16px;
        padding: 1.75rem;
        color: white;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .ai-insight::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -25%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .ai-insight-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .ai-insight-icon {
        width: 36px;
        height: 36px;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    
    .ai-insight-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.15rem;
        font-weight: 700;
    }
    
    .ai-insight-content {
        font-size: 0.95rem;
        line-height: 1.7;
        position: relative;
        z-index: 1;
        background: rgba(255, 255, 255, 0.1);
        padding: 1.25rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* BADGES */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .badge-outstanding {
        background: #ECFDF5;
        color: #059669;
    }
    
    .badge-excellent {
        background: #EBF4FF;
        color: #2E5090;
    }
    
    .badge-very-good {
        background: #FFFBEB;
        color: #D97706;
    }
    
    .badge-good {
        background: #F3E8FF;
        color: #7C3AED;
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* FILE BADGES */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .file-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #FFFFFF;
        border: 2px solid;
        border-radius: 10px;
        padding: 0.625rem 1rem;
        margin: 0.375rem;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    
    .file-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .file-badge-delegate {
        border-color: #2E5090;
        background: #EBF4FF;
        color: #1a365d;
    }
    
    .file-badge-partner {
        border-color: #D4A574;
        background: #FEF3E2;
        color: #92400E;
    }
    
    .file-badge-master {
        border-color: #7CB342;
        background: #ECFDF5;
        color: #166534;
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* PROCESSING ANIMATION */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .processing-container {
        background: linear-gradient(135deg, #2E5090 0%, #1a365d 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 2rem 0;
    }
    
    .processing-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .processing-steps {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .processing-step {
        background: rgba(255, 255, 255, 0.15);
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        animation: fadeInUp 0.5s ease-out both;
    }
    
    .processing-step:nth-child(1) { animation-delay: 0.1s; }
    .processing-step:nth-child(2) { animation-delay: 0.2s; }
    .processing-step:nth-child(3) { animation-delay: 0.3s; }
    .processing-step:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ═══════════════════════════════════════════════════════════════════ */
    /* STREAMLIT OVERRIDES */
    /* ═══════════════════════════════════════════════════════════════════ */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #F9FAFB;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0 1.5rem;
        background: transparent;
        border-radius: 8px;
        font-weight: 500;
        color: #4B5563 !important;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #FFFFFF;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2E5090 !important;
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] * {
        color: white !important;
    }
    
    div[data-testid="stFileUploader"] section {
        background: #FFFFFF;
        border: 2px dashed #E5E7EB;
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stFileUploader"] section:hover {
        border-color: #2E5090;
        box-shadow: 0 4px 20px rgba(46, 80, 144, 0.1);
    }
    
    /* Force all text to be dark */
    .stMarkdown, .stText, p, span, label, h1, h2, h3, h4, h5, h6,
    div[data-testid="stMarkdownContainer"] {
        color: #1a1a1a !important;
    }
    
    /* Plotly chart text */
    .js-plotly-plot .plotly text {
        fill: #1a1a1a !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #F9FAFB !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    /* DataFrames */
    .dataframe thead th {
        background: #F9FAFB !important;
        color: #1a1a1a !important;
    }
    
    .dataframe tbody td {
        color: #1a1a1a !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F3F4F6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D1D5DB;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    
    /* Feedback quotes section */
    .feedback-section {
        background: #F9FAFB;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    
    .feedback-title {
        color: #2E5090;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feedback-quote {
        background: #FFFFFF;
        padding: 0.875rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #2E5090;
        color: #374151;
        font-style: italic;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# AI-POWERED DATA SEGREGATOR
# ============================================================================

class AIDataSegregator:
    """Intelligently identifies and categorizes uploaded files"""
    
    @staticmethod
    def identify_file_type(df: pd.DataFrame, filename: str) -> str:
        """Uses AI-like heuristics to determine file type"""
        filename_lower = filename.lower()
        columns_lower = [str(col).lower() for col in df.columns]
        
        delegate_keywords = ['delegate', 'participant', 'student', 'attendee', 'tutor', 'trainer']
        partner_keywords = ['partner', 'company', 'organization', 'client']
        master_keywords = ['master', 'all', 'combined', 'complete', 'full']
        
        if any(kw in filename_lower for kw in delegate_keywords):
            return 'delegate'
        if any(kw in filename_lower for kw in partner_keywords):
            return 'partner'
        if any(kw in filename_lower for kw in master_keywords):
            return 'master'
        
        delegate_column_patterns = ['course', 'rating', 'tutor', 'trainer', 'presenter']
        delegate_score = sum(1 for pattern in delegate_column_patterns 
                            if any(pattern in col for col in columns_lower))
        
        partner_column_patterns = ['company', 'organisation', 'organization', 'business']
        partner_score = sum(1 for pattern in partner_column_patterns 
                           if any(pattern in col for col in columns_lower))
        
        if delegate_score >= 2:
            return 'delegate'
        elif partner_score >= 1:
            return 'partner'
        elif len(df) > 50:
            return 'master'
        else:
            return 'delegate'
    
    @staticmethod
    def merge_similar_files(files_dict: Dict[str, List[pd.DataFrame]]) -> Dict[str, pd.DataFrame]:
        """Merges multiple files of the same type"""
        merged_data = {}
        
        for file_type, dfs in files_dict.items():
            if len(dfs) == 0:
                continue
            elif len(dfs) == 1:
                merged_data[file_type] = dfs[0]
            else:
                try:
                    merged_df = pd.concat(dfs, ignore_index=True)
                    merged_df = merged_df.drop_duplicates()
                    merged_data[file_type] = merged_df
                except Exception as e:
                    st.warning(f"Error merging {file_type} files: {e}")
                    merged_data[file_type] = dfs[0]
        
        return merged_data

# ============================================================================
# OCR FORM PROCESSOR
# ============================================================================

class OCRFormProcessor:
    """Process scanned/photographed feedback forms using OCR and AI"""
    
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        
    def preprocess_image(self, image: 'Image.Image') -> np.ndarray:
        """Enhance image for better OCR"""
        img_array = np.array(image)
        
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        denoised = cv2.fastNlMeansDenoising(enhanced)
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        return thresh
    
    def extract_text(self, image: 'Image.Image') -> str:
        """Extract text from image using OCR"""
        try:
            processed = self.preprocess_image(image)
            text = pytesseract.image_to_string(processed, config='--psm 6')
            return text.strip()
        except Exception as e:
            return f"OCR Error: {str(e)}"
    
    def extract_with_ai(self, text: str) -> Dict:
        """Use AI to structure the extracted text"""
        if not self.openai_client:
            return {"raw_text": text, "error": "No AI client available"}
        
        prompt = f"""Extract training feedback data from this OCR text and return as JSON:

Text: {text[:1000]}

Return JSON with these fields (use null if not found):
{{
    "participant_name": "name",
    "date": "DD/MM/YYYY",
    "course_name": "course",
    "trainer_name": "trainer",
    "overall_rating": "1-5",
    "comments": "feedback text"
}}

Return ONLY valid JSON."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract data from forms. Return only JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            result = response.choices[0].message.content.strip()
            result = result.replace('```json', '').replace('```', '').strip()
            return json.loads(result)
        except Exception as e:
            return {"raw_text": text, "error": str(e)}
    
    def process_forms(self, images: List['Image.Image']) -> pd.DataFrame:
        """Process multiple form images"""
        data = []
        progress = st.progress(0)
        status = st.empty()
        
        for idx, img in enumerate(images):
            status.text(f"Processing form {idx + 1} of {len(images)}...")
            progress.progress((idx + 1) / len(images))
            
            text = self.extract_text(img)
            extracted = self.extract_with_ai(text)
            
            extracted['form_number'] = idx + 1
            extracted['processing_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append(extracted)
        
        progress.empty()
        status.empty()
        
        df = pd.DataFrame(data)
        
        column_map = {
            'participant_name': 'Participant Name',
            'date': 'Date',
            'course_name': 'Course',
            'trainer_name': 'Trainer',
            'overall_rating': 'Please give the course a rating out of 5',
            'comments': 'Comments'
        }
        
        return df.rename(columns=column_map)

# ============================================================================
# DATA PROCESSOR
# ============================================================================

class QTSDataProcessor:
    def __init__(self):
        self.delegate_data = None
        self.partner_data = None
        self.master_data = None
        
    def parse_date(self, date_value):
        """Parse dates with multiple format support"""
        if pd.isna(date_value):
            return None
        
        date_str = str(date_value).strip()
        
        for fmt in DATE_FORMATS:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        try:
            return pd.to_datetime(date_str)
        except:
            return None
    
    def get_quarter(self, date):
        """Assign quarter based on date"""
        if pd.isna(date):
            return None
        try:
            quarter = f"Q{((date.month - 1) // 3) + 1} {date.year}"
            return quarter
        except:
            return None
    
    def process_files(self, uploaded_files: List) -> Tuple[bool, str]:
        """Process multiple uploaded files with AI segregation"""
        if not uploaded_files:
            return False, "No files uploaded"
        
        try:
            categorized_files = {
                'delegate': [],
                'partner': [],
                'master': []
            }
            
            segregator = AIDataSegregator()
            
            for uploaded_file in uploaded_files:
                try:
                    excel_file = pd.ExcelFile(uploaded_file)
                    
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                        
                        if df.empty:
                            continue
                        
                        file_type = segregator.identify_file_type(df, uploaded_file.name)
                        categorized_files[file_type].append(df)
                        
                except Exception as e:
                    st.warning(f"Could not process {uploaded_file.name}: {str(e)}")
                    continue
            
            merged_data = segregator.merge_similar_files(categorized_files)
            
            if 'delegate' in merged_data:
                self.delegate_data = self._process_delegate_data(merged_data['delegate'])
            
            if 'partner' in merged_data:
                self.partner_data = merged_data['partner']
            
            if 'master' in merged_data:
                self.master_data = merged_data['master']
            elif self.delegate_data is not None:
                self.master_data = self.delegate_data
            
            if self.delegate_data is None or len(self.delegate_data) == 0:
                return False, "No valid delegate feedback data found"
            
            return True, f"Successfully processed {len(uploaded_files)} file(s)"
            
        except Exception as e:
            return False, f"Error processing files: {str(e)}"
    
    def _process_delegate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process delegate data with date parsing and quarter assignment"""
        df = df.copy()
        
        date_col = None
        for col in df.columns:
            if any(word in str(col).lower() for word in ['date', 'completion', 'submitted', 'time']):
                date_col = col
                break
        
        if date_col:
            df['Parsed_Date'] = df[date_col].apply(self.parse_date)
            df['Quarter'] = df['Parsed_Date'].apply(self.get_quarter)
        
        return df

# ============================================================================
# ANALYTICS ENGINE
# ============================================================================

class QTSAnalytics:
    def __init__(self, processor: QTSDataProcessor):
        self.processor = processor
        self.df = processor.delegate_data
    
    def calculate_kpis(self) -> Dict:
        """Calculate comprehensive KPIs"""
        kpis = {}
        
        rating_col = 'Please give the course a rating out of 5'
        if rating_col in self.df.columns:
            kpis['overall_rating'] = pd.to_numeric(self.df[rating_col], errors='coerce').mean()
            kpis['total_responses'] = len(self.df)
        
        if rating_col in self.df.columns:
            ratings = pd.to_numeric(self.df[rating_col], errors='coerce').dropna()
            promoters = len(ratings[ratings >= 4.5])
            detractors = len(ratings[ratings <= 3.5])
            kpis['nps'] = ((promoters - detractors) / len(ratings) * 100) if len(ratings) > 0 else 0
        
        trainer_col = None
        for col in self.df.columns:
            if any(word in col.lower() for word in ['tutor', 'trainer', 'presenter']):
                trainer_col = col
                break
        
        if trainer_col:
            kpis['trainer_count'] = self.df[trainer_col].nunique()
        
        course_col = None
        for col in self.df.columns:
            if 'course' in col.lower():
                course_col = col
                break
        
        if course_col:
            kpis['course_count'] = self.df[course_col].nunique()
        
        return kpis
    
    def create_trend_chart(self):
        """Create trend chart"""
        if 'Quarter' not in self.df.columns:
            return None
        
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.df.columns:
            return None
        
        df_trend = self.df.groupby('Quarter')[rating_col].apply(
            lambda x: pd.to_numeric(x, errors='coerce').mean()
        ).reset_index()
        df_trend.columns = ['Quarter', 'Average_Rating']
        df_trend = df_trend.sort_values('Quarter')
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_trend['Quarter'],
            y=df_trend['Average_Rating'],
            fill='tozeroy',
            fillcolor='rgba(46, 80, 144, 0.1)',
            line=dict(color='#2E5090', width=3),
            mode='lines+markers',
            marker=dict(size=10, color='#2E5090', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Rating: %{y:.2f}/5.0<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text='Quarterly Performance Trends',
                font=dict(family='Playfair Display, Georgia, serif', size=18, color='#1a1a1a')
            ),
            xaxis_title='Quarter',
            yaxis_title='Average Rating',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12, color='#1a1a1a'),
            height=400,
            yaxis=dict(range=[3.5, 5.0], gridcolor='#E5E7EB', tickfont=dict(color='#6B7280')),
            xaxis=dict(gridcolor='#E5E7EB', tickfont=dict(color='#6B7280'))
        )
        
        return fig
    
    def create_trainer_comparison(self):
        """Create trainer comparison chart"""
        trainer_col = None
        for col in self.df.columns:
            if any(word in col.lower() for word in ['tutor', 'trainer', 'presenter']):
                trainer_col = col
                break
        
        if not trainer_col:
            return None
        
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.df.columns:
            return None
        
        df_trainers = self.df.groupby(trainer_col)[rating_col].apply(
            lambda x: pd.to_numeric(x, errors='coerce').mean()
        ).reset_index()
        df_trainers.columns = ['Trainer', 'Average_Rating']
        df_trainers = df_trainers.sort_values('Average_Rating', ascending=True)
        
        colors = [TRAINER_COLORS.get(trainer, TRAINER_COLORS['Default']) 
                 for trainer in df_trainers['Trainer']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_trainers['Trainer'],
            x=df_trainers['Average_Rating'],
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>Rating: %{x:.2f}/5.0<extra></extra>',
            text=df_trainers['Average_Rating'].apply(lambda x: f'{x:.2f}'),
            textposition='outside'
        ))
        
        fig.update_layout(
            title=dict(
                text='Trainer Performance Comparison',
                font=dict(family='Playfair Display, Georgia, serif', size=18, color='#1a1a1a')
            ),
            xaxis_title='Average Rating',
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12, color='#1a1a1a'),
            height=max(350, len(df_trainers) * 55),
            xaxis=dict(range=[0, 5.5], gridcolor='#E5E7EB', tickfont=dict(color='#6B7280')),
            yaxis=dict(tickfont=dict(color='#1a1a1a')),
            showlegend=False
        )
        
        return fig
    
    def create_satisfaction_donut(self):
        """Create satisfaction distribution donut chart"""
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.df.columns:
            return None
        
        ratings = pd.to_numeric(self.df[rating_col], errors='coerce').dropna()
        
        categories = []
        for rating in ratings:
            if rating >= 4.5:
                categories.append('Outstanding (4.5-5)')
            elif rating >= 4.0:
                categories.append('Excellent (4-4.5)')
            elif rating >= 3.5:
                categories.append('Good (3.5-4)')
            else:
                categories.append('Needs Improvement (<3.5)')
        
        df_dist = pd.Series(categories).value_counts()
        
        colors = ['#10b981', '#2E5090', '#f59e0b', '#ef4444']
        
        fig = go.Figure(data=[go.Pie(
            labels=df_dist.index,
            values=df_dist.values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(width=2, color='white')),
            textinfo='percent+label',
            textfont=dict(size=11, family='Inter, sans-serif'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text='Satisfaction Distribution',
                font=dict(family='Playfair Display, Georgia, serif', size=18, color='#1a1a1a')
            ),
            annotations=[dict(
                text=f'{len(ratings)}<br>Total',
                x=0.5, y=0.5,
                font=dict(size=18, family='Playfair Display, Georgia, serif', color='#2E5090'),
                showarrow=False
            )],
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(color='#1a1a1a')),
            height=420,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', color='#1a1a1a')
        )
        
        return fig

# ============================================================================
# AI INSIGHTS ENGINE
# ============================================================================

class AIInsightsEngine:
    def __init__(self):
        api_key = None
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            api_key = st.secrets['OPENAI_API_KEY']
        else:
            api_key = os.getenv('OPENAI_API_KEY')
        
        self.client = None
        if api_key and OpenAI:
            try:
                self.client = OpenAI(api_key=api_key, timeout=30.0, max_retries=2)
                self.client.models.list()
            except TypeError as e:
                error_msg = str(e)
                if 'proxies' in error_msg or 'http_client' in error_msg:
                    try:
                        self.client = OpenAI(api_key=api_key)
                    except:
                        st.warning("OpenAI client initialization issue. Update openai: pip install --upgrade openai")
                        self.client = None
                else:
                    st.error(f"OpenAI TypeError: {error_msg}")
                    self.client = None
            except Exception as e:
                st.error(f"OpenAI connection error: {str(e)[:100]}")
                self.client = None
        elif not OpenAI:
            st.warning("OpenAI library not found. Install: pip install openai")
        
        self.model = "gpt-3.5-turbo"
        self.available = self.client is not None
    
    def generate_overall_insights(self, kpis: Dict, df: pd.DataFrame) -> str:
        """Generate AI-powered overall insights"""
        if not self.available:
            return self._generate_fallback_overall_insights(kpis)
        
        prompt = f"""Analyze this training feedback data and provide 3 key insights:

Data Summary:
- Total Responses: {kpis.get('total_responses', 0)}
- Overall Rating: {kpis.get('overall_rating', 0):.2f}/5.0
- NPS Score: {kpis.get('nps', 0):.1f}
- Number of Trainers: {kpis.get('trainer_count', 0)}
- Number of Courses: {kpis.get('course_count', 0)}

Provide 3 bullet points:
1. Overall performance assessment
2. What's working well
3. Areas for improvement

Keep it concise, professional, and actionable. Use bullet points."""
        
        return self._call_openai(prompt)
    
    def generate_trainer_insights(self, trainer_name: str, metrics: Dict, comments: List[str]) -> str:
        """Generate personalized trainer insights"""
        if not self.available:
            return self._generate_fallback_trainer_insights(trainer_name, metrics)
        
        sample_comments = comments[:10] if comments else []
        
        if not sample_comments:
            return f"No participant comments available yet for {trainer_name}."
        
        prompt = f"""Summarize what participants say about {trainer_name}'s training sessions.

ACTUAL PARTICIPANT COMMENTS:
{chr(10).join([f'- "{comment}"' for comment in sample_comments])}

Write a 2-3 sentence summary that captures what participants are ACTUALLY saying in their comments.

RULES:
- Use natural, conversational language
- Highlight recurring themes from the comments
- Mention specific things participants praised
- Keep it simple and human-sounding
- DO NOT mention scores or numbers
- DO NOT use corporate jargon

Write a natural summary:"""
        
        return self._call_openai(prompt)
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst creating performance summaries. Be specific and cite actual data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI insights unavailable: {str(e)}"
    
    def _generate_fallback_overall_insights(self, kpis: Dict) -> str:
        """Generate insights without AI"""
        rating = kpis.get('overall_rating', 0)
        nps = kpis.get('nps', 0)
        
        insights = []
        
        if rating >= 4.5:
            insights.append("• Outstanding Performance: Training programs achieving excellent results with a top-tier rating.")
        elif rating >= 4.0:
            insights.append("• Strong Performance: Training is well-received with consistent quality delivery.")
        else:
            insights.append("• Room for Growth: Current ratings suggest opportunities to enhance effectiveness.")
        
        if nps >= 50:
            insights.append("• High Satisfaction: Strong participant loyalty and likelihood to recommend.")
        elif nps >= 0:
            insights.append("• Positive Sentiment: Generally satisfied participants with room to increase enthusiasm.")
        else:
            insights.append("• Action Needed: Focus on addressing participant concerns.")
        
        insights.append("• Focus Areas: Continue building on trainer strengths and gather detailed feedback.")
        
        return "\n\n".join(insights)
    
    def _generate_fallback_trainer_insights(self, trainer_name: str, metrics: Dict) -> str:
        """Generate trainer insights without AI"""
        overall = metrics.get('overall', 0)
        count = int(metrics.get('count', 0))
        
        if overall >= 4.7:
            return f"Participants rate {trainer_name} very highly ({overall:.2f}/5.0) across {count} sessions. Feedback consistently shows strong satisfaction with their training delivery."
        elif overall >= 4.5:
            return f"{trainer_name} receives excellent ratings ({overall:.2f}/5.0) from participants across {count} sessions. Comments indicate high-quality training experiences."
        elif overall >= 4.0:
            return f"{trainer_name} maintains solid performance with a {overall:.2f}/5.0 rating over {count} sessions. Participants generally express satisfaction."
        else:
            return f"{trainer_name} has delivered {count} sessions with a {overall:.2f}/5.0 rating. Gathering more feedback would help identify improvement areas."

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_trainer_color(trainer_name: str) -> str:
    """Get consistent color for trainer"""
    return TRAINER_COLORS.get(trainer_name, TRAINER_COLORS['Default'])

def get_performance_level(rating: float) -> Tuple[str, str]:
    """Get performance level and color for rating"""
    for threshold, (level, color) in sorted(PERFORMANCE_LEVELS.items(), reverse=True):
        if rating >= threshold:
            return level, color
    return 'Needs Improvement', '#ef4444'

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Hero Header
    st.markdown("""
        <div class="hero-header">
            <h1 class="hero-title">QTS Analytics</h1>
            <p class="hero-subtitle">Intelligent Feedback Analysis • Real-Time Insights • AI-Powered Recommendations</p>
            <div class="hero-badge">★ Next-Generation Analytics Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    # Upload Section
    st.markdown("""
        <div class="upload-container">
            <div class="upload-icon">
                <span class="upload-icon-arrow">↑</span>
            </div>
            <div class="upload-title">Upload Your Feedback Files</div>
            <div class="upload-subtitle">
                Drop all your Excel files here - our AI will automatically identify and organize them.<br>
                Mix delegate, partner, and master data files together.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose Excel files",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.markdown("""
            <div class="upload-features">
                <div class="upload-feature">
                    <span class="upload-feature-check">✓</span>
                    <span>AI-Powered Segregation</span>
                </div>
                <div class="upload-feature">
                    <span class="upload-feature-check">✓</span>
                    <span>Automatic Merging</span>
                </div>
                <div class="upload-feature">
                    <span class="upload-feature-check">✓</span>
                    <span>Duplicate Detection</span>
                </div>
                <div class="upload-feature">
                    <span class="upload-feature-check">✓</span>
                    <span>Real-Time Analytics</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Process Button
    if uploaded_files and st.button("◆ Process Data with AI", type="primary", use_container_width=True):
        with st.spinner(""):
            st.markdown("""
                <div class="processing-container">
                    <div class="processing-title">AI Processing in Progress</div>
                    <div class="processing-steps">
                        <div class="processing-step">◆ Analyzing Files</div>
                        <div class="processing-step">◆ Segregating Data</div>
                        <div class="processing-step">◆ Merging Records</div>
                        <div class="processing-step">◆ Generating Insights</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            processor = QTSDataProcessor()
            success, message = processor.process_files(uploaded_files)
            
            if success:
                st.session_state.processor = processor
                st.session_state.processed = True
                
                file_count_delegate = len(processor.delegate_data) if processor.delegate_data is not None else 0
                file_count_partner = len(processor.partner_data) if processor.partner_data is not None else 0
                
                st.success(f"✓ {message}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                        <div class="file-badge file-badge-delegate">
                            ■ Delegate: {file_count_delegate} records
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class="file-badge file-badge-partner">
                            ■ Partner: {file_count_partner} records
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                        <div class="file-badge file-badge-master">
                            ★ Ready for Analysis
                        </div>
                    """, unsafe_allow_html=True)
                
                st.rerun()
            else:
                st.error(f"✗ {message}")
    
    # Display Analytics
    if st.session_state.processed and 'processor' in st.session_state:
        processor = st.session_state.processor
        analytics = QTSAnalytics(processor)
        ai_engine = AIInsightsEngine()
        
        if ai_engine.available:
            st.success("✓ OpenAI API Connected - AI insights enabled")
        else:
            st.info("OpenAI API not configured. Using fallback insights. Add OPENAI_API_KEY to secrets for AI features.")
        
        kpis = analytics.calculate_kpis()
        
        st.markdown('<div class="section-header">Performance Dashboard</div>', unsafe_allow_html=True)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">★</div>
                    <div class="kpi-label">Overall Rating</div>
                    <div class="kpi-value">{kpis.get('overall_rating', 0):.2f}</div>
                    <div class="kpi-trend">Out of 5.0</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">◆</div>
                    <div class="kpi-label">Total Responses</div>
                    <div class="kpi-value">{kpis.get('total_responses', 0):,}</div>
                    <div class="kpi-trend">Feedback Entries</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            nps_val = kpis.get('nps', 0)
            nps_color = '#10b981' if nps_val >= 50 else '#f59e0b' if nps_val >= 0 else '#ef4444'
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">◎</div>
                    <div class="kpi-label">NPS Score</div>
                    <div class="kpi-value" style="color: {nps_color};">{nps_val:.1f}</div>
                    <div class="kpi-trend">Net Promoter</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">●</div>
                    <div class="kpi-label">Active Trainers</div>
                    <div class="kpi-value">{kpis.get('trainer_count', 0)}</div>
                    <div class="kpi-trend">Team Members</div>
                </div>
            """, unsafe_allow_html=True)
        
        # AI Insights
        if ai_engine.available:
            with st.spinner("AI is analyzing your data..."):
                overall_insights = ai_engine.generate_overall_insights(kpis, processor.delegate_data)
                st.markdown(f"""
                    <div class="ai-insight">
                        <div class="ai-insight-header">
                            <div class="ai-insight-icon">◈</div>
                            <span class="ai-insight-title">AI-Powered Insights</span>
                        </div>
                        <div class="ai-insight-content">
                            {overall_insights}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["◆ Visualizations", "● Trainers", "◆ Partners", "■ Data", "◆ Scanned Forms"])
        
        with tab1:
            st.markdown('<div class="section-header">Performance Visualizations</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                trend_chart = analytics.create_trend_chart()
                if trend_chart:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(trend_chart, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                donut_chart = analytics.create_satisfaction_donut()
                if donut_chart:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(donut_chart, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="section-header">Trainer Excellence</div>', unsafe_allow_html=True)
            
            trainer_chart = analytics.create_trainer_comparison()
            if trainer_chart:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(trainer_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="section-header">Trainer Profiles</div>', unsafe_allow_html=True)
            
            trainer_col = None
            for col in processor.delegate_data.columns:
                if any(word in col.lower() for word in ['tutor', 'trainer', 'presenter']):
                    trainer_col = col
                    break
            
            if trainer_col:
                trainers_data = []
                
                for trainer_name in processor.delegate_data[trainer_col].unique():
                    if pd.notna(trainer_name):
                        df_trainer = processor.delegate_data[processor.delegate_data[trainer_col] == trainer_name]
                        if len(df_trainer) >= 3:
                            rating_col = 'Please give the course a rating out of 5'
                            avg_rating = pd.to_numeric(df_trainer[rating_col], errors='coerce').mean() if rating_col in df_trainer.columns else 0
                            trainers_data.append({
                                'name': trainer_name,
                                'count': len(df_trainer),
                                'rating': avg_rating,
                                'data': df_trainer
                            })
                
                trainers_data.sort(key=lambda x: x['rating'], reverse=True)
                
                if trainers_data:
                    trainer_options = ["★ View All Trainers"] + [
                        f"{t['name']} - {t['rating']:.2f}/5.0 ({t['count']} sessions)"
                        for t in trainers_data
                    ]
                    
                    selected_option = st.selectbox(
                        "Select a trainer to view details:",
                        options=trainer_options,
                        index=0
                    )
                    
                    if selected_option == "★ View All Trainers":
                        trainers_to_show = trainers_data
                    else:
                        selected_name = selected_option.split(" - ")[0]
                        trainers_to_show = [t for t in trainers_data if t['name'] == selected_name]
                    
                    for idx, trainer_info in enumerate(trainers_to_show):
                        trainer_name = trainer_info['name']
                        df_trainer = trainer_info['data']
                        
                        color = get_trainer_color(trainer_name)
                        
                        metrics = {}
                        for metric_key in ['knowledge', 'adaptability', 'feedback', 'guidance']:
                            cols = [col for col in df_trainer.columns if metric_key.lower() in col.lower()]
                            if cols:
                                metrics[metric_key] = pd.to_numeric(df_trainer[cols[0]], errors='coerce').mean()
                        
                        rating_col = 'Please give the course a rating out of 5'
                        avg_rating = trainer_info['rating']
                        metrics['overall'] = avg_rating
                        metrics['count'] = len(df_trainer)
                        
                        performance, perf_color = get_performance_level(avg_rating)
                        
                        badge_class = f"badge-{performance.lower().replace(' ', '-')}"
                        
                        st.markdown(f"""
                            <div class="trainer-card" style="border-left-color: {color};">
                                <div class="trainer-name">
                                    {trainer_name}
                                    <span class="badge {badge_class}">{performance}</span>
                                </div>
                                <div class="trainer-metrics">
                                    <div class="trainer-metric">
                                        <div class="trainer-metric-value">{avg_rating:.2f}</div>
                                        <div class="trainer-metric-label">Avg Rating</div>
                                    </div>
                                    <div class="trainer-metric">
                                        <div class="trainer-metric-value">{len(df_trainer)}</div>
                                        <div class="trainer-metric-label">Sessions</div>
                                    </div>
                                    <div class="trainer-metric">
                                        <div class="trainer-metric-value">{metrics.get('knowledge', 0):.2f}</div>
                                        <div class="trainer-metric-label">Knowledge</div>
                                    </div>
                                    <div class="trainer-metric">
                                        <div class="trainer-metric-value">{metrics.get('adaptability', 0):.2f}</div>
                                        <div class="trainer-metric-label">Adaptability</div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # AI Insights
                        feedback_col = None
                        for col in df_trainer.columns:
                            if any(word in col.lower() for word in ['comment', 'feedback']):
                                feedback_col = col
                                break
                        
                        comments = df_trainer[feedback_col].dropna().tolist() if feedback_col else []
                        
                        text_color = get_contrast_text_color(color)
                        
                        if ai_engine.available:
                            with st.spinner(f"AI analyzing {trainer_name}'s performance..."):
                                trainer_insights = ai_engine.generate_trainer_insights(trainer_name, metrics, comments)
                        else:
                            trainer_insights = ai_engine._generate_fallback_trainer_insights(trainer_name, metrics)
                        
                        st.markdown(f"""
                            <div class="ai-insight" style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%);">
                                <div class="ai-insight-header">
                                    <div class="ai-insight-icon">✦</div>
                                    <span class="ai-insight-title">Performance Summary</span>
                                </div>
                                <div class="ai-insight-content">
                                    {trainer_insights}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Feedback quotes
                        if feedback_col and comments:
                            valid_comments = [c for c in comments if pd.notna(c) and len(str(c).strip()) > 10][:3]
                            if valid_comments:
                                st.markdown(f"""
                                    <div class="feedback-section" style="border-left: 4px solid {color};">
                                        <div class="feedback-title">
                                            <span>▪</span> Participant Feedback
                                        </div>
                                """, unsafe_allow_html=True)
                                
                                for comment in valid_comments:
                                    st.markdown(f"""
                                        <div class="feedback-quote">
                                            "{str(comment).strip()}"
                                        </div>
                                    """, unsafe_allow_html=True)
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        if idx < len(trainers_to_show) - 1:
                            st.markdown('<hr style="margin: 2rem 0; border: none; border-top: 1px solid #E5E7EB;">', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="section-header">Partner Feedback</div>', unsafe_allow_html=True)
            
            if processor.partner_data is not None and len(processor.partner_data) > 0:
                for idx, row in processor.partner_data.iterrows():
                    with st.expander(f"Partner Feedback #{idx+1}", expanded=False):
                        cols = st.columns(2)
                        for i, col in enumerate(processor.partner_data.columns):
                            if pd.notna(row[col]) and str(row[col]).strip():
                                with cols[i % 2]:
                                    st.markdown(f"**{col}:**")
                                    st.write(row[col])
            else:
                st.info("No partner feedback data available")
        
        with tab4:
            st.markdown('<div class="section-header">Raw Data</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(processor.delegate_data):,}")
            with col2:
                st.metric("Columns", len(processor.delegate_data.columns))
            with col3:
                st.metric("Missing Values", f"{processor.delegate_data.isnull().sum().sum():,}")
            
            st.dataframe(processor.delegate_data, use_container_width=True, height=400)
            
            col1, col2 = st.columns(2)
            with col1:
                csv = processor.delegate_data.to_csv(index=False)
                st.download_button(
                    "↓ Download CSV",
                    csv,
                    f"qts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    processor.delegate_data.to_excel(writer, index=False, sheet_name='Data')
                
                st.download_button(
                    "↓ Download Excel",
                    output.getvalue(),
                    f"qts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with tab5:
            st.markdown('<div class="section-header">Process Scanned Forms</div>', unsafe_allow_html=True)
            
            if not OCR_AVAILABLE:
                st.error("""
                    OCR features are not available. Install required packages:
                    ```bash
                    pip install pytesseract opencv-python Pillow
                    ```
                    Also install Tesseract OCR on your system.
                """)
            else:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #2E5090 0%, #1a365d 100%); 
                                border-radius: 16px; padding: 1.75rem; color: white; margin: 1.5rem 0;">
                        <h3 style="margin: 0 0 0.5rem 0; font-family: 'Playfair Display', serif;">Upload Scanned Feedback Forms</h3>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.95rem;">
                            Upload photos or scans - AI will extract all data automatically.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                uploaded_images = st.file_uploader(
                    "Upload Form Images",
                    type=['png', 'jpg', 'jpeg'],
                    accept_multiple_files=True,
                    help="Upload clear photos/scans of completed feedback forms"
                )
                
                if uploaded_images:
                    st.success(f"✓ {len(uploaded_images)} form(s) uploaded")
                    
                    with st.expander("Preview Forms", expanded=False):
                        cols = st.columns(min(len(uploaded_images), 3))
                        for idx, img_file in enumerate(uploaded_images[:6]):
                            with cols[idx % 3]:
                                image = Image.open(img_file)
                                st.image(image, caption=f"Form {idx + 1}", use_column_width=True)
                    
                    if st.button("◆ Process Forms with AI", type="primary", use_container_width=True):
                        with st.spinner("Extracting data from forms..."):
                            ocr = OCRFormProcessor(
                                openai_client=ai_engine.client if ai_engine.available else None
                            )
                            
                            images = [Image.open(f) for f in uploaded_images]
                            df_ocr = ocr.process_forms(images)
                            
                            st.success(f"✓ Processed {len(df_ocr)} forms!")
                            
                            st.markdown("### Extracted Data")
                            st.dataframe(df_ocr, use_container_width=True)
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                csv = df_ocr.to_csv(index=False)
                                st.download_button(
                                    "↓ Download CSV",
                                    csv,
                                    f"ocr_forms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    "text/csv",
                                    use_container_width=True
                                )
                            
                            with col2:
                                output = io.BytesIO()
                                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                    df_ocr.to_excel(writer, index=False, sheet_name='OCR Data')
                                st.download_button(
                                    "↓ Download Excel",
                                    output.getvalue(),
                                    f"ocr_forms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            with col3:
                                if st.button("◆ Merge with Dataset", use_container_width=True):
                                    processor.delegate_data = pd.concat([processor.delegate_data, df_ocr], ignore_index=True)
                                    st.success("✓ Merged! Refresh to see updated analytics.")
                                    st.rerun()
                else:
                    st.markdown("""
                        <div style="background: #F9FAFB; border-radius: 12px; padding: 1.5rem; 
                                    border: 1px solid #E5E7EB;">
                            <h4 style="color: #1a1a1a; margin: 0 0 1rem 0;">Tips for Best Results</h4>
                            <ul style="color: #4B5563; line-height: 1.8; margin: 0; padding-left: 1.25rem;">
                                <li>Clear, well-lit photos</li>
                                <li>Forms flat on surface (no shadows)</li>
                                <li>Right-side up orientation</li>
                                <li>All text visible and legible</li>
                                <li>PNG, JPG, or JPEG format</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()