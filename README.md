
# 🌍 WanderWise – Your Personalized Travel Companion

![WanderWise](./screenshots/wanderwise-banner.png)

### Introduction - Welcome to WanderWise! 🚀  
Your go-to platform for exploring countries based on your preferences. With WanderWise, you’ll not only get country recommendations but also discover must-visit places and local foods to try.

---

## 🎯 Project Inspiration

As a passionate traveler and tech enthusiast, I’ve always been fascinated by how technology can simplify complex decisions. WanderWise was born out of my personal challenge of finding countries to visit that align with my interests—beyond the usual tourist traps.

In today’s fast-paced world, we want recommendations tailored to our likes and dislikes, not generic advice. WanderWise bridges that gap by asking for your preferences in climate, continent, and returning **personalized country suggestions** along with **food and activity recommendations**.

> **Challenge:** How can we create a recommendation system that gives users not just a list of countries, but also an a feel of the country in its rich description and local cuisine?

---

## 🚀 Deployed Site & Blog Article
[link-1]
https://dev.to/ebitech02/wanderwise-app-mf1

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript 
- **Backend:** Flask (Python) with integrated APIs
- **APIs:**
  - [RestCountries API](https://restcountries.com) for country data (flag, capital, currency, etc.)
  - [OpenTripMap API](https://opentripmap.io) for notable places and activities
  - [WikiVoyage API](https://wikivoyage.org) for enriched country descriptions
  - [Spoonacular API](https://spoonacular.com) for local food suggestions 

---

## 🧠 The Algorithm

At its core, WanderWise is powered by a **simple recommendation algorithm**. The app compares user preferences (like climate and continent) with available country data and selects the best match. Here's a brief breakdown of how it works:

1. **User Input:**
   - Preferred continent
   - Climate type (e.g., tropical, temperate)
   
2. **Data Collection:**
   - Using the **RestCountries API**, we fetch country details like name, capital, and latitude/longitude.
   - **OpenTripMap** fetches notable places to visit, using country latitude/longitude as parameters.
   - If available, **WikiVoyage** provides a detailed description of the country; otherwise, we display a default message to "check the country's official website."

3. **Recommendation Generation:**
   - Matching user preferences with country data using a scoring mechanism.
   - Countries are sorted by their compatibility with the user's input.
   - The top matches are displayed with **images of the country flag**, **capital**, **currency**, and **suggested cuisine**.

4. **Food and Activities:** 
   - We use **Spoonacular API** to fetch local food suggestions, though currently, it’s underperforming in returning accurate results.
   - In case no notable activities are found, a message will guide users to check more details online.

---

## 🤯 Challenges Faced

Developing WanderWise wasn’t without its hurdles. Here are a few major ones:

- **API Integrations**: Initially, it was tricky to synchronize different APIs and ensure they returned consistent data. Particularly, Spoonacular was challenging as it barely provided accurate food recommendations for many countries.
- **Latitude/Longitude Handling**: Encountered issues with missing latitude and longitude data, which was resolved by fetching those details via the **RestCountries API**.
- **Error Handling**: Managing API failures gracefully, especially when one API didn’t return data, was an ongoing effort. Adding default messages ensured a smooth user experience.
  
   > "When the going gets tough, the tough get debugging! 🛠️"

---

## 💡 What’s Next?

This is just the beginning for WanderWise! Future iterations will include:

- **Enhanced Recommendation Engine**: Incorporating **machine learning** with **scikit-learn** or **TensorFlow** to improve the accuracy of suggestions based on user behavior and feedback.
- **Database Integration**: PostgreSQL for user preferences and Redis for caching country data.
- **Local Hotel and Restaurant Recommendations**: Integrating APIs like **Booking.com** or **Yelp** for deeper recommendations.
- **User Accounts**: So users can save their travel preferences and get updated suggestions based on new data.

---

## 📸 Screenshots

### WanderWise Home Page
![Home Page](./screenshots/wanderwise-home.png)

### Country Recommendations
![Recommendations](./screenshots/wanderwise-recommendations.png)

---

## 🎉 Timeline & Reflection

I began this project with an ambitious goal of creating a personalized travel recommendation app in under six weeks. It wasn’t always smooth sailing—I spent countless late nights troubleshooting API issues, but it was incredibly rewarding. 

I look forward to continuing WanderWise's development and seeing where this journey takes me. More than anything, I’m proud of how I’ve grown as a developer through this project and hope to continue building solutions that excite and inspire users.

> “Travel is the only thing you buy that makes you richer.” 🌍

---

## 🙋‍♂️ Meet the Developer

HI!, My Name is Precious Oromoni and I’m a software engineer with a passion for building tools that make life easier. My work on WanderWise helped me deepen my skills in **Python**, **API integrations**, and **user-centric design**. When I’m not coding, I’m probably reading fictions novels or playing chess.

Connect with me on [LinkedIn](https://linkedin.com) or check out my other projects [here](https://github.com/ebitech02/).


## 💻 Installation
To get WanderWise running on your local machine:

1. **Clone the repository**:
    git clone https://github.com/yourusername/wanderwise.git

2. **Navigate to the project directory**:
    cd wanderwise

3. **Activate Virtual Environment**:
    python3 -m venv wanderwise-venv
    source wanderwise-venv/bin/activate
   for windows - 
      wanderwise-env\Scripts\activate

4. **Install the required dependencies**:
   pip install -r requirements.txt
5. **Run flask application**:
   python run.py

## 🛠️ Usage
Once the app is running, follow these steps:

Input your travel preferences: Choose your desired climate and continent.
Get recommendations: WanderWise will suggest countries based on your preferences, along with additional information like notable places and foods.
Explore details: Each recommendation provides the country’s flag, capital, currency, and local attractions.

## 🤝 Contributing
1. Contributions are welcome! Here’s how you can contribute:
2. Fork the repository.
3. Create a feature branch (git checkout -b feature-branch).
4. Make your changes and commit (git commit -m "Your message").
5. Push to your branch (git push origin feature-branch).
6. Submit a pull request.

## 🔗 Related Projects
If you like WanderWise, check out these other travel-related projects:

1. NomadList: A crowdsourced database of cities for digital nomads.
2. TripIt: A tool to organize your travel plans.
3. WikiVoyage: A free, worldwide travel guide.

## 📄 Licensing
This project is licensed under the MIT License. See the LICENSE file for more details.

---

Thanks for visiting WanderWise! If you have any feedback or suggestions, I’d love to hear from you! 😊

