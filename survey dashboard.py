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
from typing import Dict, List, Optional
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION - TRAINER COLOR SYSTEM
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
    'Outstanding': {'color': '#1B5E20', 'light': '#E8F5E9', 'icon': '⭐'},
    'Excellent': {'color': '#2E5090', 'light': '#E3F2FD', 'icon': '✨'},
    'Very Good': {'color': '#F57C00', 'light': '#FFF3E0', 'icon': '👍'},
}

BRAND_COLOR = '#2E5090'
CHART_COLORS = ['#2E5090', '#D4A574', '#7CB342', '#E57373', '#6C63B6', '#FF8A80', '#4A90E2']

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
# PAGE SETUP - PREMIUM EXPERIENCE
# ============================================================================

st.set_page_config(
    page_title="QTS Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM CSS STYLING
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
        background: #FAFBFC;
        font-family: 'Poppins', sans-serif;
        color: #1a1a1a;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* ELEGANT HEADER */
    /* ═══════════════════════════════════════════════════════════ */
    
    .premium-header {
        background: linear-gradient(135deg, #2E5090 0%, #1B3D6F 100%);
        padding: 2.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2.5rem -1rem;
        box-shadow: 0 8px 24px rgba(46, 80, 144, 0.15);
    }
    
    .premium-header h1 {
        color: white;
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .premium-header p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        font-weight: 300;
        margin: 0;
        letter-spacing: 0.3px;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* KPI CARDS - MINIMAL & ELEGANT */
    /* ═══════════════════════════════════════════════════════════ */
    
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E8EAED;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .kpi-card:hover {
        border-color: #2E5090;
        box-shadow: 0 12px 32px rgba(46, 80, 144, 0.08);
        transform: translateY(-2px);
    }
    
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.75rem;
    }
    
    .kpi-value {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #2E5090;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .kpi-subtitle {
        font-size: 0.85rem;
        color: #9CA3AF;
        font-weight: 400;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* SECTION HEADERS */
    /* ═══════════════════════════════════════════════════════════ */
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E8EAED;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* TRAINER SUMMARY CARDS - PREMIUM */
    /* ═══════════════════════════════════════════════════════════ */
    
    .trainer-header-card {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        border-left: 5px solid;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .trainer-header-card:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    .trainer-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .trainer-meta {
        display: flex;
        gap: 1.5rem;
        font-size: 0.9rem;
        color: #6B7280;
        margin-bottom: 0;
        flex-wrap: wrap;
    }
    
    .trainer-meta-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* INSIGHT CARDS */
    /* ═══════════════════════════════════════════════════════════ */
    
    .insight-container {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .insight-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-content {
        font-size: 0.95rem;
        line-height: 1.7;
        color: #374151;
    }
    
    .insight-highlight {
        background: linear-gradient(120deg, rgba(46, 80, 144, 0.05), rgba(46, 80, 144, 0.02));
        padding: 0.875rem 1.25rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        border-left: 3px solid;
        font-style: italic;
        color: #4B5563;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* BADGE STYLES */
    /* ═══════════════════════════════════════════════════════════ */
    
    .badge-outstanding {
        background: #E8F5E9;
        color: #1B5E20;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-excellent {
        background: #E3F2FD;
        color: #2E5090;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* CHARTS */
    /* ═══════════════════════════════════════════════════════════ */
    
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        border: 1px solid #E8EAED;
        margin-bottom: 1.5rem;
    }
    
    /* ═══════════════════════════════════════════════════════════ */
    /* UTILITY */
    /* ═══════════════════════════════════════════════════════════ */
    
    .divider {
        height: 1px;
        background: #E8EAED;
        margin: 1.5rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #2E5090 0%, #1B3D6F 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(46, 80, 144, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(46, 80, 144, 0.4) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_trainer_color(trainer_name):
    """Get unique color for trainer"""
    return TRAINER_COLORS.get(trainer_name, TRAINER_COLORS['Default'])

def parse_date(date_string):
    """Parse date with multiple format support"""
    if pd.isna(date_string):
        return None
    
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(date_string, format=fmt)
        except:
            continue
    return pd.to_datetime(date_string, errors='coerce')

def clean_numeric(value):
    """Clean numeric values"""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.replace(',', '').strip()
    try:
        return float(value)
    except:
        return None

def get_performance_level(rating):
    """Determine performance level from rating"""
    if rating >= 4.7:
        return 'Outstanding'
    elif rating >= 4.3:
        return 'Excellent'
    else:
        return 'Very Good'

# ============================================================================
# AI INTEGRATION (OLLAMA)
# ============================================================================

class AIInsightsEngine:
    """Ollama-powered insights engine (runs locally, completely free!)"""
    
    def __init__(self, model: str = "llama3.2", ollama_url: str = "http://localhost:11434"):
        self.model = model
        self.ollama_url = ollama_url
        self.available = self._check_ollama_available()
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '').split(':')[0] for m in models]
                return any(self.model in name for name in model_names)
            return False
        except:
            return False
    
    def _call_ollama(self, prompt: str, system_prompt: str, max_tokens: int = 200) -> str:
        """Make a call to Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                return None
        except Exception as e:
            return None
    
    def generate_personalized_trainer_summary(self, trainer_name: str, metrics: Dict, comments: List[str]) -> str:
        """Generate detailed personalized trainer summary"""
        if not self.available or not comments:
            return self._fallback_trainer_summary(trainer_name, metrics, comments)
        
        # Sample comments if too many
        sample_comments = comments[:5] if len(comments) > 5 else comments
        
        prompt = f"""Analyze this trainer's performance and generate a comprehensive but concise profile (3-4 sentences):

Trainer: {trainer_name}
Knowledge Score: {metrics.get('knowledge', 'N/A')}/5.0
Adaptability Score: {metrics.get('adaptability', 'N/A')}/5.0
Feedback Quality Score: {metrics.get('feedback', 'N/A')}/5.0
Guidance Score: {metrics.get('guidance', 'N/A')}/5.0
Average Rating: {metrics.get('overall', 'N/A')}/5.0

Participant Comments:
{chr(10).join([f'- "{c}"' for c in sample_comments if c and str(c).strip()])}

Create a personalized profile highlighting:
1. Key teaching strengths (based on metrics)
2. What makes them exceptional (from comments)
3. One area they excel at most
Be specific, warm, and actionable."""

        system_prompt = "You are a training evaluation expert. Write personalized, specific profiles that celebrate achievements. Be warm but professional."
        
        result = self._call_ollama(prompt, system_prompt, max_tokens=250)
        
        if result:
            return result
        else:
            return self._fallback_trainer_summary(trainer_name, metrics, comments)
    
    def _fallback_trainer_summary(self, trainer_name: str, metrics: Dict, comments: List[str]) -> str:
        """Fallback personalized trainer summary"""
        knowledge = metrics.get('knowledge', 0)
        adaptability = metrics.get('adaptability', 0)
        overall = metrics.get('overall', 0)
        
        strengths = []
        if knowledge >= 4.5:
            strengths.append("exceptional subject expertise")
        if adaptability >= 4.5:
            strengths.append("outstanding adaptability to different learning styles")
        if overall >= 4.7:
            strengths.append("consistently outstanding delivery")
        
        strength_text = ", ".join(strengths) if strengths else "strong performance across all metrics"
        
        summary = f"{trainer_name} demonstrates {strength_text}. "
        
        if comments:
            comment = [c for c in comments if c and str(c).strip()]
            if comment:
                summary += f'Participants specifically noted that "{comment[0]}". '
        
        summary += f"With an average rating of {overall:.2f}/5.0, they consistently deliver high-quality training experiences."
        
        return summary
    
    def generate_summary_insight(self, kpis: Dict, data: pd.DataFrame) -> str:
        """Generate executive summary"""
        if not self.available:
            return self._fallback_summary(kpis, data)
        
        prompt = f"""Analyze this training feedback data and provide a brief executive summary (2-3 sentences):

- Overall Quality Score: {kpis['satisfaction']:.2f}/5.0
- Course Rating: {kpis['rating']:.2f}/5.0
- NPS Score: {kpis.get('nps_score', 0):.1f}
- Total Responses: {kpis['responses']}
- Response Rate: {kpis['response_rate']:.0f}%
- Number of Trainers: {data.get('Tutor Name', pd.Series()).nunique() if 'Tutor Name' in data.columns else 'N/A'}

Focus on the most important insight and one actionable recommendation."""

        system_prompt = "You are a data analyst specializing in training program evaluation. Be concise and actionable."
        
        result = self._call_ollama(prompt, system_prompt, max_tokens=150)
        
        if result:
            return result
        else:
            return self._fallback_summary(kpis, data)
    
    def _fallback_summary(self, kpis: Dict, data: pd.DataFrame) -> str:
        """Fallback summary"""
        quality = kpis['satisfaction']
        
        if quality >= 4.5:
            assessment = "Outstanding performance"
        elif quality >= 4.0:
            assessment = "Strong performance"
        elif quality >= 3.5:
            assessment = "Good performance"
        else:
            assessment = "Performance needs attention"
        
        return f"{assessment} with {kpis['rating']:.2f}/5.0 course rating across {kpis['responses']} responses. NPS Score of {kpis.get('nps_score', 0):.1f} indicates strong recommendation potential. Focus on maintaining trainer quality and gathering more feedback for continuous improvement."

# ============================================================================
# DATA PROCESSING
# ============================================================================

class QTSDataProcessor:
    """Enhanced data processor with better error handling"""
    
    def __init__(self):
        self.delegate_data = None
        self.partner_data = None
        self.master_data = None
        self.processing_log = []
    
    def safe_date_parse(self, data, date_column):
        """Smart date parsing with multiple format attempts"""
        if date_column not in data.columns:
            return data
        
        for fmt in DATE_FORMATS:
            try:
                parsed = pd.to_datetime(data[date_column], format=fmt, errors='coerce')
                if parsed.notna().sum() / len(data) > 0.8:
                    data[date_column] = parsed
                    self.processing_log.append(f"✓ Parsed dates with format: {fmt}")
                    return data
            except:
                continue
        
        return data
    
    def load_excel_smart(self, file):
        """Load Excel with multi-sheet support"""
        try:
            excel_data = pd.read_excel(file, sheet_name=None)
            
            if isinstance(excel_data, dict):
                dfs = []
                for sheet_name, df in excel_data.items():
                    if not df.empty:
                        df['Source_Sheet'] = sheet_name
                        dfs.append(df)
                if dfs:
                    self.processing_log.append(f"✓ Combined {len(dfs)} sheets")
                    return pd.concat(dfs, ignore_index=True)
            else:
                return list(excel_data.values())[0]
        except Exception as e:
            st.error(f"Error loading Excel: {e}")
            self.processing_log.append(f"✗ Error: {str(e)}")
            return None
    
    def clean_numeric_columns(self, data):
        """Clean and standardize numeric rating columns"""
        rating_columns = [col for col in data.columns if 'rating' in col.lower() or 'score' in col.lower()]
        
        for col in rating_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        return data
    
    def load_data(self, delegate_file=None, partner_file=None, master_file=None):
        """Load data from uploaded files with enhanced processing"""
        self.processing_log = []
        success = False
        
        if delegate_file:
            self.delegate_data = self.load_excel_smart(delegate_file)
            if self.delegate_data is not None:
                self.delegate_data.columns = self.delegate_data.columns.str.strip()
                self.delegate_data = self.safe_date_parse(self.delegate_data, 'Date of Course')
                self.delegate_data = self.clean_numeric_columns(self.delegate_data)
                st.success(f"✅ Delegate feedback: {len(self.delegate_data):,} records")
                success = True
        
        if partner_file:
            self.partner_data = self.load_excel_smart(partner_file)
            if self.partner_data is not None:
                self.partner_data.columns = self.partner_data.columns.str.strip()
                self.partner_data = self.clean_numeric_columns(self.partner_data)
                st.success(f"✅ Partner feedback: {len(self.partner_data):,} records")
                success = True
        
        if master_file:
            self.master_data = self.load_excel_smart(master_file)
            if self.master_data is not None:
                self.master_data.columns = self.master_data.columns.str.strip()
                self.master_data = self.safe_date_parse(self.master_data, 'Date of Course')
                self.master_data = self.clean_numeric_columns(self.master_data)
                st.success(f"✅ Master data: {len(self.master_data):,} records")
                success = True
        
        return success

# ============================================================================
# ENHANCED ANALYTICS
# ============================================================================

class QTSAnalytics:
    """Enhanced analytics engine with more insights"""
    
    def __init__(self, data):
        self.data = data
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        kpis = {
            'satisfaction': 0,
            'rating': 0,
            'responses': len(self.data),
            'response_rate': 0,
            'nps_score': 0,
            'completion_rate': 0
        }
        
        rating_col = 'Please give the course a rating out of 5'
        
        if rating_col in self.data.columns:
            kpis['satisfaction'] = self.data[rating_col].mean()
            kpis['rating'] = self.data[rating_col].mean()
        else:
            satisfaction_cols = [col for col in self.data.columns if 
                               any(word in col.lower() for word in ['quality', 'rating', 'satisfaction', 'overall'])]
            if satisfaction_cols:
                kpis['satisfaction'] = self.data[satisfaction_cols[0]].mean()
                kpis['rating'] = self.data[satisfaction_cols[0]].mean()
        
        if rating_col in self.data.columns:
            kpis['response_rate'] = (self.data[rating_col].notna().sum() / len(self.data)) * 100
        else:
            kpis['response_rate'] = 100
        
        if rating_col in self.data.columns:
            ratings = self.data[rating_col].dropna()
            if len(ratings) > 0:
                promoters = (ratings >= 4.5).sum()
                detractors = (ratings <= 3.5).sum()
                kpis['nps_score'] = ((promoters - detractors) / len(ratings)) * 100
        
        return kpis
    
    def create_trainer_comparison_chart(self, trainer_col='Tutor Name'):
        """Create trainer performance chart with trainer-specific colors"""
        if trainer_col not in self.data.columns:
            return None
        
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.data.columns:
            return None
        
        trainer_stats = []
        for trainer in self.data[trainer_col].unique():
            if pd.notna(trainer):
                df_trainer = self.data[self.data[trainer_col] == trainer]
                if len(df_trainer) >= 1:  # Show all trainers, not just 3+
                    avg_rating = pd.to_numeric(df_trainer[rating_col], errors='coerce').mean()
                    if pd.notna(avg_rating):
                        trainer_stats.append({
                            'Trainer': str(trainer),
                            'Rating': avg_rating,
                            'Sessions': len(df_trainer),
                            'Color': get_trainer_color(str(trainer))
                        })
        
        if not trainer_stats:
            return None
        
        df_stats = pd.DataFrame(trainer_stats).sort_values('Rating', ascending=False)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_stats['Trainer'],
            x=df_stats['Rating'],
            orientation='h',
            marker=dict(color=df_stats['Color'], line=dict(width=0)),
            text=[f"{r:.2f}" for r in df_stats['Rating']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Rating: %{x:.2f}/5.0<br>Sessions: %{customdata}<extra></extra>',
            customdata=df_stats['Sessions'],
            showlegend=False
        ))
        
        fig.update_layout(
            title='Trainer Performance Comparison',
            xaxis_title='Average Rating (out of 5.0)',
            yaxis_title='',
            height=max(250, len(df_stats) * 50),
            margin=dict(l=150, r=100, t=50, b=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            font=dict(family='Poppins', size=12, color='#374151'),
            xaxis=dict(range=[0, 5.2], gridcolor='#E8EAED', zeroline=False),
            yaxis=dict(showgrid=False)
        )
        
        return fig
    
    def create_trend_chart(self):
        """Create enhanced trend chart with moving average - SIMPLIFIED"""
        if 'Date of Course' not in self.data.columns:
            return None
        
        if not pd.api.types.is_datetime64_any_dtype(self.data['Date of Course']):
            return None
        
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.data.columns:
            return None
        
        df = self.data[['Date of Course', rating_col]].copy()
        df['Rating'] = pd.to_numeric(df[rating_col], errors='coerce')
        df = df.dropna()
        
        if len(df) < 2:
            return None
        
        # Group by month for cleaner display
        df['Month'] = df['Date of Course'].dt.strftime('%b %Y')  # "Jan 2025" format
        monthly = df.groupby(['Date of Course', 'Month'])['Rating'].agg(['mean', 'count']).reset_index()
        monthly = monthly.sort_values('Date of Course').drop('Date of Course', axis=1)
        monthly['MA'] = monthly['mean'].rolling(window=3, min_periods=1).mean()
        
        fig = go.Figure()
        
        # Line for actual monthly average
        fig.add_trace(go.Scatter(
            x=monthly['Month'],
            y=monthly['mean'],
            mode='lines+markers',
            name='Monthly Average',
            line=dict(color=BRAND_COLOR, width=3),
            marker=dict(size=8, color=BRAND_COLOR),
            hovertemplate='<b>%{x}</b><br>Average: %{y:.2f}/5.0<extra></extra>'
        ))
        
        # Dashed line for moving average
        fig.add_trace(go.Scatter(
            x=monthly['Month'],
            y=monthly['MA'],
            mode='lines',
            name='3-Month Trend',
            line=dict(color='#10b981', width=2, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Trend: %{y:.2f}/5.0<extra></extra>'
        ))
        
        fig.update_layout(
            title='Quality Trend Over Time',
            xaxis_title="Month",
            yaxis_title="Rating (out of 5.0)",
            hovermode='x unified',
            height=400,
            yaxis=dict(range=[3, 5.2], gridcolor='#E8EAED'),
            xaxis=dict(gridcolor='#E8EAED'),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            font=dict(family='Poppins', size=12, color='#374151'),
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
        )
        
        return fig
    
    def create_distribution_chart(self):
        """Create rating distribution histogram"""
        rating_col = 'Please give the course a rating out of 5'
        if rating_col not in self.data.columns:
            return None
        
        ratings = self.data[rating_col].dropna()
        
        if len(ratings) == 0:
            return None
        
        fig = go.Figure(data=[go.Histogram(
            x=ratings,
            nbinsx=20,
            marker_color=BRAND_COLOR,
            opacity=0.7
        )])
        
        mean_rating = ratings.mean()
        fig.add_vline(
            x=mean_rating,
            line_dash="dash",
            line_color="#ef4444",
            annotation_text=f"Mean: {mean_rating:.2f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            title=None,
            xaxis_title="Rating",
            yaxis_title="Frequency",
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            font=dict(family='Poppins', size=11, color='#374151'),
            showlegend=False
        )
        
        return fig
    
    def create_heatmap(self):
        """Create correlation heatmap for RATING columns only (simplified)"""
        # Find only rating/score columns (not all columns)
        rating_cols = [col for col in self.data.columns if any(
            word in col.lower() for word in 
            ['rating', 'score', 'satisfaction', 'quality', 'knowledge', 'feedback', 
             'guidance', 'content', 'pace', 'accommodation', 'training', 'appropriate',
             'objectives', 'structure', 'responded', 'climate', 'constructive']
        )]
        
        if len(rating_cols) < 2:
            return None
        
        # Convert to numeric
        numeric_data = self.data[rating_cols].copy()
        numeric_data = numeric_data.astype(float, errors='ignore')
        numeric_data = numeric_data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            return None
        
        corr_matrix = numeric_data.corr()
        
        # Clean up column names for display
        clean_names = [
            name.replace('Please give the course a rating out of 5', 'Overall Rating')
            .replace('Demonstrated knowledge about the subject matter', 'Subject Knowledge')
            .replace('Gave useful feedback which helped individuals and the group', 'Feedback Quality')
            .replace('Adopted and responded to the needs of individuals', 'Adaptability')
            .replace('Provided appropriate guidance when needed', 'Guidance')
            .replace('The content was appropriate and relevant to individual needs', 'Content Relevance')
            .replace('The structure enabled the learning objectives to be met', 'Structure')
            .replace('The accommodation and services were appropriate', 'Accommodation')
            [:40]  # Truncate long names
            for name in corr_matrix.columns
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=clean_names,
            y=clean_names,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='.2f',
            textfont={"size": 10},
            colorbar=dict(title="Correlation", thickness=20, len=0.7),
            hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='How Training Metrics Correlate',
            height=500,
            width=700,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Poppins', size=10, color='#374151'),
            xaxis=dict(tickangle=-45),
            margin=dict(b=150, l=150)
        )
        
        return fig

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Premium Header
    st.markdown("""
        <div class="premium-header">
            <h1>📊 QTS Analytics Pro</h1>
            <p>Professional insights into trainer performance and course effectiveness</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - File Upload
    with st.sidebar:
        st.markdown("### 📁 Upload Data")
        delegate_file = st.file_uploader("Delegate Feedback", type=['xlsx', 'xls'], key='delegate')
        partner_file = st.file_uploader("Partner Feedback", type=['xlsx', 'xls'], key='partner')
        master_file = st.file_uploader("Master Data", type=['xlsx', 'xls'], key='master')
        
        process_button = st.button("🔄 Process Data", use_container_width=True)
    
    if not process_button:
        if not delegate_file:
            st.info("👈 Upload files using the sidebar to get started")
        return
    
    # Initialize processors
    processor = QTSDataProcessor()
    ai_engine = AIInsightsEngine()
    
    # Load data
    if not processor.load_data(delegate_file, partner_file, master_file):
        st.error("No files processed successfully")
        return
    
    # Use delegate data as primary
    if processor.delegate_data is None:
        st.error("Delegate feedback data is required")
        return
    
    # Analytics
    analytics = QTSAnalytics(processor.delegate_data)
    kpis = analytics.calculate_kpis()
    
    # ════════════════════════════════════════════════════════════════
    # KPI SUMMARY
    # ════════════════════════════════════════════════════════════════
    
    st.markdown('<div class="section-header">📈 Summary Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Overall Rating</div>
                <div class="kpi-value">{kpis['satisfaction']:.2f}</div>
                <div class="kpi-subtitle">Out of 5.0</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Responses</div>
                <div class="kpi-value">{kpis['responses']:,}</div>
                <div class="kpi-subtitle">Feedback entries</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Response Rate</div>
                <div class="kpi-value">{kpis['response_rate']:.0f}%</div>
                <div class="kpi-subtitle">Completion rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">NPS Score</div>
                <div class="kpi-value">{kpis['nps_score']:.1f}</div>
                <div class="kpi-subtitle">Recommendation index</div>
            </div>
        """, unsafe_allow_html=True)
    
    # AI Summary
    if ai_engine.available:
        st.markdown("#### 🤖 AI Executive Summary")
        with st.spinner("Generating insights..."):
            summary = ai_engine.generate_summary_insight(kpis, processor.delegate_data)
            st.markdown(f"""
                <div class="insight-container" style="border-left-color: {BRAND_COLOR};">
                    <div class="insight-content">
                        {summary}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Charts", "⭐ Trainers", "🤝 Partner", "📈 Advanced", "📋 Data"])
    
    with tab1:
        st.markdown('<div class="section-header">Performance Trends</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            trend_chart = analytics.create_trend_chart()
            if trend_chart:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(trend_chart, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            dist_chart = analytics.create_distribution_chart()
            if dist_chart:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(dist_chart, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-header">🏆 Trainer Performance</div>', unsafe_allow_html=True)
        
        # Trainer comparison chart with colors
        trainer_chart = analytics.create_trainer_comparison_chart()
        if trainer_chart:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(trainer_chart, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">⭐ Trainer Profiles</div>', unsafe_allow_html=True)
        
        # Personalized trainer summaries
        trainer_col = None
        for col in processor.delegate_data.columns:
            if 'tutor' in col.lower() or 'trainer' in col.lower() or 'presenter' in col.lower():
                trainer_col = col
                break
        
        feedback_col = None
        for col in processor.delegate_data.columns:
            if 'comment' in col.lower() or 'feedback' in col.lower():
                feedback_col = col
                break
        
        if trainer_col:
            trainers = sorted([t for t in processor.delegate_data[trainer_col].unique() if pd.notna(t)])
            
            rating_col = 'Please give the course a rating out of 5'
            
            for trainer_name in trainers:
                df_trainer = processor.delegate_data[processor.delegate_data[trainer_col] == trainer_name]
                
                if len(df_trainer) >= 3:
                    color = get_trainer_color(trainer_name)
                    
                    # Calculate metrics
                    metrics = {}
                    for metric_key in ['knowledge', 'adaptability', 'feedback', 'guidance']:
                        cols = [col for col in df_trainer.columns if metric_key.lower() in col.lower()]
                        if cols:
                            metrics[metric_key] = pd.to_numeric(df_trainer[cols[0]], errors='coerce').mean()
                    
                    if rating_col in df_trainer.columns:
                        metrics['overall'] = pd.to_numeric(df_trainer[rating_col], errors='coerce').mean()
                    
                    performance = get_performance_level(metrics.get('overall', 0))
                    perf_theme = PERFORMANCE_THEMES.get(performance, PERFORMANCE_THEMES['Excellent'])
                    
                    # Trainer header
                    st.markdown(f"""
                        <div class="trainer-header-card" style="border-left-color: {color};">
                            <div class="trainer-name" style="color: {color};">{trainer_name} {perf_theme['icon']}</div>
                            <div class="trainer-meta">
                                <div class="trainer-meta-item">
                                    <span style="font-weight: 600; color: {color};">{metrics.get('overall', 0):.2f}/5.0</span>
                                    <span>Average Rating</span>
                                </div>
                                <div class="trainer-meta-item">
                                    <span style="font-weight: 600;">{len(df_trainer)}</span>
                                    <span>Sessions</span>
                                </div>
                                <div class="trainer-meta-item">
                                    <span class="badge-{performance.lower().replace(' ', '-')}">{performance}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # AI Personalized Summary
                    if ai_engine.available:
                        comments = df_trainer[feedback_col].dropna().unique().tolist() if feedback_col else []
                        if comments or metrics:
                            with st.spinner(f"Analyzing {trainer_name}..."):
                                summary = ai_engine.generate_personalized_trainer_summary(trainer_name, metrics, comments)
                                st.markdown(f"""
                                    <div class="insight-container" style="border-left-color: {color};">
                                        <div class="insight-title" style="color: {color};">
                                            ✨ Trainer Profile
                                        </div>
                                        <div class="insight-content">
                                            {summary}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                    
                    # Feedback highlights
                    if feedback_col:
                        comments = df_trainer[feedback_col].dropna().unique().tolist()
                        if comments:
                            st.markdown(f"""
                                <div class="insight-container" style="border-left-color: {color};">
                                    <div class="insight-title" style="color: {color};">
                                        💬 Participant Feedback
                                    </div>
                            """, unsafe_allow_html=True)
                            
                            for comment in comments[:2]:
                                if pd.notna(comment) and len(str(comment).strip()) > 10:
                                    st.markdown(f"""
                                        <div class="insight-highlight" style="border-left-color: {color};">
                                            "{str(comment).strip()}"
                                        </div>
                                    """, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🤝 Partner Feedback")
        
        if processor.partner_data is not None and len(processor.partner_data) > 0:
            for idx, row in processor.partner_data.iterrows():
                with st.expander(f"Partner Feedback #{idx+1}"):
                    cols = st.columns(2)
                    col_idx = 0
                    for col in processor.partner_data.columns:
                        if pd.notna(row[col]) and row[col] != '':
                            with cols[col_idx % 2]:
                                st.markdown(f"**{col}:**")
                                st.write(row[col])
                            col_idx += 1
        else:
            st.info("No partner feedback data available")
    
    with tab4:
        st.markdown("### 📈 Advanced Analytics")
        
        st.markdown("#### Metric Correlations")
        heatmap = analytics.create_heatmap()
        if heatmap:
            st.plotly_chart(heatmap, use_container_width=True)
        else:
            st.info("Need more numeric columns for correlation analysis")
    
    with tab5:
        st.markdown("### 📋 Raw Data View")
        
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
                "📥 Download as CSV",
                csv,
                f"qts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                processor.delegate_data.to_excel(writer, index=False, sheet_name='Data')
                kpi_df = pd.DataFrame([kpis])
                kpi_df.to_excel(writer, index=False, sheet_name='Summary')
            
            st.download_button(
                "📥 Download as Excel",
                output.getvalue(),
                f"qts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

if __name__ == "__main__":
    main()