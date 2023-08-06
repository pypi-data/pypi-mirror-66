import json

student_data = {
    "1.FirstName": "Gildong",
    "2.LastName": "Hong",
    "3.Age": 20,
    "4.University": "Yonsei University",
    "5.Courses": [
        {
            "Major": "Statistics",
            "Classes": ["Probability",
                        "Generalized Linear Model",
                        "Categorical Data Analysis"]
        },
        {
            "Minor": "ComputerScience",
            "Classes": ["Data Structure",
                        "Programming",
                        "Algorithms"]
        }
    ]
}
with open("../test.json", "w") as json_file:
    json.dump(student_data, json_file)

temp_json = json.dumps(student_data, indent=4)
print(temp_json)
