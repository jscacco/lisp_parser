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

        
    def to_ast(self):
        """Return an array representing the Node and its children."""
        ast = [self.label]
        for c in self.children:
            if c.children == []:
                ast.append(c.label)
            else:
                ast.append(c.to_ast())
        return ast
        

    def __str__(self):
        return str(self.to_ast())


def custom_slice(program):
    """Given a program, return (slice, new_program), where slice = the next piece of
       info we want and new_program = the rest of the program after this slice is 
       removed."""

    if program == "":
        return "", ""
    
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

        # we got our slice, so keep track of what the new_program is
        new_program = program[current_index:]
        if new_program != "":
            # Remove the space that would be at the start of the rest of the program
            new_program = new_program[1:]
        return subprogram, new_program

    # This isn't a subprogram, so we want to get all the info up until the first space
    else:
        custom_split = program.split(" ", 1)
        try:
            return custom_split[0], custom_split[1]
        except IndexError:
            # This means there is only one piece of info, so new_program = ""
            # (we know the first piece of info is there because we check above)
            return custom_split[0], ""

    
def program_to_node(program):
    """Given a string representing a program, return an AST for that program."""

    # Make sure the program has parens on either end (and then remove them)
    assert(program[0] == "(" and program[-1] == ")")
    program = program[1:-1]

    # Get the label
    label, program = custom_slice(program)

    # While we still have info left, get the children
    children = []
    while program != "":
        child, program = custom_slice(program)
        children.append(child)

    # No children = base case. Return the Node.
    if children == []:
        return Node(label)
    # Children = time to recur. Get the children and turn them all into Nodes
    else:
        root = Node(label)
        for c in children:
            # This is a little messy - feels like it could be more concise but that would
            # require a re-working of the recursive structure.
            if c[0] == "(":
                root.add_child(program_to_node(c))
            else:
                root.add_child(Node(c))

        return root

    
def main():
    test_cases = [
        "(first (list 1 (+ 2 3) 9))",
        "()",
        "(+ (- 7 2) (* 3 4 ))",
    ]

    for t in range(len(test_cases)):
        this_test = test_cases[t]
        print("Test", t, ":", this_test)
        test_tree = program_to_node(this_test)
        print(test_tree.to_ast())

if __name__ == "__main__":
    main()
