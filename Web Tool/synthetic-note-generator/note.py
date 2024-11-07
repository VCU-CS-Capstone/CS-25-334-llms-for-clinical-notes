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

        # Groq regeneration True/False
        self.regen_sections = {
            'hpi_regen': kwargs.get('regen_hpi', False),
            'assessment_regen': kwargs.get('regen_assmplan', False)
        }

        # Print the regen_sections dictionary
        print("\nRegen Sections:", self.regen_sections)
        
        # Print the individual values
        print("HPI Regen:", self.regen_sections['hpi_regen'])
        print("Assessment Regen:", self.regen_sections['assessment_regen'])
        
        # Initialize base date and patient
        self.base_date = NoteDate(offset_days=random.randint(0, 1000), direction=DateOffset.AFTER)
        self.patient = Patient(
            age=kwargs.get('patient_age'),
            sex=kwargs.get('patient_sex'),
            race=kwargs.get('patient_race'),
            first_name=kwargs.get('patient_first_name'),
            last_name=kwargs.get('patient_last_name')
        )
        
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
        
        # Initialize remaining components
        self.colonoscopy = Colonoscopy()
        self.prostatectomy = Prostatectomy(patient_last_name=self.patient.last_name)
        self.vitals = Vitals()
        self.problem_list = ProblemList()
        self.staging = Staging(risk_level=kwargs.get('risk_level'))
        
        # Initialize imaging and dates
        self.psa_date = NoteDate(reference_date=self.base_date.value, direction=DateOffset.BEFORE, offset_days=200)
        self.pelvic_ct = Imaging(image_type='pelvic_ct', base_date=self.base_date.value)
        self.pelvic_mri = Imaging(image_type='pelvic_mri', base_date=self.base_date.value)
        self.bone_scan = Imaging(image_type='bone_scan', base_date=self.base_date.value)
                
        # Initialize histories
        self.social_history = SocialHistory(reference_date=self.base_date.value)
        self.family_history = FamilyHistory()
        self.prior_treatment = PriorTreatment(reference_date=self.base_date.value)
        self.allergies = Allergies()
        self.medications = Medications()
        self.performance_score = PerformanceScore()
        
        self.mri_date = NoteDate(reference_date=self.base_date.value, direction=DateOffset.BEFORE, offset_days=200)

    def get_text(self):
        if self.note_text == '':
            self.generate_note()
        return self.note_text

    def get_data_fields(self):
        if self.dose_data is not None:
            dose_data = self.dose_data.value
        else:
            dose_data = None
        # super().get_data_fields()
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
        biopsy_entries = [Biopsy(base_date=self.base_date.value, 
                                gleason_primary=gleason_primary,
                                gleason_secondary=gleason_secondary)]
        for _ in [0, 1]:
            biopsy_entries.append(Biopsy(base_date=biopsy_entries[-1].biopsy_date.value))
        return biopsy_entries

    def generate_psa(self, initial_value=None):
        """Modified to accept initial PSA value"""
        psa_entries = [PSA(base_date=self.base_date.value, score=initial_value)]
        for i in range(random.randint(1, 6)):
            psa_entries.append(PSA(base_date=psa_entries[-1].psa_date.value, 
                                 previous_score=psa_entries[-1].psa_score))
        return psa_entries

    def hpi(self, regen=False):
        hpi_index = random.randint(0, 13)

        if hpi_index == 0:
            if self.current_biopsy.biopsy_type is None:
                biopsy = 'Biopsy'
            else:
                biopsy = f'A {self.current_biopsy.biopsy_type} '
            text = f'pt is a {self.patient.age} male newly diagnosed with prostate ca after screening a PSA of {self.current_psa.psa_score}. ' \
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
            text = f'Mr. {self.patient.last_name} is a {self.patient.age} year old male with a hx of gradually rising PSA since ' \
                   f'{self.psa_history[-1].psa_date} and had a {self.current_biopsy.biopsy_type} on {self.current_biopsy.biopsy_date} and ' \
                   f'pathology reported {self.current_biopsy.gleason} {self.staging.histology} involving {self.current_biopsy.right_cores} and ' \
                   f'{self.current_biopsy.left_cores}. Most recent PSA was {self.current_psa.psa_score} recorded on {self.current_psa.psa_date}. He is ' \
                   f'experiencing moderate GU symptoms with {self.aua} with nocturia about {random.randint(1, 5)} ' \
                   f'times. He is sexually active without need of any medication with {self.shim}. ' \
                   f'{self.colonoscopy} Stating workup including CTAB and bone scan were reported negative for ' \
                   f'metastatic disease. He is not interest in surgical option, and referred for radiotherapy evaluation.'
        elif hpi_index == 3:
            text = f'Mr. {self.patient.last_name} is a {self.patient.age} male, who was found to initially have microscopic ' \
                   f'hematuria and subsequently found PSA elevation of {self.current_psa.psa_score} on {self.psa_date}. The patient ' \
                   f'then underwent a {self.current_biopsy.biopsy_type} on {self.current_biopsy.biopsy_date}, which showed ' \
                   f'{self.current_biopsy.total_cores} for prostate {self.staging.histology}, {self.current_biopsy.gleason}, {self.staging.tnm}.' \
                   f'{self.prostatectomy} {self.colonoscopy}'
        elif hpi_index == 4:
            text = f'{self.patient.last_name}, {self.patient.first_name} is a {self.patient.age} year old male with a history of ' \
                   f'recently diagnosed {self.staging.risk} prostate cancer, who is referred to our clinic to discuss ' \
                   f'radiotherapy options. Information pertinent to his oncologic evaluation is as follows:\n' \
                   f'Mr. {self.patient.last_name} has a history of elevated PSAs with the more recent score of ' \
                   f'{self.current_psa.psa_score} on {self.current_psa.psa_date}. Pathology showed {self.current_biopsy.gleason} prostate {self.staging.histology} ' \
                   f'with {self.current_biopsy.total_cores}. {self.colonoscopy}'
        elif hpi_index == 5:
            prior_psa_text = f'\tDate\tPSA\n'
            for i in range(len(self.psa_history)):
                prior_psa_text += f'\t{self.psa_history[i].psa_date}\t{self.psa_history[i].psa_score}\n'
            text = f'History of Present Interest: Mr. {self.patient.last_name} is a {self.patient.age} yo man previously seen in ' \
                   f'our department in {self.base_date.year - random.randint(0, 5)}. He presented with a slow rising PSA which ' \
                   f'prompted a biopsy (see below): ' \
                   f'\n' \
                   f'{prior_psa_text}\n' \
                   f'On {self.biopsy_history[-1].biopsy_date} a {self.biopsy_history[-1].biopsy_type} demonstrated {self.biopsy_history[-1].gleason} ' \
                   f'disease in {self.biopsy_history[-1].total_cores}, volume estimate {random.randint(20, 60)}cc. ' \
                   f'He elected active surveillance and has been following with urology. Repeat biopsy on ' \
                   f'{self.current_biopsy.biopsy_date} showed {self.current_biopsy.gleason} in {self.current_biopsy.total_cores} with 35% of the cores involved ' \
                   f'and PNI. His PSA is also steadily rising. He has elected EBRT and STADT after doing much research ' \
                   f'on his own and meeting with a private practice radiation oncologist. {self.colonoscopy}' \
                   f'Subjectively, he has urinary frequency several times a night ({self.aua}), {self.shim}.\n' \
                   f'Impression: Patient with a clinical {self.staging.tnm}, Gleason ' \
                   f'{self.current_biopsy.gleason}, PSA {self.current_psa.psa_score}, {self.staging.histology} of the prostate.'
        elif hpi_index == 6:
            text = f'CHIEF COMPLAINT: Newly diagnosed {self.staging.risk} prostate cancer.\n' \
                   f'HISTORY OF PRESENT ILLNESS:\n' \
                   f'Patient with a clinical {self.staging.tnm}, Gleason {self.current_biopsy.gleason.total}, ' \
                   f'{self.current_psa.psa_score}, {self.staging.histology} of the prostate.\nMr. {self.patient.last_name} is a very pleasant ' \
                   f'{self.patient.age}-year-old, who was seen in consultation for evaluation and treatment recommendations ' \
                   f'regarding newly diagnosed prostate cancer. The patient had his first screening PSA performed on ' \
                   f'{self.psa_history[-1].psa_date} and it was elevated at {self.psa_history[-1].psa_date}. A repeat PSA on ' \
                   f'{self.psa_date} shows a change in the lab value and is still markedly elevated at {self.current_psa.psa_score}. ' \
                   f'He was referred to the Urology Clinic and underwent a {self.current_biopsy.biopsy_type}. The patient then ' \
                   f'underwent {self.current_biopsy.biopsy_type} on {self.current_biopsy.biopsy_date}. This shows a {self.current_biopsy.gleason} prostate ' \
                   f'cancer involving the right side of the gland. Biopsies from the left side of the gland shows ' \
                   f'{self.current_biopsy.left_cores}. There were {self.current_biopsy.right_cores}, however, there were ' \
                   f'{self.current_biopsy.right_cores.value - random.randint(0, self.current_biopsy.right_cores.value)}' \
                   f'/6 cores involved with focal perineural invasion noted. Anywhere ' \
                   f'from 40 to 80% of the cores from different regions of the prostate were involved with disease.\n' \
                   f'{self.colonoscopy}' \
                   f'\nIMPRESSION: Patient with a clinical {self.staging.tnm}, Gleason ' \
                   f'{self.current_biopsy.gleason.total}, {self.current_psa.psa_score}, {self.staging.histology} of the prostate.'
        elif hpi_index == 7:
            if self.staging.tnm.m != 'M0':
                bone_scan = 'a bone scan shows some activity and lytic/blastic lesions were seen on CT scan and ' \
                            f'as such he was deemed {self.staging.tnm.m}'
            else:
                bone_scan = 'a bone scan shows some activity but lytic/blastic lesions were not seen on CT scan and ' \
                            f'as such he was deemed {self.staging.tnm.m}'
            original_year = self.base_date.year - random.randint(1, 3)
            text = f'DIAGNOSIS: Prostate {self.staging.histology}\n' \
                   f'STAGE: At least {self.staging.tnm}\n' \
                   f'PROGNOSTIC FACTORS: {self.current_biopsy.gleason} in {self.current_biopsy.total_cores}. {self.psa_history[-1].psa_score}→{self.current_psa.psa_score}. ' \
                   f'Pt seen originally in {original_year}, no tx due to pt not following up.\n' \
                   f'DATE OF PRIOR {str(self.biopsy_history[-1].biopsy_type).capitalize()} BIOPSIES: {self.biopsy_history[-1].biopsy_date}\n' \
                   f'HPI: Mr. {self.patient.last_name} is a pleasant {self.patient.age} y/o with hx of {self.staging.risk} Prostate ' \
                   f'Cancer diagnosed in {original_year} who were lost to follow up who returns to clinic today for ' \
                   f'reevaluation after moving back from {random.choice(states)}. Briefly, pt was originally diagnosed ' \
                   f'with PSA of {self.psa_history[-1].psa_score} on {self.psa_history[-1].psa_date} and {self.current_biopsy.biopsy_type} bx on ' \
                   f'{self.current_biopsy.biopsy_date} showing {self.current_biopsy.gleason} in {self.current_biopsy.total_cores}.' \
                   f'{self.prostatectomy} There was some concern over actual gleason score but per path ' \
                   f'report, {self.biopsy_history[-1].gleason.primary}+{self.biopsy_history[-1].gleason.secondary} ' \
                   f'was confirmed after consensus review. Upon workup in {original_year}, {bone_scan}. Patient at that time was ' \
                   f'lost to follow up after multiple attempts were made by RadOnc to contact patient. He apparently ' \
                   f'moved to {random.choice(states)} and saw Urology NP in {self.base_date.year} after repeat PSA on ' \
                   f'{self.current_psa.psa_date} was {self.current_psa.psa_score}. He again did not receive any treatment and moved back to ' \
                   f'{random.choice(states)} several months ago and has re-established care. {self.colonoscopy}He has ' \
                   f'been re-referred to RadOnc by pts PCP for discussion.'
        elif hpi_index == 8:
            text = f'HISTORY OF PRESENT ILLNESS: Pt is a {self.patient.age} yo HM with hx of elevated PSA on {self.current_psa.psa_date} ' \
                   f'of {self.current_psa.psa_score}. Pt had recent {self.current_biopsy.biopsy_type}/bx on {self.current_biopsy.biopsy_date} which revealed ' \
                   f'{self.current_biopsy.total_cores} for mainly {self.current_biopsy.gleason} {self.staging.histology} of prostate. Pt had systemic ' \
                   f'w/u of CT of A/P and bone scan which revealed no evidence of mets. Pt does have presence of ' \
                   f'bladder stone and enlarged prostate.{self.prostatectomy} Pt has {self.ipss} and ' \
                   f'{self.shim}. pt was evaluated by Urology and has now been asked to see Radiation Oncology for ' \
                   f'evaluation and treatment recommendations. {self.colonoscopy}\nASSESSMENT: Pt is a {self.patient.age} ' \
                   f'yo HM with hx of probably {self.staging.tnm}, Gleason {self.current_biopsy.gleason.total}, ' \
                   f'{self.staging.histology} of prostate.'
        elif hpi_index == 9:
            psa_loop = ''
            for value in range(len(self.psa_history) - 1, 1, -1):  # TODO: check this
                psa_loop += f'{self.psa_history[value].psa_score} on {self.psa_history[value].psa_score} then '

            text = f'PRESENT ILLNESS: Mr {self.patient.last_name} is a {self.patient.age} year old male with {self.staging.risk} ' \
                   f'prostate cancer, PSA {self.current_psa.psa_score}, {self.current_biopsy.gleason}, {self.staging.tnm}. Mr {self.patient.last_name} ' \
                   f'was found to have PSA elevated to {psa_loop}{self.current_psa.psa_score} on {self.current_psa.psa_date}. ' \
                   f'{self.current_biopsy.biopsy_type} shows {self.current_biopsy.gleason} on {self.current_biopsy.biopsy_date}. Overall ' \
                   f'{self.current_biopsy.total_cores} involved. He had a prostate and pelvic MRI on ' \
                   f'{self.mri_date} showing legion in the right peripheral zone with ' \
                   f'potential EPE and a lobulated protrosuion in the right ' \
                   f'SV. There is a {random.randint(3, 9)} mm LN in the short axis in the right external iliac chain. ' \
                   f'Bone scan on {self.bone_scan} was ' \
                   f'negative for metastases.{self.prostatectomy} {self.colonoscopy}' \
                   f'He was referred by urology to discuss treatment options.'

        elif hpi_index == 10:
            text = f'A {self.patient.age}-year-old male, Mr {self.patient.last_name}, presented to discuss his newly diagnosed prostate cancer. ' \
                    f'He had undergone a PSA screening, which revealed a PSA level of {self.current_psa.psa_score}, leading to a referral to urology.' \
                    f' A {self.biopsy_history[-1].biopsy_type} was performed on {self.biopsy_history[-1].biopsy_date}, and the pathology report revealed a {self.biopsy_history[-1].gleason}.' \
                    f'The left base was found to be the site of the {self.current_biopsy.left_cores}. ' \
                    f'Mr. {self.patient.last_name} scheduled a future appointment to discuss treatment options.' \

        elif hpi_index == 11:
            text = f'Mr {self.patient.first_name} {self.patient.last_name}, a {self.patient.age}-year-old {self.patient.sex.value}, was found to have an elevated PSA level of {self.current_psa.psa_score} during routine screening, ' \
                    f'followed by a {self.biopsy_history[-1].biopsy_type} on {self.biopsy_history[-1].biopsy_date} revealing a right nodule. ' \
                    f'Subsequent biopsies confirmed prostate adenocarcinoma, {self.current_biopsy.gleason}, in {self.current_biopsy.total_cores}. ' \
                    f'Staging scans, including a bone scan and CT abdomen/pelvis, showed no evidence of metastatic disease. ' \
                    f'He also reports significant urinary symptoms, including urgency, frequency, and nocturia, ' \
                    f'and is currently being evaluated for radiation therapy to treat his prostate cancer.' \
                    
        elif hpi_index == 12:
            text = f'{self.patient.first_name} {self.patient.last_name}, a {self.patient.age}-year-old {self.patient.sex.value}, presented for a routine follow-up visit on {self.current_psa.psa_date}, ' \
                    f'where an elevated PSA level of {self.current_psa.psa_score} was discovered. This prompted a urology workup, ' \
                    f'which revealed a diagnosis of high-risk prostate adenocarcinoma with glandular scores of {self.current_biopsy.gleason} through a {self.current_biopsy.biopsy_type}. ' \
                    f'The pathology report indicated that the cancer was localized to the left side of the prostate, ' \
                    f'with co-existing acute and chronic prostatitis on the right side. ' \
                    f'At the time of his current visit, Mr. {self.patient.last_name} reports feeling well, continues to work full-time, ' \
                    f'and experiences no urinary symptoms or sexual dysfunction. He is sexually active and has had no changes in his sexual activity or experience.' \

        else:
            text = ''
        # ----- Regenerate note --------
        if regen:
            text = regenerate(text)
            print('regenerated assmplan')
        return text

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

    def assessment_plan(self, regen=False):
        self.dose_data = Dose()
        index = random.randint(1, 10)
        if index == 1:
            text = f'Assessment: Mr. {self.patient.last_name} is a {self.patient.age} year old gentleman diagnosed with ' \
                   f'{self.staging.risk} prostate {self.staging.histology} in {self.base_date.year - random.randint(0, 3)}. He has stage ' \
                   f'{self.staging.group_stage} {self.staging.risk} risk prostate cancer with Gleason {self.current_biopsy.gleason} and most ' \
                   f'recent PSA {self.current_psa.psa_score}. We discussed treatment options and recommended combined ADT hormone ' \
                   f'therapy and external beam radiation to a dose of {self.dose_data.total_dose} cGy in ' \
                   f'{self.dose_data.num_fractions} fractions over {self.dose_data.weeks_of_rt} weeks to the prostate with Image ' \
                   f'Guided IMRT using Tomotherapy. Treatment field will include regional pelvic nodes to the ' \
                   f'microscopic disease ablation dose.\nTreatment recommendation is in accordance with NCCN guidelines.\n'
        elif index == 2:
            text = f'IMPRESSION:\nMr. {self.patient.last_name} is a {self.patient.age}-year old gentleman with newly diagnosed ' \
                   f'{self.staging.risk} risk prostate cancer. While he has multiple medical comorbidities, his heart ' \
                   f'disease appears to be under good control at this time, and has been for many years. Therefore we ' \
                   f'would lean towards pursuing to try modality therapy with short course of androgen deprivation. We ' \
                   f'discussed with the patient the option for enrolling in RTOG 0924 which would randomize patients ' \
                   f'based external beam radiotherapy that would either include or not include the pelvis. The patient ' \
                   f'is amenable to pursing this if he is deemed a candidate.\n\n'
            text += 'RECOMMENDATION:\n' \
                    f'- CT A/P to rule out pelvic lymphadenopathy\n' \
                    f'- MRI prostate to rule out ECE/SVI\n' \
                    f'- NaF PET/CT to rule out osseous disease\n' \
                    f'- Patient will return in roughly 1 month to discuss the results of his scans. We will review ' \
                    f'his case with research nurser is to evaluate if he is a candidate for RTOG 0924\n' \
                    f'- Tentative plan for short course androgen deprivation with {self.dose_data.total_dose} ' \
                    f'gray of external beam radiotherapy followed by an LDR brachytherapy boost\n' \
                    f'- Will consult anesthesia to evaluate if patient would be candidate for anesthesia for ' \
                    f'brachytherapy procedure \n' \
                    f'- Patient will contract our clinic for questions or concerns\n\n'
        elif index == 3:
            text = f'ASSESSMENT: {self.patient.age}yM w/Prostate {self.staging.histology}, Stage {self.staging.tnm}, Group ' \
                   f'{self.staging.group_stage}, {self.staging.risk} risk grade {self.current_biopsy.gleason} without perineural invasion ' \
                   f'and moderately rising and elevated PSA now {self.current_psa.psa_score}. He is a healthy and active gentleman ' \
                   f'with a >10yr life expectancy and no symptoms from his disease.\n'

            if self.staging.risk == 'low':
                text += f'His options are surgery of definitive radiation therapy, but he wants radiation.\n'
            else:
                text += f'With {self.staging.risk} risk and long expected life span, he needs treatment now. His options are ' \
                        f'surgery or definitive radiation therapy, but he wants radiation. Radiation seed implant is ' \
                        f'excluded because of high grade {self.current_biopsy.gleason} disease. Therefore, external beam therapy is ' \
                        f'recommended.\n'
            text += f'Possible acute side effects of external beam therapy discussed are further reduced urinary ' \
                    f'outflow leading to slow stream, frequency, urgency, and nocturia. His current IPSS score is ' \
                    f'{self.ipss} and he should have no flow problems with radiation. Other effects are mild rectal ' \
                    f'pain and inflammation. Generalized fatigue may occur. A late effect might be further erectile ' \
                    f'dysfunction.\n'

            if self.staging.risk != 'low':
                text += f'{self.staging.risk} and high grade prostate cancer has a high treatment success rate when hormonal ' \
                        f'therapy precedes the radiation by {random.randint(2, 4)} months, is combined with the ' \
                        f'radiation, and continues ongoing for up to {random.choice([6, 12, 18, 24])} months. ' \
                        f'Reference: Bolla NEJM 1997 and 2009.\n'

            first_phase_fractions = self.dose_data.num_fractions - random.randint(10, 20)
            text += f'PLAN: Radiation treatment {self.staging.risk} grade disease is delivered in 2 phases to the ' \
                    f'prostate/seminal vesicle volume to {first_phase_fractions * self.dose_data.dose_per_fraction} cGy ' \
                    f'followed by prostate only to {self.dose_data.total_dose} cGy all delivered using IMRT techniques ' \
                    f'to spare normal adjacent structures like the rectum and bladder at ' \
                    f'{self.dose_data.dose_per_fraction} cGy a day in {self.dose_data.dose_per_fraction} treatment ' \
                    f'fractions.\n'
            text += f'I will make a referral a Medical Oncology for anti-androgen therapy. We will ask Urology here to ' \
                    f'place fiducial gold seed markers for reliable day to day setup on this treatment table using IGRT ' \
                    f'techniques. After marker placement and {random.randint(2, 4)} weeks to allow for return of the ' \
                    f'prostate to normal size, we will simulate him on the CT simulator.\n'

            if self.staging.risk == 'intermediate':
                text += f'Although he has intermediate risk cancer, with a PSA under 10 he will not need a bone scan or ' \
                        f'pelvic CT to look for metastases. There were ordered however and the CT result is negative. ' \
                        f'No pelvic lympohadenopathy. Kidneys appear normal in light of prior history of renal ca. Bone ' \
                        f'scan is pending.\n'
        elif index == 4:
            first_phase_fractions = random.randint(20, 30)
            first_phase_dose = first_phase_fractions * self.dose_data.dose_per_fraction
            second_phase_fractions = self.dose_data.num_fractions - first_phase_fractions
            second_phase_dose = second_phase_fractions * self.dose_data.dose_per_fraction

            text = f'A/P: Mr. {self.patient.last_name} is a {self.patient.age}y AAM w/ {self.staging.risk} risk prostate cancer, ' \
                   f'{self.current_biopsy.gleason}, large volume disease w/ PSA {self.current_psa.psa_score} who presents for definitive radiation ' \
                   f'treatment options. Risks, benefits and alternatives were discussed, patient wishes to proceed.\n'
            text += f'--Formal consent obtained today in clinic\n'
            text += f'--Refer back to urology for diducial marker placement, patient currently on warfarin and will need ' \
                    f'to be bridge. Defer to urology for instructions on blood thinner mgmt.\n'
            text += f'--RTC 3 weeks post fiducial placement for CT simulation and treatment planning\n'
            text += f'--Will treat whole pelvis to {first_phase_dose}gGy, SV to {second_phase_dose}cGy and prostate to ' \
                    f'{self.dose_data.total_dose}cGy in {self.dose_data.num_fractions} total fractions\n\n'

            if self.is_cosigner:
                text += f'I have seen and discussed the patient with the attending physician, {self.note_cosigner}, ' \
                        f'who agrees with my assessment and plan.\n\n'
            return text
        elif index == 5:
            text = f'RECOMMENDATION:\nMr. {self.patient.last_name} is a {self.patient.age} year old man with {self.staging.risk} risk ' \
                   f'Stage {self.staging.group_stage}, {self.staging.tnm} prostate cancer. We will start Bicalutamide 50 mg ' \
                   f'daily. Will schedule fudicial seed appointment. He will need a CT Simulation about 7-10 days after ' \
                   f'his fudicial seed placement. He will then start his {self.dose_data.weeks_of_rt} week radiation therapy ' \
                   f'course about {random_time_period(2, 6, "week")} thereafter.'
        elif index == 6:
            text = f'DIAGNOSTIC/THERAPEUTIC PLAN: Greater then {random.choice([30, 45, 60, 90])} minutes was spent ' \
                   f'discussing with the patient the details fo his prostate cancer diagnosis, staging and management ' \
                   f'options. We explained that due to the presence high psa he falls into the {self.staging.risk} risk ' \
                   f'group for recurrence after definitive treatment of localized prostate cancer. We discussed ' \
                   f'potential management options including watchful waiting/active surveillance, surgery, cryosurgery, ' \
                   f'hormone therapy and radiation therapy.\n'
            text += f'We recommended definitive external beam radiotherapy to the prostate to a total dose of ' \
                    f'{self.dose_data.total_dose} cGy delivered in daily fractions of {self.dose_data.dose_per_fraction} ' \
                    f'cGy over {self.dose_data.weeks_of_rt} weeks. We also recommend neoadjuvant, concurrent, and adjuvant ' \
                    f'hormone therapy using Eligard for {random_time_period(2, 6, "month")} and casodex 50 mg daily for ' \
                    f'{random_time_period(2, 6, "month")}. We will start radiotherapy ' \
                    f'{random_time_period(2, 6, "month")} after the start of the hormone therapy.\n'
            text += f'We discussed in detail the potentially acute and long-term toxicities associated with EBRT to the ' \
                    f'prostate including but limited to: fatigue, skin reaction, urinary frequency or obstructive ' \
                    f'symptoms, dysuria, hematuria, bowel/bladder incontinence, erectile dysfunction, uretheral ' \
                    f'obstruction, rectal soreness, diarrhea or loose stool, rectal bleeding, fecal incontinence and ' \
                    f'second malignancy. We also discussed the potential side effects of hormone therapy including but ' \
                    f'not limited to: fatigue, weight gain, hot flashes, breast tenderness, gynecomastia, erectile ' \
                    f'dysfunction, anemia and increased risk of osteoporosis and cardiovascular disease. The patient ' \
                    f'asked a number of appropriate questions which were answered to his satisfaction.\n'
            text += f'After discussion, the patient expressed his desire to proceed with the recommended treatment. We ' \
                    f'will schedule him from CT simulation in approximate {random_time_period(1, 3, "month")} and plan ' \
                    f'to start radiotherapy in approximately {random_time_period(1, 8, "week")}. We also spent some ' \
                    f'time discussing the process of simulation and radiation  treatment delivery, on treatment and ' \
                    f'follow up visits and give the patient instructions on how he can help achieve a comfortably ' \
                    f'full bladder and empty rectum ad the time of simulation and treatment. The patient expressed good ' \
                    f'understanding of our recommendations.\n\n'
        elif index == 7:
            text = f'ASSESSMENT: {self.staging.risk} risk prostate ca {self.current_biopsy.gleason} PSA={self.current_psa.psa_score}, T{self.staging.tnm.t}\n' \
                   f'PLAN:\n' \
                   f'1.    Recommend XRT: Curative\n' \
                   f'2.    The risks, benefits of XRT, are alternatives were discussed. Pt want to decide in ' \
                   f'{random_time_period(1, 3, "week")} surgery vs XRT\n' \
                   f'3.    We wil plan to treat to {self.dose_data.total_dose} cGy in {self.dose_data.num_fractions} ' \
                   f'fractions, 5 fractions/week: IMRT IGRT\n' \
                   f'4.    Concomitant Chemotherapy: no\n' \
                   f'      ADT: {random_time_period(1, 3, "year")}\n' \
                   f'5.    Fiducial marker: yes in patient decide XRT\n'
        elif index == 8:
            self.dose_data = None
            text = f'Asessment plan {self.staging.tnm} Gleason {self.current_biopsy.gleason} {self.staging.histology} of the prostate. ' \
                   f'Patient is a candidate for either prostatectomy or an {random_time_period(4, 8, "week")} course ' \
                   f'of definitive image guided IMRT radiation therapy in the management of his disease with or without ' \
                   f'hormonal manipulation. I would recommend hormonal manipulation with radiation therapy because of a ' \
                   f'survival benefit and have advised the patient that his would be his own decision and I briefly ' \
                   f'discussed the side effects of hormonal manipulation with him. I also recommender the patient have ' \
                   f'gold seed marker placement in his prostate for greater accuracy. I discussed the goals benefits ' \
                   f'risks complications and logistics of radiation therapy with the patient during this visit.' \
                   f'This discussion included but was not limited to the risk of permanent lower extremity weakness, ' \
                   f'permanent lower extremity swelling risk of bone fracture, teh risk of second malignancies, the risk ' \
                   f'of bone fractoin, the risk of second malignancies, the risk of bone fraction, the risk of nausea ' \
                   f'and vomiting, damage to the bowel and/or bladder (which could cause rectal bleeding hematuria, ' \
                   f'increased frequency of urination, including a permanent urostomy and/or colostomy), impotence, ' \
                   f'sterility, urinary leakage, fecal leakage, skin changes (hyperpigmentation of the skin, permanent ' \
                   f'dryness of skin, permanent hair loss in the treatment area), a 50% impotence rate and the ' \
                   f'likelihood of fatigue. The patient voiced his understanding of this discussion. He had an ' \
                   f'opportunity ask questions and all of his questions were answered satisfactorily. I spent well over ' \
                   f'an hour with the patient and greater than 51% of the time was spent in counseling and ' \
                   f'coordinating care. We did discuss using hormonal nuclear relation prior to during and after ' \
                   f'radiation therapy however he does have a great deal of cardiac issues and weight issues which ' \
                   f'might be more detrimental to him if they should worsen then the single digit benefit of having ' \
                   f'hormonal manipulation before during and after radiotherapy especially since they only a small ' \
                   f'component Gleason {self.current_biopsy.gleason} was noted on his biopsy.  We\'ll be sending him up for ' \
                   f'simulation shortly.'
        elif index == 9:
            text = f'PLAN: The various treatments available for prostate cancer were reviewed including radical ' \
                   f'prostatectomy, external beam radiation therapy, hormonal manipulation, combinations of the above, ' \
                   f'and conservative management. The relative risks and benefits of these therapies were discussed at ' \
                   f'length. It was recommended that external beam radiation therapy be administered for definitive ' \
                   f'treatment. After considering the above patient has elected to accept external beam radiation ' \
                   f'therapy.\nPatient has {self.staging.risk}-risk features in his biopsy specimen which would normally be ' \
                   f'treated with hormonal manipulation in conjunctioon with external beam irradiation. Long-term ill ' \
                   f'effects include increased risk of cardiac events in patients with coronary artery disease. ' \
                   f'Hormonal ablation was therefore not recommended. Patient has severe coronary artery disease and is ' \
                   f'not a surgical candidate. Furthermore stents are apparently not an option (by patient history).\n' \
                   f'I plan to administer a total dose of {self.dose_data.total_dose} gray by IMRT technique to the ' \
                   f'prostate and {self.dose_data.num_fractions} fractions over {self.dose_data.weeks_of_rt} duration. CT scan of ' \
                   f'the pelvis will be obtained for planning purposes after fiduciary markers have been placed.\n' \
                   f'Total consultation time {random.choice([30, 45, 60, 90])} minutes.\n'
        elif index == 10:
            offset = random.randint(1, 3)
            first = self.base_date.value + datetime.timedelta(days=30 * offset)
            first_month = calendar.month_name[first.month]
            if first.month == 12:
                second_month = 0
            else:
                second_month = first.month + 1
            second_month = calendar.month_name[second_month]

            text = f'PLAN OF THERAPY/RECOMMENDATION:\nPatient seen, examined and chart reviewed. The recommended salvage ' \
                   f'radiation therapy to prostatic bed was discussed with patient if the work up ordered by Urology ' \
                   f'with CT of pelvis and bone scans were negative for spread to reduce the chance of local ' \
                   f'recurrence. Plan to deliver {self.dose_data.total_dose} Gy/{self.dose_data.num_fractions} fx with IMRT, ' \
                   f'multiple fields, 6 MVX. The rationale of therapy, benefits, potential reactions expected and risks ' \
                   f'involved, radiation cystitis, proctitis, low chance of rectal ulceration, recurrence and bladder ' \
                   f'neck contracture that it may requires urological intervention were explained to him who after ' \
                   f'questions that were answered to his sastifaction he understood, agreed. His ED is some improved ' \
                   f'with sildenafil. He had a plan for a vacation in {second_month} that he may cancel it if he decides ' \
                   f'for the treatment. Patient wants to wait until he sees the urologist sometimes in {first_month} ' \
                   f'with a new PSA that i recommended to evaluate its velocity. FU appt. to be given for {first_month}.'
        else:
            text = ''
            assert 'invalid note index'
        # ----- Regenerate note --------
        if regen:
            text = regenerate(text)
            print('regenerated assmplan')
        return text