#
#    Copyright (C) 2014 Alexandre Viau <alexandre@alexandreviau.net>
#
#    This file is part of python-pass.
#
#    python-pass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-pass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-pass.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import shutil
import tempfile
import unittest

import click.testing

import pypass.command


class TestCommand(unittest.TestCase):

    def run_cli(self, args, input=None):
        args = ['--PASSWORD_STORE_DIR', self.dir] + list(args)
        runner = click.testing.CliRunner()
        result = runner.invoke(pypass.command.main, args, input=input)
        return result

    def setUp(self):
        self.dir = tempfile.mkdtemp()

        # .gpg_id file
        open(os.path.join(self.dir, '.gpg_id'), 'w').write('3CCC3A3A')

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_init(self):
        init_dir = tempfile.mkdtemp()
        self.run_cli(
            [
                'init',
                '-p', os.path.join(init_dir, '.password-store'),
                '3CCC3A3A'
            ]
        )

        self.assertTrue(
            os.path.isdir(os.path.join(init_dir, '.password-store'))
        )

        self.assertTrue(
            os.path.isfile(
                os.path.join(init_dir, '.password-store', '.gpg_id')
            )
        )

        self.assertEqual(
            open(
                os.path.join(init_dir, '.password-store', '.gpg_id'),
                'r'
            ).read(),
            '3CCC3A3A'
        )
        shutil.rmtree(init_dir)

    def test_insert(self):
        self.run_cli(
            [
                'insert', 'test.com'
            ],
            input='super_secret\nsuper_secret'
        )

        self.assertTrue(
            os.path.isfile(os.path.join(self.dir, 'test.com.gpg'))
        )
