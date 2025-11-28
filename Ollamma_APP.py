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
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION - ENHANCED COLOR SYSTEM
# ============================================================================

TRAINER_COLORS = {
    'Les Dodd': '#2E5090',      # Deep Blue
    'Mike Pratt': '#D4A574',    # Warm Gold
    'Chris Davies': '#7CB342',  # Sage Green
    'Brad Miles': '#E57373',    # Coral Red
    'Conrad Owen': '#6C63B6',   # Purple
    'Heather Pippin': '#FF8A80', # Rose Pink
    'Default': '#4A90E2'        # Default Blue
}

PERFORMANCE_THEMES = {
    'Outstanding': {'color': '#1B5E20', 'light': '#E8F5E9', 'icon': '⭐', 'gradient': 'linear-gradient(135deg, #1B5E20, #43A047)'},
    'Excellent': {'color': '#2E5090', 'light': '#E3F2FD', 'icon': '✨', 'gradient': 'linear-gradient(135deg, #2E5090, #5C7BC8)'},
    'Very Good': {'color': '#F57C00', 'light': '#FFF3E0', 'icon': '👍', 'gradient': 'linear-gradient(135deg, #F57C00, #FFA726)'},
}

BRAND_COLOR = '#2E5090'
ACCENT_COLORS = ['#2E5090', '#D4A574', '#7CB342', '#E57373', '#6C63B6', '#FF8A80', '#4A90E2', '#26C6DA', '#AB47BC', '#EC407A']

PERFORMANCE_LEVELS = {
    4.7: ('Outstanding', '🌟', '#10b981'),
    4.3: ('Excellent', '⭐', '#2E5090'),
    4.0: ('Very Good', '✨', '#3b82f6'),
    3.5: ('Good', '👍', '#f59e0b'),
    0.0: ('Needs Improvement', '📈', '#ef4444')
}

DATE_FORMATS = [
    '%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', 
    '%Y/%m/%d', '%d/%m/%y', '%y-%m-%d', '%m/%d/%y'
]

# ============================================================================
# PAGE SETUP - NEXT-GEN EXPERIENCE
# ============================================================================

