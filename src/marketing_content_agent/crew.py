from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
import os
import agentops
from dotenv import load_dotenv
load_dotenv(override=True)
agentops_api_key = os.getenv("AGENTOPS_API_KEY")

agentops.init(api_key=agentops_api_key, default_tags=["production"])


@CrewBase
class MarketingContentAgent():
    """MarketingContentAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    
    @agent
    def competitor_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['competitor_finder'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def data_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['data_scraper'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def trend_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_analyzer'],
            verbose=True
        )
    
    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],
            verbose=True
        )
    
    @agent
    def action_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['action_recommender'],
            verbose=True
        )
   
    @task
    def find_competitors_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_competitors_task'] 
        )

    @task
    def scrape_competitor_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_competitor_data_task']
        )

    @task
    def analyze_trends_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_trends_task'],
            output_file= "trends_report.md"
        )

    @task
    def generate_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_task'],
            output_file= "final_report.md"
        )
    
    @task
    def recommend_actions_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommend_actions_task'],
            output_file= "actions.md" 
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the MarketingContentAgent crew"""
       

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            
        )
