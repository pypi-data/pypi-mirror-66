import logging
from .base_entity import BaseEntity
from devops_microsoft_mapping_sspo import factories 
from sspo_db.application import factories as application_factories
logging.basicConfig(level=logging.INFO)
from datetime import datetime
from pprint import pprint

class Sprint(BaseEntity):

    def do(self,data):
        try:
            logging.info("Sprint: Start")
            self.config(data)
            content = data["content"]
            project_id = content['all']['resourceContainers']['project']['id']

            projects = self.tfs.get_projects()
            element = None
            for project in projects: 
                if project.id == project_id:
                    element = project
                    break
            
            teams = self.tfs.get_teams(element.id)
            
            for team in teams:
                interactions = self.tfs.get_interactions(element,team)
                
                for interaction in interactions:
                    logging.info("Interaction: Creating interaction")
                        
                    #sprint_mapping.create(interaction,scrum_process)


            logging.info("Sprint: End")
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  