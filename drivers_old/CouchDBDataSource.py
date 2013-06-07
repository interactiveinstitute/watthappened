#!/usr/bin/python
#   Interactive Institute
#

from DataSource import DataSource
import couchdbkit
import restkit
import config

class CouchDBDataSource(DataSource):
    def __init__(self,Adress,User,Password,Database):
        self.Adress = Adress
        self.User = User
        self.Password = Password
        self.Database = Database
            
            
        DataSource.__init__(self)

    
        #Create the server connection
        self.auth = restkit.BasicAuth(User,Password)
        self.server = couchdbkit.Server(uri=Adress, filters=[self.auth])

        self.db = self.server.get_db(Database)
            
        info = self.db.list('energy_data/feeds_and_datastreams', 'by_source_and_time', group_level=1)
        self.feeds = info['feeds']
        self.DataStreamNames = info['datastreams']

        return

    def ListDataFeeds(self,cached = True):

        if not cached:
            self.UpdateStreamNames()
            
        return self.DataStreamNames


    def UpdateStreamNames(self):
        info = db.list('energy_data/feeds_and_datastreams', 'by_source_and_time', group_level=1)
        self.feeds = info['feeds']
        self.DataStreamNames = info['datastreams']
        
        return
            


if __name__ == '__main__':
    
    print "Test program of CouchDBDataSource"
    
    Source = CouchDBDataSource(config.COUCHDB_SERVER,config.COUCHDB_USER,config.COUCHDB_PASSWORD,config.COUCHDB_DATABASE)

    print Source.ListDataFeeds()


    
    