import csv
import argparse

class LoadBalancer:
    def __init__(self):
        self.banks = {}
        self.facilities = []    # ordered by facility interest rate
        self.covenants = {}

    def read_facilities(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                amount = float(row['amount'])
                interest_rate = float(row['interest_rate'])
                id = int(row['id'])
                bank_id = int(row['bank_id'])
                self.facilities.append({'amount': amount, 'interest_rate': interest_rate,
                    'id': id, 'bank_id': bank_id})
        self.facilities = sorted(self.facilities, key=lambda f: f['interest_rate'])
        print(self.facilities)

    def read_covenants(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                facility_id = -1 if not len(row['facility_id']) else int(row['facility_id'])
                max_default_likelihood = 1.0 if not len(row['max_default_likelihood']) else float(row['max_default_likelihood'])
                bank_id = int(row['bank_id'])
                banned_state = row['banned_state']
                if bank_id not in self.covenants:
                    self.covenants[bank_id] = {}
                self.covenants[bank_id][facility_id] = {
                    'max_default_likelihood': max_default_likelihood,
                    'banned_state': banned_state,
                    }
        print(self.covenants)

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

if __name__ == "__main__":
    main()
