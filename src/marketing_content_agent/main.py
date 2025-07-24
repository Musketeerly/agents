#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from marketing_content_agent.crew import MarketingContentAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """
    Run the marketing crew.
    """
    inputs = {
        'message': 'Eco-friendly skincare brands in the US',
        'current_date': datetime.now().strftime("%Y-%m-%d") 
    }
    
    result = MarketingContentAgent().crew().kickoff(inputs=inputs)
    print(result.raw)
if __name__ == "__main__":
    run()
    