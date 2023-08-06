import os
import random
from os.path import join

from faker import Faker

from catcher.core.runner import Runner
from test.abs_test_class import TestClass
from test.test_utils import check_file


class VariablesTest(TestClass):
    def __init__(self, method_name):
        super().__init__('variables_test', method_name)

    # variables, passed via cmd `e` options should override all variables
    def test_cmd_override_all(self):
        self.populate_file('main.yaml', '''---
        variables:
            foo: baz
        steps:
            - echo: 
                actions: 
                    - {from: 'hello', register: {foo: 'bar'}}
                    - {from: '{{ foo }}', to: one.output}
            
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, environment={'foo': 'bad'})
        runner.run_tests()
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), 'bad'))

    # test computed variables available later
    def test_computed_available_later(self):
        self.populate_file('main.yaml', '''---
        steps:
            - echo: 
                actions: 
                    - {from: 'hello', register: {foo: 'bar'}}
                    - {from: '{{ foo }}', to: one.output}
            
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        runner.run_tests()
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), 'bar'))

    # test computed available in the other step
    def test_computed_available_other_step(self):
        self.populate_file('main.yaml', '''---
        steps:
            - echo: {from: 'hello', register: {foo: 'bar'}}
            - echo: {from: '{{ foo }}', to: one.output}
            
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        runner.run_tests()
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), 'bar'))

    # test var can be computed from the template
    def test_computed_with_template(self):
        self.populate_file('main.yaml', '''---
        variables:
            path: /home/user
            test: main.yml
        steps:
            - echo: {from: 'hello', register: {foo: '{{ path }}/{{ test }}'}}
            - echo: {from: '{{ foo }}', to: one.output}
            
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        runner.run_tests()
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), '/home/user/main.yml'))

    # test if env vars included from inventory
    def test_env_vars_included(self):
        os.environ['FOO'] = '1'
        self.populate_file('main.yaml', '''---
        steps:
            - check: {equals: {the: '{{ FOO }}', is: '1'}}

        ''')
        runner = Runner(self.test_dir,
                        join(self.test_dir, 'main.yaml'),
                        None,
                        system_environment=dict(os.environ))
        self.assertTrue(runner.run_tests())

    # env var should be overridden with any other var
    def test_var_override_env(self):
        os.environ['FOO'] = '1'
        self.populate_file('main.yaml', '''---
        variables:
            FOO: 2
        steps:
            - check: {equals: {the: '{{ FOO }}', is: '2'}}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())

    def test_env_var_in_vars(self):
        os.environ['FOO'] = '1'
        self.populate_file('main.yaml', '''---
                variables:
                    foo: '{{ FOO }}'
                steps:
                    - check: {equals: {the: '{{ foo }}', is: '1'}}

                ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, system_environment=dict(os.environ))
        self.assertTrue(runner.run_tests())

    # faker can be called from catcher
    def test_random_functions(self):
        Faker.seed(4321)
        self.populate_file('main.yaml', '''---
        steps:
            - echo: {from: '{{ random("ipv4_private") }}', to: one.output}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), '10.32.135.245'))

    # random int with args can be called
    def test_random_int(self):
        random.seed(123)
        self.populate_file('main.yaml', '''---
        steps:
            - echo: {from: '{{ random_int(1, 10) }}', to: one.output}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), '2'))

        random.seed(123)
        # no upper limit
        self.populate_file('main.yaml', '''---
        steps:
            - echo: {from: '{{ random_int(1) }}', to: one.output}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), '7733829868136316427'))

        random.seed(123)
        # no lower limit
        self.populate_file('main.yaml', '''---
        steps:
            - echo: {from: '{{ random_int(range_to=1) }}', to: one.output}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), '-2229762486649458603'))

    # random choice on a list can be called
    def test_random_choice(self):
        random.seed(123)
        self.populate_file('main.yaml', '''---
        variables:
            my_list: ['one', 'two', 'three']
        steps:
            - echo: {from: '{{ random_choice(my_list) }}', to: one.output}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), 'one'))

    # hash function is properly called
    def test_hash(self):
        self.populate_file('main.yaml', '''---
        variables:
            my_var: test
        steps:
            - echo: {from: '{{ "test" | hash("sha1") }}', to: one.output}
            - echo: {from: '{{ my_var | hash("sha1") }}', to: two.output}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None)
        self.assertTrue(runner.run_tests())
        self.assertTrue(check_file(join(self.test_dir, 'one.output'), 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'))
        self.assertTrue(check_file(join(self.test_dir, 'two.output'), 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'))

