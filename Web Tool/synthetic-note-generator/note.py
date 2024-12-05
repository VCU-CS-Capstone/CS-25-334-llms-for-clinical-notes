import datetime
import random
import calendar
from constants import states, header_titles
from utils import get_feature_probabilities, random_time_period, format_date, regenerate
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

        if hpi_index == 0:
            if self.current_biopsy.biopsy_type is None:
                biopsy = 'Biopsy'
            else:
                biopsy = f'A {self.current_biopsy.biopsy_type} '
            text = f'pt is a {self.patient.age} {self.patient.sex.value} newly diagnosed with prostate ca after screening a PSA of {self.current_psa.psa_score}. ' \
                   f'{biopsy} showed {self.current_biopsy.gleason} in {self.current_biopsy.left_cores} and less than 5% of submitted issue ' \
                   f'and {self.current_biopsy.right_cores} and 10% of the tissue. {self.prostatectomy} Pt had ' \
                   f'problems with nocturia and bladder control following a prolonged hospitalization in ' \
                   f'{self.base_date.year - random.randint(1, 5)} but this has responded to medication and he says he only ' \
                   f'rare nocturia and good bladder control. {self.colonoscopy}'
        elif hpi_index == 1:
            text =  f'Mr. {self.patient.last_name} is a {self.patient.age} y/o {self.patient.race} {self.patient.sex.value} who ' \
                   f'presented to Urology with elevated PSA of {self.current_psa.psa_score} drawn on {self.current_psa.psa_date}. He underwent a ' \
                   f'{self.current_biopsy.biopsy_type} with pathology on {self.current_biopsy.biopsy_date} showing ' \
                   f'{self.current_biopsy.gleason}. {self.colonoscopy} Diagnosis: {self.staging.tnm}, {self.staging.risk} ' \
                   f'prostate cancer. The patient is now referred for evaluation for definitive radiation therapy.'
        elif hpi_index == 2:
            text = f'Mr. {self.patient.last_name} is a {self.patient.age} year old {self.patient.sex.value} with a hx of gradually rising PSA since ' \
                   f'{self.psa_history[-1].psa_date} and had a {self.current_biopsy.biopsy_type} on {self.current_biopsy.biopsy_date} and ' \
                   f'pathology reported {self.current_biopsy.gleason} {self.staging.histology} involving {self.current_biopsy.right_cores} and ' \
                   f'{self.current_biopsy.left_cores}. Most recent PSA was {self.current_psa.psa_score} recorded on {self.current_psa.psa_date}. ' \
                   f'The patient has ECOG score of {self.ecog} and reports {self.aua} with nocturia about {random.randint(1, 5)} ' \
                   f'times. Sexual function assessment shows {self.shim}. ' \
                   f'{self.colonoscopy} Staging workup including CT abdomen/pelvis and bone scan were reported negative for ' \
                   f'metastatic disease. The patient is not interested in surgical options and has been referred for radiotherapy evaluation.'
        elif hpi_index == 3:
            text = f'Mr. {self.patient.last_name} is a {self.patient.age} year old {self.patient.sex.value}, who was found to have elevated ' \
                   f'PSA of {self.current_psa.psa_score} on {self.current_psa.psa_date}. The patient ' \
                   f'underwent a {self.current_biopsy.biopsy_type} on {self.current_biopsy.biopsy_date}, which showed ' \
                   f'{self.current_biopsy.total_cores} for prostate {self.staging.histology}, {self.current_biopsy.gleason}, {self.staging.tnm}.' \
                   f'{self.prostatectomy} {self.colonoscopy}'
        elif hpi_index == 4:
            text = f'{self.patient.last_name}, {self.patient.first_name} is a {self.patient.age} year old {self.patient.sex.value} with a history of ' \
                   f'recently diagnosed {self.staging.risk} prostate cancer, who is referred to our clinic to discuss ' \
                   f'radiotherapy options. Information pertinent to the oncologic evaluation is as follows:\n' \
                   f'Mr. {self.patient.last_name} has a history of elevated PSAs with the most recent score of ' \
                   f'{self.current_psa.psa_score} on {self.current_psa.psa_date}. Pathology showed {self.current_biopsy.gleason} prostate {self.staging.histology} ' \
                   f'with {self.current_biopsy.total_cores}. {self.colonoscopy}'
        elif hpi_index == 5:
            prior_psa_text = f'\tDate\tPSA\n'
            for i in range(len(self.psa_history)):
                prior_psa_text += f'\t{self.psa_history[i].psa_date}\t{self.psa_history[i].psa_score}\n'
            text = f'History of Present Illness: Mr. {self.patient.last_name} is a {self.patient.age} year old {self.patient.sex.value} previously seen in ' \
                   f'our department in {self.base_date.year - random.randint(0, 5)}. The patient presented with rising PSA levels which ' \
                   f'prompted a biopsy (PSA history below): ' \
                   f'\n' \
                   f'{prior_psa_text}\n' \
                   f'On {self.biopsy_history[-1].biopsy_date} a {self.biopsy_history[-1].biopsy_type} demonstrated {self.biopsy_history[-1].gleason} ' \
                   f'disease. Current staging shows {self.staging.tnm} disease. ' \
                   f'Relevant scores include: AUA {self.aua}, SHIM {self.shim}.\n' \
                   f'Impression: Patient with clinical {self.staging.tnm}, Gleason ' \
                   f'{self.current_biopsy.gleason}, PSA {self.current_psa.psa_score}, {self.staging.histology} of the prostate.'
        elif hpi_index == 6:
            text = f'CHIEF COMPLAINT: Newly diagnosed {self.staging.risk} prostate cancer.\n' \
                   f'HISTORY OF PRESENT ILLNESS:\n' \
                   f'Patient with clinical {self.staging.tnm}, Gleason {self.current_biopsy.gleason.total}, ' \
                   f'PSA {self.current_psa.psa_score}, {self.staging.histology} of the prostate.\n' \
                   f'Mr. {self.patient.last_name} is a {self.patient.age} year old {self.patient.race} {self.patient.sex.value} who was seen in consultation ' \
                   f'for evaluation and treatment recommendations regarding newly diagnosed prostate cancer. Initial PSA on ' \
                   f'{self.psa_history[-1].psa_date} was {self.psa_history[-1].psa_score}. Most recent PSA from ' \
                   f'{self.current_psa.psa_date} shows {self.current_psa.psa_score}. ' \
                   f'Biopsy performed on {self.current_biopsy.biopsy_date} shows {self.current_biopsy.gleason} prostate ' \
                   f'cancer. {self.colonoscopy}'
        else:
            text = f'Mr. {self.patient.last_name} is a {self.patient.age} year old {self.patient.race} {self.patient.sex.value} with {self.staging.risk} risk ' \
                   f'prostate cancer, stage {self.staging.tnm}. Initial PSA was {self.psa_history[-1].psa_score} on ' \
                   f'{self.psa_history[-1].psa_date}, most recently {self.current_psa.psa_score} on {self.current_psa.psa_date}. ' \
                   f'Biopsy on {self.current_biopsy.biopsy_date} showed Gleason {self.current_biopsy.gleason}. ' \
                   f'{self.colonoscopy}'

        if regen:
            text = regenerate(text)
        return text

    def assessment_plan(self, regen=False):
        self.dose_data = Dose()
        plan_index = random.randint(1, 5)
        
        if plan_index == 1:
            text = f'Assessment: Mr. {self.patient.last_name} is a {self.patient.age} year old {self.patient.sex.value} diagnosed with ' \
                   f'{self.staging.risk} prostate {self.staging.histology}. Stage ' \
                   f'{self.staging.group_stage} {self.staging.risk} risk disease with Gleason {self.current_biopsy.gleason} and most ' \
                   f'recent PSA {self.current_psa.psa_score}. Treatment plan includes combined hormone ' \
                   f'therapy and external beam radiation to a dose of {self.dose_data.total_dose} cGy in ' \
                   f'{self.dose_data.num_fractions} fractions over {self.dose_data.weeks_of_rt} weeks using Image ' \
                   f'Guided IMRT.\n\nTreatment plan follows NCCN guidelines.'
        elif plan_index == 2:
            text = f'ASSESSMENT AND PLAN:\n' \
                   f'1. {self.staging.risk} risk prostate cancer, {self.staging.tnm}, Gleason {self.current_biopsy.gleason}\n' \
                   f'2. Will proceed with external beam radiation therapy\n' \
                   f'3. Treatment dose: {self.dose_data.total_dose} cGy in {self.dose_data.num_fractions} fractions\n' \
                   f'4. Will arrange for fiducial marker placement\n' \
                   f'5. Follow-up scheduled in {random_time_period(2, 4, "week")}\n'
        elif plan_index == 3:
            text = f'PLAN:\n' \
                   f'We discussed treatment options in detail today. Given the patient\'s {self.staging.risk} risk disease, ' \
                   f'we recommend definitive radiation therapy with total dose {self.dose_data.total_dose} cGy. ' \
                   f'Treatment will be delivered over {self.dose_data.weeks_of_rt} weeks using IMRT/IGRT technique. ' \
                   f'Side effects and expectations were discussed in detail.'
        elif plan_index == 4:
            text = f'Treatment Recommendation:\n' \
                   f'For {self.patient.age} year old {self.patient.sex.value} with {self.staging.risk} risk prostate cancer, ' \
                   f'recommend definitive radiation therapy. Will treat to {self.dose_data.total_dose} cGy in ' \
                   f'{self.dose_data.num_fractions} fractions using IMRT/IGRT. ' \
                   f'Current performance status ECOG {self.ecog}. Will proceed with treatment planning.'
        else:
            text = f'ASSESSMENT AND PLAN:\n' \
                   f'1. Stage {self.staging.tnm} prostate cancer\n' \
                   f'2. Gleason score {self.current_biopsy.gleason}\n' \
                   f'3. PSA {self.current_psa.psa_score}\n' \
                   f'4. Will proceed with radiation therapy planning\n' \
                   f'5. Dose: {self.dose_data.total_dose} cGy / {self.dose_data.num_fractions} fractions\n'

        if regen:
            text = regenerate(text)
        return text