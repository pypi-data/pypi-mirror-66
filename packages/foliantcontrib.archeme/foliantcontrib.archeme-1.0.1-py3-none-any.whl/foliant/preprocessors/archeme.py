'''
Archeme integration Preprocessor for Foliant documentation authoring tool.
'''

import re
from pathlib import Path
from hashlib import md5
from subprocess import run, PIPE, STDOUT, CalledProcessError
from yaml import load, Loader
from typing import Dict
OptionValue = int or float or bool or str

from archeme.generate import GenerateGraphvizSource
from archeme.merge import MergeMultipleSchemes

from foliant.utils import output
from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'cache_dir': Path('.archemecache'),
        'graphviz_paths': {
            'dot': 'dot',
            'neato': 'neato',
            'fdp': 'fdp',
        },
        'action': 'generate',
        'config_file': None,
        'format': 'png',
        'targets': []
    }

    tags = 'archeme',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cache_dir_path = (self.project_path / self.options['cache_dir']).resolve()

        self.logger = self.logger.getChild('archeme')

        self._config = {}

        if self.options['config_file']:
            self.logger.debug('Reading default config from user-specified file')

            with open(Path(self.options['config_file']).resolve()) as config_file:
                self._config = load(config_file, Loader)

        self._modules = {}

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def _generate_gv_source(self, diagram_definition: dict, diagram_gv_file_path: Path) -> None:
        self.logger.debug(f'Calling Archeme to generate the Graphviz source: {diagram_gv_file_path}')

        diagram_gv_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(diagram_gv_file_path, 'w', encoding='utf8') as diagram_gv_file:
            diagram_gv_file.write(GenerateGraphvizSource().generate_graphviz_source(diagram_definition))

        return None

    def _draw_diagram(
        self,
        engine: str,
        format: str,
        diagram_gv_file_path: Path,
        diagram_image_file_path: Path
    ) -> None:
        command = f'{self.options["graphviz_paths"][engine]} '

        if engine == 'neato' or engine == 'fdp':
            command += '-n '

        command += f'-T {format} "{diagram_gv_file_path}" -o "{diagram_image_file_path}"'

        self.logger.debug(f'Calling Graphviz to draw the diagram, command: {command}')

        try:
            command_output = run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

            if command_output.stdout:
                command_output_decoded = command_output.stdout.decode('utf8', errors='ignore')

                self.logger.debug(f'Output of the command: {command_output_decoded}')

        except CalledProcessError as exception:
            self.logger.error(str(exception))

            raise RuntimeError(f'Failed: {exception.output.decode()}')

        return None

    def _archeme_generate(self, options: OptionValue, body: str or dict) -> str:
        if options.get('config_file', None):
            self.logger.debug(f'Reading current config from user-specified file: {options["config_file"]}')

            with open(Path(options['config_file']).resolve()) as config_file:
                config = load(config_file, Loader)

        else:
            config = self._config

        self.logger.debug(f'Config for the current diagram: {config}')

        if not isinstance(body, dict):
            self.logger.debug('Parsing diagram body as YAML string')

            body = load(body, Loader)

        self.logger.debug(f'Diagram definition without config: {body}')

        diagram_definition = {**config, **body}

        self.logger.debug(f'Full diagram definition with config: {diagram_definition}')

        engine = diagram_definition.get('engine', 'dot')

        format = options.get('format', None) or self.options['format']

        if options.get('module_id', None):
            diagram_gv_file_path = Path(self._cache_dir_path / f'custom_{options["module_id"]}.gv').resolve()
            self._generate_gv_source(diagram_definition, diagram_gv_file_path)
            diagram_image_file_path = Path(self._cache_dir_path / f'custom_{options["module_id"]}.{format}').resolve()
            self._draw_diagram(engine, format, diagram_gv_file_path, diagram_image_file_path)

            self.logger.debug(f'Remembering module {options["module_id"]}')

            if options['module_id'] in self._modules.keys():
                warning_message = f'WARNING: Duplicate module ID: {options["module_id"]}'
                output(warning_message, self.quiet)

                self.logger.warning(warning_message)

            self._modules[options['module_id']] = body

            self.logger.debug(f'Remembered module description: {self._modules[options["module_id"]]}')

        else:
            diagram_hash = md5(str(diagram_definition).encode()).hexdigest()

            diagram_gv_file_path = Path(self._cache_dir_path / f'auto_{diagram_hash}.gv').resolve()

            if not diagram_gv_file_path.exists():
                self._generate_gv_source(diagram_definition, diagram_gv_file_path)

            else:
                self.logger.debug(f'Graphviz source found in cache: {diagram_gv_file_path}')

            diagram_image_file_path = Path(
                self._cache_dir_path / f'auto_{diagram_hash}.{format}'
            ).resolve()

            if not diagram_image_file_path.exists():
                self._draw_diagram(engine, format, diagram_gv_file_path, diagram_image_file_path)

            else:
                self.logger.debug(f'Drawn diagram found in cache: {diagram_image_file_path}')

        return f'![{options.get("caption", "")}]({diagram_image_file_path})'

    def _archeme_merge(self, options: OptionValue, body: str or dict) -> str:
        if not isinstance(body, dict):
            self.logger.debug('Parsing multi-module diagram body as YAML string')

            body = load(body, Loader)

        self.logger.debug(f'Multi-module diagram full description: {body}')

        structure = body.get('structure', {})

        self.logger.debug(f'Multi-module diagram structure: {structure}')

        for structure_item in structure:
            module_reference = structure_item.get('module', None)

            if module_reference:
                module_id = module_reference.get('id', None)

                if module_id:
                    self.logger.debug(f'Module reference found, ID: {module_id}')

                    if not module_reference.get('description', None) and not module_reference.get('file', None):
                        self.logger.debug(f'No description or file specified for module, using remembered data')

                        if module_id in self._modules.keys():
                            self.logger.debug(
                                f'Taking remembered description for the module {module_id}: ' +
                                f'{self._modules[module_id]}'
                            )

                            module_reference['description'] = self._modules[module_id]

                        else:
                            self.logger.debug(f'No remembered data for the module {module_id}')

        self.logger.debug(f'Calling Archeme to perform merging, source: {body}')

        processed_body = MergeMultipleSchemes()._merge_modules(body)

        self.logger.debug(f'Merge result: {processed_body}')
        self.logger.debug(f'Now performing generate action, options: {options}')

        return self._archeme_generate(options, processed_body)

    def process_archeme(self, content: str, action: str) -> str:
        def _sub(archeme_definition) -> str:
            options = self.get_options(archeme_definition.group('options'))
            required_action = options.pop('action', self.options['action'])

            self.logger.debug(
                f'Archeme definition found, current action: {action}, required action: {required_action}, ' +
                f'options: {options}'
            )

            if action == 'generate' and required_action == 'generate':
                return self._archeme_generate(options, archeme_definition.group('body'))

            elif action == 'merge' and required_action == 'merge':
                return self._archeme_merge(options, archeme_definition.group('body'))

            else:
                self.logger.debug('Skipping')

                return archeme_definition.group(0)

        return self.pattern.sub(_sub, content)

    def apply(self):
        self.logger.info('Applying preprocessor')

        self.logger.debug(f'Allowed targets: {self.options["targets"]}')
        self.logger.debug(f'Current target: {self.context["target"]}')

        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            for action in ['generate', 'merge']:
                for markdown_file_path in self.working_dir.rglob('*.md'):
                    self.logger.debug(f'Action {action}, processing the file: {markdown_file_path}')

                    with open(markdown_file_path, encoding='utf8') as markdown_file:
                        content = markdown_file.read()

                    processed_content = self.process_archeme(content, action)

                    if processed_content:
                        with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                            markdown_file.write(processed_content)

        self.logger.info('Preprocessor applied')
