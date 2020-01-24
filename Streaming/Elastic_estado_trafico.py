
"""
Created on Wed Jan 15 18:31:37 2020

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

import utm
import json
import ast


#Create a function to iterate through the utm coordinates list 
#the function return a list of lat and long coordinates 
def WonderWoman(coordinates1):
    newlist=[]
    lista= ast.literal_eval(coordinates1)
    for coord in lista:
            new_coord = utm.to_latlon(coord[0], coord[1], 30, 'U')
            lat=new_coord[1]
            long=new_coord[0]
            new_new_coord="["+str(lat)+","+str(long)+"]"
            newlist.append(ast.literal_eval(new_new_coord))
    return newlist
    
class LocationConcat(beam.DoFn):
    """
    Filter data for inserts
    """

    def process(self, element):

#{"idtramo":"240","denominacion":"CAMPANAR (DE P���?O XII A TIRSO DE MOLINA)","modified":"2020-01-15T18:42:04.797+01:00","estado":"0","coordinates":"[[724080.288,4373021.159],[724133.682,4373191.511],[724200.715,4373393.157]]","uri":"http://apigobiernoabiertortod.valencia.es/apirtod/datos/estado_trafico/240.json"}        
        
        item = json.loads(element)
        return [{'idtramo':item['idtramo'],
                 'denominacion':item['denominacion'],
                 'date':item['modified'],
                 'estado':(item['estado']),
                 'location':    { "type": "linestring", "coordinates": (WonderWoman(item['coordinates'])) },#here is where the convertion function is use
                 'uri':item['uri']                
                                 
                 }]

                    #'location':str(item['latitude'])+","+str(item['longitude'])  
    
class IndexDocument(beam.DoFn):
   
    es=Elasticsearch([{'host':'localhost','port':9200}])
    
    def process(self,element):
        
        res = self.es.index(index='estado_trafico',body=element)
        
        print(res)
 
        
    
def run(argv=None, save_main_session=True):
  """Main entry point; defines and runs the wordcount pipeline."""
  parser = argparse.ArgumentParser()
  
  #1 Replace your hackathon-edem with your project id 
  parser.add_argument('--input_topic',
                      dest='input_topic',
                      #1 Add your project Id and topic name you created
                      # Example projects/versatile-gist-251107/topics/iexCloud',
                      default='projects/hackathon2-luis1201/topics/estado_trafico',
                      help='Input file to process.')
  #2 Replace your hackathon-edem with your project id 
  parser.add_argument('--input_subscription',
                      dest='input_subscription',
                      #3 Add your project Id and Subscription you created you created
                      # Example projects/versatile-gist-251107/subscriptions/quotesConsumer',
                      default='projects/hackathon2-luis1201/subscriptions/streaming_trafico',
                      help='Input Subscription')
  
  
  
    
  known_args, pipeline_args = parser.parse_known_args(argv)

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
   
  google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
  #3 Replace your hackathon-edem with your project id 
  google_cloud_options.project = 'hackathon2-luis1201'
  google_cloud_options.job_name = 'myjob2'
 
  # Uncomment below and add your bucket if you want to execute on Dataflow
  #google_cloud_options.staging_location = 'gs://edem-bucket-roberto/binaries'
  #google_cloud_options.temp_location = 'gs://edem-bucket-roberto/temp'

  pipeline_options.view_as(StandardOptions).runner = 'DirectRunner'
  #pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
  pipeline_options.view_as(StandardOptions).streaming = True

 
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session


 

  p = beam.Pipeline(options=pipeline_options)


  # Read the pubsub messages into a PCollection.
  trafficStatus = p | beam.io.ReadFromPubSub(subscription=known_args.input_subscription)

  # Print messages received
 
  
  
  trafficStatus = ( trafficStatus | beam.ParDo(LocationConcat()))
  
  trafficStatus | 'Print Quote' >> beam.Map(print)
  
  # Store messages on elastic
  trafficStatus | 'Status of traffic' >> beam.ParDo(IndexDocument())
  
  
  
 
  result = p.run()
  result.wait_until_finish()

  
if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()