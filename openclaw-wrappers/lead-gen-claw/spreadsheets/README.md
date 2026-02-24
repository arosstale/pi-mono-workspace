# Discord + OpenClaw Money Making - Spreadsheet Templates

---

## 📊 Overview

Complete spreadsheet templates for tracking Discord lead generation and revenue. Import these CSVs into Google Sheets or Excel to start tracking your OpenClaw + Discord money-making system.

---

## 📁 Spreadsheet Files

### 1. leads_template.csv
**Purpose:** Track all leads from Discord

**Columns:**
- Discord ID - Unique Discord user ID
- Username - Discord username
- Email - Lead's email address
- Server - Discord server name
- Channel - Channel where lead was captured
- Captured At - Timestamp of lead capture
- Source - Lead source (discord_bot, manual, referral)
- Status - Lead status (new, contacted, demo_scheduled, closed, lost)
- Follow-up Date - Date for next follow-up
- Last Contacted - Date/time of last contact
- Notes - Additional notes

**Usage:**
1. Import into Google Sheets
2. Add formula for automatic status tracking
3. Filter by status for follow-up lists

---

### 2. sales_template.csv
**Purpose:** Track all sales and revenue

**Columns:**
- Discord ID - Client's Discord ID
- Amount - Sale amount ($)
- Product - Product/service sold
- Closed At - Timestamp of sale
- Status - Payment status (Paid, Pending, Overdue)
- Commission - Commission amount (30% default)
- Client Name - Client company name
- Server ID - Client's Discord server ID
- Payment Method - Payment method used
- Notes - Additional notes

**Usage:**
1. Import into Google Sheets
2. Add formulas for automatic totals
3. Track commission payouts

**Formulas:**
```excel
=SUMIF(D:D, "Paid", B:B)  // Total Revenue
=SUMIF(D:D, "Paid", F:F)  // Total Commission
=COUNTA(D:D) - 1  // Total Sales
=AVERAGE(B:B)  // Average Deal Size
```

---

### 3. revenue_template.csv
**Purpose:** Monthly revenue tracking and forecasting

**Columns:**
- Month - Reporting month
- New Leads - New leads captured
- Demos Booked - Demos scheduled
- Deals Closed - Deals won
- Revenue - Total revenue
- Commission - Total commission paid
- Active Clients - Number of active clients
- New Clients - New clients added
- Churned Clients - Clients that canceled
- LTV - Customer lifetime value
- Avg Deal Size - Average deal size
- Notes - Monthly notes

**Usage:**
1. Import into Google Sheets
2. Create charts for visualization
3. Track growth over time

**Formulas:**
```excel
=SUM(E:E)  // Total Revenue
=SUM(F:F)  // Total Commission
=AVERAGE(H:H)  // Average Active Clients
=I2/I2*H2  // LTV (simplified)
=AVERAGE(B:B)/H2  // Leads Per Client
```

---

### 4. clients_template.csv
**Purpose:** Client relationship management

**Columns:**
- Client Name - Client company name
- Server ID - Client's Discord server ID
- Service - Service subscribed to
- Price - Monthly price
- Plan - Plan tier (Starter, Pro, Enterprise)
- Start Date - Subscription start date
- Status - Client status (Active, At Risk, Churned, Completed)
- Next Renewal - Next billing date
- Payment Method - Payment method
- Contact Email - Client email
- Contact Discord - Client Discord username
- Notes - Additional notes

**Usage:**
1. Import into Google Sheets
2. Use for client management
3. Track renewals and churn

**Formulas:**
```excel
=COUNTIF(G:G, "Active")  // Active Clients
=SUM(D:D)  // Monthly Recurring Revenue (MRR)
=SUMIF(G:G, "Active", D:D)  // Active MRR
=COUNTIF(G:G, "At Risk")  // At Risk Clients
```

---

## 🛠 Google Sheets Setup

### Step 1: Import Templates

1. Open Google Sheets
2. File → Import → Upload
3. Select each CSV file
4. Import to new sheet

### Step 2: Add Formulas

**Leads Sheet:**
```excel
=COUNTA(A:A) - 1  // Total Leads (Row 2)
=COUNTIF(H:H, "new")  // New Leads
=COUNTIF(H:H, "contacted")  // Contacted Leads
=COUNTIF(H:H, "closed")  // Closed Deals
```

**Sales Sheet:**
```excel
=SUMIF(D:D, "Paid", B:B)  // Total Revenue
=SUMIF(D:D, "Pending", B:B)  // Pending Revenue
=AVERAGE(B:B)  // Average Deal Size
```

**Revenue Sheet:**
```excel
=SUM(E:E)  // Total Revenue (all time)
=SUM(F:F)  // Total Commission
=AVERAGE(I:I)  // Average Active Clients
```

