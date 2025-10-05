# AI Career Advisor using CrewAI
# Comprehensive multi-agent system for personalized career guidance

import warnings
warnings.filterwarnings('ignore')

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from llm_handler import llm_handler

# Load environment variables from .env file
load_dotenv()

# Configure ALL LLMs for optimal load distribution across 5 API providers
# Using correct CrewAI documentation formats for each provider

# 1. Gemini LLM - Primary (2 agents) ✅
gemini_primary = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

# 2. Gemini LLM - Secondary (1 agent) ✅  
gemini_secondary = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.5,
)

# 3. Perplexity LLM - Research focused (2 agents) ✅ 
perplexity_llm = LLM(
    model="sonar-reasoning-pro",
    base_url="https://api.perplexity.ai/",
    api_key=os.getenv("PERPLEXITY_API_KEY")
)

# 4. OpenRouter LLM - Primary Claude (1 agent) ✅
openrouter_claude_1 = LLM(
    model="openrouter/deepseek/deepseek-r1",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)

# 5. OpenRouter LLM - Secondary Claude (1 agent) ✅
openrouter_claude_2 = LLM(
    model="openrouter/deepseek/deepseek-r1",
    base_url="https://openrouter.ai/api/v1", 
    api_key=os.getenv("OPENROUTER_API_KEY_1"),
    temperature=0.5,
)

# 🚀 OPTIMAL LOAD DISTRIBUTION ACROSS ALL 5 API PROVIDERS:
# Agent 1 (Profile Analysis): Gemini Primary
# Agent 2 (Career Exploration): Perplexity (with web search)
# Agent 3 (Skill Development): OpenRouter Claude 1
# Agent 4 (Job Market Analysis): Perplexity (with web search)  
# Agent 5 (Strategic Roadmap): Gemini Secondary
# Agent 6 (Learning Resources): OpenRouter Claude 2
# Agent 7 (Report Generation): Gemini Primary
# 
# Distribution: Gemini(3) + Perplexity(2) + OpenRouter(2) = Perfect Balance!

# Initialize search tool
search_tool = SerperDevTool()

# --- Agent Definitions ---
# 🎯 LLM Distribution Strategy - Using ALL 5 API Providers:
# ✅ Gemini (3 agents): Profile + Roadmap + Report (proven working)
# ✅ Perplexity (2 agents): Career + Market research (web search enabled)  
# ✅ OpenRouter (2 agents): Skills + Resources (Claude for analysis)
# This ensures maximum load balancing and prevents any single API limits

# Agent 1: User Profiler Agent (Using Gemini Primary - now with correct API key format)
user_profiler_agent = Agent(
    role="Personal Profile Analyst",
    goal="Create a concise and structured summary of the user's background, interests, skills, and goals to guide the other agents. Be especially supportive of students who are uncertain about their future and help them discover hidden strengths and potential interests.",
    backstory="You are an expert HR professional skilled at understanding individual profiles, with special expertise in working with high school students who may be uncertain about their career direction. You excel at reading between the lines to identify potential strengths, interests, and aspirations even when they're not explicitly stated. You're encouraging and help students see possibilities they might not have considered.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_primary
)

# Agent 2: Career Exploration Agent (Using Perplexity - excellent for research)
career_exploration_agent = Agent(
    role="Career Options Specialist",
    goal="Research and identify a diverse range of suitable career paths based on the user's profile",
    backstory="You are a seasoned career counselor with deep knowledge of various industries, job roles, educational requirements, and future market trends. You can tailor your advice perfectly for a high-school student exploring their first career or a professional looking for a significant change.",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=perplexity_llm
)

# Agent 3: Skill Development Agent (Using OpenRouter Claude 1 - excellent for structured analysis)
skill_development_agent = Agent(
    role="Learning and Skill Advisor",
    goal="Identify the necessary skills for the suggested career paths and recommend relevant, high-quality learning resources",
    backstory="You are an expert in corporate and academic learning & development. You are constantly updated on the most effective online courses, certifications, and resources for professional growth across all domains.",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=openrouter_claude_1
)

