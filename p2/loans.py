#Loans
import json
from io import TextIOWrapper
from zipfile import ZipFile
from io import TextIOWrapper
from zipfile import ZipFile
import csv
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}
   
values = {'activity_year': '2020', 'lei': '549300FX7K8PTEQUU487', 'derived_msa-md': '31540', 'state_code': 'WI',
         'county_code': '55025', 'census_tract': '55025002402', 'conforming_loan_limit': 'C',
         'derived_loan_product_type': 'Conventional:First Lien',
         'derived_dwelling_category': 'Single Family (1-4 Units):Site-Built',
         'derived_ethnicity': 'Not Hispanic or Latino', 'derived_race': 'White', 'derived_sex': 'Male',
         'action_taken': '3', 'purchaser_type': '0', 'preapproval': '2', 'loan_type': '1', 'loan_purpose': '4',
         'lien_status': '1', 'reverse_mortgage': '2', 'open-end_line_of_credit': '1',
         'business_or_commercial_purpose': '2', 'loan_amount': '225000.0', 'loan_to_value_ratio': '78.671',
         'interest_rate': '3.000', 'rate_spread': 'NA', 'hoepa_status': '3', 'total_loan_costs': 'NA',
         'total_points_and_fees': 'NA', 'origination_charges': 'NA', 'discount_points': 'NA',
         'lender_credits': 'NA', 'loan_term': '360', 'prepayment_penalty_term': 'NA', 'intro_rate_period': '1',
         'negative_amortization': '2', 'interest_only_payment': '2', 'balloon_payment': '2',
         'other_nonamortizing_features': '2', 'property_value': '285000', 'construction_method': '1',
         'occupancy_type': '1', 'manufactured_home_secured_property_type': '3',
         'manufactured_home_land_property_interest': '5', 'total_units': '1', 'multifamily_affordable_units': 'NA',
         'income': '0', 'debt_to_income_ratio': '>60%', 'applicant_credit_score_type': '1',
         'co-applicant_credit_score_type': '10', 'applicant_ethnicity-1': '2', 'applicant_ethnicity-2': '',
         'applicant_ethnicity-3': '', 'applicant_ethnicity-4': '', 'applicant_ethnicity-5': '',
         'co-applicant_ethnicity-1': '5', 'co-applicant_ethnicity-2': '', 'co-applicant_ethnicity-3': '',
         'co-applicant_ethnicity-4': '', 'co-applicant_ethnicity-5': '', 'applicant_ethnicity_observed': '2',
         'co-applicant_ethnicity_observed': '4', 'applicant_race-1': '5', 'applicant_race-2': '',
         'applicant_race-3': '', 'applicant_race-4': '', 'applicant_race-5': '', 'co-applicant_race-1': '8',
         'co-applicant_race-2': '', 'co-applicant_race-3': '', 'co-applicant_race-4': '', 'co-applicant_race-5': '',
         'applicant_race_observed': '2', 'co-applicant_race_observed': '4', 'applicant_sex': '1',
         'co-applicant_sex': '5', 'applicant_sex_observed': '2', 'co-applicant_sex_observed': '4',
         'applicant_age': '55-64', 'co-applicant_age': '9999', 'applicant_age_above_62': 'Yes',
         'co-applicant_age_above_62': 'NA', 'submission_of_application': '1', 'initially_payable_to_institution': '1',
         'aus-1': '6', 'aus-2': '', 'aus-3': '', 'aus-4': '', 'aus-5': '', 'denial_reason-1': '1',
         'denial_reason-2': '', 'denial_reason-3': '', 'denial_reason-4': '', 'tract_population': '3572',
         'tract_minority_population_percent': '41.1499999999999986', 'ffiec_msa_md_median_family_income': '96600',
         'tract_to_msa_income_percentage': '64', 'tract_owner_occupied_units': '812',
         'tract_one_to_four_family_homes': '910', 'tract_median_age_of_housing_units': '45'}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
                
    def __repr__(self):
        racelist = list(self.race)
        return f"Applicant('{(self.age)}', {racelist})"
        
        

    def lower_age(self):
        return int(self.age.replace(">", "").replace("<", "").split("-")[0])
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    



class Loan:
    def __init__(self, values):
        lamount = values["loan_amount"]
        pvalue = values["property_value"]
        irate = values["interest_rate"]
        self.loan_amount = float(lamount) if (lamount != "NA" and lamount != "Exempt") else -1
        self.property_value = float(pvalue) if (pvalue != "NA" and pvalue != "Exempt") else -1
        self.interest_rate = float(irate) if (irate != "NA" and irate != "Exempt") else -1
        self.applicants = []
        app_age = values["applicant_age"]
        app_race = []
        coapp_race = []
        coapp_age = values["co-applicant_age"]
        for i in range(1,6):
            app_race.append(values["applicant_race-" + str(i)])
            coapp_race.append(values["co-applicant_race-" + str(i)])
        self.applicants.append(Applicant(app_age, app_race))
        if coapp_age != "9999":
            self.applicants.append(Applicant(coapp_age, coapp_race))  

        
    def __str__(self):
        return f'<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>'
    def __repr__(self):
        return f'<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>'

        
        
    
    
    
    def yearly_amounts(self, yearly_payment):
    # TODO: assert interest and amount are positive
        assert self.interest_rate > 0.0
        assert self.loan_amount > 0.0
        
        result = []
        amt = self.loan_amount

        while amt > 0:
            yield amt
            amt += amt * (self.interest_rate / 100)
            amt -= yearly_payment
    
    
    
class Bank:
    def __init__(self,name):
        self.name = name
        self.lei = ""
        self.list = []
        with open("banks.json") as f:
            data = json.load(f)    
        dict = [bank for bank in data if bank["name"] == self.name]            
        if len(dict) != 0:
            dict = dict[0] 
            self.lei = dict["lei"]
            assert self.lei != -1

        with ZipFile('wi.zip') as zf:
            with zf.open("wi.csv") as csvfile:
                tio = TextIOWrapper(csvfile)
                reader = csv.DictReader(tio)
                for item in reader:
                    if item["lei"] == self.lei:
                        self.list.append(Loan(item))
                
                
    def __len__(self):
        return len(self.list)
       
        
    def __getitem__(self,lookup):
        return self.list[lookup]
        
            
        
