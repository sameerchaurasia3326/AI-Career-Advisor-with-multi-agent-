# AI Career Advisor

A comprehensive multi-agent AI system that provides personalized and actionable career advice using CrewAI framework.

## Features

- **Multi-Agent Architecture**: 5 specialized AI agents working together
- **Personalized Guidance**: Tailored advice for high school students, college students, and working professionals
- **Real-time Research**: Uses Brave Search for current market data and trends
- **Comprehensive Reports**: Detailed markdown reports with actionable insights

## Screenshots

### Demo Landing Page
![Demo Page](careeradvisor/Screenshot%202025-10-06%20at%202.12.09%20AM.png)

### Main Application Interface
![Main App](careeradvisor/Screenshot%202025-10-06%20at%202.07.02%20AM.png)

### Career Analysis Process
![Analysis Process](careeradvisor/Screenshot%202025-10-06%20at%202.06.19%20AM.png)

### Report Generation
![Report Generation](careeradvisor/Screenshot%202025-10-06%20at%202.05.44%20AM.png)

### Results Display
![Results](careeradvisor/Screenshot%202025-10-06%20at%202.05.05%20AM.png)

### API Testing
![API Testing](careeradvisor/Screenshot%202025-10-06%20at%202.03.21%20AM.png)

## Agent Roles

1. **User Profiler Agent**: Analyzes user background and creates structured profiles
2. **Career Exploration Agent**: Researches and identifies suitable career paths
3. **Skill Development Agent**: Recommends learning resources and skill development plans
4. **Job Market Insights Agent**: Provides current market data and salary information
5. **Report Generation Agent**: Synthesizes all information into comprehensive reports

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   - Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Get a Brave Search API key from [Brave Search API](https://brave.com/search/api/)
   - Update the `.env` file with your actual API keys

3. **Run the Career Advisor**:
   ```bash
   python main.py
   ```

## Usage

1. Run the script and follow the prompts
2. Provide detailed information about yourself including:
   - Your name and current stage (student/professional)
   - Your interests and passions
   - Existing skills and experience
   - Career goals and aspirations
3. The AI agents will analyze your profile and generate a comprehensive career report
4. The report will be saved as `career_report.md`

## Output

The system generates a detailed markdown report containing:
- Personalized profile analysis
- Recommended career paths with pros/cons
- Skill development roadmap with learning resources
- Current job market insights and salary data
- Actionable next steps

## Requirements

- Python 3.8+
- Google Gemini API key
- Brave Search API key
- Internet connection for real-time research
