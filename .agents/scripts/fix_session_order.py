"""
For each PHP file: find the <?php ... require ...config.inc.php... ?> block
and move it to the very first line, before any HTML comment or other output.
"""
import re, os

FILES = [
    "admin/admin_profile.php", "admin/create_hm.php", "admin/manager_profile.php",
    "admin/admin_projects.php", "admin/admin_home.php", "admin/admin_contact.php",
    "admin/students.php", "profile.php", "vacate_rooms.php", "home.php",
    "home_manager.php", "services.php", "message_user.php", "message_hostel_manager.php",
    "allocated_rooms.php", "allocate_room.php", "application_form.php",
    "empty_rooms.php", "contact.php", "contact_manager.php",
]

# Matches a <?php ... ?> block that contains a require of config.inc.php
PHP_REQUIRE_RE = re.compile(
    r'(<\?php\s.*?require\s+[\'"].*?config\.inc\.php[\'"].*?\?>)',
    re.DOTALL
)

for fpath in FILES:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    m = PHP_REQUIRE_RE.search(content)
    if not m:
        print(f"  SKIP (no match): {fpath}")
        continue

    php_block = m.group(1)
    # If it's already the very first thing, nothing to do
    if content.startswith(php_block):
        print(f"  OK (already first): {fpath}")
        continue

    # Remove the block from its current position (plus any surrounding blank lines)
    new_content = content[:m.start()].rstrip('\n') + '\n' + content[m.end():].lstrip('\n')
    # Prepend the block at the top
    new_content = php_block + '\n' + new_content.lstrip('\n')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  FIXED: {fpath}")

print("Done.")
