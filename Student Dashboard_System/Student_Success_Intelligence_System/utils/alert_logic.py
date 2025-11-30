"""
Alert Logic & Risk Calculation System - Fast & Optimized
"""

import pandas as pd
from typing import Dict, List, Tuple


class AlertSystem:
    """Fast alert generation and risk scoring system"""
    
    GPA_CRITICAL = 2.0
    GPA_WARNING = 2.5
    ATTENDANCE_WARNING = 80
    UNPAID_FEES_CRITICAL = 500
    CREDITS_FRESHMAN = 30
    COUNSELING_VISITS_MIN = 1
    WARNINGS_CRITICAL = 2
    ENGAGEMENT_LOW = 50
    
    @staticmethod
    def calculate_gpa_alert(gpa: float) -> Tuple[str, str, str]:
        try:
            gpa_val = float(gpa)
        except (ValueError, TypeError):
            return 'none', '', '#999'
        if gpa_val < 2.0:
            return 'critical', f'Critical GPA: {gpa_val}', '#d62728'
        elif gpa_val < 2.5:
            return 'warning', f'Warning GPA: {gpa_val}', '#ff7f0e'
        return 'none', '', '#2ca02c'
    
    @staticmethod
    def calculate_financial_alert(unpaid_fees: float, aid_status: str = 'Active') -> Tuple[str, str, str]:
        try:
            fees = float(unpaid_fees) if unpaid_fees else 0
        except (ValueError, TypeError):
            fees = 0
        if fees > 500 or aid_status.lower() == 'delayed':
            return 'critical', f'Financial risk: ${fees}', '#d62728'
        elif fees > 100:
            return 'warning', f'Outstanding: ${fees}', '#ff7f0e'
        return 'none', '', '#2ca02c'
    
    @staticmethod
    def calculate_attendance_alert(attendance_pct: float) -> Tuple[str, str, str]:
        try:
            att = float(attendance_pct)
        except (ValueError, TypeError):
            return 'none', '', '#999'
        if att < 80:
            return 'warning', f'Attendance: {att}%', '#ff7f0e'
        return 'none', '', '#2ca02c'
    
    @staticmethod
    def calculate_engagement_alert(engagement_score: float, counseling_visits: int = 0) -> Tuple[str, str, str]:
        try:
            eng = float(engagement_score)
        except (ValueError, TypeError):
            eng = 50
        if counseling_visits < 1:
            return 'warning', 'No counseling visits', '#ff7f0e'
        elif eng < 50:
            return 'warning', f'Low engagement: {eng}', '#ff7f0e'
        return 'none', '', '#2ca02c'
    
    @staticmethod
    def calculate_credits_alert(credits: float, is_freshman: bool = False) -> Tuple[str, str, str]:
        try:
            cred = float(credits)
        except (ValueError, TypeError):
            cred = 0
        if cred < 30 and is_freshman:
            return 'critical', f'Dropout risk: {cred} credits', '#d62728'
        elif cred < 30:
            return 'warning', f'Low credits: {cred}', '#ff7f0e'
        return 'none', '', '#2ca02c'
    
    @staticmethod
    def calculate_warnings_alert(warnings_count: int) -> Tuple[str, str, str]:
        if warnings_count >= 2:
            return 'critical', f'{warnings_count} warnings', '#d62728'
        elif warnings_count > 0:
            return 'warning', f'{warnings_count} warning(s)', '#ff7f0e'
        return 'none', '', '#2ca02c'
    
    @staticmethod
    def calculate_comprehensive_risk_score(student_data: Dict) -> Dict:
        """Fast risk score calculation"""
        gpa = float(student_data.get('gpa', 3.0)) if student_data.get('gpa') else 3.0
        credits = float(student_data.get('credits', 60)) if student_data.get('credits') else 60
        warnings = int(student_data.get('warnings', 0)) if student_data.get('warnings') else 0
        unpaid = float(student_data.get('unpaid_fees', 0)) if student_data.get('unpaid_fees') else 0
        aid_status = student_data.get('financial_aid_status', 'Active')
        attendance = float(student_data.get('attendance', 90)) if student_data.get('attendance') else 90
        counseling = int(student_data.get('counseling_visits', 0)) if student_data.get('counseling_visits') else 0
        engagement = float(student_data.get('engagement_score', 70)) if student_data.get('engagement_score') else 70
        
        gpa_score = min(100, max(0, (4.0 - gpa) / 4.0 * 100))
        credits_score = min(100, max(0, (120 - credits) / 120 * 100))
        warnings_score = min(100, warnings * 50)
        academic_score = (gpa_score * 0.5 + credits_score * 0.3 + warnings_score * 0.2)
        
        fees_score = min(100, (unpaid / 500 * 100)) if unpaid and 500 > 0 else 0
        aid_score = 50 if aid_status.lower() == 'delayed' else 0
        financial_score = (fees_score * 0.6 + aid_score * 0.4)
        
        attendance_score = min(100, max(0, (100 - attendance) / 100 * 100))
        counseling_score = 50 if counseling < 1 else 0
        engagement_score_component = min(100, max(0, (100 - engagement) / 100 * 100))
        engagement_score_calc = (attendance_score * 0.4 + counseling_score * 0.3 + engagement_score_component * 0.3)
        
        overall_score = (academic_score * 0.4 + financial_score * 0.3 + engagement_score_calc * 0.3)
        
        if overall_score >= 70:
            risk_level = 'High'
        elif overall_score >= 40:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        alerts = []
        gpa_sev, gpa_msg, _ = AlertSystem.calculate_gpa_alert(gpa)
        if gpa_sev != 'none':
            alerts.append({'type': 'GPA', 'severity': gpa_sev, 'message': gpa_msg})
        
        fin_sev, fin_msg, _ = AlertSystem.calculate_financial_alert(unpaid, aid_status)
        if fin_sev != 'none':
            alerts.append({'type': 'Financial', 'severity': fin_sev, 'message': fin_msg})
        
        att_sev, att_msg, _ = AlertSystem.calculate_attendance_alert(attendance)
        if att_sev != 'none':
            alerts.append({'type': 'Attendance', 'severity': att_sev, 'message': att_msg})
        
        eng_sev, eng_msg, _ = AlertSystem.calculate_engagement_alert(engagement, counseling)
        if eng_sev != 'none':
            alerts.append({'type': 'Engagement', 'severity': eng_sev, 'message': eng_msg})
        
        cred_sev, cred_msg, _ = AlertSystem.calculate_credits_alert(credits, is_freshman=(credits < 30))
        if cred_sev != 'none':
            alerts.append({'type': 'Credits', 'severity': cred_sev, 'message': cred_msg})
        
        warn_sev, warn_msg, _ = AlertSystem.calculate_warnings_alert(warnings)
        if warn_sev != 'none':
            alerts.append({'type': 'Warnings', 'severity': warn_sev, 'message': warn_msg})
        
        return {
            'overall_score': round(overall_score, 2),
            'risk_level': risk_level,
            'academic_score': round(academic_score, 2),
            'financial_score': round(financial_score, 2),
            'engagement_score': round(engagement_score_calc, 2),
            'alerts': alerts,
            'critical_alert_count': len([a for a in alerts if a['severity'] == 'critical']),
            'warning_alert_count': len([a for a in alerts if a['severity'] == 'warning'])
        }
    
    @staticmethod
    def get_students_with_alerts(df: pd.DataFrame) -> Tuple[List[Dict], int]:
        """Get students with alerts - optimized for speed"""
        if df.empty:
            return [], 0
        
        students_with_alerts = []
        total_alerts = 0
        
        alert_store = None
        try:
            from . import alert_store as _alert_store
            alert_store = _alert_store
            alert_store.init_db()
        except Exception:
            pass
        
        for _, row in df.iterrows():
            student_data = row.to_dict()
            risk_assessment = AlertSystem.calculate_comprehensive_risk_score(student_data)
            
            if risk_assessment['alerts']:
                sid = row.get('student_id')
                students_with_alerts.append({
                    'student_id': sid,
                    'name': row.get('name'),
                    'advisor': row.get('advisor'),
                    'alerts': risk_assessment['alerts'],
                    'risk_level': risk_assessment['risk_level'],
                    'overall_score': risk_assessment['overall_score']
                })
                total_alerts += len(risk_assessment['alerts'])
                
                if alert_store:
                    for a in risk_assessment['alerts']:
                        try:
                            alert_store.log_alert(
                                student_id=sid,
                                alert_type=a.get('type'),
                                severity=a.get('severity'),
                                message=a.get('message'),
                                source='rule_engine'
                            )
                        except Exception:
                            pass
        
        students_with_alerts.sort(
            key=lambda x: (
                -len([a for a in x['alerts'] if a['severity'] == 'critical']),
                -len(x['alerts'])
            )
        )
        
        return students_with_alerts, total_alerts
    
    @staticmethod
    def get_alert_color(severity: str) -> str:
        """Get color for alert severity"""
        return {
            'critical': '#d62728',
            'warning': '#ff7f0e',
            'info': '#0099ff',
            'none': '#2ca02c'
        }.get(severity, '#999')
