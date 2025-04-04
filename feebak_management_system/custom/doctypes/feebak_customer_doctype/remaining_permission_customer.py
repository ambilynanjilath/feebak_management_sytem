import frappe

def ensure_permission_and_enable_import(doctype_name="Feebak Customer", role_name="System Manager"):
    """Ensure Doctype is importable, then enable import permission for a role."""
    try:
        # Fetch the Doctype
        doc = frappe.get_doc("DocType", doctype_name)

        # ✅ Step 1: Ensure Doctype is marked as importable
        if not doc.allow_import:
            doc.allow_import = 1
            doc.save()
            frappe.db.commit()
            print(f"✅ '{doctype_name}' is now importable.")

        # ✅ Step 2: Check if the role already has permission
        perm = frappe.get_all("DocPerm", filters={"parent": doctype_name, "role": role_name}, fields=["name"])

        if not perm:
            print(f"⚠️ No existing permission found. Creating a new permission for '{role_name}' on '{doctype_name}'.")

            # Append new permission
            doc.append("permissions", {
                "role": role_name,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "import": 1,  # Now we can set this safely
                "export": 1,
                "submit": 1,
                "cancel": 1,
                "print": 1,
                "email": 1
            })

            doc.save()
            frappe.db.commit()
            print(f"✅ New permission created for '{role_name}' on '{doctype_name}'.")

        else:
            # ✅ Step 3: Update existing permission to enable import
            frappe.db.set_value("DocPerm", perm[0]["name"], "import", 1)
            frappe.db.commit()
            print(f"✅ Import permission enabled for '{role_name}' on '{doctype_name}'.")

    except Exception as e:
        print(f"❌ Error: {e}")

# Run with:
# bench execute testing_app.scripts.ensure_permission_and_enable_import --kwargs "{'doctype_name': 'Feebak Subscription Data', 'role_name': 'System Manager'}"

