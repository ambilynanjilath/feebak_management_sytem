

import frappe

def create_feebak_purchase_report():
    """Creates the Feebak Purchase Report with optional filters"""

    report_name = "Feebak Purchase Report"
    report_exists = frappe.db.exists("Report", report_name)
    
    if not report_exists:
        # Create the report document
        report_doc = frappe.get_doc({
            "doctype": "Report",
            "report_name": report_name,
            "ref_doctype": "Feebak Subscription Data",  # The Doctype the report is based on
            "report_type": "Query Report",  # The type of report (Query Report for custom SQL)
            "is_standard": "Yes",
            "module": "Feebak Management System",  # Adjust this based on your module
            "roles": [{"role": "System Manager"}],  # Set the appropriate role permissions
            "filters": [
                {
                    "fieldname": "Status",
                    "label": "Status",
                    "fieldtype": "Select",
                    "options": "\nActive\nInactive\nAmended\nCancelled",  # Default empty option for no filter
                    "reqd": 0  # Optional filter
                },
                {
                    "fieldname": "Billing Term",
                    "label": "Billing Term",
                    "fieldtype": "Select",
                    "options": "\nAnnual M2M\nAnnual Pre-Pay\nM2M",  # Default empty option
                    "reqd": 0
                },
                {
                    "fieldname": "Part Name",
                    "label": "Part Name",
                    "fieldtype": "Select",
                    "options": "\nFeebak 1 Concurrent for Genesys Cloud\nFeebak 1 for Genesys Cloud\nFeebak 1 Named User License\nFeebak 2 Concurrent for Genesys Cloud\nFeebak 2 Concurrent User License\nFeebak 2 Digital Only for Genesys Cloud\nFeebak 2 for Genesys Cloud\nFeebak 2 for Genesys Cloud Concurrent\nFeebak 2 Named User License\nFeebak Agentless Metered for Genesys Cloud\nFeebak Digital Addon Concurrent for Genesys Cloud\nFeebak Digital Addon for Genesys Cloud\nFeebak for Genesys Cloud Hourly Service Rate\nFeebak Named User License",  # Default empty option
                    "reqd": 0
                },
                {
                    "fieldname": "Subscription Start Date",
                    "label": "Select a Date",
                    "fieldtype": "Date",
                    "reqd": 0
                }
            ]
        })
        
        # Insert the report document
        report_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Report '{report_name}' created successfully!")

        # Define the SQL query for fetching data with dynamic filters
        query = """
            SELECT 
                fs.name AS "Subscription ID:Link/Feebak Subscription Data:200",
                fs.subscription_start_date AS "Subscription Start Date:Date:200",
                fs.subscription_end_date AS "Subscription End Date:Date:200",
                fs.customer_name AS "Customer:Link/Customer:200",
                fs.status AS "Status:Data:150",
                fs.billing_term AS "Billing Term:Data:150",
                fs.subscription_id_3rd_party AS "Subscription ID (3rd Party Reference):Data:200",
                fi.part_name AS "Product Details(Part Name):Data:200",
                fi.part_number AS "Product Details(Part Number):Data:200",
                fi.quantity AS "Product Details(Quantity):Data:100",
                fi.selling_price AS "Product Details(Selling Price):Currency:100",
                fs.organisation_id AS "Organisation ID:Data:150"
            FROM
                `tabFeebak Subscription Data` fs
            LEFT JOIN
                `tabFeebak Subscription Items` fi ON fi.parent = fs.name
            WHERE
                fs.docstatus < 2
                AND (%(Status)s = '' OR fs.status = %(Status)s)  # Filter for Status (optional)
                AND (%(Billing Term)s = '' OR fs.billing_term = %(Billing Term)s)  # Filter for Billing Term (optional)
                AND (%(Part Name)s = '' OR fi.part_name = %(Part Name)s)  # Filter for Part Name (optional)
                AND (%(Subscription Start Date)s IS NULL OR %(Subscription Start Date)s BETWEEN fs.subscription_start_date AND fs.subscription_end_date)  # Filter for Subscription Start Date (optional)
            ORDER BY
                fs.subscription_start_date DESC
        """
        
        # Update the report with the query
        report_doc.query = query
        report_doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Query added to the report '{report_name}' successfully!")

    else:
        print("⚠️ Report already exists.")

# Run the function to create the Feebak Purchase Report
create_feebak_purchase_report()