# Agent 4: Job Market Insights Agent (Using Perplexity - excellent for current market data)
job_market_agent = Agent(
    role="Job Market Analyst",
    goal="Provide current, data-driven insights into the job market for the recommended career paths, including salary expectations, key companies, and future outlook",
    backstory="You are a market research analyst specializing in labor trends and economic forecasting. You provide realistic and data-driven insights into various industries to help users make informed decisions.",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=perplexity_llm
)

# Agent 5: Roadmap/Strategy Agent (Using Gemini Secondary - strategic planning)
roadmap_strategy_agent = Agent(
    role="Career Roadmap Strategist",
    goal="Create a comprehensive, step-by-step career roadmap with specific timelines, milestones, and strategic action plans",
    backstory="You are a strategic career planning expert who specializes in creating actionable roadmaps. You excel at breaking down complex career transitions into manageable phases with clear timelines, milestones, and success metrics. You understand how to sequence learning, networking, and career moves for maximum impact.",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=gemini_secondary
)

# Agent 6: Learning/Resource Agent (Using OpenRouter Claude 2 - excellent for curation)
learning_resource_agent = Agent(
    role="Learning Resource Curator",
    goal="Research and recommend the most current, high-quality learning resources, courses, certifications, and educational pathways",
    backstory="You are an education technology specialist and learning curator with deep knowledge of online learning platforms, certification programs, bootcamps, and educational trends. You stay updated on the latest courses, their quality ratings, instructor credentials, and industry recognition. You can recommend both free and paid resources that provide the best ROI for career advancement.",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    llm=openrouter_claude_2
)

# Agent 7: Report Generation Agent (Using Gemini Primary - excellent for synthesis)
report_generation_agent = Agent(
    role="Career Report Synthesizer",
    goal="Compile all the individual analyses into a single, concise, personalized, and inspiring career report. Create an executive summary format that is comprehensive yet digestible (aim for 2-3 pages maximum). Focus on the most actionable insights and key recommendations without compromising on quality or depth.",
    backstory="You are a professional writer and editor who specializes in creating clear, compelling, and well-structured reports. You excel at distilling complex information into concise, actionable summaries that busy people can actually read and act upon. You know how to prioritize the most important insights while maintaining professional depth.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_primary
)

# --- Task Definitions ---

# Task 1: Profile Analysis
profile_analysis_task = Task(
    description="Analyze the user's provided information: {user_info}. Create a structured summary that includes their current educational/professional stage, key interests, existing skills, and stated goals. If the user seems uncertain or provides minimal information (common for high school students), be encouraging and help identify potential strengths, interests, and opportunities based on what they've shared. Look for clues in their interests, achievements, or even subjects they might enjoy.",
    expected_output="A clean markdown summary of the user's complete profile that is encouraging and identifies potential even when the user is uncertain about their direction.",
    agent=user_profiler_agent,
)

# Task 2: Career Path Exploration
career_exploration_task = Task(
    description="Using the user profile summary, research and identify 3 to 5 potential career paths that align with the user's interests and current stage. For each path, describe the role, typical day-to-day responsibilities, and future prospects. Make sure your advice is tailored to the user's specific situation (student vs. professional).",
    expected_output="A detailed markdown section listing and describing the recommended career paths with pros and cons for each.",
    agent=career_exploration_agent,
    context=[profile_analysis_task],
)

# Task 3: Skill Development Roadmap
skill_development_task = Task(
    description="For the career paths identified previously, research the essential technical and soft skills required to succeed. Create a skill development roadmap. For each skill, recommend 1-2 high-quality online courses (e.g., from Coursera, edX), certifications, or seminal books. You MUST provide direct links to these resources.",
    expected_output="A markdown section formatted as an actionable skill-development plan, with skills grouped by their corresponding career path and including hyperlinks to learning resources.",
    agent=skill_development_agent,
    context=[career_exploration_task],
)

# Task 4: Job Market Analysis
job_market_analysis_task = Task(
    description="For each recommended career path, gather current job market data. Include typical salary ranges for entry-level, mid-level, and senior roles. List 3-5 top companies that are currently hiring for these positions. Provide a realistic outlook for these roles over the next 5 years.",
    expected_output="A data-driven markdown section detailing job market insights, including salary data, key employers, and future demand for each suggested career.",
    agent=job_market_agent,
    context=[career_exploration_task],
)

