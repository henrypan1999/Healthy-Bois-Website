from .Referral import Referral
class ReferralSystem:
    def __init__(self):
        self._referrals = []
    
    @property
    def referrals(self):
        return self._referrals
    
    def make_referral(self, GP, specialist, patient, note):
        new_referral = Referral(GP, specialist, patient, note)
        self._referrals.append(new_referral)
        return new_referral
    
    def get_patient_referrals(self, patient):
        referrals = []
        for referral in self._referrals:
            if referral.patient == patient:
                referrals.append(referral)
        return referrals

    def get_specialist_referrals(self, specialist):
        referrals = []
        for referral in self._referrals:
            if referral.specialist == specialist:
                referrals.append(referral)
        return referrals