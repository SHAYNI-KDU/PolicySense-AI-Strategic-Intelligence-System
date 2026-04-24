PolicySense AI: Strategic Intelligence System
PolicySense AI is a specialized tool designed to transform dense, unstructured policy documents into actionable strategic insights. By leveraging Large Language Models (LLMs) and advanced NLP preprocessing, the system automates metadata extraction, generates executive summaries, and provides an interactive scenario-based chatbot for policy testing.

Key Features
Automated Metadata Extraction: Instantly identifies Policy Title, Timeframe, and Primary Focus from raw PDF data.

Structured Executive Summaries: Uses Gemini 1.5 Flash to distill 20+ page documents into clear, high-level summaries.

Scenario-Based Chatbot: An interactive simulation environment allowing users to test how policies apply to real-world situations.

NLP Cleaning Pipeline: A custom Regex-based sanitization engine that removes PDF noise (headers, footers, page numbers) for higher AI accuracy.

Stateful UX: Implements Session State management to maintain document context across continuous user interactions.

Tech Stack
Frontend: Streamlit (Python-based Web Dashboard)

AI Engine: Google Gemini 1.5 Flash API

Data Processing: PyPDF2 (Parsing) & Regular Expressions (Cleaning)

State Management: Streamlit Session State

 How It Works
Upload: User uploads a PDF policy document via the sidebar.

Sanitize: The system runs a re (Regex) pipeline to clean the text.

Analyze: A single, optimized JSON prompt is sent to the Gemini API to extract metadata and summaries.

Interact: The user can then query the "Scenario Chatbot" to explore specific policy implications.