st.set_page_config(
    page_title="QTS Analytics AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# NEXT-GEN CSS STYLING WITH ANIMATIONS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, .main {
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF2F7 100%);
        font-family: 'Poppins', sans-serif;
        color: #1a1a1a;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* ANIMATED HERO HEADER */
    /* ═══════════════════════════════════════════════════════════ */
    
    .hero-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
        padding: 3rem 2.5rem;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2.5rem -1rem;
        box-shadow: 0 20px 60px rgba(26, 35, 126, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.3; }
    }
    
    .hero-title {
        color: white;
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
        animation: slideInFromLeft 0.8s ease-out;
    }
    
    @keyframes slideInFromLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 300;
        margin: 0;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
        animation: slideInFromLeft 0.8s ease-out 0.2s both;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
        animation: slideInFromLeft 0.8s ease-out 0.4s both;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* UNIFIED UPLOAD ZONE - PREMIUM DRAG & DROP */
    /* ═══════════════════════════════════════════════════════════ */
    
    .upload-container {
        background: white;
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        border: 3px dashed #E0E7FF;
        box-shadow: 0 8px 32px rgba(46, 80, 144, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
    }
    
    .upload-container:hover {
        border-color: #2E5090;
        box-shadow: 0 16px 48px rgba(46, 80, 144, 0.15);
        transform: translateY(-4px);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .upload-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #2E5090;
        margin-bottom: 0.75rem;
    }
    
    .upload-subtitle {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .upload-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
    }
    
    .upload-feature {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #4B5563;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .upload-feature-icon {
        color: #10b981;
        font-size: 1.2rem;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* PROCESSING ANIMATION */
    /* ═══════════════════════════════════════════════════════════ */
    
    .processing-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .processing-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .processing-steps {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .processing-step {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 500;
        animation: fadeInUp 0.6s ease-out both;
    }
    
    .processing-step:nth-child(1) { animation-delay: 0.1s; }
    .processing-step:nth-child(2) { animation-delay: 0.2s; }
    .processing-step:nth-child(3) { animation-delay: 0.3s; }
    .processing-step:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* KPI CARDS - GLASSMORPHISM STYLE */
    /* ═══════════════════════════════════════════════════════════ */
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.75rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(46, 80, 144, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(30%, -30%);
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(31, 38, 135, 0.15);
        border-color: #2E5090;
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .kpi-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #2E5090;
        line-height: 1;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .kpi-trend {
        font-size: 0.85rem;
        color: #10b981;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.3rem;
        position: relative;
        z-index: 1;
    }
    
    .kpi-trend.negative {
        color: #ef4444;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* SECTION HEADERS WITH UNDERLINE ANIMATION */
    /* ═══════════════════════════════════════════════════════════ */
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid #E8EAED;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #2E5090, #667eea);
        animation: expandWidth 1s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 80px; }
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* CHART CONTAINERS - ELEVATED DESIGN */
    /* ═══════════════════════════════════════════════════════════ */
    
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* TRAINER CARDS - PREMIUM DESIGN */
    /* ═══════════════════════════════════════════════════════════ */
    
    .trainer-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border-left: 6px solid;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .trainer-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, currentColor 0%, transparent 70%);
        opacity: 0.05;
        border-radius: 50%;
        transform: translate(30%, -30%);
    }
    
    .trainer-card:hover {
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
        transform: translateX(8px);
    }
    
    .trainer-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .trainer-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .trainer-metric {
        background: rgba(46, 80, 144, 0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .trainer-metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #2E5090;
        margin-bottom: 0.3rem;
    }
    
    .trainer-metric-label {
        font-size: 0.75rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* AI INSIGHT CARDS - GLOWING EFFECT */
    /* ═══════════════════════════════════════════════════════════ */
    
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .ai-insight::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
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
        font-size: 1.8rem;
    }
    
    .ai-insight-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .ai-insight-content {
        font-size: 1rem;
        line-height: 1.7;
        position: relative;
        z-index: 1;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* BADGES & TAGS */
    /* ═══════════════════════════════════════════════════════════ */
    
    .badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-outstanding {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .badge-excellent {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    .badge-very-good {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }
    
    .badge-good {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        color: white;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* DATA FILE BADGES */
    /* ═══════════════════════════════════════════════════════════ */
    
    .file-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: white;
        border: 2px solid;
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .file-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    
    .file-badge-delegate {
        border-color: #2E5090;
        color: #2E5090;
    }
    
    .file-badge-partner {
        border-color: #D4A574;
        color: #D4A574;
    }
    
    .file-badge-master {
        border-color: #7CB342;
        color: #7CB342;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* RESPONSIVE DESIGN */
    /* ═══════════════════════════════════════════════════════════ */
    
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .upload-title { font-size: 1.4rem; }
        .kpi-grid { grid-template-columns: 1fr; }
        .trainer-metrics { grid-template-columns: 1fr; }
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* SCROLLBAR STYLING */
    /* ═══════════════════════════════════════════════════════════ */
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2E5090, #667eea);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1a237e, #283593);
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* STREMLIT OVERRIDES */
    /* ═══════════════════════════════════════════════════════════ */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 2rem;
        background: transparent;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(46, 80, 144, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E5090, #667eea) !important;
        color: white !important;
    }
    
    div[data-testid="stFileUploader"] {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    div[data-testid="stFileUploader"] section {
        background: white;
        border: 3px dashed #E0E7FF;
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stFileUploader"] section:hover {
        border-color: #2E5090;
        box-shadow: 0 8px 24px rgba(46, 80, 144, 0.12);
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
        """
        Uses AI-like heuristics to determine file type
        Returns: 'delegate', 'partner', or 'master'
        """
        filename_lower = filename.lower()
        columns_lower = [str(col).lower() for col in df.columns]
        
        # Keyword-based classification
        delegate_keywords = ['delegate', 'participant', 'student', 'attendee', 'tutor', 'trainer']
        partner_keywords = ['partner', 'company', 'organization', 'client']
        master_keywords = ['master', 'all', 'combined', 'complete', 'full']
        
        # Check filename
        if any(kw in filename_lower for kw in delegate_keywords):
            return 'delegate'
        if any(kw in filename_lower for kw in partner_keywords):
            return 'partner'
        if any(kw in filename_lower for kw in master_keywords):
            return 'master'
        
        # Check columns for delegate feedback patterns
        delegate_column_patterns = ['course', 'rating', 'tutor', 'trainer', 'presenter']
        delegate_score = sum(1 for pattern in delegate_column_patterns 
                            if any(pattern in col for col in columns_lower))
        
        # Check columns for partner feedback patterns
        partner_column_patterns = ['company', 'organisation', 'organization', 'business']
        partner_score = sum(1 for pattern in partner_column_patterns 
                           if any(pattern in col for col in columns_lower))
        
        # Decision logic
        if delegate_score >= 2:
            return 'delegate'
        elif partner_score >= 1:
            return 'partner'
        elif len(df) > 50:  # Large file likely master data
            return 'master'
        else:
            return 'delegate'  # Default to delegate
    
    @staticmethod
    def merge_similar_files(files_dict: Dict[str, List[pd.DataFrame]]) -> Dict[str, pd.DataFrame]:
        """Merges multiple files of the same type"""
        merged_data = {}
        
        for file_type, dfs in files_dict.items():
            if len(dfs) == 1:
                merged_data[file_type] = dfs[0]
            else:
                # Smart merge with duplicate handling
                try:
                    merged_df = pd.concat(dfs, ignore_index=True)
                    # Remove exact duplicates
                    merged_df = merged_df.drop_duplicates()
                    merged_data[file_type] = merged_df
                except Exception as e:
                    st.warning(f"Error merging {file_type} files: {e}")
                    merged_data[file_type] = dfs[0]  # Use first file as fallback
        
        return merged_data

# ============================================================================
# DATA PROCESSOR - ENHANCED VERSION
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
        """
        Process multiple uploaded files with AI segregation
        Returns: (success, message)
        """
        if not uploaded_files:
            return False, "No files uploaded"
        
        try:
            # Initialize file categorization
            categorized_files = {
                'delegate': [],
                'partner': [],
                'master': []
            }
            
            segregator = AIDataSegregator()
            
            # Process each uploaded file
            for uploaded_file in uploaded_files:
                try:
                    # Read Excel file (handle multiple sheets)
                    excel_file = pd.ExcelFile(uploaded_file)
                    
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                        
                        if df.empty:
                            continue
                        
                        # AI-powered file type identification
                        file_type = segregator.identify_file_type(df, uploaded_file.name)
                        categorized_files[file_type].append(df)
                        
                except Exception as e:
                    st.warning(f"Could not process {uploaded_file.name}: {str(e)}")
                    continue
            
            # Merge files of same type
            merged_data = segregator.merge_similar_files(categorized_files)
            
            # Process delegate data
            if 'delegate' in merged_data:
                self.delegate_data = self._process_delegate_data(merged_data['delegate'])
            
            # Process partner data
            if 'partner' in merged_data:
                self.partner_data = merged_data['partner']
            
            # Process master data (fallback to delegate if not separate)
            if 'master' in merged_data:
                self.master_data = merged_data['master']
            elif self.delegate_data is not None:
                self.master_data = self.delegate_data
            
            # Validate we have at least delegate data
            if self.delegate_data is None or len(self.delegate_data) == 0:
                return False, "No valid delegate feedback data found"
            
            return True, f"Successfully processed {len(uploaded_files)} file(s)"
            
        except Exception as e:
            return False, f"Error processing files: {str(e)}"
    
    def _process_delegate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process delegate data with date parsing and quarter assignment"""
        df = df.copy()
        
        # Find date column
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
# ANALYTICS ENGINE - ENHANCED
# ============================================================================

class QTSAnalytics:
    def __init__(self, processor: QTSDataProcessor):
        self.processor = processor
        self.df = processor.delegate_data
    
    def calculate_kpis(self) -> Dict:
        """Calculate comprehensive KPIs"""
        kpis = {}
        
        # Overall rating
        rating_col = 'Please give the course a rating out of 5'
        if rating_col in self.df.columns:
            kpis['overall_rating'] = pd.to_numeric(self.df[rating_col], errors='coerce').mean()
            kpis['total_responses'] = len(self.df)
        
        # NPS calculation
        if rating_col in self.df.columns:
            ratings = pd.to_numeric(self.df[rating_col], errors='coerce').dropna()
            promoters = len(ratings[ratings >= 4.5])
            detractors = len(ratings[ratings <= 3.5])
            kpis['nps'] = ((promoters - detractors) / len(ratings) * 100) if len(ratings) > 0 else 0
        
        # Trainer count
        trainer_col = None
        for col in self.df.columns:
            if any(word in col.lower() for word in ['tutor', 'trainer', 'presenter']):
                trainer_col = col
                break
        
        if trainer_col:
            kpis['trainer_count'] = self.df[trainer_col].nunique()
        
        # Course count
        course_col = None
        for col in self.df.columns:
            if 'course' in col.lower():
                course_col = col
                break
        
        if course_col:
            kpis['course_count'] = self.df[course_col].nunique()
        
        return kpis
    
    def create_trend_chart(self):
        """Create animated trend chart"""
        if 'Quarter' not in self.df.columns:
            return None
        
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.df.columns:
            return None
        
        # Calculate quarterly averages
        df_trend = self.df.groupby('Quarter')[rating_col].apply(
            lambda x: pd.to_numeric(x, errors='coerce').mean()
        ).reset_index()
        df_trend.columns = ['Quarter', 'Average_Rating']
        df_trend = df_trend.sort_values('Quarter')
        
        # Create figure
        fig = go.Figure()
        
        # Add area fill
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
                text='📈 Quarterly Performance Trends',
                font=dict(family='Playfair Display', size=20, color='#1a1a1a')
            ),
            xaxis_title='Quarter',
            yaxis_title='Average Rating',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', size=12),
            height=400,
            yaxis=dict(range=[3.5, 5.0], gridcolor='rgba(0,0,0,0.05)'),
            xaxis=dict(gridcolor='rgba(0,0,0,0.05)')
        )
        
        return fig
    
    def create_trainer_comparison(self):
        """Create colorful trainer comparison chart"""
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
        
        # Calculate trainer averages
        df_trainers = self.df.groupby(trainer_col)[rating_col].apply(
            lambda x: pd.to_numeric(x, errors='coerce').mean()
        ).reset_index()
        df_trainers.columns = ['Trainer', 'Average_Rating']
        df_trainers = df_trainers.sort_values('Average_Rating', ascending=True)
        
        # Assign colors
        colors = [TRAINER_COLORS.get(trainer, TRAINER_COLORS['Default']) 
                 for trainer in df_trainers['Trainer']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_trainers['Trainer'],
            x=df_trainers['Average_Rating'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{y}</b><br>Rating: %{x:.2f}/5.0<extra></extra>',
            text=df_trainers['Average_Rating'].apply(lambda x: f'{x:.2f}'),
            textposition='outside'
        ))
        
        fig.update_layout(
            title=dict(
                text='🏆 Trainer Performance Comparison',
                font=dict(family='Playfair Display', size=20, color='#1a1a1a')
            ),
            xaxis_title='Average Rating',
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', size=12),
            height=max(400, len(df_trainers) * 60),
            xaxis=dict(range=[0, 5.5], gridcolor='rgba(0,0,0,0.05)'),
            showlegend=False
        )
        
        return fig
    
    def create_satisfaction_donut(self):
        """Create satisfaction distribution donut chart"""
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.df.columns:
            return None
        
        ratings = pd.to_numeric(self.df[rating_col], errors='coerce').dropna()
        
        # Categorize ratings
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
            marker=dict(colors=colors, line=dict(width=3, color='white')),
            textinfo='percent+label',
            textfont=dict(size=11, family='Poppins'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text='📊 Satisfaction Distribution',
                font=dict(family='Playfair Display', size=20, color='#1a1a1a')
            ),
            annotations=[dict(
                text=f'{len(ratings)}<br>Total',
                x=0.5, y=0.5,
                font=dict(size=20, family='Playfair Display', color='#2E5090'),
                showarrow=False
            )],
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins')
        )
        
        return fig
    
    def create_metric_radar(self, trainer_name: str = None):
        """Create radar chart for trainer metrics"""
        if trainer_name:
            trainer_col = None
            for col in self.df.columns:
                if any(word in col.lower() for word in ['tutor', 'trainer', 'presenter']):
                    trainer_col = col
                    break
            
            if trainer_col:
                df_trainer = self.df[self.df[trainer_col] == trainer_name]
            else:
                df_trainer = self.df
        else:
            df_trainer = self.df
        
        # Find metric columns
        metrics = {}
        metric_keywords = {
            'Knowledge': ['knowledge', 'expertise'],
            'Adaptability': ['adaptability', 'flexible'],
            'Feedback': ['feedback', 'response'],
            'Guidance': ['guidance', 'support'],
            'Engagement': ['engagement', 'interactive']
        }
        
        for metric_name, keywords in metric_keywords.items():
            for col in df_trainer.columns:
                if any(kw in col.lower() for kw in keywords):
                    avg = pd.to_numeric(df_trainer[col], errors='coerce').mean()
                    if not pd.isna(avg):
                        metrics[metric_name] = avg
                    break
        
        if len(metrics) < 3:
            return None
        
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(46, 80, 144, 0.2)',
            line=dict(color='#2E5090', width=3),
            marker=dict(size=8, color='#2E5090')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5],
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                angularaxis=dict(gridcolor='rgba(0,0,0,0.1)')
            ),
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', size=12)
        )
        
        return fig

# ============================================================================
# AI INSIGHTS ENGINE - OLLAMA INTEGRATION (FREE & LOCAL!)
# ============================================================================

class AIInsightsEngine:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """
        Initialize with Ollama (free, local LLM)
        Default model: llama3.2 (fast and good quality)
        
        Install Ollama:
        1. Download from https://ollama.ai
        2. Run: ollama pull llama3.2
        """
        self.ollama_url = ollama_url
        self.model = "llama3.2"  # Fast, efficient model
        self.available = self._check_ollama_available()
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
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

Keep it concise, professional, and actionable. Use bullet points (•)."""
        
        return self._call_ollama(prompt)
    
    def generate_trainer_insights(self, trainer_name: str, metrics: Dict, comments: List[str]) -> str:
        """Generate personalized trainer insights"""
        if not self.available:
            return self._generate_fallback_trainer_insights(trainer_name, metrics)
        
        sample_comments = comments[:5] if comments else []
        
        prompt = f"""Create a personalized performance summary for trainer {trainer_name}:

Metrics:
{json.dumps(metrics, indent=2)}

Sample Participant Feedback:
{json.dumps(sample_comments, indent=2)}

Provide:
1. A warm, encouraging opening statement
2. 2-3 key strengths with specific examples
3. 1 growth opportunity (if ratings suggest)

Tone: Professional, supportive, specific. Keep under 150 words."""
        
        return self._call_ollama(prompt)
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['response'].strip()
            else:
                return "Unable to generate AI insights. Check Ollama connection."
                
        except Exception as e:
            return f"AI insights unavailable: {str(e)}"
    
    def _generate_fallback_overall_insights(self, kpis: Dict) -> str:
        """Generate insights without AI (fallback)"""
        rating = kpis.get('overall_rating', 0)
        nps = kpis.get('nps', 0)
        
        insights = []
        
        # Performance assessment
        if rating >= 4.5:
            insights.append("• **Outstanding Performance**: Your training programs are achieving excellent results with a rating of {:.2f}/5.0, placing you in the top tier of training providers.".format(rating))
        elif rating >= 4.0:
            insights.append("• **Strong Performance**: Your training is well-received with a solid {:.2f}/5.0 rating, indicating consistent quality delivery.".format(rating))
        else:
            insights.append("• **Room for Growth**: Current rating of {:.2f}/5.0 suggests opportunities to enhance training effectiveness.".format(rating))
        
        # NPS assessment
        if nps >= 50:
            insights.append("• **High Satisfaction**: Your NPS score of {:.1f} demonstrates strong participant loyalty and likelihood to recommend your programs.".format(nps))
        elif nps >= 0:
            insights.append("• **Positive Sentiment**: NPS score of {:.1f} shows generally satisfied participants with room to increase enthusiasm.".format(nps))
        else:
            insights.append("• **Action Needed**: NPS score of {:.1f} indicates a need to address participant concerns and improve experience.".format(nps))
        
        # Recommendation
        insights.append("• **Focus Areas**: Continue building on trainer strengths, gather detailed feedback for improvement opportunities, and maintain consistency across all sessions.")
        
        return "\n\n".join(insights)
    
    def _generate_fallback_trainer_insights(self, trainer_name: str, metrics: Dict) -> str:
        """Generate trainer insights without AI (fallback)"""
        rating = metrics.get('overall', 0)
        
        if rating >= 4.5:
            return f"{trainer_name} demonstrates exceptional teaching excellence with an outstanding rating of {rating:.2f}/5.0. Participants consistently praise their expertise, engagement, and ability to create an effective learning environment. This exceptional performance sets a high standard for training delivery."
        elif rating >= 4.0:
            return f"{trainer_name} maintains strong performance with a solid {rating:.2f}/5.0 rating. Their consistent delivery and professional approach create positive learning experiences. Participants value their knowledge and teaching style, with opportunities to further enhance engagement techniques."
        else:
            return f"{trainer_name} shows a rating of {rating:.2f}/5.0, indicating opportunities for development. Focus on gathering specific feedback from participants to identify areas for improvement in content delivery, engagement strategies, and participant support."

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_trainer_color(trainer_name: str) -> str:
    """Get consistent color for trainer"""
    return TRAINER_COLORS.get(trainer_name, TRAINER_COLORS['Default'])

def get_performance_level(rating: float) -> str:
    """Get performance level for rating"""
    for threshold, (level, _, _) in sorted(PERFORMANCE_LEVELS.items(), reverse=True):
        if rating >= threshold:
            return level
    return 'Needs Improvement'

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Hero Header
    st.markdown("""
        <div class="hero-header">
            <h1 class="hero-title">🚀 QTS Analytics AI Pro</h1>
            <p class="hero-subtitle">Intelligent Feedback Analysis • Real-Time Insights • AI-Powered Recommendations</p>
            <div class="hero-badge">✨ Next-Generation Analytics Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    # Unified Upload Section
    st.markdown("""
        <div class="upload-container">
            <div class="upload-icon">📤</div>
            <div class="upload-title">Upload Your Feedback Files</div>
            <div class="upload-subtitle">
                Drop all your Excel files here - our AI will automatically identify and organize them!<br>
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
                    <span class="upload-feature-icon">✓</span>
                    <span>AI-Powered Segregation</span>
                </div>
                <div class="upload-feature">
                    <span class="upload-feature-icon">✓</span>
                    <span>Automatic Merging</span>
                </div>
                <div class="upload-feature">
                    <span class="upload-feature-icon">✓</span>
                    <span>Duplicate Detection</span>
                </div>
                <div class="upload-feature">
                    <span class="upload-feature-icon">✓</span>
                    <span>Real-Time Analytics</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Process Button
    if uploaded_files and st.button("🔮 Process Data with AI", type="primary", use_container_width=True):
        with st.spinner(""):
            st.markdown("""
                <div class="processing-container">
                    <div class="processing-title">🤖 AI Processing in Progress</div>
                    <div class="processing-steps">
                        <div class="processing-step">🔍 Analyzing Files</div>
                        <div class="processing-step">🎯 Segregating Data</div>
                        <div class="processing-step">🔗 Merging Records</div>
                        <div class="processing-step">📊 Generating Insights</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Initialize processor
            processor = QTSDataProcessor()
            
            # Process files
            success, message = processor.process_files(uploaded_files)
            
            if success:
                st.session_state.processor = processor
                st.session_state.processed = True
                
                # Show file categorization results
                file_count_delegate = len(processor.delegate_data) if processor.delegate_data is not None else 0
                file_count_partner = len(processor.partner_data) if processor.partner_data is not None else 0
                
                st.success(f"✅ {message}")
                
                # Display categorization
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                        <div class="file-badge file-badge-delegate">
                            📋 Delegate: {file_count_delegate} records
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class="file-badge file-badge-partner">
                            🤝 Partner: {file_count_partner} records
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                        <div class="file-badge file-badge-master">
                            ✨ Ready for Analysis
                        </div>
                    """, unsafe_allow_html=True)
                
                st.rerun()
            else:
                st.error(f"❌ {message}")
    
    # Display Analytics if processed
    if st.session_state.processed and 'processor' in st.session_state:
        processor = st.session_state.processor
        analytics = QTSAnalytics(processor)
        ai_engine = AIInsightsEngine()
        
        # Calculate KPIs
        kpis = analytics.calculate_kpis()
        
        st.markdown('<div class="section-header">📊 Performance Dashboard</div>', unsafe_allow_html=True)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">⭐</div>
                    <div class="kpi-label">Overall Rating</div>
                    <div class="kpi-value">{kpis.get('overall_rating', 0):.2f}</div>
                    <div class="kpi-trend">
                        <span>↑</span> Out of 5.0
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">📝</div>
                    <div class="kpi-label">Total Responses</div>
                    <div class="kpi-value">{kpis.get('total_responses', 0):,}</div>
                    <div class="kpi-trend">
                        <span>📊</span> Feedback Entries
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            nps_color = '#10b981' if kpis.get('nps', 0) >= 50 else '#f59e0b' if kpis.get('nps', 0) >= 0 else '#ef4444'
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">🎯</div>
                    <div class="kpi-label">NPS Score</div>
                    <div class="kpi-value" style="color: {nps_color};">{kpis.get('nps', 0):.1f}</div>
                    <div class="kpi-trend">
                        <span>📈</span> Net Promoter
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">👥</div>
                    <div class="kpi-label">Active Trainers</div>
                    <div class="kpi-value">{kpis.get('trainer_count', 0)}</div>
                    <div class="kpi-trend">
                        <span>✨</span> Team Members
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # AI Overall Insights
        if ai_engine.available:
            with st.spinner("🤖 AI is analyzing your data..."):
                overall_insights = ai_engine.generate_overall_insights(kpis, processor.delegate_data)
                st.markdown(f"""
                    <div class="ai-insight">
                        <div class="ai-insight-header">
                            <span class="ai-insight-icon">🤖</span>
                            <span class="ai-insight-title">AI-Powered Insights</span>
                        </div>
                        <div class="ai-insight-content">
                            {overall_insights}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Tabs for detailed analysis
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualizations", "👥 Trainers", "🤝 Partners", "📋 Data"])
        
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
            st.markdown('<div class="section-header">🏆 Trainer Excellence</div>', unsafe_allow_html=True)
            
            # Trainer comparison
            trainer_chart = analytics.create_trainer_comparison()
            if trainer_chart:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(trainer_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Individual trainer cards
            st.markdown('<div class="section-header">Trainer Profiles</div>', unsafe_allow_html=True)
            
            trainer_col = None
            for col in processor.delegate_data.columns:
                if any(word in col.lower() for word in ['tutor', 'trainer', 'presenter']):
                    trainer_col = col
                    break
            
            if trainer_col:
                # Collect ALL trainers with their data
                trainers_data = []
                
                for trainer_name in processor.delegate_data[trainer_col].unique():
                    if pd.notna(trainer_name):
                        df_trainer = processor.delegate_data[processor.delegate_data[trainer_col] == trainer_name]
                        if len(df_trainer) >= 3:  # Minimum 3 sessions
                            rating_col = 'Please give the course a rating out of 5'
                            avg_rating = pd.to_numeric(df_trainer[rating_col], errors='coerce').mean() if rating_col in df_trainer.columns else 0
                            trainers_data.append({
                                'name': trainer_name,
                                'count': len(df_trainer),
                                'rating': avg_rating,
                                'data': df_trainer
                            })
                
                # Sort by rating (highest first)
                trainers_data.sort(key=lambda x: x['rating'], reverse=True)
                
                if trainers_data:
                    # Interactive trainer selection dropdown
                    st.markdown("""
                        <div style="background: white; padding: 1.5rem; border-radius: 16px; margin-bottom: 2rem; 
                                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                            <p style="margin: 0 0 1rem 0; font-weight: 600; color: #2E5090; font-size: 1rem;">
                                📋 Select a trainer to view their detailed profile:
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create selection options
                    trainer_options = ["🌟 View All Trainers"] + [
                        f"{t['name']} ⭐ {t['rating']:.2f}/5.0 ({t['count']} sessions)"
                        for t in trainers_data
                    ]
                    
                    selected_option = st.selectbox(
                        "Choose trainer:",
                        options=trainer_options,
                        index=0,
                        label_visibility="collapsed"
                    )
                    
                    # Determine which trainers to show
                    if selected_option == "🌟 View All Trainers":
                        trainers_to_show = trainers_data
                        show_all = True
                    else:
                        selected_name = selected_option.split(" ⭐")[0]
                        trainers_to_show = [t for t in trainers_data if t['name'] == selected_name]
                        show_all = False
                    
                    # Display trainer profiles
                    for idx, trainer_info in enumerate(trainers_to_show):
                        trainer_name = trainer_info['name']
                        df_trainer = trainer_info['data']
                        
                        color = get_trainer_color(trainer_name)
                        
                        # Calculate all metrics
                        metrics = {}
                        for metric_key in ['knowledge', 'adaptability', 'feedback', 'guidance']:
                            cols = [col for col in df_trainer.columns if metric_key.lower() in col.lower()]
                            if cols:
                                metrics[metric_key] = pd.to_numeric(df_trainer[cols[0]], errors='coerce').mean()
                        
                        rating_col = 'Please give the course a rating out of 5'
                        avg_rating = trainer_info['rating']
                        metrics['overall'] = avg_rating
                        
                        performance = get_performance_level(avg_rating)
                        
                        # Trainer card
                        st.markdown(f"""
                            <div class="trainer-card" style="border-left-color: {color}; color: {color};">
                                <div class="trainer-name" style="color: {color};">
                                    {trainer_name}
                                    <span class="badge badge-{performance.lower().replace(' ', '-')}">{performance}</span>
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
                        if ai_engine.available:
                            feedback_col = None
                            for col in df_trainer.columns:
                                if any(word in col.lower() for word in ['comment', 'feedback']):
                                    feedback_col = col
                                    break
                            
                            comments = df_trainer[feedback_col].dropna().tolist() if feedback_col else []
                            
                            with st.spinner(f"🤖 AI analyzing {trainer_name}'s performance..."):
                                trainer_insights = ai_engine.generate_trainer_insights(trainer_name, metrics, comments)
                                st.markdown(f"""
                                    <div class="ai-insight" style="background: linear-gradient(135deg, {color}dd, {color}aa);">
                                        <div class="ai-insight-header">
                                            <span class="ai-insight-icon">✨</span>
                                            <span class="ai-insight-title">AI-Powered Insights</span>
                                        </div>
                                        <div class="ai-insight-content">
                                            {trainer_insights}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            # Fallback without AI
                            fallback_insights = ai_engine._generate_fallback_trainer_insights(trainer_name, metrics)
                            st.markdown(f"""
                                <div class="ai-insight" style="background: linear-gradient(135deg, {color}dd, {color}aa);">
                                    <div class="ai-insight-header">
                                        <span class="ai-insight-icon">📊</span>
                                        <span class="ai-insight-title">Performance Summary</span>
                                    </div>
                                    <div class="ai-insight-content">
                                        {fallback_insights}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Participant feedback
                        feedback_col = None
                        for col in df_trainer.columns:
                            if any(word in col.lower() for word in ['comment', 'feedback']):
                                feedback_col = col
                                break
                        
                        if feedback_col:
                            comments = df_trainer[feedback_col].dropna().unique().tolist()
                            if comments:
                                comment_limit = 5 if not show_all else 2
                                
                                st.markdown(f"""
                                    <div style="background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.05); 
                                                border-radius: 16px; padding: 1.5rem; margin: 1rem 0; 
                                                border-left: 4px solid {color};">
                                        <div style="color: {color}; font-weight: 600; margin-bottom: 1rem; 
                                                    display: flex; align-items: center; gap: 0.5rem;">
                                            <span style="font-size: 1.2rem;">💬</span>
                                            <span>Participant Feedback</span>
                                        </div>
                                """, unsafe_allow_html=True)
                                
                                displayed = 0
                                for comment in comments:
                                    if pd.notna(comment) and len(str(comment).strip()) > 10:
                                        st.markdown(f"""
                                            <div style="background: white; padding: 1rem; border-radius: 12px; 
                                                        margin-bottom: 0.75rem; border-left: 3px solid {color};
                                                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                                                <span style="color: #374151; font-style: italic;">
                                                    "{str(comment).strip()}"
                                                </span>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        displayed += 1
                                        if displayed >= comment_limit:
                                            break
                                
                                if len(comments) > comment_limit:
                                    st.markdown(f"""
                                        <div style="text-align: center; color: {color}; 
                                                    font-size: 0.9rem; margin-top: 0.5rem;">
                                            +{len(comments) - comment_limit} more comments
                                        </div>
                                    """, unsafe_allow_html=True)
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Divider between trainers when showing all
                        if show_all and idx < len(trainers_to_show) - 1:
                            st.markdown('''
                                <div style="margin: 2.5rem 0; border-bottom: 2px solid #E8EAED;"></div>
                            ''', unsafe_allow_html=True)
                    
                    # Team summary when viewing all
                    if show_all and len(trainers_data) > 1:
                        st.markdown('<div class="section-header">📊 Team Performance Summary</div>', unsafe_allow_html=True)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        avg_team_rating = sum(t['rating'] for t in trainers_data) / len(trainers_data)
                        total_sessions = sum(t['count'] for t in trainers_data)
                        top_performer = trainers_data[0]['name']
                        consistency = 1 - (max(t['rating'] for t in trainers_data) - min(t['rating'] for t in trainers_data)) / 5
                        
                        with col1:
                            st.markdown(f"""
                                <div class="kpi-card">
                                    <div class="kpi-icon">⭐</div>
                                    <div class="kpi-label">Team Average</div>
                                    <div class="kpi-value">{avg_team_rating:.2f}</div>
                                    <div class="kpi-trend">Out of 5.0</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                                <div class="kpi-card">
                                    <div class="kpi-icon">📊</div>
                                    <div class="kpi-label">Total Sessions</div>
                                    <div class="kpi-value">{total_sessions}</div>
                                    <div class="kpi-trend">{len(trainers_data)} trainers</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                                <div class="kpi-card">
                                    <div class="kpi-icon">🏆</div>
                                    <div class="kpi-label">Top Performer</div>
                                    <div class="kpi-value" style="font-size: 1.2rem;">{top_performer.split()[0]}</div>
                                    <div class="kpi-trend">{trainers_data[0]['rating']:.2f}/5.0</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            st.markdown(f"""
                                <div class="kpi-card">
                                    <div class="kpi-icon">✨</div>
                                    <div class="kpi-label">Consistency</div>
                                    <div class="kpi-value">{consistency*100:.0f}%</div>
                                    <div class="kpi-trend">Team coherence</div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("📌 No trainer data available (minimum 3 sessions required per trainer)")
            else:
                st.warning("⚠️ Could not identify trainer column in the data")
        
        with tab3:
            st.markdown('<div class="section-header">🤝 Partner Feedback</div>', unsafe_allow_html=True)
            
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
                st.info("📌 No partner feedback data available")
        
        with tab4:
            st.markdown('<div class="section-header">📋 Raw Data</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(processor.delegate_data):,}")
            with col2:
                st.metric("Columns", len(processor.delegate_data.columns))
            with col3:
                st.metric("Missing Values", f"{processor.delegate_data.isnull().sum().sum():,}")
            
            st.dataframe(processor.delegate_data, use_container_width=True, height=400)
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                csv = processor.delegate_data.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
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
                    "📥 Download Excel",
                    output.getvalue(),
                    f"qts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()