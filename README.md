# Fetch Points Reward System

Author: Nikit Bobba

I have created a Python webservice for processing receipts and calculating the total reward points. I have decided to build this using **FastAPI**. It is packaged in **Docker**, so you only need **Docker installed** to run it.

---

## **Running the Web Service with Docker**
### **Clone the Repository**
First, pull the repository from GitHub:
```bash
git clone https://github.com/nikitbobba/fetch-points-reward-system.git

cd fetch-points-reward-system
```

### **Build the Docker Image**
Run this command inside the project directory
```bash
docker build -t fetch-points-reward-system .
```

### **Run the Docker Container**
Start the service by running this command
```bash
docker run -d -p 8000:8000 fetch-points-reward-system
```

## **Making API Calls**
### **Open FastAPI Swagger Docs**
You can explore the APIs via your browser here
```bash
http://localhost:8000/docs
```

### **Process a Receipt**
```bash
curl -X 'POST' 'http://localhost:8000/receipts/process' \
-H 'Content-Type: application/json' \
-d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}'
```

### **Get Receipt Points**
Use the "id" from the previous step:
```bash
curl -X 'GET' 'http://localhost:8000/receipts/{id}/points'

```