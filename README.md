# **Unified API Middleware**

## **Overview**
The Unified API Middleware provides a robust solution for calculating postage rates by integrating multiple courier services.

At this moment, the API supports **domestic postage within Malaysia only (CityLink, Poslaju and J&T)**. In future updates, it will support **international postage** for various couriers.

---

## **Key Features**

- **Domestic Postage Support**:
  - Calculate rates for parcels and documents within Malaysia.

- **Middleware for Enhanced Performance**:
  - Caching with Redis to optimize repeated requests.
  - Rate limiting to ensure fair usage and API security.

- **Scalable Design**:
  - API versioning for seamless updates.
  - Ready for future international postage expansion.

---

## **Getting Started**

### **Setup Instructions**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lvkmannn/unified_API.git
   cd unified_API
   ```

2. **Install Dependencies**:
   - Using a Python virtual environment:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     pip install -r requirements.txt
     ```

3. **Run the Middleware**:
   - Locally:
     ```bash
     uvicorn app.main:app --reload --port 8080
     ```
   - Docker:
     ```bash
     docker-compose up --build
     ```

4. **Verify the Server**:
   - Visit: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

---

## **API Endpoint**

### **Get Rates**
**Endpoint**: `POST /api/v1/get-rates`

**Example Request**:
```bash
curl -X POST http://127.0.0.1:8080/api/v1/get-rates \
-H "Content-Type: application/json" \
-d '{
    "package_type": "parcel",
    "origin": {
        "postcode": "77400",
        "state": "Johor"
    },
    "destination": {
        "postcode": "47130",
        "state": "Selangor"
    },
    "package": {
        "weight": 24,
        "dimensions": {
            "length": 1,
            "width": 2,
            "height": 3
        }
    }
}'
```

**Example Response**:
```json
{
    "data": [
        { "courier": "citylink", "rate": 53.0 },
        { "courier": "jt", "rate": 46.64 },
        { "courier": "poslaju", "rate": 59.91 }
    ]
}
```

---

## **Documentation**
For detailed setup, testing instructions, and payload validation rules, refer to the [Wiki](https://github.com/lvkmannn/unified_API/wiki).

---

## **Future Plans**
- **International Postage Support**:
  - Expand API functionality to handle international deliveries based on courier.

- **New Features**:
  - Dynamic rate calculation for insurance coverage.
  - Integration with additional couriers.

---

## **Contributing**
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with a detailed explanation.

---

## **Contact**
For questions, issues, or suggestions, please open an issue on [GitHub](https://github.com/lvkmannn/unified_API/issues) or email me at `lnhafizramli@gmail.com`.

