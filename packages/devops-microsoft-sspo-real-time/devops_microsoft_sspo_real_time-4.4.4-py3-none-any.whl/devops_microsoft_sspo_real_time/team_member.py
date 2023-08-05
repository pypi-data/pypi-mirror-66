import logging
from .base_entity import BaseEntity
from devops_microsoft_mapping_sspo import factories 
from sspo_db.application import factories as application_factories
logging.basicConfig(level=logging.INFO)
from datetime import datetime
from pprint import pprint

class TeamMember(BaseEntity):

    def do(self,data):
        try:
            logging.info("Team Member: Start")
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
            teammember_mapping = factories.TeamMemberFactory(organization=self.organization,configuration=self.configuration)
            
            team_member_application = application_factories.TeamMemberFactory()
            
            for team in teams:
                team_members = self.tfs.get_team_members(project_id,team.id)
                
                for team_member in team_members:
                    team_member = team_member_application.retrive_by_external_id_and_project_name(team_member.identity.id,element.name)
                    if team_member is None:
                        teammember_mapping.create(team_member, team)
            

            logging.info("Team Member: End")
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  

