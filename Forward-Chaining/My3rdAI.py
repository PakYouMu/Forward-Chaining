# import json
# import re

# # Load existing knowledge from a JSON file if available
# def load_knowledge_base(filename):
#     try:
#         with open(filename, 'r') as file:
#             knowledge_base = json.load(file)
#         return knowledge_base
#     except FileNotFoundError:
#         return {
#             "facts": [],
#             "rules": [],
#         }

# # Save the knowledge base to a JSON file
# def save_knowledge_base(kb, filename):
#     with open(filename, 'w') as file:
#         json.dump(kb, file, indent=4)

# # Function to clear the contents of the knowledge base JSON file
# def clear_knowledge_base(filename):
#     knowledge_base = {
#         "facts": [],
#         "rules": [],
#     }
#     save_knowledge_base(knowledge_base, filename)
#     print("Contents of the knowledge base cleared.")

# # Function to display facts and rules
# def display_knowledge_base(kb):
#     print("Facts:")
#     for fact in kb["facts"]:
#         print(f"- {fact}")
#     print("\nRules:")
#     for rule in kb["rules"]:
#         statement = rule.get("statement", "")
#         antecedent = rule.get("antecedent", "")
#         consequent = rule.get("consequent", "")
#         if statement:
#             print(f"- {statement} => {consequent}")
#         else:
#             print(f"- IF {antecedent} THEN {consequent}")

# # Function to add a new fact to the knowledge base
# def add_fact(kb, fact):
#     if fact not in kb["facts"]:
#         kb["facts"].append(fact)
#         save_knowledge_base(kb, kb_file)

# # Function to add a new rule to the knowledge base
# def add_rule(kb, rule_str):
#     # Use regular expressions to split the rule into antecedent and consequent
#     match = re.match(r"if (.+?) ,then (.+)", rule_str)
    
#     if match:
#         antecedent = match.group(1).strip()
#         consequent = match.group(2).strip()
        
#         antecedent_conditions = re.split(r'\s+(?:and|or)\s+', antecedent)  # Split by "and" or "or"
        
#         rule_data = {
#             "antecedent": antecedent,
#             "consequent": consequent
#         }
        
#         kb["rules"].append(rule_data)  # Append the rule to the list of rules
#         save_knowledge_base(kb, kb_file)
#     else:
#         print("Invalid rule format. Use 'if <antecedent>, then <consequent>'.")

# # Function to infer new facts based on existing facts and rules using forward chaining
# def forward_chaining(kb):
#     new_facts = set()
#     existing_facts = set(kb["facts"])
#     rules = kb["rules"]
    
#     while True:
#         new_facts_in_iteration = set()

#         for rule in rules:
#             antecedent_conditions = rule.get("antecedent", "").split(' or ')

#             # Check if any of the antecedent conditions are satisfied
#             if any(condition in existing_facts for condition in antecedent_conditions):
#                 new_fact = rule.get("consequent", "")
#                 if new_fact not in existing_facts:
#                     new_facts_in_iteration.add(new_fact)

#         # If no new facts were inferred in this iteration, break the loop
#         if not new_facts_in_iteration:
#             break

#         # Add the new facts from this iteration to the set of new facts and existing facts
#         new_facts.update(new_facts_in_iteration)
#         existing_facts.update(new_facts_in_iteration)

#     return new_facts

# if __name__ == "__main__":
#     kb_file = "knowledge_base.json"
#     knowledge_base = load_knowledge_base(kb_file)

#     while True:
#         print("\nKnowledge Base:")
#         display_knowledge_base(knowledge_base)
#         print("\n1. Add a Fact")
#         print("2. Add a Rule (in the format 'IF antecedent THEN consequent')")
#         print("3. Infer New Facts")
#         print("4. Clear Contents of Knowledge Base")
#         print("5. Exit")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             fact = input("Enter a new fact: ")
#             add_fact(knowledge_base, fact)
#         elif choice == "2":
#             rule_str = input("Enter a rule in the format 'IF antecedent THEN consequent': ")
#             add_rule(knowledge_base, rule_str)
#         elif choice == "3":
#             new_facts = forward_chaining(knowledge_base)
#             for fact in new_facts:
#                 add_fact(knowledge_base, fact)
#                 print(f"Inferred new fact: {fact}")
#         elif choice == "4":
#             clear_knowledge_base(kb_file)
#         elif choice == "5":
#             break