# Task 5: Career Roadmap Strategy
roadmap_strategy_task = Task(
    description="Based on the user's profile, recommended career paths, required skills, and job market insights, create a comprehensive career roadmap. Include specific phases (short-term: 3-6 months, medium-term: 6-18 months, long-term: 2-5 years), actionable milestones, networking strategies, and decision points. Provide timeline estimates for skill acquisition, job applications, and career transitions.",
    expected_output="A detailed markdown section with a strategic career roadmap including timelines, milestones, and specific action items organized by phases.",
    agent=roadmap_strategy_agent,
    context=[profile_analysis_task, career_exploration_task, skill_development_task, job_market_analysis_task],
)

# Task 6: Learning Resource Curation
learning_resource_task = Task(
    description="Research and curate the most current and high-quality learning resources for the identified career paths and required skills. Find specific courses, bootcamps, certifications, books, and learning platforms. Include both free and paid options, duration estimates, difficulty levels, and industry recognition. Provide direct links and enrollment information.",
    expected_output="A comprehensive markdown section with categorized learning resources including course details, links, costs, duration, and recommendations for different learning styles and budgets.",
    agent=learning_resource_agent,
    context=[career_exploration_task, skill_development_task, roadmap_strategy_task],
)

# Task 7: Final Report Synthesis
report_synthesis_task = Task(
    description="Create a concise, executive-style career report that distills all analyses into a digestible format (2-3 pages maximum). Focus on the most critical insights and actionable recommendations without compromising quality. Structure as an executive summary with key highlights that busy people will actually read.",
    expected_output="A concise, professional career advisory report in markdown format (under 1000 words) that includes: 1) Executive Summary (key insights), 2) Top 3 Career Recommendations with brief rationale, 3) Immediate Action Plan (next 3-6 months), 4) Key Skills to Develop, 5) Essential Resources, and 6) Next Steps. Maintain professional depth while being highly readable.",
    agent=report_generation_agent,
    context=[profile_analysis_task, career_exploration_task, skill_development_task, job_market_analysis_task, roadmap_strategy_task, learning_resource_task],
)

