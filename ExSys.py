from experta import *
import sys
from sympy import true

def is_valid(str):
    if (str != 'yes' and str != 'no'):
        print("Wrong input! Please do it over again")
        sys.exit()


class BipolarDiag(KnowledgeEngine):
    username = "",

    @DefFacts()
    def data_needed(self):

        yield Fact(diagBipolar = 'true')
        print ("This system can help you self diagnose your bipolar symptoms. We will ask a few questions")


    @Rule(Fact (diagBipolar = 'true'), NOT (Fact(name = W())), salience = 1000)
    def ask_name(self):
        self.username = input("What's your name?\n")
        if (self.username == 'reset'):
            sys.exit()
        self.declare(Fact(name = self.username))

    @Rule (Fact(diagBipolar = 'true'), NOT(Fact(manic_0 = W())), salience = 100)
    def ask_manic_0(self):
        sym = """1. Inflated self-esteem or grandiosity.\n 2. Decreased need for sleep (e.g., feels rested after 3 hours of sleep).\n3. More talkative than usual, or acts pressured to keep talking.\n4. Flights of ideas or subjective experience that thoughts are racing.\n5. Increase in goal-directed activity, or psychomotor acceleration.\n6. Distractibility (too easily drawn to unimportant or irrelevant external stimuli). \n7. Excessive involvement in activities with a high likelihood of painful consequences.(e.g., extravagant shopping, improbable commercial schemes, hypersexuality)\n"""
        self.manic_0 = input ("Do you feel at least 4 of these symptoms? \n" + sym + "Write yes or no ->")
        self.manic_0 = self.manic_0.strip().lower()
        is_valid(str(self.manic_0))
        self.declare(Fact(manic_0 = self.manic_0))
        

    @Rule (Fact(diagBipolar = 'true'), NOT(Fact(manic_intensity = W())), Fact(manic_0 ='yes'), salience = 99)
    def ask_manic_intensity(self):
        self.manic_intensity = input ("Does it feel very intense and to certain extent uncontrolable\n" + "Write yes or no ->")
        self.manic_intensity= self.manic_intensity.strip().lower()
        is_valid(str(self.manic_intensity))
        self.declare(Fact(manic_intensity = self.manic_intensity))

    @Rule (Fact (diagBipolar = 'true'), NOT(Fact (is_mania = W())), Fact (manic_intensity = 'yes' ), salience = 98)
    def ask_manic_weeks(self):
        self.manic_weeks = input ("Does each episode persisted for a week or more?\n" + "Write yes or no ->")
        self.manic_weeks = self.manic_weeks.strip().lower()
        is_valid(str(self.manic_weeks))
        self.declare(Fact(is_mania = self.manic_weeks))

    @Rule (Fact (diagBipolar = 'true'), NOT(Fact(is_hypomania = W())), Fact(manic_intensity = 'no'), salience = 97)
    def ask_manic_days(self):
        self.manic_days = input('Does each episodes persisted for 4 days or more?' + "\n Write yes or no ->")
        self.manic_days = self.manic_days.strip().lower()
        is_valid(str(self.manic_days))
        self.declare(Fact(is_hypomania = self.manic_days))


    @Rule (Fact (diagBipolar = 'true'), NOT(Fact(depressive_0 = W())), salience = 90)
    def ask_depressive_0(self):
        sym = """1. Down, upset or tearful\n2. Tired or sluggish\n3. Uninterested in things you usually enjoy\n4. Low self-esteem and a lack of confidence\n5. Guilty, worthless or hopeless\n6. Agitated and tense\n7. Like you can't concentrate on anything\n8. Suicidal\n"""
        self.depressive_0 = input ("Do u feel at least 4 of these symptoms" + sym + "\n Write yes or no ->" )
        self.depressive_0 = self.depressive_0.strip().lower()
        is_valid(str(self.depressive_0))
        self.declare(Fact(depressive_0 = self.depressive_0))

    @Rule (Fact (diagBipolar = 'true'), NOT(Fact(depressive_intensity = W())), Fact (depressive_0 = 'yes'), salience = 89)
    def ask_depressive_intensity(self):
        self.depressive_intensity = input("Do you feel those symptomse so intense that it can be uncontrollable? " + "\nWrite yes or no ->")
        self.depressive_intensity = self.depressive_intensity.strip().lower()
        is_valid(str(self.depressive_intensity))
        self.declare(Fact(depressive_intensity = self.depressive_intensity))
    
    @Rule (Fact (diagBipolar = 'true'), NOT (Fact (long_term = W())), Fact (manic_intensity = 'no'), Fact (depressive_intensity = 'no'), salience = 80)
    def ask_long_term(self):
        self.long_term = input("Do you feel these mood changing symptoms for over 2 years?\n" + "Write yes or no ->")
        self.long_term = self.long_term.strip().lower()
        is_valid(str(self.long_term))
        self.declare(Fact (long_term = self.long_term))


    @Rule (Fact (diagBipolar = 'true'), Fact (is_mania = 'yes'))
    def bipolar_1(self):
        self.declare(Fact (disease = "Bipolar I"))
    
    @Rule(Fact (diagBipolar = 'true'), Fact (is_hypomania = 'yes'), Fact(depressive_intensity = 'yes'))
    def bipolar_2(self):
        self.declare(Fact(disease = "Bipolar II"))
    
    @Rule(Fact (diagBipolar = 'true'), Fact (long_term = 'yes'))
    def cyclopathic(self):
        self.declare(Fact(disease = "Cyclothymic Bipolar"))

    
    @Rule (Fact (diagBipolar = 'true'), NOT (Fact(disease = W())), Fact (manic_0 = 'yes'), Fact (depressive_0 = 'yes'), salience = -1)
    def unspecified(self):
        self.declare(Fact (disease = 'Unspecified Bipolar'))

    @Rule (Fact (diagBipolar = 'true'), NOT (Fact(disease = W())), salience = -10)
    def healthy(self):
        self.declare(Fact (disease = 'none'))


    @Rule (Fact (diagBipolar = 'true'), Fact(disease = MATCH.disease), salience = 1)
    def diagnose(self, disease):
        print ("""
[Disclaimer: This is just a preliminary diagnosis and in no way is the most comprehensive.
If your problem persists, do check to your local therapist for more comprehensive test result]\n""")
        if (disease == 'none'):
            print ('RESULT: You may [not have a bipolar disorder]. This doesnt mean you dont have any other mental illness\n')

        else:
            print ('RESULT:You may have [' + disease + "]. Please check to your nearest therapist")
        print("Hope you're well, " + self.username + "!\n")
while true:
    if __name__ == "__main__":
        engine = BipolarDiag()
        engine.reset()
        engine.run()
        



    


    