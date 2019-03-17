import csv
import argparse

DL = 'default_likelihood'
MDL = 'max_default_likelihood'
FID = 'facility_id'
BID = 'bank_id'
ITR = 'interest_rate'
UIR = 'user_interest_rate'
LID = 'loan_id'
AMT = 'amount'
BNS = 'banned_state'
ID = 'id'
EY = 'expected_yield'
class LoadBalancer:
    def __init__(self):
        self.banks = {}
        self.facilities = []    # ordered by facility interest rate
        self.covenants = {}

    def read_facilities(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                amount = int(float(row[AMT]))
                interest_rate = float(row[ITR])
                fid = int(row[ID])
                bid = int(row[BID])
                self.facilities.append({AMT: amount, ITR: interest_rate,
                    FID: fid, BID: bid})
        self.facilities = sorted(self.facilities, key=lambda f: f[ITR])

    def read_covenants(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fid = -1 if not len(row[FID]) else int(row[FID])
                mdl = 1.0 if not len(row[MDL]) else float(row[MDL])
                bid = int(row[BID])
                banned_state = row[BNS]
                if bid not in self.covenants:
                    self.covenants[bid] = {}
                if fid not in self.covenants[bid]:
                    self.covenants[bid][fid] = {
                            MDL: 1.0,
                            BNS: set()
                            }
                self.covenants[bid][fid][MDL] = min(mdl, self.covenants[bid][fid][MDL])
                self.covenants[bid][fid][BNS].add(banned_state)

    def process(self, loan_fn, assignment_fn, yields_fn):
        with open(loan_fn, newline='') as loan_file:
            reader = csv.DictReader(loan_file)
            assignment = {}
            yields = {}
            for row in reader:
                user_interest_rate = float(row[ITR])
                amount = int(row[AMT])
                loan_id = int(row[ID])
                default_likelihood = float(row[DL])
                state = row['state']
                loan = {UIR: user_interest_rate,
                        AMT: amount,
                        LID: loan_id,
                        DL: default_likelihood,
                        'state': state}
                self.assign_loan(loan, assignment, yields)
        self.write_assignment(assignment, assignment_fn)
        self.write_yields(yields, yields_fn)

    def write_assignment(self, assignment, assignment_fn):
        with open(assignment_fn, 'w', newline='') as assignment_file:
            writer = csv.DictWriter(assignment_file, fieldnames=[LID, FID])
            writer.writeheader()
            for lid, fid in assignment.items():
                writer.writerow({LID: lid, FID: fid})

    def write_yields(self, yields, yields_fn):
        with open(yields_fn, 'w', newline='') as yields_file:
            writer = csv.DictWriter(yields_file, fieldnames=[FID, EY])
            writer.writeheader()
            for fid, ey in yields.items():
                writer.writerow({FID: fid, EY: round(ey)})

    def respect_covenant(self, loan, covenant):
        return covenant[MDL] >= loan[DL] and loan['state'] not in covenant[BNS]

    def assign_loan(self, loan, assignment, yields):
        for fidx in range(len(self.facilities)):
            facility = self.facilities[fidx]
            if facility[AMT] < loan[AMT]:
                continue
            bid = facility[BID]
            fid = facility[FID]
            if fid in self.covenants[bid] and not self.respect_covenant(loan, self.covenants[bid][fid]):
                continue
            if -1 in self.covenants[bid] and not self.respect_covenant(loan, self.covenants[bid][-1]):
                continue
            self.facilities[fidx][AMT] -= loan[AMT]
            assignment[loan[LID]] = fid
            if fid not in yields:
                yields[fid] = 0
            yields[fid] += (1 - loan[DL]) * loan[UIR] * loan[AMT] - loan[DL] * loan[AMT] - facility[ITR] * loan[AMT]
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', dest='data_dir')
    parser.add_argument('--banks', dest='banks', default='banks.csv')
    parser.add_argument('--facilities', dest='facilities', default='facilities.csv')
    parser.add_argument('--covenants', dest='covenants', default='covenants.csv')
    parser.add_argument('--loans', dest='loans', default='loans.csv')
    parser.add_argument('--assignments', dest='assignments', default='assignments.csv')
    parser.add_argument('--yields', dest='yields', default='yields.csv')
    args = parser.parse_args()

    loan_balancer = LoadBalancer()
    loan_balancer.read_facilities(args.data_dir + '/' + args.facilities)
    loan_balancer.read_covenants(args.data_dir + '/' + args.covenants)
    loan_balancer.process(args.data_dir + '/' + args.loans,
                          args.data_dir + '/' + args.assignments,
                          args.data_dir + '/' + args.yields)

if __name__ == "__main__":
    main()
