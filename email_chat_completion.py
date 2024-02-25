import json
from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import logging
  
app = Flask(__name__)
CORS(app, supports_credentials=True)
CORS(app)
app.config['SECRET_KEY'] = 'sampleee1'

@app.route('/connectorMailTag/email_summarizer', methods=['POST'])
def email_summarizer():
    logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    logging.info ("Entering email_sumamrizer API call ")
    email = request.json['email']
    subject=request.json['subject']
    print(subject)
    try:
        client = OpenAI(
                    api_key='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',
                )
        prompt="""
                expected output format is, if information is not available, do create new information. Stick to the given format ONLY.
                The date format should be MM/dd format only like 
                    03rd September : 09/03
                    Mar 12th : 03/12
                    March 12th, 2024 : 03/12
                    03/11/2024: 03/11
                    5th Sept 2024 : 09/05
                {
                    "SubjectMatter": "The subject matter of the email is the response to an invitation to an exclusive property showcase event. The sender, Venkatesh, expresses his interest in attending the event, particularly to view the waterfront homes. He also mentions his interest in discussing financing options and potential for renovations on older properties.",
                    "RequiredActions": "Prepare for Venkatesh's attendance at the property showcase event, including arranging personalized tours. Be ready to discuss financing options and renovation potentials for older properties.",
                    "NotesDescription:"High level summary of the mail from Venkat, expressing his interest in attending the tour",
                    "EventSubject":"Home tour , name of the property", Discover Your Dream Home
                    "TaskSubject":""
                    "Meetings": {
                        "Date": "MM/dd",
                        "StartTime": "10:00 AM",
                        "EndTime": "02:00 PM"
                        "Participants": ["Venkatesh", "Narasimha"]
                    "UrgencyLevel": "Medium"                                        
                }
            """

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content":f'{prompt}{email}{subject}'
                    }
            ],
            model="gpt-4",
            )
        print(completion)
        response=completion.choices[0].message.content       
        return response       
    except Exception as e:
        logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)
        logging.error("Exception has occured")
        print(e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
   