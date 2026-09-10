import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.vm import (
    Compiler,
    VM,
    serialize_chunk,
    deserialize_chunk,
    compile_file_to_skc,
    load_skc_file,
)


class TestSKCSerialization(unittest.TestCase):
    def test_serialize_deserialize_chunk(self):
        code = """
        kaam square(n) {
            farka n * n
        }
        rakha res = square(9)
        dekha res
        """
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        chunk = Compiler("test.sk").compile(ast)

        # Roundtrip via serialize / deserialize
        raw_bytes = serialize_chunk(chunk)
        self.assertTrue(raw_bytes.startswith(b"SKC\x01"))

        restored_chunk = deserialize_chunk(raw_bytes, "restored.skc")
        self.assertEqual(len(restored_chunk.code), len(chunk.code))
        self.assertEqual(len(restored_chunk.constants), len(chunk.constants))

        # Execute restored chunk in VM
        output = []
        vm = VM(filename="restored.skc", output_fn=output.append)
        vm.run(restored_chunk)
        self.assertEqual(output, ["81"])

    def test_compile_file_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = Path(tmpdir) / "prog.sk"
            skc_file = Path(tmpdir) / "prog.skc"

            src_file.write_text(
                'rakha msg = "Sikhar Bytecode Works"\ndekha msg\n',
                encoding="utf-8",
            )

            out_path = compile_file_to_skc(str(src_file), str(skc_file))
            self.assertTrue(Path(out_path).exists())

            loaded_chunk = load_skc_file(out_path)
            output = []
            vm = VM(filename=out_path, output_fn=output.append)
            vm.run(loaded_chunk)
            self.assertEqual(output, ["Sikhar Bytecode Works"])


if __name__ == "__main__":
    unittest.main()
