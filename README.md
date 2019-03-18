# Coding Challenge: Balance the Loan Books

## Usage

- Run small data set and compare with solution. Note that the following command assume the
solution has been renamed as `assignments_solution.csv` and `yields_solution.csv`.
    ```
    cd loan_balancer
    python loan_balancer.py --data_dir=small
    diff -w small/assignments.csv small/assignments_solution.csv
    diff -w small/yields.csv small/yields_solution.csv
    ```

- Run large data set
    ```
    cd loan_balancer
    python loan_balancer.py --data_dir=large
    ```

- Run unittest
    ```
    cd loan_balancer
    python -m unittest test.test_loan_balancer.TestLoanBalancer
    ```
