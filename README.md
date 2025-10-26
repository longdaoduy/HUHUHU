# HUHUHU
# Tourism Helper Application

A comprehensive tourism application that helps users plan their trips, recognize landmarks, and manage their travel photos.

## Features

### 1. Image Recognition
- Upload images to identify landmarks
- Preview uploaded images
- Get AI-powered landmark recognition results

### 2. Travel Recommendations
- Get suggestions for tourist attractions within a specified radius
- Filter by province/city
- View ratings and sample reviews for each location
- Intelligent recommendations based on user preferences and location

### 3. Photo Album Management
- Create and manage multiple photo albums
- Bulk photo upload support
- Preview photos in a grid layout
- Download entire albums as ZIP files
- Automatic timestamp tracking for uploads

## Project Structure

```
prj/
├── demo.py           # Main Streamlit application
ai_recommend.py       # AI-powered recommendation engine
```

## Technologies Used

- Python
- Streamlit - Web application framework
- OpenAI API - For AI-powered image recognition
- PIL (Python Imaging Library) - Image processing
- Mathematical calculations for distance (Haversine formula)

## Setup and Installation

1. Install the required dependencies:
```bash
pip install streamlit pillow openai
```

2. Configure your OpenAI API key in the relevant files

3. Run the application:
```bash
streamlit run demo.py
```

## Features in Detail

### Image Recognition
The application uses OpenAI's API to recognize landmarks in uploaded images, providing quick and accurate identification of tourist locations.

### Location-Based Recommendations
- Uses the Haversine formula to calculate distances
- Provides recommendations within specified radius
- Includes ratings and user reviews
- Supports multiple provinces/cities in Vietnam

### Photo Album Management
- Create multiple albums
- Bulk upload support
- Preview functionality
- ZIP download option
- Timestamp tracking

## Navigation

The application features an intuitive sidebar navigation with the following sections:
- Home
- Image Recognition
- Travel Recommendations
- Photo Albums

## Data Management

- Session state management for albums
- Local data storage for attractions
- Coordinates system for major cities
- User preference handling

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is proprietary and confidential. All rights reserved.
