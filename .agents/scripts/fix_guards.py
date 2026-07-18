"""
Fix login guards that were placed outside the PHP block.
Move them inside: <?php require...; GUARD ?> 
Also add require+guard to admin_services.php and admin_about.php which had no require.
"""
import re

def fix_file(fpath, guard_code):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: <?php\n require ...\n?>\nGUARD_LINE
    # Replace with: <?php\n require ...\nGUARD_LINE\n?>
    pattern = re.compile(
        r'(<\?php\s+require\s+[\'"].*?config\.inc\.php[\'"];?\s*)\?>\s*\n'
        r'if \(!isset\(\$_SESSION\[[^\]]+\]\)\) \{ header\([^)]+\); exit\(\); \}\s*\n',
        re.DOTALL
    )
    if pattern.search(content):
        new_content = pattern.sub(
            lambda m: m.group(1) + guard_code + '\n?>\n',
            content
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  FIXED: {fpath}")
    else:
        print(f"  SKIP (pattern not found): {fpath}")

STUDENT_GUARD  = "if (!isset($_SESSION['roll'])) { header('Location: index.php'); exit(); }"
STUDENT_GUARD2 = "if (!isset($_SESSION['roll'])) { header('Location: ../index.php'); exit(); }"
MANAGER_GUARD  = "if (!isset($_SESSION['username'])) { header('Location: login-hostel_manager.php'); exit(); }"
MANAGER_GUARD2 = "if (!isset($_SESSION['username'])) { header('Location: ../login-hostel_manager.php'); exit(); }"

for f in ["home.php", "services.php", "message_user.php", "application_form.php", "contact.php", "profile.php"]:
    fix_file(f, STUDENT_GUARD)

for f in ["home_manager.php", "contact_manager.php", "message_hostel_manager.php",
          "allocated_rooms.php", "allocate_room.php", "empty_rooms.php", "vacate_rooms.php"]:
    fix_file(f, MANAGER_GUARD)

for f in ["admin/admin_home.php", "admin/admin_contact.php", "admin/admin_projects.php",
          "admin/admin_profile.php", "admin/students.php", "admin/create_hm.php", "admin/manager_profile.php"]:
    fix_file(f, MANAGER_GUARD2)

# admin_services.php and admin_about.php — no require block yet, add one at the top
for fpath in ["admin/admin_services.php", "admin/admin_about.php"]:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'config.inc.php' not in content:
        php_block = "<?php\nrequire '../includes/config.inc.php';\n" + MANAGER_GUARD2 + "\n?>\n"
        content = php_block + content
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ADDED require+guard: {fpath}")
    else:
        print(f"  SKIP (already has require): {fpath}")

print("Done.")
