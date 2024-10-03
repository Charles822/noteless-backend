from django.contrib import admin
from .models import AgentRole, AgentResponse

admin.site.register(AgentRole)
admin.site.register(AgentResponse)

# Set the site header
admin.site.site_header = "HTFBI Admin Panel"

# Set the site title (appears in the browser's title bar)
admin.site.site_title = "HTFBI Admin Panel"

# Set the index title (appears on the main admin index page)
admin.site.index_title = "Welcome to HTFBI Admin Panel"