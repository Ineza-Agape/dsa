class SparseMatrix:
    def load_matrix(self, file_path):
        matrix = {}
        try:
            with open(file_path, 'r') as file:
                rows = int(file.readline().split('=')[1].strip())
                cols = int(file.readline().split('=')[1].strip())
                self.numRows = rows
                self.numCols = cols

                for line in file:
                    if line.strip():
                        row, col, value = self.parse_entry(line)
                        if row not in matrix:
                            matrix[row] = {}
                        matrix[row][col] = value
        except Exception as e:
            raise ValueError("Input file has wrong format: {}".format(e))

        return matrix

    def __init__(self, matrix_file=None, numRows=None, numCols=None):
        if matrix_file:
            self.matrix = self.load_matrix(matrix_file)
        else:
            self.matrix = {}
            self.numRows = numRows
            self.numCols = numCols

    def parse_entry(self, line):
        entry = line.strip()[1:-1].split(',')
        return int(entry[0]), int(entry[1]), int(entry[2])

    def get_element(self, row, col):
        return self.matrix.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        if row not in self.matrix:
            self.matrix[row] = {}
        self.matrix[row][col] = value

    def add(self, other_matrix):
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

        for row in range(self.numRows):
            for col in range(self.numCols):
                sum_value = self.get_element(row, col) + other_matrix.get_element(row, col)
                result.set_element(row, col, sum_value)

        return result

    def subtract(self, other_matrix):
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

        for row in range(self.numRows):
            for col in range(self.numCols):
                difference_value = self.get_element(row, col) - other_matrix.get_element(row, col)
                result.set_element(row, col, difference_value)

        return result

    def multiply(self, other_matrix):
        if self.numCols != other_matrix.numRows:
            raise ValueError("Matrix multiplication not possible with incompatible sizes.")

        result = SparseMatrix(numRows=self.numRows, numCols=other_matrix.numCols)

        for row in self.matrix:
            for col in other_matrix.matrix:
                if col in self.matrix[row]:
                    value_sum = sum(
                        self.get_element(row, k) * other_matrix.get_element(k, col)
                        for k in range(self.numCols)
                    )
                    result.set_element(row, col, value_sum)

        return result

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write("rows={}\n".format(self.numRows))
            file.write("cols={}\n".format(self.numCols))

            for row in self.matrix:
                for col, value in self.matrix[row].items():
                    file.write("({}, {}, {})\n".format(row, col, value))


if __name__ == "__main__":
    matrix1 = SparseMatrix(matrix_file='/dsa/sparse_matrix/sample_inputs/easy_sample_01_2.txt')
    matrix2 = SparseMatrix(matrix_file='/dsa/sparse_matrix/sample_inputs/easy_sample_03_1.txt')

    print("Choose a matrix operation:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    
    choice = int(input("Enter your choice (1/2/3): "))

    if choice == 1:
        result = matrix1.add(matrix2)
        print("Matrices added successfully!")
    elif choice == 2:
        result = matrix1.subtract(matrix2)
        print("Matrices subtracted successfully!")
    elif choice == 3:
        result = matrix1.multiply(matrix2)
        print("Matrices multiplied successfully!")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

    output_file = 'result.txt'
    if not output_file.startswith('./sparse_matrix/results/'):
        output_file = './sparse_matrix/results/' + output_file
        
    result.save_to_file(output_file)
    print("Result saved to {}".format(output_file))
