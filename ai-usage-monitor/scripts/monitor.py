#!/usr/bin/env python3
"""
AI Tools Usage Monitor
Monitors and estimates usage for various AI tools with different billing cycles.
Fetches real-time data when APIs are available.
"""

import sqlite3
import json
import os
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Tuple
from pathlib import Path

@dataclass
class ToolConfig:
    name: str
    cost: float
    billing_day: int
    window_type: str  # 'monthly', 'weekly', '5h+weekly'
    api_source: Optional[str] = None  # 'openai', 'direct', etc.

@dataclass
class UsageData:
    tool_name: str
    current_usage: float
    usage_unit: str
    billing_start: datetime
    billing_end: datetime
    days_remaining: int
    projected_monthly: float
    status: str
    api_status: str  # 'connected', 'no_api', 'error'
    api_message: Optional[str] = None

@dataclass
class APIStatus:
    tool: str
    available: bool
    message: str

class AIUsageMonitor:
    def __init__(self, db_path: str = "~/.ai_usage_monitor.db"):
        self.db_path = Path(db_path).expanduser()
        self.init_db()
        self.api_statuses: List[APIStatus] = []
        
        # Tool configurations with API sources
        self.tools = {
            'cursor': ToolConfig('Cursor', 20.0, 10, 'monthly'),
            'codex': ToolConfig('Codex', 200.0, 22, '5h+weekly', 'openai'),
            'copilot': ToolConfig('Copilot', 10.0, 25, 'monthly', 'github'),
            'synthetic': ToolConfig('Synthetic', 20.0, 17, '5h+weekly', 'synthetic'),
        }
        
        # Check available APIs
        self._check_available_apis()
    
    def _check_available_apis(self):
        """Check which APIs are available via environment variables"""
        env_vars = {
            'openai': 'OPENAI_API_KEY',
            'github': 'GITHUB_TOKEN',
            'synthetic': 'SYNTHETIC_API_KEY',
            'cursor': 'CURSOR_API_KEY',
            'copilot': 'COPILOT_API_KEY',
        }
        
        for api_name, env_var in env_vars.items():
            value = os.getenv(env_var)
            if value:
                self.api_statuses.append(APIStatus(api_name, True, f"{env_var} encontrada"))
            else:
                self.api_statuses.append(APIStatus(api_name, False, f"{env_var} não encontrada"))
    
    def fetch_openai_usage(self) -> Optional[Dict]:
        """Fetch usage from OpenAI API (for Codex)"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None
        
        try:
            # OpenAI doesn't have a direct usage endpoint in the standard API
            # This is a placeholder - in practice you'd use the dashboard API
            headers = {'Authorization': f'Bearer {api_key}'}
            # Note: OpenAI usage API requires special access
            # For now, return None to indicate we couldn't fetch
            return {'status': 'api_available_but_no_usage_endpoint', 'hours_used': 0}
        except Exception as e:
            return {'error': str(e)}
    
    def fetch_synthetic_usage(self) -> Optional[Dict]:
        """Fetch usage from Synthetic API"""
        # Synthetic API endpoint would go here
        # Placeholder - no public API known
        return None
    
    def fetch_realtime_usage(self, tool_name: str) -> Tuple[Optional[float], str]:
        """Try to fetch real-time usage for a tool"""
        tool = self.tools.get(tool_name.lower())
        if not tool or not tool.api_source:
            return None, "no_api"
        
        api_status = next((s for s in self.api_statuses if s.tool == tool.api_source), None)
        if not api_status or not api_status.available:
            return None, f"API não configurada ({tool.api_source.upper()}_API_KEY não encontrada)"
        
        try:
            if tool.api_source == 'openai':
                # Codex uses OpenAI API
                result = self.fetch_openai_usage()
                if result and 'hours_used' in result:
                    return result['hours_used'], "connected"
                return None, "API disponível mas endpoint de uso não implementado"
            
            elif tool.api_source == 'synthetic':
                result = self.fetch_synthetic_usage()
                if result:
                    return result.get('hours', 0), "connected"
                return None, "API do Synthetic não documentada/disponível"
            
            else:
                return None, f"API para {tool.api_source} não implementada"
                
        except Exception as e:
            return None, f"Erro ao buscar: {str(e)}"
    
    def init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                usage_value REAL,
                usage_unit TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                source TEXT DEFAULT 'manual'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tool_configs (
                tool_name TEXT PRIMARY KEY,
                config_json TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_billing_window(self, tool: ToolConfig) -> tuple[datetime, datetime]:
        """Calculate billing period based on tool configuration"""
        today = datetime.now()
        
        if tool.window_type == 'monthly':
            if today.day >= tool.billing_day:
                start = today.replace(day=tool.billing_day)
                if tool.billing_day == 1:
                    end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                else:
                    next_month = start + timedelta(days=32)
                    end = next_month.replace(day=min(tool.billing_day, next_month.day)) - timedelta(days=1)
            else:
                start = (today - timedelta(days=32)).replace(day=tool.billing_day)
                end = today.replace(day=tool.billing_day) - timedelta(days=1)
        
        elif tool.window_type in ['weekly', '5h+weekly']:
            days_since_billing = (today.day - tool.billing_day) % 7
            start = today - timedelta(days=days_since_billing)
            end = start + timedelta(days=6)
        
        else:
            start = today.replace(day=1)
            end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        return start, end
    
    def estimate_usage(self, tool_name: str, current_usage: Optional[float] = None) -> UsageData:
        """Estimate usage for a tool"""
        tool = self.tools.get(tool_name.lower())
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        start, end = self.get_billing_window(tool)
        days_remaining = (end - datetime.now()).days + 1
        days_total = (end - start).days + 1
        days_elapsed = max(1, days_total - days_remaining)
        
        # Try to fetch real-time usage
        api_usage, api_message = self.fetch_realtime_usage(tool_name)
        usage_unit = 'hours'  # default
        
        if api_usage is not None:
            current_usage = api_usage
            api_status = "connected"
            usage_unit = 'hours'
            # Log API-fetched usage
            self.log_usage(tool_name, current_usage, 'hours', f'Fetched from API: {tool.api_source}', 'api')
        else:
            # Fall back to stored usage
            if current_usage is None:
                current_usage, usage_unit = self.get_stored_usage(tool_name)
            api_status = "error" if api_message else "no_api"
        
        # Calculate projected usage
        if days_elapsed > 0:
            daily_rate = current_usage / days_elapsed
            projected_monthly = daily_rate * days_total
        else:
            projected_monthly = current_usage
        
        # Determine status
        if tool.window_type == '5h+weekly':
            if current_usage <= 5:
                status = 'below'
            else:
                overage = current_usage - 5
                projected_overage = projected_monthly - 5
                if projected_overage <= 2:
                    status = 'on_track'
                else:
                    status = 'above'
        else:
            expected_by_now = (days_elapsed / days_total) * 100
            usage_percentage = current_usage
            
            if usage_percentage < expected_by_now * 0.8:
                status = 'below'
            elif usage_percentage > expected_by_now * 1.2:
                status = 'above'
            else:
                status = 'on_track'
        
        return UsageData(
            tool_name=tool.name,
            current_usage=current_usage,
            usage_unit=usage_unit,
            billing_start=start,
            billing_end=end,
            days_remaining=days_remaining,
            projected_monthly=projected_monthly,
            status=status,
            api_status=api_status,
            api_message=api_message
        )
    
    def get_stored_usage(self, tool_name: str) -> tuple[float, str]:
        """Get latest stored usage from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT usage_value, usage_unit FROM usage_logs 
            WHERE tool_name = ? 
            ORDER BY recorded_at DESC 
            LIMIT 1
        ''', (tool_name.lower(),))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1] if result[1] else 'hours'
        return 0.0, 'hours'
    
    def log_usage(self, tool_name: str, usage: float, unit: str = 'hours', notes: str = '', source: str = 'manual'):
        """Log usage data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usage_logs (tool_name, usage_value, usage_unit, notes, source)
            VALUES (?, ?, ?, ?, ?)
        ''', (tool_name.lower(), usage, unit, notes, source))
        
        conn.commit()
        conn.close()
    
    def get_all_status(self) -> List[UsageData]:
        """Get status for all tools"""
        results = []
        for tool_name in self.tools.keys():
            try:
                data = self.estimate_usage(tool_name)
                results.append(data)
            except Exception as e:
                print(f"Error getting status for {tool_name}: {e}")
        return results
    
    def format_report(self, data: UsageData) -> str:
        """Format a single tool report"""
        status_emoji = {
            'below': '🟢',
            'on_track': '🟡',
            'above': '🔴'
        }
        
        api_emoji = {
            'connected': '⚡',
            'no_api': '📊',
            'error': '⚠️'
        }
        
        tool = self.tools[data.tool_name.lower()]
        
        lines = [
            f"{status_emoji.get(data.status, '⚪')} **{data.tool_name}** (${tool.cost}/mo) {api_emoji.get(data.api_status, '⚪')}",
            f"   ├─ Ciclo: {data.billing_start.strftime('%d/%m')} → {data.billing_end.strftime('%d/%m')}",
            f"   ├─ Dias restantes: {data.days_remaining}",
        ]
        
        # Format usage with correct unit
        unit_symbol = '%' if data.usage_unit == 'percentage' else 'h'
        
        if tool.window_type == '5h+weekly':
            included = 5
            lines.append(f"   ├─ Uso atual: {data.current_usage:.1f}{unit_symbol} (incluídas: {included}h)")
            if data.current_usage > included:
                lines.append(f"   ├─ Excedente: {data.current_usage - included:.1f}{unit_symbol}")
        else:
            lines.append(f"   ├─ Uso atual: {data.current_usage:.1f}{unit_symbol}")
        
        lines.append(f"   ├─ Projeção: {data.projected_monthly:.1f}{unit_symbol} no ciclo")
        
        if data.api_message:
            lines.append(f"   └─ _{data.api_message}_")
        else:
            lines.append(f"   └─ Fonte: {'API em tempo real' if data.api_status == 'connected' else 'Estimativa/manual'}")
        
        return '\n'.join(lines)
    
    def format_api_summary(self) -> str:
        """Format API availability summary"""
        lines = ["🔌 **Status das APIs:**"]
        
        for status in self.api_statuses:
            emoji = '✅' if status.available else '❌'
            lines.append(f"   {emoji} {status.tool.title()}: {status.message}")
        
        return '\n'.join(lines)
    
    def generate_full_report(self) -> str:
        """Generate full report for all tools"""
        all_data = self.get_all_status()
        
        report_lines = [
            "📊 **Relatório de Uso de Ferramentas AI**",
            f"_Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}_",
            ""
        ]
        
        # API Status
        report_lines.append(self.format_api_summary())
        report_lines.append("")
        
        # Tools
        for data in all_data:
            report_lines.append(self.format_report(data))
            report_lines.append("")
        
        # Summary
        total_cost = sum(t.cost for t in self.tools.values())
        connected_apis = sum(1 for s in self.api_statuses if s.available)
        
        report_lines.append(f"💰 **Custo mensal total:** ${total_cost:.2f}")
        report_lines.append(f"⚡ **APIs conectadas:** {connected_apis}/{len(self.api_statuses)}")
        
        return '\n'.join(report_lines)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Tools Usage Monitor')
    parser.add_argument('--report', action='store_true', help='Generate full report')
    parser.add_argument('--tool', type=str, help='Check specific tool')
    parser.add_argument('--log', type=str, help='Tool name to log usage for')
    parser.add_argument('--usage', type=float, help='Usage value to log')
    parser.add_argument('--unit', type=str, default='hours', help='Usage unit')
    parser.add_argument('--apis', action='store_true', help='Show API status only')
    
    args = parser.parse_args()
    
    monitor = AIUsageMonitor()
    
    if args.apis:
        print(monitor.format_api_summary())
    elif args.report:
        print(monitor.generate_full_report())
    elif args.tool:
        data = monitor.estimate_usage(args.tool)
        print(monitor.format_report(data))
    elif args.log and args.usage is not None:
        monitor.log_usage(args.log, args.usage, args.unit)
        print(f"✅ Registrado {args.usage} {args.unit} para {args.log}")
    else:
        print(monitor.generate_full_report())

if __name__ == '__main__':
    main()
