import streamlit as st
import json
import operator

OPERATORS = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne
}

def evaluate_applicant(applicant_data, rules):
    """
    Evaluates the applicant data against a set of sorted rules.
    Highest priority rule that matches all conditions is executed.
    """
   
    sorted_rules = sorted(rules, key=lambda x: x["priority"], reverse=True)
    
    for rule in sorted_rules:
        conditions_met = True
        for condition in rule["conditions"]:
            attr, op_str, req_val = condition
            
           
            if attr not in applicant_data:
                conditions_met = False
                break
                
            app_val = applicant_data[attr]
            
            
            if not OPERATORS[op_str](app_val, req_val):
                conditions_met = False
                break
                
        if conditions_met:
            return rule["name"], rule["action"]
            
    return "No match", {"decision": "NO AWARD", "reason": "Applicant did not meet any existing rule criteria."}

def main():
    st.set_page_config(page_title="Scholarship Advisory System", layout="wide")
    st.title("🎓 Rule-Based Scholarship Advisory System")
    st.markdown("This decision support tool evaluates applicant eligibility using a transparent rule-based engine.")

   
    st.sidebar.header("Applicant Profile")
    cgpa = st.sidebar.number_input("Cumulative GPA (CGPA)", min_value=0.0, max_value=4.0, value=3.5, step=0.01)
    family_income = st.sidebar.number_input("Monthly Family Income (RM)", min_value=0, value=5000, step=100)
    co_curricular_score = st.sidebar.number_input("Co-curricular Score (0-100)", min_value=0, max_value=100, value=75, step=1)
    disciplinary_actions = st.sidebar.number_input("Disciplinary Actions", min_value=0, value=0, step=1)
    
    applicant_data = {
        "cgpa": cgpa,
        "family_income": family_income,
        "co_curricular_score": co_curricular_score,
        "disciplinary_actions": disciplinary_actions
    }

   
    st.subheader("Rule Configuration (JSON Editor)")
    
    default_rules = [
        {
            "name": "Top merit candidate",
            "priority": 100,
            "conditions": [
                ["cgpa", ">=", 3.7],
                ["co_curricular_score", ">=", 80],
                ["family_income", "<=", 8000],
                ["disciplinary_actions", "==", 0]
            ],
            "action": {
                "decision": "Full Scholarship",
                "reason": "Excellent academic & co-curricular performance, with acceptable need"
            }
        },
        {
            "name": "Good candidate partial scholarship",
            "priority": 80,
            "conditions": [
                ["cgpa", ">=", 3.3],
                ["co_curricular_score", ">=", 60],
                ["family_income", "<=", 12000],
                ["disciplinary_actions", "<=", 1]
            ],
            "action": {
                "decision": "AWARD PARTIAL",
                "reason": "Good academic & involvement record with moderate need"
            }
        },
        {
            "name": "Need-based review",
            "priority": 70,
            "conditions": [
                ["cgpa", ">=", 2.5],
                ["family_income", "<=", 4000]
            ],
            "action": {
                "decision": "REVIEW",
                "reason": "High need but borderline academic score"
            }
        },
        {
            "name": "Low CGPA not eligible",
            "priority": 95,
            "conditions": [
                ["cgpa", "<", 2.5]
            ],
            "action": {
                "decision": "REJECT",
                "reason": "CGPA below minimum scholarship requirement"
            }
        },
        {
            "name": "Serious disciplinary record",
            "priority": 90,
            "conditions": [
                ["disciplinary_actions", ">=", 2]
            ],
            "action": {
                "decision": "REJECT",
                "reason": "Too many disciplinary records"
            }
        }
    ]

    rules_json_str = st.text_area("Edit rules here to adjust the academic and financial aid committee requirements:", 
                                  value=json.dumps(default_rules, indent=4), height=400)
    
    
    st.subheader("Evaluation Result")
    if st.button("Evaluate Applicant", type="primary"):
        try:
            
            rules = json.loads(rules_json_str)
            
            
            triggered_rule, action = evaluate_applicant(applicant_data, rules)
            
            
            st.success(f"**Decision:** {action['decision']}")
            st.info(f"**Reason:** {action['reason']}")
            st.caption(f"**Rule Triggered:** {triggered_rule}")
            
        except json.JSONDecodeError:
            st.error("Invalid JSON format in the rule editor. Please check your syntax.")
        except Exception as e:
            st.error(f"An error occurred during evaluation: {str(e)}")

if __name__ == "__main__":
    main()
