#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:52:55 2020

@author: luisn
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

import ast
import json


class LocationConcat(beam.DoFn):
    """
    Filter data for inserts
    """

    def process(self, element):
        
#{"geo":"","hashtags":"","name":"T...","coordinates":"","created_at":"Wed Jan 22 17:04:40 +0000 2020","description":"Técnico ...”    \uD83C\uDDEA\uD83C\uDDF8","location":"Valencia ","id":"1220029525","text":"RT @SalvaGomis97: ¿Pero","lang":"es"}     
        item = json.loads(element)
        return [{'created_at':item['created_at'],
                 'id':item['id'],
                 'lang':item['lang'],
                 'text':item['text'],
                 'geo':item['geo'],
                 'coordinates':item['coordinates'],
                 'location':item['location'],
                 'name':item['name'],
                 'description':item['description'],
                 'hashtags':(ast.literal_eval(item['hashtags']))            
                 }]


class IndexDocument(beam.DoFn):
   
    es=Elasticsearch([{'host':'localhost','port':9200}])
    
    def process(self,element):
        
        res = self.es.index(index='twitter_index',body=element)
        
        print(res)
 
        
    
def run(argv=None, save_main_session=True):
  """Main entry point; defines and runs the wordcount pipeline."""
  parser = argparse.ArgumentParser()
  
  #1 Replace your hackathon-edem with your project id 
  parser.add_argument('--input_topic',
                      dest='input_topic',
                      #1 Add your project Id and topic name you created
                      # Example projects/versatile-gist-251107/topics/iexCloud',
                      default='projects/hackathon2-luis1201/topics/twitter_topic',
                      help='Input file to process.')
  #2 Replace your hackathon-edem with your project id 
  parser.add_argument('--input_subscription',
                      dest='input_subscription',
                      #3 Add your project Id and Subscription you created you created
                      # Example projects/versatile-gist-251107/subscriptions/quotesConsumer',
                      default='projects/hackathon2-luis1201/subscriptions/twitter_sub',
                      help='Input Subscription')
  
  
  
    
  known_args, pipeline_args = parser.parse_known_args(argv)

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
   
  google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
  #3 Replace your hackathon-edem with your project id 
  google_cloud_options.project = 'hackathon2-luis1201'
  google_cloud_options.job_name = 'myjob6'
 
  # Uncomment below and add your bucket if you want to execute on Dataflow
  #google_cloud_options.staging_location = 'gs://edem-bucket-roberto/binaries'
  #google_cloud_options.temp_location = 'gs://edem-bucket-roberto/temp'

  pipeline_options.view_as(StandardOptions).runner = 'DirectRunner'
  #pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
  pipeline_options.view_as(StandardOptions).streaming = True

 
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session


 

  p = beam.Pipeline(options=pipeline_options)


  # Read the pubsub messages into a PCollection.
  Twitter_tweet = p | beam.io.ReadFromPubSub(subscription=known_args.input_subscription)

  # Print messages received
 
  
  
  Twitter_tweet = ( Twitter_tweet | beam.ParDo(LocationConcat()))
  
  Twitter_tweet | 'Print Quote' >> beam.Map(print)
  
  # Store messages on elastic
  Twitter_tweet | 'Twitter tweeds' >> beam.ParDo(IndexDocument())
  
  
  
 
  result = p.run()
  result.wait_until_finish()

  
if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()