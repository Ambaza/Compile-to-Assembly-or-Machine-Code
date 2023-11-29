class AssemblyCompiler:
    def __init__(self):
        self.label_counter = 0

    def compile(self, ast):
        assembly_code = ".data\n"
        assembly_code += ".text\n"
        assembly_code += "global _start\n\n"
        assembly_code += self.compile_ast(ast)
        return assembly_code

    def compile_ast(self, ast):
        if isinstance(ast, list):  # It's an S-expression
            operator = ast[0]
            if operator in ('+', '-', '*', '/'):
                return self.compile_binary_operation(operator, ast[1], ast[2])
            else:
                raise ValueError(f"Unknown operator: {operator}")
        elif isinstance(ast, int):  # It's a literal number
            return f"    push {ast}\n"
        else:
            raise ValueError(f"Unexpected AST node: {ast}")

    def compile_binary_operation(self, operator, left, right):
        return (
            self.compile_ast(left) +
            self.compile_ast(right) +
            f"    pop ebx\n" +
            f"    pop eax\n" +
            self.generate_operation_code(operator) +
            f"    push eax\n"
        )

    def generate_operation_code(self, operator):
        if operator == '+':
            return "    add eax, ebx\n"
        elif operator == '-':
            return "    sub eax, ebx\n"
        elif operator == '*':
            return "    imul eax, ebx\n"
        elif operator == '/':
            return (
                "    cdq\n" +  # Sign-extend EAX into EDX
                "    idiv ebx\n"
            )
        else:
            raise ValueError(f"Unknown operator: {operator}")

# Example usage:
ast = ['+', 3, ['*', 4, 5]]  # Represents (+ 3 (* 4 5))
compiler = AssemblyCompiler()
assembly_code = compiler.compile(ast)

print(assembly_code)
