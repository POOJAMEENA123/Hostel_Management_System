"""
Add login guards right after the require 'config.inc.php' line in each protected page.
- Student pages: check $_SESSION['roll'], redirect to index.php
- Manager/admin pages: check $_SESSION['username'], redirect to login-hostel_manager.php
"""
import re

STUDENT_GUARD = (
    "\nif (!isset($_SESSION['roll'])) { header('Location: index.php'); exit(); }\n"
)
STUDENT_GUARD_SUBDIR = (
    "\nif (!isset($_SESSION['roll'])) { header('Location: ../index.php'); exit(); }\n"
)
MANAGER_GUARD = (
    "\nif (!isset($_SESSION['username'])) { header('Location: login-hostel_manager.php'); exit(); }\n"
)
MANAGER_GUARD_SUBDIR = (
    "\nif (!isset($_SESSION['username'])) { header('Location: ../login-hostel_manager.php'); exit(); }\n"
)

STUDENT_FILES = [
    "home.php", "services.php", "message_user.php",
    "application_form.php", "contact.php", "profile.php",
]
MANAGER_FILES = [
    "home_manager.php", "contact_manager.php", "message_hostel_manager.php",
    "allocated_rooms.php", "allocate_room.php", "empty_rooms.php", "vacate_rooms.php",
]
ADMIN_FILES = [
    "admin/admin_home.php", "admin/admin_contact.php", "admin/admin_projects.php",
    "admin/admin_services.php", "admin/admin_about.php", "admin/admin_profile.php",
    "admin/students.php", "admin/create_hm.php", "admin/manager_profile.php",
]

# Pattern: the closing ?> of the require block
REQUIRE_END_RE = re.compile(
    r'(<\?php\s.*?require\s+[\'"].*?config\.inc\.php[\'"].*?\?>)',
    re.DOTALL
)

def add_guard(fpath, guard):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if guard already present
    if "isset($_SESSION[" in content and "header('Location:" in content[:500]:
        print(f"  SKIP (guard exists): {fpath}")
        return

    m = REQUIRE_END_RE.search(content)
    if not m:
        print(f"  SKIP (no require found): {fpath}")
        return

    insert_pos = m.end()
    new_content = content[:insert_pos] + guard + content[insert_pos:]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  FIXED: {fpath}")

for f in STUDENT_FILES:
    add_guard(f, STUDENT_GUARD)

for f in MANAGER_FILES:
    add_guard(f, MANAGER_GUARD)

for f in ADMIN_FILES:
    add_guard(f, MANAGER_GUARD_SUBDIR)

print("Done.")
