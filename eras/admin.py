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
    list_filter = ( ('scheme',admin.RelatedOnlyFieldListFilter), 'status')
    change_form_template = 'eras/admin_era_change.html'
    change_list_template = 'eras/admin_era_scheme.html'

    def changelist_view(self, request, extra_context=None):
        try :
            scheme_id = int(request.GET['scheme__id__exact'])
        except KeyError :
            scheme_id = None 
        extra_context = extra_context or {}
        extra_context['scheme_id'] = scheme_id
        return super(EraAdmin, self).changelist_view(request, 
                                        extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try :
            scheme_id = Era.objects.get(id=object_id).scheme.id
        except KeyError :
            scheme_id = None 
        extra_context = extra_context or {}
        extra_context['scheme_id'] = scheme_id
        extra_context['object_id'] = object_id
        return super(EraAdmin, self).change_view(request, object_id, form_url=form_url,
                                        extra_context=extra_context)
                                        
    fieldsets = (   (_(u'Era'), {'fields':('term','startYear','startDate','startYearUncert','endYear','endDate','endYearUncert')}),
                    (_(u'Scheme'), {'fields':('uri','scheme','pref_label','top_concept','rank','definition')}),
                    (_(u'Meta-data'),
                    {'fields':('prefStyle','changenote','created','modified'),
                     'classes':('collapse',)}),
                     )
    inlines = [   NotationInline, LabelInline, RelInline, SKOSMappingInline ,ConceptMetaInline ,]
 

admin.site.register(Era, EraAdmin)

class EraFrameAdmin(admin.ModelAdmin):
    pass

admin.site.register(EraFrame, EraFrameAdmin)

class EraInline(ConceptInline):
    model = Era
#    list_fields = ('pref_label', )
    show_change_link = True
    max_num = 20
    fields = ('term','pref_label','rank','startYear','endYear',)
 #   list_display = ('pref_label',)
    related_search_fields = {'concept' : ('prefLabel','definition')}
    extra = 0
    
class EraSchemeAdmin(SchemeAdmin):
    change_form_template = 'eras/admin_era_scheme_change.html'
    inlines = [   EraInline, ]
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try :
            scheme_id = object_id
        except KeyError :
            scheme_id = None 
        extra_context = extra_context or {}
        extra_context['scheme_id'] = scheme_id
        extra_context['object_id'] = object_id
        return super(EraSchemeAdmin, self).change_view(request, object_id, form_url=form_url,
                                        extra_context=extra_context)
                     

admin.site.register(EraScheme, EraSchemeAdmin)

class EraSourceAdmin(ImportedConceptSchemeAdmin):
    pass

admin.site.register(EraSource, EraSourceAdmin)
    