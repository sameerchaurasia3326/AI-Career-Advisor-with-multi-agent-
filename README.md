<img width="1710" height="1112" alt="Screenshot 2025-10-06 at 2 34 02 AM" src="https://github.com/user-attachments/assets/51df0ce8-9ccb-4e44-a529-673cda7d2698" /><img width="1706" height="923" alt="Screenshot 2025-10-06 at 2 07 02 AM" src="https://github.com/user-attachments/assets/063ba097-4b30-4f36-8a41-4108a5f28e4d" /># AI Career Advisor

A comprehensive multi-agent AI system that provides personalized and actionable career advice using CrewAI framework.

## Features

- **Multi-Agent Architecture**: 5 specialized AI agents working together
- **Personalized Guidance**: Tailored advice for high school students, college students, and working professionals
- **Real-time Research**: Uses Brave Search for current market data and trends
- **Comprehensive Reports**: Detailed markdown reports with actionable insights


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

## career_advisor_images

<img width="1709" height="925" alt="Screenshot 2025-10-06 at 2 03 21 AM" src="https://github.com/user-attachments/assets/2c342c01-bee3-470a-9474-2b94620da5e1" />
<img width="1685" height="933" alt="Screenshot 2025-10-06 at 2 05 05 AM" src="https://github.com/user-attachments/assets/23fdd7a6-9f19-4e9e-adc7-c5ec1122ef3d" />
<img width="1708" height="928" alt="Screenshot 2025-10-06 at 2 05 44 AM" src="https://github.com/user-attachments/assets/1c57a164-a573-477a-b27f-f99a043a53f6" />
<img width="1710" height="926" alt="Screenshot 2025-10-06 at 2 06 19 AM" src="https://github.com/user-attachments/assets/acb89ddd-013a-40ea-aa24-3c33c3da71d0" />
<img width="1706" height="923" alt="Screenshot 2025-10-06 at 2 07 02 AM" src="https://github.com/user-attachments/assets/7dd9eb81-9530-4bf2-b472-3e44a4e3398b" />
<img width="1710" height="1112" alt="Screenshot 2025-10-06 at 2 34 02 AM" src="https://github.com/user-attachments/assets/0f171ec6-2a35-4f53-9a13-9f595d692661" />
