# SpeciesSense: ML Species Prediction Web App

A Flask web application that predicts a species from user-supplied measurements using a trained scikit-learn model. It is packaged with Docker and deployed on AWS (ECR + EC2).

> **Note:** Edit the "Dataset and Features" section below to match the data your model was trained on.

## Live Demo

http://107.22.132.11:5000

> This runs on an AWS EC2 instance that is stopped when not in use, and its public IP changes on every restart. If the link does not load, the instance is likely stopped. Run the project locally using the steps below.

## How It Works

1. The user enters measurements in the web form.
2. The Flask backend scales the input with a saved `MinMaxScaler`.
3. A saved `LogisticRegression` model predicts the class.
4. A saved `LabelEncoder` converts the prediction back to the species name, which is shown on the page.

The trained objects are stored as `model.joblib`, `scaler.joblib`, and `encoder.joblib`.

## Technologies Used

| Area | Technology |
|------|------------|
| Language | Python 3.12 |
| Web framework | Flask |
| Machine learning | scikit-learn (LogisticRegression, MinMaxScaler, LabelEncoder) |
| Model storage | joblib |
| Frontend | HTML, CSS, JavaScript (Flask templates and static files) |
| Containerization | Docker |
| Image registry | Amazon ECR |
| Hosting | Amazon EC2 (Ubuntu) |
| Access control | AWS IAM (role for EC2 to pull from ECR) |

## Project Structure

```
.
├── app.py              # Flask app and prediction logic
├── templates/          # HTML pages
├── static/             # CSS / JS / images
├── model.joblib        # Trained classifier
├── scaler.joblib       # Fitted MinMaxScaler
├── encoder.joblib      # Fitted LabelEncoder
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build instructions
└── .dockerignore
```

## Run Locally (without Docker)

```bash
git clone https://github.com/YOUR_USERNAME/speciessense.git
cd speciessense
python -m venv venv
venv\Scripts\activate        # Windows (use: source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Run with Docker

```bash
docker build -t speciessense .
docker run -d -p 5000:5000 --name speciessense speciessense
```

Open http://localhost:5000

## Deploy to AWS (ECR + EC2)

**1. Create an ECR repository** named `flask-app` in your region (for example `ap-south-1`).

**2. Log in, build, and push the image** (from your PC):

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
docker build -t ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest .
docker push ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest
```

**3. Launch an EC2 instance** (Ubuntu, t3.micro) with:
- An IAM role that has `AmazonEC2ContainerRegistryReadOnly`
- A Security Group allowing SSH (22) and Custom TCP (5000)

**4. On the EC2 instance:**

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo snap install aws-cli --classic

aws ecr get-login-password --region ap-south-1 | sudo docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
sudo docker pull ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest
sudo docker run -d --name flask-app -p 5000:5000 --restart unless-stopped ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest
```

**5. Open** `http://<EC2_PUBLIC_IP>:5000`

Replace `ACCOUNT_ID` with your 12-digit AWS account ID.

## Updating the Deployment

Rebuild and push from your PC, then on EC2 run:

```bash
sudo docker pull ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest
sudo docker rm -f flask-app
sudo docker run -d --name flask-app -p 5000:5000 --restart unless-stopped ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-app:latest
```

## Notes and Limitations

- Models were trained with scikit-learn 1.6.1, so `requirements.txt` pins that version to avoid unpickling warnings.
- The app uses Flask's built-in server, which is fine for demos. For production use gunicorn behind Nginx or a load balancer with HTTPS.
- Never commit AWS keys, `.env` files, or other secrets.

## Future Improvements

- Serve with gunicorn and add HTTPS
- Add CI/CD with GitHub Actions to build and push to ECR automatically
- Add input validation and automated tests

## Author

Manya
