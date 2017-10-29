# -*- coding: utf-8 -*-

from django.db import models

from skosxl.models import *
from rdf_io.models import RDFpath_Field
from rdflib.term import URIRef, Literal

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
                startYear = self.getPathVal(gr,c,self.startTimeProperty) 
                try:
                    era.startYear = float(startYear)
                except:
                    era.startDate = startYear
                endYear = self.getPathVal(gr,c,self.endTimeProperty) 
                try:
                    era.endYear = float(endYear)
                except:
                    era.endDate = endYear
                era.startYearUncert = self.getPathVal(gr,c,self.startTimeUncertProperty ) 
                era.endYearUncert = self.getPathVal(gr,c,self.endTimeUncertProperty ) 
                era.save()
            except Exception as e:
                print "Couldnt access path startTimeProperty for concept %s , %s " % (c,e)
    