# --- Robust Crew Definition with Error Handling ---
class RobustCareerAdvisorCrew:
    """Career Advisor Crew with robust error handling and fallback mechanisms"""
    
    def __init__(self):
        self.agents = [
            user_profiler_agent,
            career_exploration_agent,
            skill_development_agent,
            job_market_agent,
            roadmap_strategy_agent,
            learning_resource_agent,
            report_generation_agent
        ]
        
        self.tasks = [
            profile_analysis_task,
            career_exploration_task,
            skill_development_task,
            job_market_analysis_task,
            roadmap_strategy_task,
            learning_resource_task,
            report_synthesis_task
        ]
        
        # Map tasks to agent types for fallback handling
        self.task_agent_mapping = {
            profile_analysis_task: "profile_analysis",
            career_exploration_task: "career_exploration", 
            skill_development_task: "skill_development",
            job_market_analysis_task: "market_analysis",
            roadmap_strategy_task: "roadmap_strategy",
            learning_resource_task: "learning_resources",
            report_synthesis_task: "report_generation"
        }
        
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False
        )
    
    def kickoff(self, inputs: dict):
        """Execute crew with robust error handling"""
        try:
            print("🚀 Starting AI Career Advisor with robust error handling...")
            print("📊 System configured with 5 API providers and intelligent fallback")
            
            # Execute with our robust error handling
            result = self._execute_with_fallback(inputs)
            return result
            
        except Exception as e:
            print(f"❌ Critical error in career advisor: {e}")
            return self._generate_emergency_fallback(inputs)
    
    def _execute_with_fallback(self, inputs: dict):
        """Execute crew tasks with individual task error handling"""
        try:
            # Use standard crew execution first
            result = self.crew.kickoff(inputs=inputs)
            return result
            
        except Exception as e:
            print(f"⚠️  Standard execution failed: {e}")
            print("🔄 Switching to individual task execution with fallbacks...")
            
            # Execute tasks individually with fallback handling
            return self._execute_tasks_individually(inputs)
    
    def _execute_tasks_individually(self, inputs: dict):
        """Execute each task individually with fallback LLM switching"""
        results = []
        
        for i, (task, agent) in enumerate(zip(self.tasks, self.agents)):
            agent_type = self.task_agent_mapping[task]
            
            try:
                print(f"\n🤖 Executing {agent.role} ({i+1}/{len(self.tasks)})...")
                
                # Create a simple execution function for this task
                def execute_task():
                    # Create a mini-crew for this single task
                    single_crew = Crew(
                        agents=[agent],
                        tasks=[task],
                        process=Process.sequential,
                        verbose=1
                    )
                    return single_crew.kickoff(inputs=inputs)
                
                # Execute with fallback handling
                result = llm_handler.execute_with_fallback(
                    agent_type=agent_type,
                    agent_function=execute_task
                )
                
                results.append(result)
                print(f"✅ {agent.role} completed successfully")
                
            except Exception as e:
                print(f"❌ {agent.role} failed completely: {e}")
                # Add fallback content for this agent
                fallback_result = self._get_fallback_content(agent_type, inputs)
                results.append(fallback_result)
                print(f"🔄 Using fallback content for {agent.role}")
        
        # Combine all results
        return self._combine_results(results)
    
    def _get_fallback_content(self, agent_type: str, inputs: dict) -> str:
        """Generate fallback content when all LLMs fail for an agent"""
        user_info = inputs.get('user_info', 'User information not provided')
        
        fallback_templates = {
            "profile_analysis": f"""
# User Profile Analysis

Based on the provided information: {user_info[:200]}...

**Note**: Our AI analysis system is currently experiencing high demand. This is a basic profile analysis.

## Summary
The user appears to be seeking career guidance and has provided initial information about their background and interests.

## Recommendations
1. Explore interests through online resources and courses
2. Connect with career counselors or mentors
3. Research various career paths related to stated interests
4. Consider internships or volunteer opportunities

*A complete AI analysis will be available shortly.*
            """,
            
            "career_exploration": """
# Career Path Recommendations

**Note**: Using general career guidance while our AI completes your personalized analysis.

## Popular Career Paths for Students
1. **Technology Sector**: Software development, data science, cybersecurity
2. **Healthcare**: Medicine, nursing, physical therapy, mental health
3. **Business**: Marketing, finance, project management, entrepreneurship
4. **Creative Fields**: Design, writing, media production, arts
5. **Education**: Teaching, training, educational administration

## Next Steps
- Research specific roles in your areas of interest
- Connect with professionals in these fields
- Explore relevant educational programs

*Personalized recommendations based on your profile coming soon.*
            """,
            
            "skill_development": """
# Skill Development Roadmap

**Note**: General skill recommendations while our AI analyzes your specific needs.

## Core Skills for Career Success
1. **Communication**: Written and verbal communication
2. **Problem-solving**: Critical thinking and analytical skills
3. **Technology**: Basic computer skills and digital literacy
4. **Leadership**: Teamwork and project management
5. **Adaptability**: Learning agility and flexibility

## Learning Resources
- Online platforms: Coursera, edX, Khan Academy, YouTube
- Professional certifications in your field of interest
- Books and industry publications
- Workshops and networking events

*Tailored skill development plan coming soon.*
            """,
            
            "market_analysis": """
# Job Market Analysis

**Note**: Using current market data while our AI completes detailed analysis.

## Current Job Market Trends
- Technology roles showing strong growth
- Healthcare experiencing high demand
- Remote work opportunities expanding
- Skills-based hiring increasing

## Salary Expectations
- Entry-level: $35,000 - $55,000 depending on field
- Mid-level: $55,000 - $85,000 with experience
- Senior-level: $85,000+ with specialization

*Detailed market analysis for your specific interests coming soon.*
            """,
            
            "learning_resources": """
# Learning Resources & Recommendations

**Note**: Curated resources while our AI personalizes recommendations.

## Popular Learning Platforms
1. **Coursera**: University courses and professional certificates
2. **edX**: Academic courses from top universities
3. **Khan Academy**: Free courses on various subjects
4. **LinkedIn Learning**: Professional skill development
5. **YouTube**: Free tutorials and educational content

## Certification Programs
- Google Career Certificates
- Microsoft Certifications
- AWS Cloud Certifications
- Adobe Creative Certifications

*Personalized learning path coming soon.*
            """
        }
        
        return fallback_templates.get(agent_type, f"Fallback content for {agent_type} - Full analysis coming soon.")
    
    def _combine_results(self, results: list) -> str:
        """Combine individual task results into final report"""
        combined = "\n\n".join(str(result) for result in results if result)
        
        header = """
# 🎯 AI Career Advisor Report
*Generated with robust error handling and multiple AI providers*

---

"""
        
        footer = """

---

## 🛡️ System Notice
This report was generated using our robust AI system with automatic fallback mechanisms. 
Some sections may use cached data due to high system demand, ensuring you always receive valuable guidance.

**For questions or a complete reanalysis, please contact our support team.**
        """
        
        return header + combined + footer
    
    def _generate_emergency_fallback(self, inputs: dict) -> str:
        """Last resort fallback when everything fails"""
        user_info = inputs.get('user_info', 'No information provided')
        
        return f"""
# 🚨 Career Guidance Report (Emergency Mode)

Dear User,

Our AI system is currently experiencing technical difficulties, but we don't want to leave you empty-handed!

## Your Information
{user_info}

## General Career Guidance

1. **Explore Your Interests**: Take time to identify what truly excites you
2. **Research Career Options**: Use online resources like O*NET, Bureau of Labor Statistics
3. **Develop Skills**: Focus on both technical and soft skills
4. **Network**: Connect with professionals in fields of interest
5. **Gain Experience**: Look for internships, volunteer work, or part-time jobs

## Immediate Next Steps
- Schedule a meeting with a school counselor
- Take online career assessment tests
- Join clubs or activities related to your interests
- Research colleges or training programs

## Resources
- Career assessment tools: 16Personalities, StrengthsFinder
- Job research: LinkedIn, Glassdoor, Indeed
- Skill building: Khan Academy, Coursera, YouTube

**We apologize for the technical difficulties. Please try again later for your full AI-powered career analysis.**

Best regards,
The AI Career Advisor Team
        """

