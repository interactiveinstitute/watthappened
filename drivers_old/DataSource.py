#   Interactive Institute
#

class DataSource():
    def __init__(self):
        
        DataStreamNames = []
        DataStreamObj = []
        
        self.Connected = False
        return

    def ListDataFeeds(cached = False):
        raise NotImplementedError, "This function needs to be implemented in the specific inplementation for the database technology used"
        return

    def ListHiearkies():
        raise NotImplementedError, "This function needs to be implemented in the specific inplementation for the database technology used"
        return

    def GetFeedByName(self,name):
        raise NotImplementedError, "This function needs to be implemented in the specific inplementation for the database technology used"
        return

    