# ♻️ Djen Subnet – Waste Management on CommuneAI

Djen is a decentralized AI-powered subnet built on CommuneAI to address real-world **waste management** challenges. Citizens can report illegal dumping, missed collections, or overflowing bins via image input. Djen uses machine learning to classify the issues and reward participation through tokens.

---

## 🚀 Features

- Image classification of waste-related incidents
- Incentivized civic reporting via miners
- Validator-powered output accuracy & emissions

---

### Prerequisites  

Ensure you have **Python 3.10+** installed on your system. You can verify this by running:  

```sh
python --version
```

### Installation  

Clone the repository to your local machine:  

```sh
git clone https://github.com/Djunenv/djen.git
cd djen
```

## Install required dependencies:

```sh
pip install -r requirements.txt
```
## Validator Setup
Run the validator script to start validating predictions. Replace <name-of-your-com-key> with your actual key:
```
comx -t module serve djen.validator.djenvali.Validator  djen --ip 0.0.0.0  --port 8000 --subnets-whitelist 21
```
## Miner Setup
Run the validator script to start validating predictions. Replace <name-of-your-com-key> with your actual key:
```
comx -t module serve luminar.miner.lumimine.Miner  my-wallet --ip 0.0.0.0  --port 8001 --subnets-whitelist 21
```
