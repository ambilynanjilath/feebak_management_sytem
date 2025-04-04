import frappe

def create_doctype(doctype_data):
    """Creates a Doctype if it doesn't exist."""
    if not frappe.db.exists("DocType", doctype_data["name"]):
        print(f"✅ Creating Doctype: {doctype_data['name']}...")
        doc = frappe.get_doc(doctype_data)
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ {doctype_data['name']} created successfully!")
    else:
        print(f"⚠️ {doctype_data['name']} already exists. Skipping...")

def setup_feebak_customer_doctype():
    """Creates Feebak Customer Doctype with its child tables."""

    if not frappe.db:
        frappe.init(site="feebak")  # Replace with your actual site name
        frappe.connect()

    ### **Step 1: Create Child Tables**
    child_doctypes = [
        {
            "doctype": "DocType",
            "name": "Customer Contacts",
            "module": "Feebak Management System",  # ✅ Corrected module name
            "custom": 1,
            "istable": 1,  # Marking it as a child table
            "fields": [
                {"label": "Name", "fieldname": "contact_name", "fieldtype": "Data", "reqd": 1},
                {"label": "Email", "fieldname": "email", "fieldtype": "Data", "reqd": 1},
                {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "reqd": 1},
                {"label": "Work Phone", "fieldname": "work_phone", "fieldtype": "Data", "reqd": 1},
                {"label": "Personal Phone", "fieldname": "personal_phone", "fieldtype": "Data", "reqd": 1},
            ]
        },
        {
            "doctype": "DocType",
            "name": "Genesys Contacts",
            "module": "Feebak Management System",  # ✅ Corrected module name
            "custom": 1,
            "istable": 1,
            "fields": [
                {"label": "Name", "fieldname": "contact_name", "fieldtype": "Data", "reqd": 1},
                {"label": "Email", "fieldname": "email", "fieldtype": "Data", "reqd": 1},
                {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "reqd": 1},
                {"label": "Work Phone", "fieldname": "work_phone", "fieldtype": "Data", "reqd": 1},
                {"label": "Personal Phone", "fieldname": "personal_phone", "fieldtype": "Data", "reqd": 1},
            ]
        }
    ]

    # Create child tables
    for child in child_doctypes:
        create_doctype(child)

    print("\n⏳ Waiting before creating the Parent Doctype...")
    frappe.db.commit()

    ### **Step 2: Create Parent Doctype (Feebak Customer)**
    parent_doctype = {
        "doctype": "DocType",
        "name": "Feebak Customer",
        "module": "Feebak Management System",  # ✅ Corrected module name
        "custom": 1,
        "fields": [
            {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "reqd": 1},
            {"label": "Country", "fieldname": "country", "fieldtype": "Data", "reqd": 1},
            {"label": "Region", "fieldname": "region", "fieldtype": "Data", "reqd": 1},
            {"label": "Sub Region", "fieldname": "sub_region", "fieldtype": "Data", "reqd": 1},
            {"label": "Customer Partner", "fieldname": "customer_partner", "fieldtype": "Data", "reqd": 1},

            # **Linking child tables correctly**
            {"label": "Customer Contacts", "fieldname": "customer_contacts", "fieldtype": "Table", "options": "Customer Contacts","reqd": 1},
            {"label": "Genesys Contacts", "fieldname": "genesys_contacts", "fieldtype": "Table", "options": "Genesys Contacts","reqd": 1}
        ]
    }

    # Create Parent Doctype
    create_doctype(parent_doctype)

if __name__ == "__main__":
    setup_feebak_customer_doctype()
