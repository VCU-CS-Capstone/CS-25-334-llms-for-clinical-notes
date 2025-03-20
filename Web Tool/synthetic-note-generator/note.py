import datetime
import random
import re
from constants import states, header_titles
from utils import get_feature_probabilities, random_time_period, format_date, regenerate, replace_placeholders, regen_validation
from data_elements import Patient, Author, PSA, Biopsy, Colonoscopy, Prostatectomy, AUA, SHIM, IPSS, ECOG, Vitals, \
    NoteDate, ProblemList, Imaging, SocialHistory, FamilyHistory, PriorTreatment, Allergies, Medications, \
    PerformanceScore, Staging, Dose, DateOffset

class BaseNote:
    def __init__(self):
        self.note_text = ''
        self.feature_probabilities = get_feature_probabilities()
        self.base_date = NoteDate(offset_days=random.randint(0, 1000), direction=DateOffset.AFTER)
        self.patient = Patient()
        self.is_cosigner = None
        self.is_cosigner = True if random.random() <= self.feature_probabilities['note_cosigner'] else False
        self.note_author = Author()
        self.note_cosigner = Author(create=self.is_cosigner)
        self.dose_data = None

    def get_data_fields(self):
        self.dose_data = {
            'patient': self.patient,
            'note_author': self.note_author,
            'note_cosigner': self.note_cosigner,
            'base_date': self.base_date,
            'dose_data': self.dose_data
        }
        return self.dose_data


