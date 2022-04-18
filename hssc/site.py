from django.contrib import admin

class ClinicSite(admin.AdminSite):
    site_header = '智益诊所管理系统'
    site_title = 'Hssc Clinic'
    index_title = '诊所工作台'
    enable_nav_sidebar = False

clinic_site = ClinicSite(name = 'ClinicSite')
