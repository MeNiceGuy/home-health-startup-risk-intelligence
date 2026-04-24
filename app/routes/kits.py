from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/kits", tags=["Kits"])

KITS = [
    ("full-kit", "Full Home Health Startup Kit", 1099,
     "Complete system covering all startup, licensing, compliance, staffing, and operational requirements.",
     ["All kits included", "Full startup roadmap", "Compliance system", "Licensing guidance", "Inspection preparation"]),

    ("business-entity", "Form Business Entity Kit", 59,
     "A structured guide to establishing your legal business entity.",
     ["Entity type comparison", "Registration steps", "Documents", "Mistakes", "Compliance"]),

    ("ein", "EIN Setup Kit", 39,
     "A walkthrough of obtaining an EIN.",
     ["Application steps", "IRS requirements", "Banking setup", "Tax basics"]),

    ("virginia-scc", "Virginia SCC Registration Kit", 59,
     "Virginia SCC registration framework.",
     ["Filing steps", "Documents", "Fees", "Timeline"]),

    ("policies", "Policies & Procedures Template Pack", 349,
     "Policy framework for compliance.",
     ["Policy templates", "Patient procedures", "Compliance docs"]),

    ("leadership", "Administrator & Clinical Leadership Kit", 179,
     "Leadership structure guide.",
     ["Admin requirements", "RN requirements", "Hiring checklist"]),

    ("license", "Virginia Home Care License Application Kit", 449,
     "Licensing roadmap.",
     ["Checklist", "Application steps", "Documents"]),

    ("inspection", "Inspection Readiness Kit", 279,
     "Inspection preparation system.",
     ["Checklist", "Survey expectations", "Docs"]),

    ("hipaa", "HIPAA Records Process Kit", 229,
     "HIPAA compliance system.",
     ["HIPAA checklist", "Security setup", "Records"]),

    ("onboarding", "Staff Onboarding Kit", 229,
     "Hiring and onboarding system.",
     ["Hiring steps", "Background checks", "Onboarding"])
]

@router.get("/", response_class=HTMLResponse)
def kits_page():
    cards = ""
    for slug, title, price, desc, _ in KITS:
        cards += f"""
        <div style="background:white;padding:20px;margin-bottom:15px;">
            <h2>{title}</h2>
            <p>{desc}</p>
            <h3>${price}</h3>
            <a href="/kits/{slug}">View Kit</a>
        </div>
        """

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Startup Completion Kits</h1>
        {cards}
    </body>
    </html>
    """

@router.get("/{slug}", response_class=HTMLResponse)
def kit_detail(slug: str):
    for kit_slug, title, price, desc, includes in KITS:
        if slug == kit_slug:
            items = "".join([f"<li>{i}</li>" for i in includes])

            return f"""
            <html>
            <body style="font-family:Arial;padding:40px;">
                <h1>{title}</h1>
                <p>{desc}</p>

                <h2>What is Included</h2>
                <ul>{items}</ul>

                <h2>${price}</h2>

                <a href="/checkout/{slug}">Purchase</a><br><br>
                <a href="/kits/">Back</a>
            </body>
            </html>
            """

    return "<h1>Not Found</h1>"
