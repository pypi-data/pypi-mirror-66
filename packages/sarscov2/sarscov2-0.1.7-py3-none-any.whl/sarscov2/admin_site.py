from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "SARS-COV-2"
    site_header = "SARS-COV-2"
    index_title = "SARS-COV-2"
    site_url = "/administration/"


sarscov2_admin = AdminSite(name="sarscov2_admin")
sarscov2_admin.disable_action("delete_selected")
