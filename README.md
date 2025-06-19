# Data-Meter (Python)

### Problem Statement
Telecom operators collect large volumes of data usage logs from mobile towers, detailing consumption across different technologies (4G/5G) and scenarios (Home/Roaming). The goal is to:
1. Process multiple large log files (100K–200K rows each).
2. Aggregate data usage per mobile number, categorized as:<br>
4G Home<br>
5G Home<br>
4G Roaming<br>
5G Roaming<br>
3. Calculate billing costs with:<br>
Different rates for 4G/5G<br>
Roaming premiums (10% for 4G, 15% for 5G)<br>
Overage charges (5% if usage exceeds a threshold)

### Solution
The code processes the files, Aggregates the data usage for all mobile numbers using Dictionaries, Calculates the cost and generates the final report

### TO RUN THE CODE:<br>
1. Prerequisites: Git , pip , Python 3.10+ <br>
2. Install pytest (pip i pytest)
3. Clone the repo<br>
4. Insert /input/data.txt<br>
5. built and run : <br>
   a. Create a virtual environment (venv)<br> : python -m venv venv <br>
   venv\Scripts\activate
   b. python main.py
5. Check report in /output/report.txt<br>

### Components
<br>
usage_record.py: Represents a single log entry<br>
user_data.py: Stores aggregated usage per mobile number<br>
data_processor.py: Aggregates usage records into UserData objects<br>
billing_service.py: Calculates costs<br>
usage_datareader.py: Reads and parses input files<br>
report_generator.py: Writes the final report<br>
exception.py: Handles exceptions<br>
tests: Folder that contains unit tests for all units


### For Configuration:<br>
edit /src/main/resources/config.ini<br>
Rates per KB  <br>
g4.rate=0.1  <br>
g5.rate=0.2  <br>

Roaming premiums  <br>
roaming.g4.multiplier=1.10  <br>
roaming.g5.multiplier=1.15  <br>

Overage (5% extra if usage > 100MB)  <br>
overage.multiplier=1.05  <br>
overage.threshold=100000  <br>
<br>

### For Unit testing: pytest -v
