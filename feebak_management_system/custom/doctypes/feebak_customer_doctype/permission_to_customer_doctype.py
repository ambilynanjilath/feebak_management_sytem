import frappe

def make_doctype_submittable():
    """Make Feebak Subscription Data submittable"""
    doctype_name = "Feebak Customer"

    if not frappe.db.exists("DocType", doctype_name):
        print(f"❌ Doctype '{doctype_name}' does not exist.")
        return

    try:
        doc = frappe.get_doc("DocType", doctype_name)
        doc.is_submittable = 1
        doc.save()
        frappe.db.commit()
        print(f"✅ '{doctype_name}' is now submittable.")

    except Exception as e:
        frappe.log_error(f"❌ Error making doctype submittable: {e}", "Submittable Setup Error")
        print(f"❌ Error: {e}")

make_doctype_submittable()
