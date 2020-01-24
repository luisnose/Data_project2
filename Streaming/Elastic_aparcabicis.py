#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:18:28 2020

@author: edem
"""

from __future__ import absolute_import

import argparse
import logging

import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import StandardOptions

from apache_beam.options.pipeline_options import SetupOptions

from elasticsearch import Elasticsearch 

import utm
import json

#Create a function that convert the utm coordenates to lat and long coordinates 


def convierteutm(x,y):
    new_coord = utm.to_latlon(x, y, 30, 'U')   #the "30" belong to the zone of spain as the "U" value
    return(str(new_coord[0])+","+str(new_coord[1]) )

class LocationConcat(beam.DoFn):
    """
    Filter data for inserts
    """

    def process(self, element):
        
      
        item = json.loads(element)
        return [{'Identificador':item['properties']['id'],
                 'tipo':item['properties']['tipo'],
                 'plazas':item['properties']['plazas'],
                 'type':item['geometry']['type'],
                 'location':(convierteutm(item['geometry']['coordinates'][0],item['geometry']['coordinates'][1]))
                          #here is where the function is use           
                 }]

                    #'location':str(item['latitude'])+","+str(item['longitude'])  
    
class IndexDocument(beam.DoFn):
   
    es=Elasticsearch([{'host':'localhost','port':9200}])
    
    def process(self,element):
        
        res = self.es.index(index='ubicacion_aparcabicis',body=element)
        
        print(res)
 
        
    
def run(argv=None, save_main_session=True):
  """Main entry point; defines and runs the wordcount pipeline."""
  parser = argparse.ArgumentParser()
  
  #1 Replace your hackathon-edem with your project id 
  parser.add_argument('--input_topic',
                      dest='input_topic',
                      #1 Add your project Id and topic name you created
                      # Example projects/versatile-gist-251107/topics/iexCloud',
                      default='projects/hackathon2-luis1201/topics/aparcabicis',
                      help='Input file to process.')
  #2 Replace your hackathon-edem with your project id 
  parser.add_argument('--input_subscription',
                      dest='input_subscription',
                      #3 Add your project Id and Subscription you created you created
                      # Example projects/versatile-gist-251107/subscriptions/quotesConsumer',
                      default='projects/hackathon2-luis1201/subscriptions/streaming_aparcabicis',
                      help='Input Subscription')
  
  
  
    
  known_args, pipeline_args = parser.parse_known_args(argv)

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
   
  google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
  #3 Replace your hackathon-edem with your project id 
  google_cloud_options.project = 'hackathon2-luis1201'
  google_cloud_options.job_name = 'myjob3'
 
  # Uncomment below and add your bucket if you want to execute on Dataflow
  #google_cloud_options.staging_location = 'gs://edem-bucket-roberto/binaries'
  #google_cloud_options.temp_location = 'gs://edem-bucket-roberto/temp'

  pipeline_options.view_as(StandardOptions).runner = 'DirectRunner'
  #pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
  pipeline_options.view_as(StandardOptions).streaming = True

 
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session


 

  p = beam.Pipeline(options=pipeline_options)


  # Read the pubsub messages into a PCollection.
  Aparcabicisloc = p | beam.io.ReadFromPubSub(subscription=known_args.input_subscription)

  # Print messages received
 
  
  
  Aparcabicisloc = ( Aparcabicisloc | beam.ParDo(LocationConcat()))
  
  Aparcabicisloc | 'Print Quote' >> beam.Map(print)
  
  # Store messages on elastic
  Aparcabicisloc | 'location of aparcabicis' >> beam.ParDo(IndexDocument())
  
  
  
 
  result = p.run()
  result.wait_until_finish()

  
if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()