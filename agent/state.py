from typing import TypedDict, Annotated, List
import operator


class AgentState(TypedDict):
    question: str                                    
    subject: str                                      
    subject_label: str                                
    wiki_context: str                                 
    answer: str                                      
    follow_ups: List[str]                           
    steps_log: Annotated[List[str], operator.add]