**Clients Sheet:**
```excel
=COUNTIF(G:G, "Active")  // Active Clients
=SUMIF(G:G, "Active", D:D)  // Monthly Recurring Revenue
=COUNTIF(G:G, "At Risk")  // At Risk Clients
```

### Step 3: Create Dashboard

Create a new sheet called "Dashboard" with:

```
=== KEY METRICS ===

Total Leads: =Leads!B2
New Leads: =Leads!B3
Closed Deals: =Leads!B5

Total Revenue: =Sales!B2
Pending Revenue: =Sales!B3
Avg Deal Size: =Sales!B4

Active Clients: =Clients!B2
MRR: =Clients!B3
At Risk: =Clients!B4

=== CONVERSION RATES ===

Demo Rate: =Revenue!C2/Revenue!B2*100
Close Rate: =Revenue!D2/Revenue!B2*100
Lead to Deal: =Leads!B5/Leads!B2*100
```

### Step 4: Create Charts

1. **Revenue Chart**
   - Select Month and Revenue columns
   - Insert → Chart → Line chart
   - Title: "Monthly Revenue"

2. **Lead Funnel**
   - Select lead status counts
   - Insert → Chart → Bar chart
   - Title: "Lead Conversion Funnel"

3. **Client Growth**
   - Select Month and Active Clients
   - Insert → Chart → Line chart
   - Title: "Client Growth Over Time"

---

## 🤖 Discord Bot Integration

### Connect Bot to Sheets

Use the Python code in `DISCORD_OPENCLAW_MONEY.md`:

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json',
    ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
)
client = gspread.authorize(creds)
sheet = client.open('Discord Revenue Tracker')

# Add lead
@bot.command(name='lead')
async def capture_lead(ctx, *, email: str):
    leads_sheet = sheet.worksheet('Leads')
    row = [
        str(ctx.author.id),
        ctx.author.name,
        email,
        ctx.guild.name,
        ctx.channel.name,
        datetime.now().isoformat(),
        'discord_bot',
        'new',
        '',
        ''
    ]
    leads_sheet.append_row(row)
    await ctx.send(f"✅ Lead added to spreadsheet!")
```

---

## 📊 Automation with OpenClaw

### OpenClaw Workflow

Use the workflow in `DISCORD_OPENCLAW_MONEY.md` to automate:

1. **Lead Capture:**
   - Discord command triggers workflow
   - Lead added to spreadsheet automatically
   - Follow-up email sent automatically

2. **Revenue Tracking:**
   - Daily revenue report generated
   - Dashboard updated automatically
   - Commission calculated automatically

3. **Client Management:**
   - Renewal reminders sent automatically
   - At-risk clients flagged
   - Churn analysis automated

---

## 📈 Key Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| **Total Leads** | COUNTA(Leads!A:A) - 1 | 200+ / month |
| **New Leads** | COUNTIF(Leads!H:H, "new") | 50+ / month |
| **Closed Deals** | COUNTIF(Leads!H:H, "closed") | 12+ / month |
| **Total Revenue** | SUMIF(Sales!D:D, "Paid", B:B) | $6,000+ / month |
| **Avg Deal Size** | AVERAGE(Sales!B:B) | $500+ |
| **Active Clients** | COUNTIF(Clients!G:G, "Active") | 20+ |
| **MRR** | SUMIF(Clients!G:G, "Active", D:D) | $10,000+ |
| **Demo Rate** | Demos / Leads × 100 | 20%+ |
| **Close Rate** | Deals / Leads × 100 | 15%+ |
| **LTV** | Revenue × 12 / Active Clients | $5,000+ |

---

## 🚀 Quick Start

### Day 1: Setup

1. **Import all CSVs to Google Sheets**
2. **Add formulas to each sheet**
3. **Create dashboard**
4. **Set up Discord bot**
5. **Test lead capture**

### Day 7: First Week

1. **Review metrics**
2. **Identify bottlenecks**
3. **Optimize conversion**
4. **Scale what works**

### Day 30: First Month

1. **Review monthly revenue**
2. **Calculate ROI**
3. **Plan next month's goals**
4. **Scale to 10+ clients**

---

## 💡 Tips

1. **Daily Updates:** Update leads and sales daily
2. **Weekly Reviews:** Review metrics every Friday
3. **Monthly Analysis:** Deep dive at month-end
4. **Automate:** Use OpenClaw workflows for automation
5. **Forecast:** Use historical data to predict future revenue

---

## 📞 Support

- **Full Guide:** `DISCORD_OPENCLAW_MONEY.md`
- **Discord Bot Code:** `discord_money_bot.py`
- **Google Sheets API:** https://developers.google.com/sheets/api
- **OpenClaw Docs:** https://docs.openclaw.ai

---

**Start tracking your Discord revenue today!** 📊💰

---

*Created: 2026-02-24*
