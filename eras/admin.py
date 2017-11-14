#-*- coding:utf-8 -*-
from django.contrib import admin
from eras.models import *
from skosxl.admin import *
from django.utils.translation import ugettext_lazy as _

class EraAdmin(ConceptAdmin):
    readonly_fields = ('created','modified')
    search_fields = ['term','uri','pref_label','rank__pref_label','definition']
    list_display = ('term','pref_label','rank','startYear','endYear','top_concept')
    #list_editable = ('status','term','scheme','top_concept')
    list_filter = ('scheme','status')
    change_form_template = 'admin_concept_change.html'
    change_list_template = 'admin_concept_list.html'

    def changelist_view(self, request, extra_context=None):
        try :
            scheme_id = int(request.GET['scheme__id__exact'])
        except KeyError :
            scheme_id = 1 # FIXME: if no scheme filter is called, get the first (or "General") : a fixture to create one ?
        return super(EraAdmin, self).changelist_view(request, 
                                        extra_context={'scheme_id':scheme_id})
            
    fieldsets = (   (_(u'Era'), {'fields':('term','startYear','startDate','startYearUncert','endYear','endDate','endYearUncert')}),
                    (_(u'Scheme'), {'fields':('uri','scheme','pref_label','top_concept')}),
                    (_(u'Meta-data'),
                    {'fields':(('definition','changenote'),'created','modified'),
                     'classes':('collapse',)}),
                     )
    inlines = [   NotationInline, LabelInline, RelInline, SKOSMappingInline]
 

admin.site.register(Era, EraAdmin)

class EraFrameAdmin(admin.ModelAdmin):
    pass

admin.site.register(EraFrame, EraFrameAdmin)

class EraSchemeAdmin(SchemeAdmin):
    pass

admin.site.register(EraScheme, EraFrameAdmin)

class EraSourceAdmin(ImportedConceptSchemeAdmin):
    pass

admin.site.register(EraSource, EraSourceAdmin)
    