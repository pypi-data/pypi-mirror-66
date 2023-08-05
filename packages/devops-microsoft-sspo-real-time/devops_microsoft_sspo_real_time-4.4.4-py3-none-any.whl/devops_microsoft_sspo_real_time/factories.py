import factory
from devops_microsoft_sspo_real_time.scrum_development_task import ScrumDevelopmentTask
from devops_microsoft_sspo_real_time.scrum_project import ScrumProject
from devops_microsoft_sspo_real_time.atomic_user_story import AtomicUserStory
from devops_microsoft_sspo_real_time.epic import Epic
from devops_microsoft_sspo_real_time.team_member import TeamMember
from devops_microsoft_sspo_real_time.sprint import Sprint
import factory

class SprintFactory(factory.Factory):
    class Meta:
        model = Sprint

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = TeamMember

class EpicFactory(factory.Factory):
    class Meta:
        model = Epic

class AtomicUserStoryFactory(factory.Factory):
    class Meta:
        model = AtomicUserStory

class ScrumDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumDevelopmentTask

class ScrumProjectFactory(factory.Factory):
    class Meta:
        model = ScrumProject
