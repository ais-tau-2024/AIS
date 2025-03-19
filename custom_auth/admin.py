from django.contrib import admin
from .models import (
    GroupModel,
    # ProgramModel,
    # FundingModel,
    StudentModel,
    TeacherModel,
    TeacherAuthModel,
    TeacherAuthTokenModel,
    TeacherAchievementModel,
    TeacherScienceFieldModel,
    TeacherForeignLanguageModel,
    TeacherEducationRecordModel,
    TeacherCategoryModel
)
from django.utils.html import format_html

# -------------------
# Faculty and Related Models
# -------------------


@admin.register(GroupModel)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


# @admin.register(ProgramModel)
# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('id', 'code', 'name')
#     search_fields = ('code', 'name')
#     ordering = ('code',)


# @admin.register(FundingModel)
# class FundingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'type')
#     search_fields = ('type',)
#     ordering = ('type',)


# -------------------
# Student Model
# -------------------

@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'iin', 
        'first_name', 
        'last_name', 
        'group',
        # 'program', 
        # 'funding', 
        'birth_date', 
        'gender', 
        'nationality',
        'date_of_enrollment',
        'form_of_payment'
    )
    search_fields = (
        'iin', 
        'first_name', 
        'last_name', 
        'group__name', 
        # 'program__name', 
        # 'funding__type'
    )
    list_filter = (
        'gender', 
        # 'program', 
        # 'funding'
    )
    ordering = (
        'last_name', 
        'first_name',
    )
    date_hierarchy = 'birth_date'
    raw_id_fields = (
        'group', 
        # 'program', 
        # 'funding'
    )


# -------------------
# Teacher and Related Models
# -------------------

class AchievementInline(admin.TabularInline):
    model = TeacherAchievementModel
    extra = 1
    readonly_fields = ('__str__',)
    can_delete = True


class ScienceFieldInline(admin.TabularInline):
    model = TeacherScienceFieldModel
    extra = 1
    can_delete = True


class ForeignLanguageInline(admin.TabularInline):
    model = TeacherForeignLanguageModel
    extra = 1
    can_delete = True


class EducationRecordInline(admin.TabularInline):
    model = TeacherEducationRecordModel
    extra = 1
    can_delete = True
    readonly_fields = ('scan_copy_preview',)

    def scan_copy_preview(self, obj):
        if obj.scan_copy:
            return format_html('<a href="{}" target="_blank">View</a>', obj.scan_copy.url)
        return "No file"

    scan_copy_preview.short_description = "Scan Copy"


class TeacherCategoryInline(admin.TabularInline):
    model = TeacherCategoryModel
    extra = 1
    can_delete = True
    readonly_fields = ('confirmation_document_preview',)

    def confirmation_document_preview(self, obj):
        if obj.confirmation_document:
            return format_html('<a href="{}" target="_blank">View</a>', obj.confirmation_document.url)
        return "No file"

    confirmation_document_preview.short_description = "Confirmation Document"


@admin.register(TeacherModel)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'iin',
        'first_name',
        'last_name',
        'patronymic',
        'nationality',
        'gender',
        'birth_date',
        'citizenship',
        'marital_status',
        'place_of_birth',
        'document_type',
        'document_number',
        'document_issue_date',
        'document_expiry_date',
        'issuing_authority',
        'registration_address',
        'residential_address',
        'home_phone',
        'phone_number',
        'email',
        'teaching_language',
        'profile_photo',
        'admission_date'
    )
    search_fields = (
        'iin', 'first_name', 'last_name', 'email', 'phone_number',
        'nationality', 'teaching_language'
    )
    list_filter = ('gender', 'nationality', 'teaching_language')
    ordering = ('last_name', 'first_name')
    inlines = [
        AchievementInline,
        ScienceFieldInline,
        ForeignLanguageInline,
        EducationRecordInline,
        TeacherCategoryInline,
    ]
    readonly_fields = ('__str__',)


@admin.register(TeacherAuthModel)
class TeacherAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher',)
    search_fields = ('teacher__iin', 'teacher__first_name', 'teacher__last_name')
    readonly_fields = ('password',)
    ordering = ('teacher',)
    exclude = ('password',)  # Hide password field in the admin


@admin.register(TeacherAuthTokenModel)
class TeacherAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'token', 'created_at')
    search_fields = ('teacher__iin', 'teacher__first_name', 'teacher__last_name', 'token')
    list_filter = ('teacher',)
    ordering = ('-created_at',)
    readonly_fields = ('token', 'created_at')


# -------------------
# Additional Teacher Models
# -------------------

@admin.register(TeacherAchievementModel)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'title')
    search_fields = ('teacher__iin', 'teacher__first_name', 'teacher__last_name', 'title')
    list_filter = ('teacher',)
    ordering = ('title',)


@admin.register(TeacherScienceFieldModel)
class ScienceFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'field', 'academic_degree', 'academic_status')
    search_fields = ('teacher__iin', 'teacher__first_name', 'teacher__last_name', 'field')
    list_filter = ('academic_degree', 'academic_status')
    ordering = ('field',)


@admin.register(TeacherForeignLanguageModel)
class ForeignLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'language', 'proficiency_level')
    search_fields = ('teacher__iin', 'teacher__first_name', 'teacher__last_name', 'language')
    list_filter = ('proficiency_level',)
    ordering = ('language',)


@admin.register(TeacherEducationRecordModel)
class EducationRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'institution_name', 'graduation_year', 'qualification')
    search_fields = (
        'teacher__iin', 'teacher__first_name', 'teacher__last_name',
        'institution_name', 'qualification', 'specialization'
    )
    list_filter = ('graduation_year', 'foreign_institution')
    ordering = ('-graduation_year',)
    readonly_fields = ('scan_copy_preview',)

    def scan_copy_preview(self, obj):
        if obj.scan_copy:
            return format_html('<a href="{}" target="_blank">View</a>', obj.scan_copy.url)
        return "No file"

    scan_copy_preview.short_description = "Scan Copy"


@admin.register(TeacherCategoryModel)
class TeacherCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'category', 'order_number', 'order_date')
    search_fields = (
        'teacher__iin', 'teacher__first_name', 'teacher__last_name',
        'category', 'order_number'
    )
    list_filter = ('category', 'order_date')
    ordering = ('-order_date',)
    readonly_fields = ('confirmation_document_preview',)

    def confirmation_document_preview(self, obj):
        if obj.confirmation_document:
            return format_html('<a href="{}" target="_blank">View</a>', obj.confirmation_document.url)
        return "No file"

    confirmation_document_preview.short_description = "Confirmation Document"

