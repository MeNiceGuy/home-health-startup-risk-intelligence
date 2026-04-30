from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.kit_catalog import KIT_PRICES

router = APIRouter()

REASONS = {
    "revenue": "Recommended because the audit found denial-rate or A/R cash-flow leakage.",
    "operations": "Recommended because the audit found intake delays or missed-visit operational risk.",
    "hiring": "Recommended because the audit found staffing turnover or coverage instability.",
    "compliance": "Recommended because the audit found compliance findings or weak internal controls.",
    "full-optimization": "Recommended because the audit shows severe total risk or high estimated monthly impact."
}

@router.get("/kits", response_class=HTMLResponse)
def kits_storefront(request: Request):
    recommended_raw = request.query_params.get("recommended", "")
    recommended = [x.strip() for x in recommended_raw.split(",") if x.strip()]

    cards = ""

    for slug, kit in KIT_PRICES.items():
        price = "${:,.0f}".format(kit["amount"] / 100)
        is_recommended = slug in recommended
        star = "⭐ " if is_recommended else ""
        tag = "<div class='tag'>Recommended for this audit</div>" if is_recommended else ""
        reason = f"<div class='reason'>{REASONS.get(slug, 'Recommended based on audit findings.')}</div>" if is_recommended else ""

        cards += f"""
        <div class="card {'recommended-card' if is_recommended else ''}">
            {tag}
            {reason}
            <h2>{star}{kit["name"]}</h2>
            <p>Fix operational gaps, reduce preventable leakage, and strengthen agency execution.</p>
            <div class="price">{price}</div>
            <a class="btn" href="/cart/add/{slug}">Add to Bundle</a>
        </div>
        """

    bundle_button = ""
    if recommended:
        bundle_button = f"""
        <div class="bundle-box">
            <h2>⭐ Recommended Bundle for This Audit</h2>
            <p>These recommendations are matched to your audit findings. Start with the highest-priority fixes instead of guessing.</p>
            <a class="bundle-btn" href="/cart/add-bundle?kits={",".join(recommended)}">
                Add Recommended Bundle to Cart
            </a>
        </div>
        """

    return f"""
    <html>
    <head>
        <title>Revenue Optimization Kits</title>
        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                background:#f8fafc;
                padding:40px;
                color:#111827;
            }}

            .hero {{
                background:linear-gradient(135deg,#991b1b,#dc2626);
                color:white;
                padding:38px;
                border-radius:22px;
                margin-bottom:25px;
                box-shadow:0 12px 32px rgba(0,0,0,.12);
            }}

            .hero h1 {{
                margin:0;
                font-size:38px;
            }}

            .hero p {{
                font-size:18px;
                line-height:1.55;
                max-width:900px;
            }}

            .urgency {{
                background:#fee2e2;
                border-left:7px solid #dc2626;
                padding:18px;
                border-radius:14px;
                margin-bottom:24px;
            }}

            .roi {{
                background:white;
                padding:22px;
                border-radius:18px;
                box-shadow:0 8px 24px rgba(0,0,0,.06);
                margin-bottom:24px;
            }}

            .grid {{
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:20px;
            }}

            .card {{
                background:white;
                padding:25px;
                border-radius:16px;
                box-shadow:0 10px 25px rgba(0,0,0,.08);
                border:1px solid #e5e7eb;
            }}

            .recommended-card {{
                border:3px solid #f59e0b;
                box-shadow:0 12px 30px rgba(245,158,11,.25);
            }}

            .tag {{
                display:inline-block;
                background:#fef3c7;
                color:#92400e;
                padding:7px 12px;
                border-radius:999px;
                font-size:13px;
                font-weight:bold;
                margin-bottom:12px;
            }}

            .reason {{
                background:#fff7ed;
                border-left:5px solid #f59e0b;
                padding:12px;
                border-radius:10px;
                margin-bottom:14px;
                color:#374151;
                line-height:1.45;
            }}

            .price {{
                font-size:30px;
                color:#dc2626;
                font-weight:bold;
                margin:16px 0;
            }}

            .btn, .bundle-btn {{
                display:block;
                background:#dc2626;
                color:white;
                padding:14px;
                text-align:center;
                border-radius:12px;
                text-decoration:none;
                font-weight:bold;
            }}

            .bundle-box {{
                background:#fff7ed;
                border:2px solid #f59e0b;
                padding:24px;
                border-radius:18px;
                margin:25px 0;
                box-shadow:0 8px 24px rgba(245,158,11,.12);
            }}

            @media(max-width:900px) {{
                .grid {{
                    grid-template-columns:1fr;
                }}
            }}
        </style>
    </head>

    <body>
        <div class="hero">
            <h1>Revenue Optimization Kits</h1>
            <p>Turn audit findings into corrective action. These kits are designed to help home health agencies reduce operational leakage, strengthen controls, and improve execution.</p>
        </div>

        <div class="urgency">
            <strong>Cost of Delay:</strong> Every month unresolved denial, intake, staffing, and compliance gaps remain active, the agency risks continued revenue leakage and operational drag.
        </div>

        <div class="roi">
            <h2>ROI Logic</h2>
            <p>If one kit helps reduce even a small portion of preventable leakage, the cost can be recovered quickly. Use the recommended kits first because they are tied to the highest-risk audit findings.</p>
        </div>

        {bundle_button}

        <div class="grid">
            {cards}
        </div>
    </body>
    </html>
    """