import json
import re
import os

# Load existing knowledge from a JSON file if available
def load_knowledge_base(filename):
    try:
        with open(filename, 'r') as file:
            knowledge_base = json.load(file)
        return knowledge_base
    except FileNotFoundError:
        return {
            "facts": [],
            "rules": [],
        }

# Save the knowledge base to a JSON file
def save_knowledge_base(kb, filename):
    with open(filename, 'w') as file:
        json.dump(kb, file, indent=4)

# Function to clear the contents of the knowledge base JSON file
def clear_knowledge_base(filename):
    knowledge_base = {
        "facts": [],
        "rules": [],
    }
    save_knowledge_base(knowledge_base, filename)
    print("Contents of the knowledge base cleared.")

# Function to display facts and rules
def display_knowledge_base(kb):
    print("Facts:")
    for fact in kb["facts"]:
        print(f"- {fact}")
    print("\nRules:")
    for rule in kb["rules"]:
        print(f"- if {rule['antecedent']}, then {rule['consequent']}")

# Function to add a new fact to the knowledge base
def add_fact(kb, fact):
    if fact not in kb["facts"]:
        kb["facts"].append(fact)
        save_knowledge_base(kb, kb_file)

# Function to add a new rule to the knowledge base
def add_rule(kb, rule_str):
    # Use regular expressions to split the rule into antecedent and consequent
    match = re.match(r"if (.+?), then (.+)", rule_str)
    
    if match:
        antecedent_str = match.group(1).strip()
        consequent = match.group(2).strip()
        
        antecedent_conditions = re.split(r'\s+and\s+', antecedent_str)  # Split by "and"
        combined_antecedent = " and ".join(antecedent_conditions)
        
        rule_data = {
            "antecedent": combined_antecedent,
            "consequent": consequent
        }
        
        kb["rules"].append(rule_data)  # Append the rule to the list of rules
        save_knowledge_base(kb, kb_file)
    else:
        print("Invalid rule format. Use 'if antecedent, then consequent'.")


# Function to infer new facts based on existing facts and rules using forward chaining
def forward_chaining(kb):
    existing_facts = set(kb["facts"])
    rules = kb["rules"]

    while True:
        new_fact_added = False

        for rule in rules:
            antecedent_conditions = rule["antecedent"].split(" and ")
            conditions_met = all(condition in existing_facts for condition in antecedent_conditions)

            if conditions_met:
                new_fact = rule["consequent"]
                if new_fact not in existing_facts:
                    existing_facts.add(new_fact)
                    new_fact_added = True

        # If no new facts were inferred in this iteration, break the loop
        if not new_fact_added:
            break

    return existing_facts

if __name__ == "__main__":
    os.system('cls')
    kb_file = "knowledge_base.json"
    knowledge_base = load_knowledge_base(kb_file)

    while True:
        print("\nKnowledge Base:")
        display_knowledge_base(knowledge_base)
        print("\n1. Add a Fact")
        print("2. Add a Rule (in the format 'if antecedent, then consequent')")
        print("3. Infer New Facts")
        print("4. Clear Contents of Knowledge Base")
        print("5. Display Knowledge Base")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            fact = input("Enter a new fact: ")
            add_fact(knowledge_base, fact)
            os.system('cls')
        elif choice == "2":
            rule_str = input("Enter a rule in the format 'if antecedent, then consequent': ")
            add_rule(knowledge_base, rule_str)
            os.system('cls')
        elif choice == "3":
            new_facts = forward_chaining(knowledge_base)
            for fact in new_facts:
                add_fact(knowledge_base, fact)
                print(f"Inferred new fact: {fact}")
            os.system('cls')
        elif choice == "4":
            clear_knowledge_base(kb_file)
            os.system('cls')
            display_knowledge_base(knowledge_base)
        elif choice == "5":
            os.system('cls')
            display_knowledge_base()
        elif choice == '6':
            break