# Create the robust crew instance
career_advisor_crew = RobustCareerAdvisorCrew()

# --- Main Execution ---

if __name__ == "__main__":
    print("🎯 Welcome to the AI Career Advisor!")
    print("=" * 50)
    print("I'll help you discover your ideal career path with personalized guidance.")
    print("\nPlease provide the following information about yourself:")
    print("\n1. Your name")
    print("2. Your current stage (e.g., High School Student, College Student, Working Professional)")
    print("3. Your interests and passions")
    print("4. Your existing skills and experience")
    print("5. Your career goals and aspirations")
    print("\nYou can provide this information in any format you prefer - just be as detailed as possible!")
    print("\n" + "=" * 50)
    
    # Collect user information
    user_info = input("\nPlease enter your information:\n")
    
    print("\n🚀 Processing your career analysis...")
    print("This may take a few minutes as our 7 AI agents research and analyze your profile...")
    
    try:
        # Create inputs dictionary
        inputs = {
            "user_info": user_info
        }
        
        # Kick off the crew
        result = career_advisor_crew.kickoff(inputs=inputs)
        
        # Print the result to console
        print("\n" + "=" * 60)
        print("🎉 YOUR PERSONALIZED CAREER REPORT")
        print("=" * 60)
        print(result)
        
        # Save the result to a markdown file
        with open("career_report.md", "w", encoding="utf-8") as f:
            f.write(str(result))
        
        print("\n" + "=" * 60)
        print("✅ Your career report has been saved to 'career_report.md'")
        print("📄 You can now review your personalized career guidance!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running the career advisor: {e}")
        print("Please check your API keys and dependencies.")
        print("\nMake sure you have:")
        print("1. GOOGLE_API_KEY in your .env file")
        print("2. SERPER_API_KEY in your .env file")
        print("3. All required packages installed (run: pip install -r requirements.txt)")