class ConsultNote(BaseNote):
    def __init__(self, **kwargs):
        super().__init__()
        
        # Initialize note type
        self.note_type = kwargs.get('clinical_note_type', 'consult')
        self.note_generation_type = kwargs.get('note_generation_type', 'single')
        
        # Initialize section toggles
        self.include_sections = {
            'hpi': kwargs.get('include_hpi', True),
            'vitals': kwargs.get('include_vitals', True),
            'social': kwargs.get('include_social', True),
            'medical': kwargs.get('include_medical', True),
            'exam': kwargs.get('include_exam', True),
            'imaging': kwargs.get('include_imaging', True),
            'plan': kwargs.get('include_plan', True)
        }

        # Initialize regeneration options
        self.regen_sections = {
            'hpi_regen': kwargs.get('regen_hpi', False),
            'assessment_regen': kwargs.get('regen_assmplan', False)
        }
        
        # Initialize base date and patient
        if kwargs.get('base_date'):
            self.base_date = NoteDate(reference_date=kwargs.get('base_date'))
        else:
            self.base_date = NoteDate(offset_days=random.randint(0, 1000), direction=DateOffset.AFTER)
        
        # Initialize patient demographics
        self.patient = Patient(
            age=kwargs.get('patient_age'),
            sex=kwargs.get('patient_sex'),
            race=kwargs.get('patient_race'),
            ethnicity=kwargs.get('patient_ethnicity'),  # Added ethnicity
            first_name=kwargs.get('patient_first_name'),
            last_name=kwargs.get('patient_last_name'),
            reference_date=self.base_date.value
        )

        # Initialize authors with provided values or defaults
        if kwargs.get('note_author'):
            self.note_author = Author(create=True, name=kwargs.get('note_author'))
        else:
            self.note_author = Author()

        if kwargs.get('note_cosigner'):
            self.is_cosigner = True
            self.note_cosigner = Author(create=True, name=kwargs.get('note_cosigner'))
        else:
            self.is_cosigner = True if random.random() <= self.feature_probabilities['note_cosigner'] else False
            self.note_cosigner = Author(create=self.is_cosigner)
        
        # Initialize PSA history with provided value if available
        psa_value = kwargs.get('psa_score')
        self.psa_history = self.generate_psa(psa_value)
        self.current_psa = self.psa_history[0]
        
        # Initialize biopsy with Gleason scores if provided
        self.biopsy_history = self.generate_biopsies(
            gleason_primary=kwargs.get('gleason_primary'),
            gleason_secondary=kwargs.get('gleason_secondary')
        )
        self.current_biopsy = self.biopsy_history[0]
        
        # Initialize other medical values
        self.aua = AUA(value=kwargs.get('aua'))
        self.ipss = IPSS(value=kwargs.get('ipss'))
        self.shim = SHIM(value=kwargs.get('shim'))
        self.ecog = ECOG(value=kwargs.get('ecog'))
        
        # Initialize lists with provided values or random ones
        self.medications = Medications(medications=kwargs.get('medications'))
        self.allergies = Allergies(allergies=kwargs.get('allergies'))
        self.problem_list = ProblemList(
            active_problems=kwargs.get('problem_list'),
            surgical_history=kwargs.get('surgical_history')
        )
        
        # Initialize treatment records
        self.colonoscopy = Colonoscopy(value=kwargs.get('colonoscopy'))
        self.prostatectomy = Prostatectomy(
            value=kwargs.get('prostatectomy'),
            patient_last_name=self.patient.last_name
        )
        
        # Initialize vitals with provided values
        self.vitals = Vitals(
            temperature=kwargs.get('temperature'),
            systolic=kwargs.get('blood_pressure_systolic'),
            diastolic=kwargs.get('blood_pressure_diastolic'),
            pulse=kwargs.get('pulse'),
            respiration=kwargs.get('respiration'),
            weight=kwargs.get('weight'),
            pain=kwargs.get('pain')
        )
        
        self.staging = Staging(
            risk_level=kwargs.get('risk_level'),
            tnm=kwargs.get('tnm'),
            group_stage=kwargs.get('group_stage'),
            histology=kwargs.get('histology')
        )
        
        # Initialize dates - wrap all in NoteDate objects
        if kwargs.get('mri_date'):
            self.mri_date = NoteDate(reference_date=kwargs.get('mri_date'))
        else:
            self.mri_date = NoteDate(reference_date=self.base_date.value, direction=DateOffset.BEFORE, offset_days=200)
            
        # Initialize imaging dates
        pelvic_ct_date = kwargs.get('pelvic_ct_date')
        pelvic_mri_date = kwargs.get('pelvic_mri_date')
        bone_scan_date = kwargs.get('bone_scan_date')

        self.pelvic_ct = kwargs.get('pelvic_ct_date') and NoteDate(reference_date=pelvic_ct_date) or \
                        Imaging(image_type='pelvic_ct', base_date=self.base_date.value)
        self.pelvic_mri = kwargs.get('pelvic_mri_date') and NoteDate(reference_date=pelvic_mri_date) or \
                         Imaging(image_type='pelvic_mri', base_date=self.base_date.value)
        self.bone_scan = kwargs.get('bone_scan_date') and NoteDate(reference_date=bone_scan_date) or \
                        Imaging(image_type='bone_scan', base_date=self.base_date.value)
        
        # Initialize histories with provided values
        self.social_history = SocialHistory(
            reference_date=self.base_date.value,
            alcohol_history=kwargs.get('alcohol_history'),
            smoking_history=kwargs.get('smoking_history')
        )
        
        self.family_history = FamilyHistory()
        
        # Wrap prior treatment dates in NoteDate objects
        prior_rt_date = kwargs.get('prior_rt_date')
        hormone_therapy_date = kwargs.get('hormone_therapy_date')
        
        self.prior_treatment = PriorTreatment(
            reference_date=self.base_date.value,
            prior_rt=kwargs.get('prior_rt'),
            prior_rt_date=prior_rt_date and NoteDate(reference_date=prior_rt_date),
            chemotherapy_prescribed=kwargs.get('chemotherapy_prescribed'),
            chemotherapy_drugs=kwargs.get('chemotherapy_drugs'),
            hormone_therapy_prescribed=kwargs.get('hormone_therapy_prescribed'),
            hormone_therapy_date=hormone_therapy_date and NoteDate(reference_date=hormone_therapy_date)
        )
        
        self.performance_score = PerformanceScore(value=kwargs.get('performance_score'))

    def get_text(self):
        if self.note_text == '':
            self.generate_note()
        return self.note_text

    def get_data_fields(self):
        if self.dose_data is not None:
            dose_data = self.dose_data.value
        else:
            dose_data = None
            
        data_fields = {
            'note_type': 'consult',
            'patient': self.patient.value,
            'note_author': self.note_author.value,
            'note_cosigner': self.note_cosigner.value,
            'base_date': format_date(self.base_date.value, date_format=2),
            'dose_data': dose_data,
            'psa': self.current_psa.value,
            'biopsy': self.current_biopsy.value,
            'colonoscopy': self.colonoscopy.value,
            'prostatectomy': self.prostatectomy.value,
            'aua': self.aua.value,
            'shim': self.shim.value,
            'ipss': self.ipss.value,
            'ecog': self.ecog.value,
            'vitals': self.vitals.value,
            'problem_list': self.problem_list.value,
            'pelvic_ct': format_date(self.pelvic_ct.value, date_format=2),
            'pelvic_mri': format_date(self.pelvic_mri.value, date_format=2),
            'bone_scan': format_date(self.bone_scan.value, date_format=2),
            'social_history': self.social_history.value,
            'family_history': self.family_history.value,
            'prior_treatment': self.prior_treatment.value,
            'allergies': self.allergies.value,
            'medications': self.medications.value,
            'performance_score': self.performance_score.value,
            'staging': self.staging.value,
            'mri_date': format_date(self.mri_date.value, date_format=2)
        }

        return data_fields
    
    def generate_note(self):
        """Modified to respect section toggles"""
        self.note_text = ''
        self.note_text += self.get_header()
        
        if self.include_sections['hpi']:
            if self.regen_sections['hpi_regen']:
                self.note_text += self.hpi(regen=True)
            else:
                self.note_text += self.hpi()
        
        if self.include_sections['exam']:
            self.note_text += self.physical_exam()
            
        if self.include_sections['medical']:
            self.note_text += str(self.problem_list)
            self.note_text += str(self.medications)
            self.note_text += str(self.allergies)
            
        if self.include_sections['imaging']:
            self.note_text += str(self.pelvic_ct)
            self.note_text += str(self.pelvic_mri)
            self.note_text += str(self.bone_scan)
            
        if self.include_sections['social']:
            self.note_text += str(self.social_history)
            self.note_text += str(self.family_history)
            self.note_text += str(self.prior_treatment)
            
        if self.include_sections['plan']:
            if self.regen_sections['assessment_regen']:
                self.note_text += self.assessment_plan(regen=True)
            else:
                self.note_text += self.assessment_plan()
            
        self.note_text += self.get_footer()

    def physical_exam(self):
        text = '\nPhysical Exam:\n'
        text += str(self.vitals)
        text += f'{self.performance_score}\n'
        text += f'ECOG: {self.ecog}\n'
        return text

    def generate_biopsies(self, gleason_primary=None, gleason_secondary=None):
        """Modified to accept Gleason scores"""
        biopsy_entries = [Biopsy(
            base_date=self.base_date.value, 
            gleason_primary=gleason_primary,
            gleason_secondary=gleason_secondary
        )]
        for _ in [0, 1]:
            biopsy_entries.append(Biopsy(base_date=biopsy_entries[-1].biopsy_date.value))
        return biopsy_entries

    def generate_psa(self, initial_value=None):
        """Modified to accept initial PSA value"""
        psa_entries = [PSA(
            base_date=self.base_date.value, 
            score=initial_value
        )]
        for i in range(random.randint(1, 6)):
            psa_entries.append(PSA(
                base_date=psa_entries[-1].psa_date.value, 
                previous_score=psa_entries[-1].psa_score
            ))
        return psa_entries

    def get_header(self):
        text = f'{random.choice(header_titles)}\n'
        text += f'Site: {random.choice(states)}\n'
        text += f'Date: {self.base_date} \tAuthor: {self.note_author}\n\n'
        text += f'LOCAL TITLE:\n'
        text += f'STANDARD TITLE: RADIATION ONCOLOGY CONSULT\n'
        text += f'DATE OF NOTE: {self.base_date}\tENTRY DATE: {self.base_date}\n'
        text += f'\tAUTHOR: {self.note_author}\t\tEXP COSIGNER: {self.note_cosigner}\n'
        text += f'\tURGENCY\t\tSTATUS: COMPLETED\n'
        return text

    def get_footer(self):
        title = ['Attending', 'Staff Physician Radiation Oncologist', 'STAFF PHYSICIAN,RADIATION ONCO']
        title_choice = random.choice(title)
        text = f'\n\n/es/ {self.note_author}\n'
        if self.is_cosigner:
            text += 'Resident\n'
            text += f'Signed: {self.base_date}\n\n'
            text += 'Receipt Acknowledged By:\n'
            text += f'{self.base_date}\t\t/es/ {self.note_cosigner}\n'
            text += title_choice
        else:
            text += title_choice + '\n'
            text += f'Signed: {self.base_date}\n'
        return text
    
    def hpi(self, regen=False):
        hpi_index = random.randint(0, 13)
        prior_psa_text = ('\tDate\tPSA\n')
        biopsy = ''
        # Create mappings in order to ensure that LLM rephrasing doesn't insert random values. The mappings are eventually replaced after either rephrasing
        # or text regeneration. 
        mappings = {
            1: self.patient.age,
            2: self.patient.sex.value,
            3: self.current_psa.psa_score,
            4: biopsy,
            5: self.current_biopsy.gleason,
            6: self.current_biopsy.left_cores,
            7: self.current_biopsy.right_cores,
            8: self.prostatectomy,
            9: self.base_date.year - random.randint(1, 5),
            10: self.colonoscopy,
            11: self.patient.last_name,
            12: self.patient.first_name,
            13: self.patient.race,
            14: self.current_psa.psa_date,
            15: self.current_biopsy.biopsy_type,
            16: self.current_biopsy.biopsy_date,
            17: self.staging.tnm,
            18: self.staging.risk,
            19: self.psa_history[-1].psa_date,
            20: self.staging.histology,
            21: self.ecog,
            22: self.aua,
            23: random.randint(1, 5),
            24: self.shim,
            26: self.current_biopsy.total_cores,
            27: prior_psa_text,
            28: self.psa_history[-1].psa_score
        }

        if hpi_index == 0:
            if self.current_biopsy.biopsy_type is None:
                biopsy = 'Biopsy'
            else:
                biopsy = f'A {self.current_biopsy.biopsy_type}'
                text = ('pt is a {1} {2} newly diagnosed with prostate ca after screening a PSA of {3}. '
                '{4} showed {5} in {6} and less than 5% of submitted issue '
                'and {7} and 10% of the tissue. {8} Pt had '
                'problems with nocturia and bladder control following a prolonged hospitalization in '
                '{9} but this has responded to medication and he says he only '
                'rare nocturia and good bladder control. {10}')

        elif hpi_index == 1:
            text =  ('Mr. {11} is a {1} y/o {13} {2} who '
                   'presented to Urology with elevated PSA of {3} drawn on {14}. He underwent a '
                   '{15} with pathology on {16} showing '
                   '{5}. {10} Diagnosis: {17}, {18} '
                   'prostate cancer. The patient is now referred for evaluation for definitive radiation therapy.')
        elif hpi_index == 2:
            text = ('Mr. {11} is a {1} year old {2} with a hx of gradually rising PSA since {19} and had a {15} on {16} and '
                    'pathology reported {5} {20} involving {7} and {6}. Most recent PSA was {3} recorded on {14}. '
                    'The patient has ECOG score of {21} and reports {22} with nocturia about {23} times. '
                    'Sexual function assessment shows {24}. {10} Staging workup including CT abdomen/pelvis and bone scan '
                    'were reported negative for metastatic disease. The patient is not interested in surgical options and has been referred for radiotherapy evaluation.')

        elif hpi_index == 3:
            text = ('Mr. {11} is a {1} year old {2}, who was found to have elevated PSA of {3} on {14}. The patient '
                    'underwent a {15} on {16}, which showed {26} for prostate {20}, {5}, {17}. '
                    '{8} {10}')

        elif hpi_index == 4:
            text = ('{11}, {12} is a {1} year old {2} with a history of recently diagnosed {18} prostate cancer, who is referred to our clinic to discuss '
                    'radiotherapy options. Information pertinent to the oncologic evaluation is as follows:\n'
                    'Mr. {11} has a history of elevated PSAs with the most recent score of {3} on {14}. Pathology showed {5} prostate {20} '
                    'with {26}. {10}')

        elif hpi_index == 5:
            for i in range(len(self.psa_history)):
                prior_psa_text += ('\t{self.psa_history[i].psa_date}\t{self.psa_history[i].psa_score}\n')
            
            text = ('History of Present Illness: Mr. {11} is a {1} year old {2} previously seen in '
                    'our department in {9}. The patient presented with rising PSA levels which '
                    'prompted a biopsy (PSA history below): \n'
                    '{27}\n'
                    'On {16} a {15} demonstrated {5} disease. Current staging shows {17} disease. '
                    'Relevant scores include: AUA {22}, SHIM {24}.\n'
                    'Impression: Patient with clinical {17}, Gleason {5}, PSA {3}, {20} of the prostate.')

        elif hpi_index == 6:
            text = ('CHIEF COMPLAINT: Newly diagnosed {18} prostate cancer.\n'
                        'HISTORY OF PRESENT ILLNESS:\n'
                        'Patient with clinical {17}, Gleason {5}, PSA {3}, {20} of the prostate.\n'
                        'Mr. {11} is a {1} year old {13} {2} who was seen in consultation '
                        'for evaluation and treatment recommendations regarding newly diagnosed prostate cancer. Initial PSA on '
                        '{19} was {28}. Most recent PSA from {14} shows {3}. '
                        'Biopsy performed on {16} shows {5} prostate cancer. {10}')
        else:
            text = ('Mr. {11} is a {1} year old {13} {2} with {18} risk '
                        'prostate cancer, stage {17}. Initial PSA was {28} on '
                        '{19}, most recently {3} on {14}. '
                        'Biopsy on {16} showed Gleason {5}. {10}')

        if regen:
            regenerated_text = regenerate(text)
            text = regen_validation(regenerated_text, text)

        text = replace_placeholders(text, mappings)
        # Replaces double period problem with mapping {10}
        text = re.sub(r'\.\.', '.', text)
        return text

    def assessment_plan(self, regen=False):
        self.dose_data = Dose()
        plan_index = random.randint(1, 5)

        # Create mappings in order to ensure that LLM rephrasing doesn't insert random values. The mappings are eventually replaced after either rephrasing
        # or text regeneration. 
        mappings = {
            1: self.patient.last_name,
            2: self.patient.age,
            3: self.patient.sex.value,
            4: self.staging.risk,
            5: self.staging.histology,
            6: self.staging.group_stage,
            7: self.current_biopsy.gleason,
            8: self.dose_data.total_dose,
            9: self.dose_data.num_fractions,
            10: self.dose_data.weeks_of_rt,
            11: self.staging.tnm,
            12: self.ecog,
            13: self.current_psa.psa_score
        }
        
        if plan_index == 1:
            text = ('Assessment: Mr. {1} is a {2} year old {3} diagnosed with '
                    '{4} prostate {5}. Stage '
                    '{6} {4} risk disease with Gleason {7} and most '
                    'recent PSA {13}. Treatment plan includes combined hormone '
                    'therapy and external beam radiation to a dose of {8} cGy in '
                    '{9} fractions over {10} weeks using Image '
                    'Guided IMRT.\n\nTreatment plan follows NCCN guidelines.')
        elif plan_index == 2:
            text = ('ASSESSMENT AND PLAN:\n'
                    '1. {4} risk prostate cancer, {11}, Gleason {7}\n'
                    '2. Will proceed with external beam radiation therapy\n'
                    '3. Treatment dose: {8} cGy in {9} fractions\n'
                    '4. Will arrange for fiducial marker placement\n'
                    '5. Follow-up scheduled in {14}\n')
        elif plan_index == 3:
            text = ('PLAN:\n'
                    'We discussed treatment options in detail today. Given the patient\'s {4} risk disease, '
                    'we recommend definitive radiation therapy with total dose {8} cGy. '
                    'Treatment will be delivered over {10} weeks using IMRT/IGRT technique. '
                    'Side effects and expectations were discussed in detail.')
        elif plan_index == 4:
            text = ('Treatment Recommendation:\n'
                    'For {2} year old {3} with {4} risk prostate cancer, '
                    'recommend definitive radiation therapy. Will treat to {8} cGy in '
                    '{9} fractions using IMRT/IGRT. '
                    'Current performance status ECOG {12}. Will proceed with treatment planning.')
        else:
            text = ('ASSESSMENT AND PLAN:\n'
                    '1. Stage {11} prostate cancer\n'
                    '2. Gleason score {7}\n'
                    '3. PSA {13}\n'
                    '4. Will proceed with radiation therapy planning\n'
                    '5. Dose: {8} cGy / {9} fractions\n')


        if regen:
            regenerated_text = regenerate(text)
            text = regen_validation(regenerated_text, text)

        text = replace_placeholders(text, mappings)
        # Checks for additional periods
        text = re.sub(r'\.\.', '.', text)
        return text