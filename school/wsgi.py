"""
WSGI config for school project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")

# Auto-run migrations on startup (needed for Vercel's ephemeral /tmp)
if os.getenv("VERCEL"):
    import django
    django.setup()
    from django.core.management import call_command
    call_command("migrate", verbosity=0, interactive=False)
    # Create demo data if no users exist
    from django.contrib.auth import get_user_model
    if get_user_model().objects.count() == 0:
        call_command("load_demo_data", verbosity=0)

application = get_wsgi_application()
