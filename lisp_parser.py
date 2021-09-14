# lisp_parser.py
# Jack Scacco
# 9/14/21

class Node:
    def __init__(self, label):
        self.children = []
        self.label = label
        self.depth = 0
        
        # value is unused for now, but will be once we start evaluating programs
        self.value = None

        
    def add_child(self, other):
        """Given another Node, add it to this Node's children."""
        self.children.append(other)
        other.depth = self.depth + 1

        
    def to_abstract_syntax_tree(self):
        """Return an array representing the Node and its children."""
        ast = [self.label]
        for c in self.children:
            if c.children == []:
                ast.append(c.label)
            else:
                ast.append(c.to_abstract_syntax_tree)
        return ast
        

    def __str__(self):
        return str(self.to_abstract_syntax_tree())


def custom_slice(program):
    """Given a program, return (slice, new_program), where slice = the next piece of
       info we want and new_program = the rest of the program after this slice is 
       removed."""

    # If we have a sub-program, we want to slice until we have closed all parens
    if program[0] == "(":
        current_index = 1
        num_open_parens = 1
        subprogram = "("
        while num_open_parens > 0:
            subprogram += program[current_index]
            if program[current_index] == ")":
                num_open_parens -= 1
            elif program[current_index] == "(":
                num_open_parens += 1
            current_index += 1
        return subprogram, program[current_index:]
    else:
        custom_split = program.split(" ", 1)
        try:
            return custom_split[0], custom_split[1]
        except IndexError:
            # TODO: This might not be the way to fix this...
            # This means there is only one piece of info, so new_program = ""
            return custom_split[0], ""

    
def program_to_node(program):
    """Given a string representing a program, return an AST for that program."""

    # Make sure the program has parens on either end
    assert(program[0] == "(" and program[-1] == ")")

    # Remove those parens
    program = program[1:-1]

    # Get the label
    label, program = custom_slice(program)
    
    # While we still have info left, get the children
    children = []
    while program != "":
        child, program = custom_slice(program)
        children.append(child)

    if children == []:
        return Node(label)
    else:
        root = Node(label)
        for c in children:
            print(c)
            if c[0] == "(":
                root.add_child(program_to_node(c))
            else:
                root.add_child(Node(c))

        return root

    
def main():
    test_tree = program_to_node("(first (list 1 (+ 2 3) 9))")
    print(test_tree)

if __name__ == "__main__":
    main()
