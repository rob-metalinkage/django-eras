# -*- coding: utf-8 -*-

from django.db import models

from skosxl.models import *
from rdf_io.models import RDFpath_Field
from rdflib.term import URIRef, Literal
import json
from model_utils.models import TimeStampedModel

class EraFrame(TimeStampedModel):
    uri = models.URLField(help_text=u'URI identifying the time frame')
    name = models.CharField(max_length=100,help_text=u'Display name for the temporal axis, e.g. "millions of years BC"')
    yearFactor = models.FloatField(help_text=u'How many years represented by a unit in the start/endYear field')
    
        
    def __unicode__(self):
        return ( self.name )
    
class EraScheme(Scheme):
    """ creates a Concept scheme with additional metadata about timeframes and overall extent"""
    frame = models.ForeignKey(EraFrame)
    startYear = models.DecimalField(blank=True,null=True, max_digits=10,decimal_places=2, help_text=u'Start year, using scaling factor from timeframe specified in the EraScheme')    
    endYear = models.DecimalField(blank=True,null=True, max_digits=10,decimal_places=2, help_text=u'Start year, using timeframe specified in the EraScheme')
    
    def json_intervals(self,start=None, end=None, max=None, node=None):
        """ get a intervals array in the form used by timescale.js 
        
        allows setting start and/or end date (years, using timeframe for the era scheme), or a starting node, whose timeframe will be used
        """
        records = []
        children = {}
        childrels = SemRelation.objects.filter(rel_type=REL_TYPES.narrower, origin_concept__scheme=self)
        for rel in childrels :
            children[ rel.target_concept] = rel.origin_concept
        childrels = SemRelation.objects.filter(rel_type=REL_TYPES.broader, origin_concept__scheme=self)
        for rel in childrels :
            children[ rel.origin_concept.id ] =  rel.target_concept.id
        filters = { "startYear__isnull":False }
        if self.frame.yearFactor > 0 :
            if start:
                filters["endYear__gte"] = float(start)
            if end:
                filters["startYear__lte"] = float(end)
        else:
            if start:
                filters["endYear__lte"] = float(start)
            if end:
                filters["startYear__gte"] = float(end)            
        eras = Era.objects.filter(scheme=self.id, **filters) # pref_label__in=['Archean','Proterozoic'])
        for era in eras :
            
            details = { 'oid': era.id , 'nam':era.pref_label,  'type':'int', 'eag': float(era.startYear),  "col":"#FEBF65" }
            try:
                details['lvl']= era.rank.level or 0
            except:
                print "Failed to get level"        
            try:
                details['lag'] = float(era.endYear)
            except:
                print "No end year %s " % era
                details['eag'] = 0
            if era.top_concept :
                details ['pid']  = 0
            else :
                try:
                    details ['pid'] = children[ era.id ]
                except:
                    pass
            records.append (  details )
        return json.dumps({ 'title':self.pref_label, 'frame': { 'name':self.frame.name, 'factor':self.frame.yearFactor, 'def':self.frame.uri},  'records':records })
        
    
class Era(Concept):
    """ An era, as an extended concept with start and end times, in flexible but simple form"""
    startYear = models.DecimalField(blank=True,null=True, max_digits=10,decimal_places=2, help_text=u'Start year, using scaling factor from timeframe specified in the EraScheme')
    startYearUncert = models.DecimalField(blank=True,null=True, max_digits=10,decimal_places=2, help_text=u'Numerical measure of uncertainty for Start year, using timeframe specified in the EraScheme')
    startDate = models.DateField(help_text=u'Use this only if a precise date is known and important (year will be auto-calculated)',blank=True,null=True)
    endYear = models.DecimalField(blank=True,null=True, max_digits=10,decimal_places=2, help_text=u'Start year, using timeframe specified in the EraScheme')
    endYearUncert = models.DecimalField(blank=True,null=True, max_digits=10,decimal_places=2, help_text=u'Numerical measure of uncertainty for Start year, using timeframe specified in the EraScheme')
    endDate = models.DateField(help_text=u'Use this only if a precise date is known and important (year will be auto-calculated)',blank=True,null=True)
    nextEra = models.OneToOneField("self", related_name="next",blank=True, null=True,help_text=u'Next Era in sequence - should be at same level of detail' )
    previousEra = models.OneToOneField("self", related_name="previous", blank=True, null=True,help_text=u'Previous Era in sequence - should be at same level of detail')

class EraSource(ImportedConceptScheme):
    frame = models.ForeignKey(EraFrame)
    startTimeProperty = RDFpath_Field( blank=True, null=True, help_text=u'RDF property path for era start time. prefixes must be registered in RDF_IO.namespaces' )
    startTimeUncertProperty = RDFpath_Field( blank=True, null=True, help_text=u'RDF property path for era start time uncertainty measure. prefixes must be registered in RDF_IO.namespaces' )
    endTimeProperty = RDFpath_Field(max_length=200, blank=True, null=True, help_text=u'RDF property path for era end time. prefixes must be registered in RDF_IO.namespaces' )
    endTimeUncertProperty = RDFpath_Field(max_length=200, blank=True, null=True, help_text=u'RDF property path for era end time uncertainty measure. prefixes must be registered in RDF_IO.namespaces' )
    
    def save(self,*args,**kwargs):  
        # save first - to make file available
        import pdb; pdb.set_trace()
        if not self.force_bulk_only :
            target_repo = self.target_repo
            self.target_repo = None
            super(EraSource, self).save(*args,**kwargs)
            self.target_repo = target_repo
        else:
            super(EraSource, self).save(*args,**kwargs)
        parsedRDF = self.get_graph()
        # import the basic SKOS elements of the scheme using the era subclasses
        scheme_obj = self.importScheme(parsedRDF,self.target_scheme, self.force_refresh, schemeClass=EraScheme, conceptClass=Era, schemeDefaults={'frame':self.frame})
        # now process the temporal elements
        self.importTimes(scheme_obj,parsedRDF)
        
    def importTimes(self, scheme_obj, gr):
        for c in self.getConcepts(URIRef(scheme_obj.uri),gr):
            try:
                era = Era.objects.get(uri=str(c))
                startYear = None
                if self.startTimeProperty:
                    startYear = self.getPathVal(gr,c,self.startTimeProperty) 
                    try:
                        era.startYear = float(startYear)
                    except:
                        era.startDate = startYear
                if self.endTimeProperty :
                    endYear = self.getPathVal(gr,c,self.endTimeProperty) 
                    if startYear and not endYear:
                        endYear = 0
                    try:
                        era.endYear = float(endYear)
                    except:
                        era.endDate = endYear
                if self.startTimeUncertProperty:
                    era.startYearUncert = self.getPathVal(gr,c,self.startTimeUncertProperty ) 
                if self.endTimeUncertProperty:
                    era.endYearUncert = self.getPathVal(gr,c,self.endTimeUncertProperty ) 
                era.save()
            except Exception as e:
                print "Couldnt access path startTimeProperty for concept %s , %s " % (c,e)
    