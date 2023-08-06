from clquery import shell
from clquery import tables_aws


def test_mode():
    conn = shell.setup()
    test_shell = TestShell(db=conn)
    test_shell.process_command('.mode python')
    test_shell.process_command('.headers off')
    return test_shell


class TestShell(shell.PythonShell):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def emit_output(self, output):
        pass

    def get_output(self):
        return self.output_buffer

    def clear_output(self):
        self.output_buffer = []
