class BFConverter:
    def __init__(self, language: str = 'c', heap_allocated: bool = False, pointer_name: str = 'ptr',
                 allocation_size: int = 1000, indent_style: str = '    '):
        """Initialize BF converter
        :param language: either 'c' or 'cpp'
        :param heap_allocated: whether the char array should be heap allocated
        :param pointer_name: pointer variable name
        :param allocation_size: size of allocated bytes
        :param indent_style: style of indentation
        """

        self.__bf_chars = {}
        self.__lang = language
        self.pointer_name = pointer_name
        self.heap_allocated = heap_allocated
        self.allocation_size = allocation_size
        self.indent_style = indent_style

    @property
    def language(self) -> str:
        return self.__lang

    @property
    def is_c(self) -> bool:
        return self.__lang == 'c'

    @property
    def is_cpp(self) -> bool:
        return self.__lang == 'cpp'

    @language.setter
    def language(self, language: str):
        if language != 'cpp' and language != 'c':
            raise ValueError('Not supported language for BFConverter. Use either \'c\' or \'cpp\'.')

        self.__lang = language
        if self.is_c:
            self.__bf_chars[','] = f'scanf("%c", {self.__ptr});'
            self.__bf_chars['.'] = f'printf("%c", *{self.__ptr});'
        else:
            self.__bf_chars[','] = f'std::cin >> *{self.__ptr};'
            self.__bf_chars['.'] = f'std::cout << *{self.__ptr};'

    @property
    def pointer_name(self) -> str:
        return self.__ptr

    @pointer_name.setter
    def pointer_name(self, pointer_name: str):
        self.__ptr = pointer_name
        self.__bf_chars['['] = f'while (*{self.__ptr}) {{'
        self.__bf_chars[']'] = '}'
        self.__bf_chars['>'] = f'++{self.__ptr};'
        self.__bf_chars['<'] = f'--{self.__ptr};'
        self.__bf_chars['+'] = f'++(*{self.__ptr});'
        self.__bf_chars['-'] = f'--(*{self.__ptr});'
        self.language = self.language

    def convert(self, bf: str) -> str:
        indent = 1

        if self.is_c:
            result = '#include <stdio.h>\n'
            if self.heap_allocated:
                result += '#include <stdlib.h>\n'
        else:
            result = '#include <iostream>\n'

        result += '\nint main() {\n' + self.indent_style

        if self.heap_allocated:
            if self.language == 'c':
                result += f'char *{self.pointer_name} = (char *)malloc({self.allocation_size})'
            else:
                result += f'char *{self.pointer_name} = new char[{self.allocation_size}]'
        else:
            array_name = 'a' if self.pointer_name != 'a' else '_a'
            result += f'char {array_name}[{self.allocation_size}];\n' \
                      f'{self.indent_style}char *{self.pointer_name} = {array_name}'
        result += ';\n'

        for c in bf:
            if c in self.__bf_chars.keys():
                if c == ']':
                    indent -= 1
                result += (self.indent_style * indent) + self.__bf_chars[c] + '\n'
                if c == '[':
                    indent += 1

        result += '\n'
        if self.heap_allocated:
            result += self.indent_style
            if self.is_c:
                result += f'free({self.pointer_name};'
            else:
                result += f'delete[] {self.pointer_name};'
        result += self.indent_style + 'return 0;\n}'
        return result

    def __source_fn(self, dst: str) -> str:
        if dst.count('.') > 0:
            dst = '.'.join(dst.split('.')[:-1])
        return f'{dst}.{self.language}'

    def convert2file(self, dst: str, bf: str):
        with open(self.__source_fn(dst), 'w') as f:
            f.write(self.convert(bf))

    def compile(self, dst: str, bf: str):
        source_fn = self.__source_fn(dst)
        with open(source_fn, 'w') as f:
            f.write(self.convert(bf))
        from subprocess import call
        call(['gcc' if self.is_c else 'g++', source_fn, '-o', '.'.join(source_fn.split('.')[:-1])])
