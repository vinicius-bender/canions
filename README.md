## 🌐 Access to Production Platform  

The application is publicly available at the following address:  

🔗 **[https://faunasul.com.br/](https://faunasul.com.br/)**  

---

# 🌿 Citizen Science Platform – FaunaSul  
This project is a collaborative web platform developed as part of the Final Undergraduate Project (TCC) of the Information Systems program at UFSM. Its goal is to enable citizens to contribute records of fauna observed within the territory of the *Caminhos dos Cânions do Sul* Geopark.  

## 📌 Objective  

To facilitate the collection, storage, and analysis of local fauna data through citizen science, promoting community engagement and supporting environmental conservation actions.  

## 🔍 Features  

- Submission of observations with photos, videos, and geolocation  
- Review and validation by specialists  
- Recording of taxonomic information (family, genus, species)  
- Species listing and observation history  
- Admin dashboard with user and data management  
- Mechanism for promoting users to the specialist role  

## 🧰 Technologies Used  

- **Backend**: Python, Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: PostgreSQL  
- **Maps**: OpenStreetMap + Leaflet.js  
- **Hosting**: Ubuntu VPS with Docker and Nginx (production)  

## 🗺️ Target Audience  

Citizens, tourists, researchers, environmentalists, and managers of the *Caminhos dos Cânions do Sul* Geopark.  

## 👤 Test Accounts  

You can use the following credentials to access the platform with different user profiles (creating an account is not required to report an observation on the platform):  

| User Type            | Email                          | Password |
|----------------------|--------------------------------|----------|
| Regular User         | usuarioteste@example.com       | 123      |
| Specialist           | usuarioespecialista@example.com| 123      |
| Scientist            | usuariocientista@example.com   | 123      |
| Admin (staff)        | admin@example.com              | admin    |  

---

## 🧩 Custom Admin Dashboard  

An integrated admin dashboard is also available within the application:  

🔗 **[https://faunasul.com.br/painel_administrador](https://faunasul.com.br/painel_administrador)**  

In this dashboard it is possible to:  
- Register taxonomic hierarchies (family, genus, species);  
- View and evaluate pending observations;  
- Promote users to roles such as specialist or scientist.  

---

## 🐾 Application Flow  

1. The **administrator registers taxonomic hierarchies** in the dashboard.  
2. **Users submit observations**, including media files, location, and description.  
3. Observations are assigned the **"Pending"** status.  
4. The **admin, specialist, or scientist** reviews the observation (approving or rejecting it).  
5. If approved, the observation will appear in:  
   - **"All Observations"**  
   - **"My Observations"** (visible only to the author)  
   - **Interactive map** on the homepage  

---

## 🔮 Future Implementations  

Some planned and potential improvements for the platform include:  

- **AI-Powered Validation**: Implementing machine learning models to automatically classify and validate species in submitted photos and videos, assisting specialists in the review process.   
- **Gamification**: Adding achievements, ranking, and reward systems to encourage community engagement and continuous participation.  
- **Data Visualization Dashboards**: Advanced charts and heatmaps for researchers and managers to analyze temporal and spatial trends of fauna observations.  
- **Open Data API**: Providing an API for researchers and institutions to access and integrate observation data into their own studies or conservation projects.   
- **Multilingual Support**: Expanding language options. 
- **Citizen Feedback System**: Allowing observers to receive updates on the status of their contributions and recognition when their records are used in research or reports.  

---

Developed by Vinicius Rodolfo Bender Carlson as part of the Final Undergraduate Project of the Information Systems program at UFSM (*Universidade Federal de Santa Maria*).  
