# Run unit tests
pip install -r requirements.txt
python3 -m pytest text_analysis/tests.py word_count/tests.py entity_recognition/tests.py sentiment_analysis/tests.py
