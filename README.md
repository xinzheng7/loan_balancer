# Coding Challenge: Balance the Loan Books

## Run the code

- Run small data set and compare with solution. Note that the following command assume the
solution has been renamed as `assignments_solution.csv` and `yields_solution.csv`.
    ```
    cd loan_balancer
    python loan_balancer.py --data_dir=small
    diff -w small/assignments.csv small/assignments_solution.csv
    diff -w small/yields.csv small/yields_solution.csv
    ```

- Run large data set. The output can be found at `large/assignments.csv` and `large/yields.csv`.
    ```
    cd loan_balancer
    python loan_balancer.py --data_dir=large
    ```

- Run unittest
    ```
    cd loan_balancer
    python -m unittest test.test_loan_balancer.TestLoanBalancer
    ```

##Questions and answers
1. How long did you spend working on the problem? What did you find to be the most difficult part?
It took me 2.5 hours to write the code and another 0.5 hour to work on unittests.

2. How would you modify your data model or code to account for an eventual introduction of new, as-of-yet unknown types of covenants, beyond just maximum default likelihood and state restrictions?
Make covenant a class which define a common API called Convenant.check_convenant(loan, facility). A new types of convenant would just inherit this class and implement the API.

3. How would you architect your solution as a production service wherein new facilities can be introduced at arbitrary points in time. Assume these facilities become available by the finance team emailing your team and describing the addition with a new set of CSVs.
    The code need to be productionalized as a service which listen to either REST API or thrift API calls. Each time a new CSV comes in, the code will process the CSV and return to stand-by mode waiting for the next call. If the traffic is high, we want to use multi threads to handle simultaneous/overlapping API calls. The status of facilities will need to be persistant. Suggest using DB to store the transactions and current status.

4. Your solution most likely simulates the streaming process by directly calling a method in your code to process the loans inside of a for loop. What would a REST API look like for this same service? Stakeholders using the API will need, at a minimum, to be able to request a loan be assigned to a facility, and read the funding status of a loan, as well as query the capacities remaining in facilities.

Here are some data structure to be used in these APIs:
- class ApplyLoanRequest(). The class holds what is listed in loans.csv for a particular loan.
- class ApplyLoanResponse(). This class include the following return values:
  - successful: boolean
  - facility_id: int
  - bank_id: int
- class LoanStatus().
- class FacilityStatus().

Here are API definitions:
- apply_loan(req: ApplyLoanRequest) -> ApplyLoanResponse
- describe_loan(loan_id: int) -> LoanStatus
- describe_facility(facility_id: int) -> FacilityStatus

5. How might you improve your assignment algorithm if you were permitted to assign loans in batch rather than streaming? We are not looking for code here, but pseudo code or description of a revised algorithm appreciated.

This is an integer programming problem which is NP. We can use heuristics to achieve good enough result.

6. Discuss your solution’s runtime complexity.

