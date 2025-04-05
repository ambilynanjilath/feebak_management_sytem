
import frappe

def create_feebak_subscription_doctypes():
    """Creates Feebak Subscription Items (Child) and Feebak Subscription Data (Parent) Doctypes."""
    
    if not frappe.db:
        frappe.init(site="feebak")  # Replace with actual site name
        frappe.connect()

    # Create Child Doctype: Feebak Subscription Items
    if not frappe.db.exists("DocType", "Feebak Subscription Items"):
        print("✅ Creating Feebak Subscription Items...")

        child_doctype = frappe.get_doc({
            "doctype": "DocType",
            "name": "Feebak Subscription Items",
            "module": "Feebak Management System",
            "custom": 1,
            "istable": 1,  # Mark as child table
            "fields": [
                {"label": "Part Number", "fieldname": "part_number", "fieldtype": "Data", "reqd": 1},
                {"label": "Part Name", "fieldname": "part_name", "fieldtype": "Data", "reqd": 1},
                {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Int", "reqd": 1},
                {"label": "Selling Price", "fieldname": "selling_price", "fieldtype": "Currency", "reqd": 1}
            ]
        })
        child_doctype.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Feebak Subscription Items created successfully!")
    else:
        print("⚠️ Feebak Subscription Items already exists. Skipping...")

    # Create Parent Doctype: Feebak Subscription Data
    if not frappe.db.exists("DocType", "Feebak Subscription Data"):
        print("✅ Creating Feebak Subscription Data...")

        parent_doctype = frappe.get_doc({
            "doctype": "DocType",
            "name": "Feebak Subscription Data",
            "module": "Feebak Management System",
            "custom": 1,
            "fields": [
                {"label": "Subscription ID", "fieldname": "naming_series", "fieldtype": "Select", "options": "FCS.######", "reqd": 1},
                {"label": "Subscription Start Date", "fieldname": "subscription_start_date", "fieldtype": "Date", "reqd": 1},
                {"label": "Subscription End Date", "fieldname": "subscription_end_date", "fieldtype": "Date", "reqd": 1},
                {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Link", "options": "Feebak Customer"},
                {"label": "Organisation Id", "fieldname": "organisation_id", "fieldtype": "Data"},
                {"label": "Status", "fieldname": "status", "fieldtype": "Select", "options": "\nActive\nInactive\nAmended\nCancelled", "reqd": 1},
                {"label": "Billing Term", "fieldname": "billing_term", "fieldtype": "Select", "options": "\nAnnual M2M\nM2M\nAnnual Pre-Pay", "reqd": 1},
                {"label": "Subscription ID (3rd Party Reference)", "fieldname": "subscription_id_3rd_party", "fieldtype": "Data"},
                {"label": "Amended From Subscription ID (3rd Party Reference)", "fieldname": "amended_from_3rd_party", "fieldtype": "Data"},
                {"label": "Amended From", "fieldname": "amended_from", "fieldtype": "Link", "options": "Feebak Subscription Data"},
                {"label": "Product Details", "fieldname": "product_details", "fieldtype": "Table", "options": "Feebak Subscription Items", "reqd": 1}
            ]
        })
        parent_doctype.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Feebak Subscription Data created successfully!")
    else:
        print("⚠️ Feebak Subscription Data already exists. Skipping...")



# bench --site feebak execute feebak_management.modules.doctypes.feebak_subscription_doctype.create_feebak_subscription_doctypes