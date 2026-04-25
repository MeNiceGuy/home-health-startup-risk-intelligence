from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from app.services.templates import templates
import json

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def risk_score(value, benchmark, higher_is_bad=True):
    try:
        value = float(value or 0)
        benchmark = float(benchmark or 1)
        ratio = value / benchmark if higher_is_bad else benchmark / value if value else 2
        if ratio <= 1: return 90
        if ratio <= 1.25: return 75
        if ratio <= 1.5: return 60
        return 35
    except:
        return 40

def root_cause_diagnosis(data):
    issues = []

    if data["denial_rate"] > 10:
        issues.append(("Revenue Cycle","High denial rate","Claims are being submitted without validation controls."))

    if data["intake_time"] > 2:
        issues.append(("Operations","Slow intake","No structured intake workflow."))

    if data["missed_visits"] > 5:
        issues.append(("Operations","Missed visits","Scheduling + staffing coordination failure."))

    if data["turnover"] > 30:
        issues.append(("Staffing","High turnover","Retention + onboarding systems are weak."))

    if data["qa_score"] < 90:
        issues.append(("Compliance","QA weakness","No consistent audit or policy enforcement system."))

    return issues

def diagnosis_html(diagnoses):
    html = ""
    for area, issue, cause in diagnoses:
        html += f"<div class='diag'><h3>{area}: {issue}</h3><p>{cause}</p></div>"
    return html

@router.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("operating_intake.html", {
        "request": request,
        "form_sections": "<p>Form loads correctly</p>"
    })

@router.post("/run", response_class=HTMLResponse)
def run(
    request: Request,
    denial_rate: float = Form(0),
    intake_time: float = Form(0),
    missed_visits: float = Form(0),
    turnover: float = Form(0),
    qa_score: float = Form(0)
):
    data = {
        "denial_rate": denial_rate,
        "intake_time": intake_time,
        "missed_visits": missed_visits,
        "turnover": turnover,
        "qa_score": qa_score
    }

    diagnoses = root_cause_diagnosis(data)

    scores = [
        int(risk_score(denial_rate,10)),
        int(risk_score(intake_time,2)),
        int(risk_score(turnover,30)),
        int(risk_score(qa_score,90,False))
    ]

    context = {
        "request": request,
        "total": int(sum(scores)/len(scores)),
        "financial": scores[0],
        "operations": scores[1],
        "staffing": scores[2],
        "compliance": scores[3],
        "lost_revenue": 0,
        "delay_cost": 0,
        "total_impact": 0,
        "root_html": diagnosis_html(diagnoses),
        "labels": json.dumps(["Financial","Operations","Staffing","Compliance"]),
        "scores": json.dumps(scores)
    }

    return templates.TemplateResponse("operating_report.html", context)
