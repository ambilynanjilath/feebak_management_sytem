
import frappe
import calendar
from datetime import datetime, date

def create_subscription_mrr_query_report():
    """Creates a query-based report for subscription MRR calculations with daily breakdown."""
    report_name = "Subscription MRR Query Report"
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
                    "fieldname": "year",
                    "label": "Year",
                    "fieldtype": "Select",  # Changed to Select for string values
                    "options": "2020\n2021\n2022\n2023\n2024\n2025\n2026",  # Available years as strings
                    "reqd": 0  # Required
                },
                {
                    "fieldname": "month",
                    "label": "Month",
                    "fieldtype": "Select",  # Changed to Select for string values
                    "options": "\n01\n02\n03\n04\n05\n06\n07\n08\n09\n10\n11\n12",  # Months with leading zeros
                    "reqd": 0  # Required
                }
            ]
        })
        
        # Insert the report document
        report_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Report '{report_name}' created successfully!")
        
        # Define the SQL query for the report
        # This is a parameterized query that will be filled with the selected year and month
        query = """
        WITH date_range AS (
            SELECT DATE(CONCAT(%(year)s, '-', %(month)s, '-', LPAD(n, 2, '0'))) AS report_date
            FROM (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 
                UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 
                UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 
                UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 
                UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 
                UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 
                UNION ALL SELECT 31) days
            WHERE n <= DAY(LAST_DAY(CONCAT(%(year)s, '-', %(month)s, '-01')))
        ),
        active_subs AS (
            SELECT dr.report_date, fs.name AS subscription_name, fs.subscription_id_3rd_party
            FROM date_range dr
            JOIN `tabFeebak Subscription Data` fs 
            ON fs.subscription_start_date <= dr.report_date 
            AND fs.subscription_end_date >= dr.report_date
            AND fs.status = 'Active' AND fs.billing_term != 'M2M'
        ),
        mrr_calc AS (
            SELECT asub.report_date, SUM(fsi.quantity * fsi.selling_price) AS subscription_mrr
            FROM active_subs asub
            JOIN `tabFeebak Subscription Items` fsi ON fsi.parent = asub.subscription_name
            GROUP BY asub.report_date
        )
        SELECT dr.report_date AS "Date:Date:120",
            ROUND(COALESCE(SUM(mc.subscription_mrr), 2), 2) AS "MRR (Monthly Recurring Revenue in USD):Currency:200"
        FROM date_range dr
        LEFT JOIN mrr_calc mc ON dr.report_date = mc.report_date
        GROUP BY dr.report_date
        ORDER BY dr.report_date;

        """
        
        # Update the report with the query
        report_doc.query = query
        report_doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Query added to the report '{report_name}' successfully!")
    else:
        print("⚠️ Report already exists.")

# Run the function to create the MRR query report
create_subscription_mrr_query_report()


"""
bench --site feebak execute feebak_management.reports.mrr_report_of_month.create_subscription_mrr_query_report
"""