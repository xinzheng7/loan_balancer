import unittest
from loan_balancer import LoanBalancer

class TestLoanBalancer(unittest.TestCase):

    @staticmethod
    def make_facility(amount, interest_rate, fid, bid):
        return {'amount': amount,
                'interest_rate': interest_rate,
                'facility_id': fid,
                'bank_id': bid}

    @staticmethod
    def make_covenant(max_default_likelihood, banned_states):
        return {'max_default_likelihood': max_default_likelihood,
                'banned_state': banned_states}

    @staticmethod
    def make_loan(user_interest_rate, amount, loan_id, default_likelihood, state):
        return {'user_interest_rate': user_interest_rate,
                'amount': amount,
                'loan_id': loan_id,
                'default_likelihood': default_likelihood,
                'state': state}

    def test_assign_loan_normal(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101)]
        lb.covenants = {101: {201: self.make_covenant(0.05, set(['CA']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 20000, 301, 0.04, 'NY'), assignment, yields)
        self.assertEqual({301: 201}, assignment)
        self.assertEqual({201: 80}, yields)

    def test_assign_loan_high_default(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101)]
        lb.covenants = {101: {201: self.make_covenant(0.05, set(['CA']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 20000, 301, 0.06, 'NY'), assignment, yields)
        self.assertEqual({301: ''}, assignment)

    def test_assign_loan_banned_state(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101)]
        lb.covenants = {101: {201: self.make_covenant(0.05, set(['NY', 'CA']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 20000, 301, 0.04, 'CA'), assignment, yields)
        self.assertEqual({301: ''}, assignment)

    def test_assign_loan_amount_too_large(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101)]
        lb.covenants = {101: {201: self.make_covenant(0.05, set(['CA']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 100001, 301, 0.04, 'NY'), assignment, yields)
        self.assertEqual({301: ''}, assignment)

    def test_assign_loan_added_yields(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101)]
        lb.covenants = {101: {201: self.make_covenant(0.05, set(['CA']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 20000, 301, 0.04, 'NY'), assignment, yields)
        lb.assign_loan(self.make_loan(0.15, 40000, 302, 0.04, 'MN'), assignment, yields)
        self.assertEqual({301: 201, 302: 201}, assignment)
        self.assertEqual({201: 240}, yields)

    def test_assign_loan_first_facility_doesnt_work(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101),
                self.make_facility(100000, 0.11, 202, 102)]
        lb.covenants = {
                101: {201: self.make_covenant(0.05, set(['CA']))},
                102: {202: self.make_covenant(0.05, set(['NY']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 20000, 301, 0.04, 'CA'), assignment, yields)
        self.assertEqual({301: 202}, assignment)

    def test_assign_loan_covenant_for_all_facilities(self):
        lb = LoanBalancer()
        lb.facilities = [self.make_facility(100000, 0.1, 201, 101)]
        lb.covenants = {101: {-1: self.make_covenant(0.05, set(['CA']))}}
        assignment = {}
        yields = {}
        lb.assign_loan(self.make_loan(0.15, 20000, 301, 0.06, 'NY'), assignment, yields)
        self.assertEqual({301: ''}, assignment)




if __name__ == '__main__':
    unittest.main()
