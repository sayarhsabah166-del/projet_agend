from app.graph import graph

initial_state = {

    "patient_case": "Fièvre et toux depuis 3 jours",

    "question_count": 0,

    "patient_answers": []
}

result = graph.invoke(initial_state)

print("\n")
print(result["final_report"])