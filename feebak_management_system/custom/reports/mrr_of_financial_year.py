import frappe
import calendar
from datetime import datetime, date

def create_monthly_mrr_financial_year_report():
    """Creates a query-based report for monthly MRR calculations by financial year."""
    report_name = "Monthly MRR Financial Year"
    report_exists = frappe.db.exists("Report", report_name)
    
    if not report_exists:
        # Create the report document
        report_doc = frappe.get_doc({
            "doctype": "Report",
            "report_name": report_name,
            "ref_doctype": "Feebak Subscription Data",  # The Doctype the report is based on
            "report_type": "Query Report",  # Using Query Report type
            "is_standard": "Yes",
            "module": "Feebak Management System",  # Adjust based on your module
            "roles": [{"role": "System Manager"}],  # Set the appropriate role permissions
            "filters": [
                {
                    "fieldname": "financial_year",
                    "label": "Financial Year",
                    "fieldtype": "Select", 
                    "options": "2020-2021\n2021-2022\n2022-2023\n2023-2024\n2024-2025\n2025-2026\n2026-2027\n2027-2028",
                    "reqd": 1  # Required
                }
            ]
        })
        
        # Insert the report document
        report_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Report '{report_name}' created successfully!")
        
        # Define the SQL query for the report with proper placeholders
        query = """
        WITH financial_year_params AS (
            SELECT 
                STR_TO_DATE(CONCAT(SUBSTRING_INDEX(%(financial_year)s, '-', 1), '-04-01'), '%%Y-%%m-%%d') AS fy_start_date,
                STR_TO_DATE(CONCAT(SUBSTRING_INDEX(%(financial_year)s, '-', -1), '-03-31'), '%%Y-%%m-%%d') AS fy_end_date
        ),
        date_range AS (
            SELECT
                DATE_FORMAT(DATE_ADD(fyp.fy_start_date, INTERVAL m.month MONTH), '%%Y-%%m-01') AS first_day_of_month,
                LAST_DAY(DATE_ADD(fyp.fy_start_date, INTERVAL m.month MONTH)) AS last_day_of_month,
                DATE_FORMAT(DATE_ADD(fyp.fy_start_date, INTERVAL m.month MONTH), '%%Y-%%m') AS month_year,
                MONTHNAME(DATE_ADD(fyp.fy_start_date, INTERVAL m.month MONTH)) AS month_name
            FROM financial_year_params fyp
            CROSS JOIN (
                SELECT 0 AS month UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
                UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 
                UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11
            ) AS m
        ),
        daily_mrr_all_months AS (
            SELECT
                dr.month_year,
                dr.month_name,
                DATE_ADD(dr.first_day_of_month, INTERVAL a.day DAY) AS report_date
            FROM
                date_range dr
            CROSS JOIN (
                SELECT 0 AS day UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
                UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 
                UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19
                UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 
                UNION ALL SELECT 25 UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 
                UNION ALL SELECT 30 UNION ALL SELECT 31
            ) AS a
            WHERE
                DATE_ADD(dr.first_day_of_month, INTERVAL a.day DAY) <= dr.last_day_of_month
        ),
        mrr_calc AS (
            SELECT
                dm.month_year,
                dm.month_name,
                dm.report_date,
                SUM(fsi.quantity * fsi.selling_price) AS daily_mrr
            FROM
                daily_mrr_all_months dm
            JOIN `tabFeebak Subscription Data` fs 
                ON fs.subscription_start_date <= dm.report_date
                AND fs.subscription_end_date >= dm.report_date
                AND fs.status = 'Active' 
                AND fs.billing_term != 'M2M'
            JOIN `tabFeebak Subscription Items` fsi 
                ON fs.name = fsi.parent
            GROUP BY
                dm.month_year, dm.month_name, dm.report_date
        ),
        monthly_avg AS (
            SELECT
                dm.month_year,
                dm.month_name,
                ROUND(AVG(COALESCE(mc.daily_mrr, 0)), 2) AS avg_monthly_mrr
            FROM
                daily_mrr_all_months dm
            LEFT JOIN mrr_calc mc 
                ON dm.report_date = mc.report_date
            GROUP BY
                dm.month_year, dm.month_name
        )
        
        SELECT
            ma.month_name AS "Month:Data:150",
            ma.avg_monthly_mrr AS "MRR (Monthly Recurring Revenue in USD):Currency:200"
        FROM
            monthly_avg ma
        ORDER BY
            ma.month_year;
        """
        
        # Update the report with the query
        report_doc.query = query
        report_doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Query added to the report '{report_name}' successfully!")
    else:
        print("⚠️ Report already exists.")

# Function to run the report with filters properly applied
def run_report(filters):
    """Executes the Monthly MRR Financial Year Report 1 with applied filters."""
    try:
        # Ensure filters are in dictionary format
        if isinstance(filters, str):
            filters = frappe.parse_json(filters)

        # Ensure financial_year is present in filters
        financial_year = filters.get("financial_year")
        if not financial_year:
            frappe.throw("Financial Year filter is required!")

        # Execute the SQL query with proper filter substitution
        query = frappe.db.sql(
            """
            SELECT 
                ma.month_name AS month, 
                ma.avg_monthly_mrr AS mrr
            FROM monthly_avg ma
            WHERE ma.month_year BETWEEN 
                STR_TO_DATE(CONCAT(SUBSTRING_INDEX(%(financial_year)s, '-', 1), '-04-01'), '%%Y-%%m-%%d') 
                AND STR_TO_DATE(CONCAT(SUBSTRING_INDEX(%(financial_year)s, '-', -1), '-03-31'), '%%Y-%%m-%%d')
            ORDER BY ma.month_year;
            """,
            {"financial_year": financial_year},
            as_dict=True
        )
        return query
    except Exception as e:
        frappe.log_error(f"Error running Monthly MRR report: {str(e)}")
        return {"error": str(e)}

# Run the function to create the Monthly MRR Financial Year report
create_monthly_mrr_financial_year_report()
