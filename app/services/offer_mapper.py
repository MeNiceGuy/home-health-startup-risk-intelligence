def attach_offer_buttons(report_text):
    offers = []

    text = report_text.lower()

    if "revenue" in text or "billing" in text or "denial" in text:
        offers.append(("Revenue Cycle Kit", "/template-checkout/revenue?tenant={tenant}&client={client}", "$199"))

    if "staffing" in text or "credential" in text or "training" in text:
        offers.append(("Staffing & Credentialing Kit", "/template-checkout/hiring?tenant={tenant}&client={client}", "$179"))

    if "compliance" in text or "hipaa" in text or "audit readiness" in text:
        offers.append(("Compliance Policy Pack", "/template-checkout/compliance?tenant={tenant}&client={client}", "$199"))

    if "operations" in text or "sop" in text or "intake" in text:
        offers.append(("Operations SOP Kit", "/template-checkout/operations?tenant={tenant}&client={client}", "$199"))

    if len(offers) >= 3:
        offers.insert(0, ("Full Stabilization Bundle", "/bundle/startup-stabilization?tenant={tenant}&client={client}", "$799"))

    if not offers:
        return ""

    html = """
    <div style='margin-top:25px;padding:22px;background:#f0fdf4;border:2px solid #16a34a;border-radius:16px;'>
    <h2>Recommended Paid Solutions</h2>
    <p>Based on this AI file review, these are the highest-value fixes to offer this client.</p>
    """

    for name, link, price in offers:
        html += f"""
        <div style='margin:12px 0;padding:15px;background:white;border-radius:12px;'>
            <strong>{name}</strong><br>
            <span>Recommended Investment: {price}</span><br><br>
            <a href='{link}' style='background:#2563eb;color:white;padding:10px 14px;border-radius:8px;text-decoration:none;font-weight:bold;'>
            Sell This Solution
            </a>
        </div>
        """

    html += "</div>"
    return html



